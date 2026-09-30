import os
import datetime
from typing import List, Dict, Any, Optional

def generate_tree_map(root_dir: str, rel_paths: List[str]) -> str:
    """
    Generates a hierarchical ASCII tree structure for the given list of relative file paths.
    """
    if not rel_paths:
        return "[No files included]\n"

    tree: Dict[str, Any] = {}
    for path in sorted(rel_paths):
        parts = path.replace("\\", "/").split("/")
        curr = tree
        for part in parts[:-1]:
            curr = curr.setdefault(part, {})
        curr[parts[-1]] = None  # File indicator

    lines = []
    root_name = os.path.basename(os.path.abspath(root_dir)) or root_dir
    lines.append(f"{root_name}/")

    def _render(node: Dict[str, Any], prefix: str = ""):
        # Separate directories and files
        dirs = [k for k, v in node.items() if v is not None]
        files = [k for k, v in node.items() if v is None]
        items = sorted(dirs) + sorted(files)

        for index, item in enumerate(items):
            is_last = (index == len(items) - 1)
            connector = "└── " if is_last else "├── "
            child_prefix = "    " if is_last else "│   "

            if node[item] is not None:
                lines.append(f"{prefix}{connector}{item}/")
                _render(node[item], prefix + child_prefix)
            else:
                lines.append(f"{prefix}{connector}{item}")

    _render(tree)
    return "\n".join(lines) + "\n"

def collect_files_for_aggregation(
    target_dir: str,
    file_type: str = "All",
    custom_ext: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Scans target_dir and collects files matching the requested file_type.
    Supported file_types: 'JS', 'JSON', 'All', or custom extension.
    """
    if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        return []

    exclude_dirs = {".git", "__pycache__", "node_modules", ".idea", ".vscode", "backups", "results", "Reports"}
    
    file_type_upper = file_type.strip().upper()
    valid_exts = set()
    
    if file_type_upper == "JS":
        valid_exts = {".js", ".mjs", ".cjs", ".jsx"}
    elif file_type_upper == "JSON":
        valid_exts = {".json"}
    elif file_type_upper == "ALL":
        valid_exts = None  # None indicates all files
    elif custom_ext:
        ext = custom_ext.strip().lower()
        if not ext.startswith("."):
            ext = "." + ext
        valid_exts = {ext}

    matched_files = []
    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if valid_exts is not None and ext not in valid_exts:
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_dir)
            try:
                size = os.path.getsize(full_path)
            except OSError:
                size = 0

            matched_files.append({
                "name": file,
                "rel_path": rel_path,
                "full_path": full_path,
                "ext": ext,
                "size": size
            })

    matched_files.sort(key=lambda x: x["rel_path"].lower())
    return matched_files

def create_aggregate_file(
    target_dir: str,
    file_type: str = "All",
    custom_ext: Optional[str] = None,
    output_dir: str = r"E:\DOCU\Reports"
) -> Dict[str, Any]:
    """
    Gathers all files from target_dir matching file_type, and aggregates them
    into a single structured text file in output_dir.
    """
    target_dir = os.path.abspath(target_dir)
    os.makedirs(output_dir, exist_ok=True)

    files = collect_files_for_aggregation(target_dir, file_type=file_type, custom_ext=custom_ext)
    
    folder_name = os.path.basename(target_dir) or "root"
    safe_type = file_type.upper().replace("*", "").replace(".", "").strip()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_filename = f"aggregate_{folder_name}_{safe_type}_{timestamp}.txt"
    out_filepath = os.path.join(output_dir, out_filename)

    rel_paths = [f["rel_path"] for f in files]
    tree_map = generate_tree_map(target_dir, rel_paths)

    total_lines_written = 0

    with open(out_filepath, "w", encoding="utf-8", errors="replace") as out:
        # 1. Header and Tree Map
        out.write("=" * 80 + "\n")
        out.write("DOCU WORKSPACE FILE AGGREGATION REPORT\n")
        out.write(f"Generated At: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"Target Directory: {target_dir}\n")
        out.write(f"File Type Selection: {file_type}\n")
        out.write(f"Total Files Aggregated: {len(files)}\n")
        out.write("=" * 80 + "\n\n")

        out.write("HIERARCHICAL FILE MAP:\n")
        out.write("-" * 80 + "\n")
        out.write(tree_map)
        out.write("-" * 80 + "\n\n")

        # 2. File Content Aggregation
        for file_info in files:
            name = file_info["name"]
            rel_path = file_info["rel_path"]
            full_path = file_info["full_path"]

            out.write("=" * 80 + "\n")
            out.write(f"// FILE: {name}\n")
            out.write(f"// PATH: {rel_path}\n")
            out.write(f"// FULL PATH: {full_path}\n")
            out.write("=" * 80 + "\n")

            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as src:
                    line_count = 0
                    for line_num, line in enumerate(src, start=1):
                        content = line.rstrip("\r\n")
                        out.write(f"{line_num}::{content}\n")
                        line_count += 1
                        total_lines_written += 1
                    if line_count == 0:
                        out.write("1::[Empty File]\n")
                        total_lines_written += 1
            except Exception as e:
                out.write(f"1::[Error reading file: {e}]\n")
                total_lines_written += 1

            out.write("\n\n")

    file_size_bytes = os.path.getsize(out_filepath)

    return {
        "success": True,
        "output_path": out_filepath,
        "output_filename": out_filename,
        "total_files": len(files),
        "total_lines": total_lines_written,
        "file_size": file_size_bytes
    }
