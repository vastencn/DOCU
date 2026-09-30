import os
import sys
import datetime

# Ensure root dir is in path
sys.path.insert(0, r"E:\DOCU")

from src.utils.file_scanner import scan_directory, read_file_preview
from src.ui.app import FileBrowserApp

def run_diagnostics():
    log_lines = []
    log_lines.append(f"=== DOCU File Browser Operational Verification Log ===")
    log_lines.append(f"Timestamp: {datetime.datetime.now().isoformat()}")
    log_lines.append(f"Target Directory: E:\\DOCU")
    log_lines.append(f"Python Version: {sys.version}")
    
    # 1. Test Scanner
    scanned = scan_directory(r"E:\DOCU", include_subfolders=True)
    log_lines.append(f"\n[Test 1] Scanner Test:")
    log_lines.append(f"Discovered {len(scanned)} files:")
    for f in scanned:
        log_lines.append(f" - {f['rel_path']} ({f['size_str']}, {f['ext']})")
    assert len(scanned) > 0, "No files found during scan!"
    log_lines.append("-> Scanner Test: PASSED")

    # 2. Test File Preview
    agent_path = os.path.join(r"E:\DOCU", "AGENT.md")
    preview = read_file_preview(agent_path, max_lines=10)
    log_lines.append(f"\n[Test 2] Preview Test (AGENT.md snippet):")
    log_lines.append(f"Preview Length: {len(preview)} characters")
    log_lines.append(f"First Line: {preview.splitlines()[0] if preview.splitlines() else 'None'}")
    assert "# SYSTEM DIRECTIVE" in preview, "AGENT.md preview mismatch!"
    log_lines.append("-> Preview Test: PASSED")

    # 3. Test App Lifecycle & Widget Generation
    log_lines.append(f"\n[Test 3] CustomTkinter UI Lifecycle Test:")
    app = FileBrowserApp(initial_dir=r"E:\DOCU")
    app.update()
    
    # Verify widgets
    num_checkboxes = len(app.checkbox_vars)
    log_lines.append(f"Checkboxes dynamically packed: {num_checkboxes}")
    assert num_checkboxes == len(scanned), f"Mismatch between checkboxes ({num_checkboxes}) and files ({len(scanned)})"

    # Test Select All
    app.select_all()
    selected_count = sum(1 for v in app.checkbox_vars.values() if v.get())
    log_lines.append(f"After select_all(): {selected_count}/{num_checkboxes} selected")
    assert selected_count == num_checkboxes, "select_all failed!"

    # Test Deselect All
    app.deselect_all()
    selected_count = sum(1 for v in app.checkbox_vars.values() if v.get())
    log_lines.append(f"After deselect_all(): {selected_count}/{num_checkboxes} selected")
    assert selected_count == 0, "deselect_all failed!"

    # Test Invert
    app.invert_selection()
    selected_count = sum(1 for v in app.checkbox_vars.values() if v.get())
    log_lines.append(f"After invert_selection(): {selected_count}/{num_checkboxes} selected")
    assert selected_count == num_checkboxes, "invert_selection failed!"

    # Test Preview Trigger
    first_item = scanned[0]
    app.preview_file(first_item["full_path"], first_item)
    preview_box_content = app.txt_preview.get("1.0", "end-1c")
    log_lines.append(f"Preview Box content length: {len(preview_box_content)}")
    assert len(preview_box_content) > 0, "Preview box is empty!"

    # Destroy cleanly
    app.destroy()
    log_lines.append("App window destroyed cleanly without error.")
    log_lines.append("-> UI Lifecycle Test: PASSED")
    
    log_lines.append("\n=== All Verification Tests Completed Successfully ===")
    
    output_dir = r"E:\DOCU\results\v0.01"
    os.makedirs(output_dir, exist_ok=True)
    log_path = os.path.join(output_dir, "operational_log.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print(f"Log written to {log_path}")

if __name__ == "__main__":
    run_diagnostics()
