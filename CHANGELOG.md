# CHANGELOG

All notable changes and milestones for the DOCU project will be documented in this file.

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
