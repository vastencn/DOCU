# DOCU — Modern Documentation & File Aggregator

A code-driven desktop application built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), featuring a modern Windows 11 aesthetic. DOCU provides fast directory scanning, interactive file checklist management, in-app file previewing, and hierarchical multi-file report aggregation.

---

## Features

- **Windows 11 Native Aesthetic:** Dark and Light mode support powered by CustomTkinter and DarkDetect.
- **Directory Browser:** Quick folder navigation with native `filedialog.askdirectory()` and editable path entry.
- **Live Search & Extension Filters:** Instant filename query matching and dropdown presets (`*.md`, `*.py`, `*.json`, `*.txt`, `*.js`, `*.*`).
- **Dynamic File Checklist (`CTkScrollableFrame`):** Dynamically populated checkboxes with multi-selection helpers (`All`, `None`, `Invert`).
- **File Inspector & Previewer (`CTkTextbox`):** In-app text and syntax inspection without switching windows.
- **Create Aggregate Report Tool:**
  - One-click modal popup to select file types (`All`, `JS`, `JSON`, or `Custom`).
  - Generates a unified report in `Reports/` featuring:
    - Top-level ASCII hierarchical file tree map.
    - File header comment blocks (`// FILE:`, `// PATH:`, `// FULL PATH:`).
    - Every file numbered with `<line_number>::<line_content>`.
- **Integrity & Verification Pipeline:** Built-in verification testing (`verify_milestone.py`) and automated ZIP backup script (`docu_backup.py`).

---

## Project Structure

```text
E:\DOCU\
├── AGENT.md                 # System Directive & Standard Operating Procedure (SOP)
├── DOCUMENTATION.md         # Architecture and module responsibilities map
├── CHANGELOG.md             # Version milestone ledger
├── README.md                # Project documentation and quickstart guide
├── docu_backup.py           # Pre-flight and post-flight ZIP backup validation
├── requirements.txt         # Python package dependencies
├── pyproject.toml           # Project build and package configuration
├── package.json             # Workspace configuration
├── main.py                  # Desktop application entry point
├── backups/                 # Validated ZIP archives (ignored by git)
├── Reports/                 # Generated aggregate text reports (ignored by git)
├── results/                 # Verification logs and proof outputs (ignored by git)
└── src/
    ├── ui/
    │   ├── __init__.py      # UI package module
    │   ├── app.py           # Main application window (FileBrowserApp)
    │   └── aggregate_modal.py # Modal dialog for file aggregation
    └── utils/
        ├── __init__.py      # Utilities package module
        ├── file_scanner.py  # Recursive file scanner & preview loader
        └── aggregator.py    # Aggregation engine with tree mapping & line numbering
```

---

## Installation & Setup

### Prerequisites
- Python 3.9+ (Python 3.11 recommended)
- Git

### Installation
Clone or navigate to the repository directory:
```bash
cd E:\DOCU
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Usage

### Launch the Desktop Application
```bash
python main.py
```
Or optionally pass a folder path directly:
```bash
python main.py "E:\DOCU"
```

### Generating an Aggregate Report
1. Click **Browse...** to select your target project folder.
2. Click **Create Aggregate** next to the path entry.
3. Select your desired file type filter (`All Files`, `JS Files (*.js)`, `JSON Files (*.json)`, or custom extension).
4. Click **Create Aggregate**.
5. The unified report will be generated and saved to `Reports/`, and immediately previewed in the app inspector.

---

## Development & Testing

Run the automated milestone verification suite:
```bash
python verify_milestone_v02.py
```

Run the automated backup and verification protocol:
```bash
python docu_backup.py docu_src_v0.03
```

---

## License
MIT / ISC
