import os
import sys
import subprocess
import datetime

sys.path.insert(0, r"E:\DOCU")

def run_diagnostics():
    log_lines = []
    log_lines.append("=== DOCU Git Project Standardization Verification Log (v0.03) ===")
    log_lines.append(f"Timestamp: {datetime.datetime.now().isoformat()}")
    log_lines.append(f"Target Directory: E:\\DOCU")
    log_lines.append(f"Python: {sys.version}")

    # 1. Check Git files
    log_lines.append("\n[Test 1] Git Configuration Files Check:")
    required_files = [
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        ".gitignore",
        "DOCUMENTATION.md",
        "CHANGELOG.md",
        "AGENT.md"
    ]
    for rf in required_files:
        path = os.path.join(r"E:\DOCU", rf)
        exists = os.path.exists(path)
        log_lines.append(f" - {rf}: {'EXISTS' if exists else 'MISSING'}")
        assert exists, f"Required file {rf} is missing!"
    log_lines.append("-> Configuration Files Test: PASSED")

    # 2. Check Git Repo status
    log_lines.append("\n[Test 2] Git Repository Health Check:")
    git_dir = os.path.join(r"E:\DOCU", ".git")
    assert os.path.exists(git_dir), ".git directory does not exist!"
    log_lines.append(" - .git directory: PRESENT")
    
    # 3. Aggregator and UI modules check
    log_lines.append("\n[Test 3] Application Core Modules Integrity:")
    from src.utils.aggregator import collect_files_for_aggregation, create_aggregate_file
    from src.utils.file_scanner import scan_directory
    from src.ui.app import FileBrowserApp
    
    files = scan_directory(r"E:\DOCU")
    log_lines.append(f" - Directory scan found {len(files)} files.")
    assert len(files) > 0, "Scan found no files!"
    log_lines.append("-> Core Modules Test: PASSED")

    log_lines.append("\n=== All Verification Tests Passed Successfully for v0.03 ===")

    res_dir = r"E:\DOCU\results\v0.03"
    os.makedirs(res_dir, exist_ok=True)
    log_file = os.path.join(res_dir, "operational_log.txt")
    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write("\n".join(log_lines))
    print(f"Log written to {log_file}")

if __name__ == "__main__":
    run_diagnostics()
