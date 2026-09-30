import os
from typing import List, Dict, Any, Optional

def format_size(bytes_size: int) -> str:
    """Formats bytes size into human-readable string."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"

def scan_directory(
    target_dir: str, 
    include_subfolders: bool = True,
    search_query: str = "",
    extension_filter: str = "All Files (*.*)"
) -> List[Dict[str, Any]]:
    """
    Scans the given target directory and returns metadata for matched files.
    """
    if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        return []

    results = []
    exclude_dirs = {".git", "__pycache__", "node_modules", ".idea", ".vscode", "backups", "results"}
    
    ext_clean = ""
    if extension_filter and "*." in extension_filter:
        parts = extension_filter.split("*.")
        if len(parts) > 1:
            raw_ext = parts[1].split(")")[0].strip().lower()
            if raw_ext != "*":
                ext_clean = f".{raw_ext}"

    query_lower = search_query.strip().lower()

    if include_subfolders:
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), target_dir)
                full_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()

                if ext_clean and ext != ext_clean:
                    continue
                if query_lower and (query_lower not in file.lower() and query_lower not in rel_path.lower()):
                    continue

                try:
                    stat = os.stat(full_path)
                    size = stat.st_size
                except OSError:
                    size = 0

                results.append({
                    "name": file,
                    "rel_path": rel_path,
                    "full_path": full_path,
                    "size": size,
                    "size_str": format_size(size),
                    "ext": ext
                })
    else:
        try:
            with os.scandir(target_dir) as entries:
                for entry in entries:
                    if entry.is_file():
                        ext = os.path.splitext(entry.name)[1].lower()
                        if ext_clean and ext != ext_clean:
                            continue
                        if query_lower and query_lower not in entry.name.lower():
                            continue
                        try:
                            size = entry.stat().st_size
                        except OSError:
                            size = 0
                        results.append({
                            "name": entry.name,
                            "rel_path": entry.name,
                            "full_path": entry.path,
                            "size": size,
                            "size_str": format_size(size),
                            "ext": ext
                        })
        except OSError:
            pass

    results.sort(key=lambda x: x["rel_path"].lower())
    return results

def read_file_preview(file_path: str, max_lines: int = 150) -> str:
    """Reads the first few lines of a file for preview."""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return "[Error: File not found]"
    
    text_extensions = {
        ".txt", ".md", ".py", ".json", ".js", ".ts", ".html", 
        ".css", ".rs", ".yml", ".yaml", ".xml", ".ini", ".cfg", ".bat", ".ps1"
    }
    ext = os.path.splitext(file_path)[1].lower()
    
    # Try reading as text
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = []
            for _ in range(max_lines):
                line = f.readline()
                if not line:
                    break
                lines.append(line)
            
            content = "".join(lines)
            if not content:
                return "[Empty File]"
            return content
    except Exception as e:
        return f"[Unable to preview binary or unreadable file: {e}]"
