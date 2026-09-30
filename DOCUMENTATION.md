# DOCU Project Documentation

This document maps the structure, architecture, and responsibilities of the files in the `DOCU` documentation and workspace system.

## Project Overview
DOCU is a lightweight, modern, code-driven documentation tool and file browser built on Python 3 and CustomTkinter. It provides a Windows 11 native aesthetic, folder browsing, dynamic file checklist management, instant file inspection/previewing, and multi-file code aggregation reports.

## Directory Structure

```text
E:\DOCU\
├── .gitignore               # Comprehensive Git ignore rules (Python, IDE, OS, Reports)
├── AGENT.md                 # System Directive & Standard Operating Procedure (SOP)
├── DOCUMENTATION.md         # Map of project architecture and module responsibilities
├── CHANGELOG.md             # Chronological ledger of versions and modifications
├── README.md                # Repository overview, installation, and usage documentation
├── requirements.txt         # Pinned Python package dependencies
├── pyproject.toml           # Standard Python package and build configuration
├── docu_backup.py           # Verification and backup automation script
├── verify_milestone.py      # Automated verification runner (v0.01)
├── verify_milestone_v02.py  # Automated verification runner (v0.02)
├── main.py                  # Application entry point
├── package.json             # Workspace metadata and configuration
├── backups/                 # Validated ZIP archives generated per milestone (ignored by git)
├── Reports/                 # Generated aggregate documentation text reports (ignored by git)
├── results/                 # Verification outputs and test logs (ignored by git)
│   ├── v0.01/
│   │   └── operational_log.txt
│   ├── v0.02/
│   │   └── operational_log.txt
│   └── v0.03/
│       └── operational_log.txt
└── src/
    ├── ui/
    │   ├── __init__.py      # UI package initializer
    │   ├── app.py           # CustomTkinter modern UI implementation (FileBrowserApp)
    │   └── aggregate_modal.py # Modal dialog for selecting file types and generating reports
    └── utils/
        ├── __init__.py      # Utilities package initializer
        ├── file_scanner.py  # File system scanner, metadata extractor, and file preview loader
        └── aggregator.py    # Recursive aggregation engine with tree mapping & line numbering
```

## Module Responsibilities

### `main.py`
- Main execution entry point.
- Bootstraps the CustomTkinter runtime, resolves initial working directory, and launches `FileBrowserApp`.

### `src/ui/app.py` (`FileBrowserApp`)
- Encapsulates the desktop graphical interface using `customtkinter`.
- **Header Panel:**
  - Directory path input and `filedialog.askdirectory()` browser.
  - "Create Aggregate" button directly adjacent to the folder path for fast report generation.
  - File extension combo filter (`*.md`, `*.py`, `*.json`, `*.txt`, etc.).
  - Filename search filter with live key-up event handling.
  - Subfolder recursion toggle.
  - Theme mode toggling (Dark / Light).
- **Checklist Panel (`CTkScrollableFrame`):**
  - Dynamically renders `CTkCheckBox` components for scanned files.
  - Provides bulk selection helpers: `Select All`, `Deselect All`, `Invert Selection`.
  - Integrates file size preview badges with direct preview hooks.
- **Preview & Inspection Panel:**
  - Text area (`CTkTextbox`) for inspecting code, documentation, and generated aggregate reports.
- **Status Bar:**
  - Real-time tally of selected files versus total scanned files.

### `src/ui/aggregate_modal.py` (`AggregateModal`)
- Modal dialog triggered by clicking "Create Aggregate".
- Presents file type selection options:
  - `All`: Scans and aggregates all non-ignored project files.
  - `JS`: Targets JavaScript files (`.js`, `.mjs`, `.cjs`, `.jsx`).
  - `JSON`: Targets JSON data files (`.json`).
  - `Custom`: Allows specifying custom extensions (e.g. `.py`, `.md`).
- Executes the aggregation process, displays status, and provides a direct shortcut to open the `Reports` folder.

### `src/utils/aggregator.py`
- **`generate_tree_map()`**: Converts a list of relative file paths into a clean ASCII tree representation at the top of the aggregate report.
- **`collect_files_for_aggregation()`**: Recursively traverses the target directory, filtering by file extension while safely excluding build, cache, and version-control artifacts.
- **`create_aggregate_file()`**: Compiles all target files into a single unified report formatted with:
  - Header report metadata.
  - Hierarchical tree map.
  - File comment headers (`// FILE:`, `// PATH:`, `// FULL PATH:`).
  - Explicit line numbering on every line in `<line_number>::<line_content>` format.
  - Automatically saved to `E:\DOCU\Reports\`.

### `src/utils/file_scanner.py`
- **`scan_directory()`**: Recursively or flatly scans directories, filtering out ignored folders (`.git`, `__pycache__`, `backups`, `results`, `Reports`).
- **`format_size()`**: Formats raw byte counts into human-readable strings (B, KB, MB).
- **`read_file_preview()`**: Safely extracts lines of text and code files for instant UI display.

### `docu_backup.py`
- Validates source files against size limits and allowed extensions.
- Creates timestamped ZIP archives in `backups/`.
- Verifies archive integrity with `testzip()` and checks for blacklisted directories.
