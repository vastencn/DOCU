# DOCU Project Documentation

This document maps the structure, architecture, and responsibilities of the files in the `DOCU` documentation and workspace system.

## Project Overview
DOCU is a lightweight, modern, code-driven documentation tool and file browser built on Python 3 and CustomTkinter. It provides a Windows 11 native aesthetic, folder browsing, dynamic file checklist management, and instant file inspection/previewing.

## Directory Structure

```text
E:\DOCU\
├── AGENT.md                 # System Directive & Standard Operating Procedure (SOP)
├── DOCUMENTATION.md         # Map of project architecture and module responsibilities
├── CHANGELOG.md             # Chronological ledger of versions and modifications
├── docu_backup.py           # Verification and backup automation script
├── verify_milestone.py      # Automated verification and diagnostics runner
├── main.py                  # Application entry point
├── package.json             # Workspace metadata and configuration
├── backups/                 # Validated ZIP archives generated per milestone
├── results/                 # Verification outputs and test logs
│   └── v0.01/
│       └── operational_log.txt
└── src/
    ├── ui/
    │   ├── __init__.py      # UI package initializer
    │   └── app.py           # CustomTkinter modern UI implementation (FileBrowserApp)
    └── utils/
        ├── __init__.py      # Utilities package initializer
        └── file_scanner.py  # File system scanner, metadata extractor, and file preview loader
```

## Module Responsibilities

### `main.py`
- Main execution entry point.
- Bootstraps the CustomTkinter runtime, resolves initial working directory, and launches `FileBrowserApp`.

### `src/ui/app.py` (`FileBrowserApp`)
- Encapsulates the entire desktop graphical interface using `customtkinter`.
- **Header Panel:**
  - Directory path input and `filedialog.askdirectory()` browser.
  - File extension combo filter (`*.md`, `*.py`, `*.json`, `*.txt`, etc.).
  - Filename search filter with live key-up event handling.
  - Subfolder recursion toggle.
  - Theme mode toggling (Dark / Light).
- **Checklist Panel (`CTkScrollableFrame`):**
  - Dynamically renders `CTkCheckBox` components for scanned files.
  - Provides bulk selection helpers: `Select All`, `Deselect All`, `Invert Selection`.
  - Integrates file size preview badges with direct preview hooks.
- **Preview & Inspection Panel:**
  - Text area (`CTkTextbox`) for inspecting code, documentation, and metadata without leaving the application.
- **Status Bar:**
  - Real-time tally of selected files versus total scanned files.

### `src/utils/file_scanner.py`
- **`scan_directory()`**: Recursively or flatly scans directories, filtering out ignored folders (`.git`, `__pycache__`, `backups`, `results`).
- **`format_size()`**: Formats raw byte counts into human-readable strings (B, KB, MB).
- **`read_file_preview()`**: Safely extracts the first $N$ lines of text and code files for instant display.

### `docu_backup.py`
- Validates source files against size limits and allowed extensions.
- Creates timestamped ZIP archives in `backups/`.
- Verifies archive integrity with `testzip()` and checks for blacklisted directories.
