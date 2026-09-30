# CHANGELOG

All notable changes and milestones for the DOCU project will be documented in this file.

## [v0.02] - 2026-09-30

### Added
- **Create Aggregate Feature**:
  - Implemented `src/utils/aggregator.py` with:
    - Dynamic ASCII hierarchical tree map generation at the top of the aggregate file.
    - Full recursive scan with extension filtering for `JS` (`.js`, `.mjs`, `.cjs`, `.jsx`), `JSON` (`.json`), `All`, or custom extensions.
    - Per-file header comments including file name, relative path, and full path.
    - Explicit line numbering in `<line_number>::<line_content>` format across all lines of each file.
    - Automated export into `E:\DOCU\Reports\`.
  - Implemented `src/ui/aggregate_modal.py` (`AggregateModal`) providing a modal popup to select file types (`All`, `JS`, `JSON`, `Custom`) and trigger aggregation.
  - Added "Create Aggregate" button directly alongside the target folder path in `src/ui/app.py`.
  - Integrated immediate file previewing of the generated aggregate report upon completion.
  - Created `verify_milestone_v02.py` and output verification proof to `results/v0.02/operational_log.txt`.

## [v0.01] - 2026-09-30

### Initialized
- Localized `AGENT.md` from `packages/mindscape/` to `E:\DOCU\` and project name `DOCU`.
- Created dedicated backup and integrity verification script `docu_backup.py`.
- Installed `customtkinter` (v6.0.0) and `darkdetect` for modern Windows 11 desktop styling.
- Created `src/utils/file_scanner.py` for recursive file scanning, size formatting, and text preview loading.
- Created `src/ui/app.py` featuring:
  - Header panel with directory path bar and native directory dialog (`filedialog.askdirectory()`).
  - Search and extension filtering (`*.md`, `*.py`, `*.json`, `*.txt`, etc.).
  - `CTkScrollableFrame` with dynamically packed `CTkCheckBox` components for every scanned file.
  - Multi-selection controls: Select All, Deselect All, Invert Selection.
  - Side-by-side file content inspection panel (`CTkTextbox`).
  - Status bar with live selected file count.
- Created `main.py` entry point.
- Created `verify_milestone.py` and generated proof logs in `results/v0.01/operational_log.txt`.
