import os
import sys
import datetime

sys.path.insert(0, r"E:\DOCU")

from src.utils.aggregator import (
    generate_tree_map,
    collect_files_for_aggregation,
    create_aggregate_file
)
from src.ui.app import FileBrowserApp
from src.ui.aggregate_modal import AggregateModal

def run_diagnostics():
    log_lines = []
    log_lines.append("=== DOCU Aggregate Feature Verification Log (v0.02) ===")
    log_lines.append(f"Timestamp: {datetime.datetime.now().isoformat()}")
    log_lines.append(f"Target Directory: E:\\DOCU")
    log_lines.append(f"Python: {sys.version}")

    # 1. Tree Map Generation Test
    sample_paths = [
        "index.js",
        "package.json",
        "src/main.js",
        "src/components/button.jsx",
        "src/utils/math.js"
    ]
    tree = generate_tree_map(r"E:\DOCU", sample_paths)
    log_lines.append("\n[Test 1] Hierarchical Tree Map Generator:")
    log_lines.append(tree)
    assert "├── " in tree or "└── " in tree, "Tree connectors missing!"
    assert "components/" in tree, "Nested directory missing from tree map!"
    log_lines.append("-> Tree Map Test: PASSED")

    # 2. Test File Aggregation for 'All'
    log_lines.append("\n[Test 2] Aggregate Creation (All Files):")
    res_all = create_aggregate_file(
        target_dir=r"E:\DOCU",
        file_type="All",
        output_dir=r"E:\DOCU\Reports"
    )
    log_lines.append(f"Output File: {res_all['output_path']}")
    log_lines.append(f"Files aggregated: {res_all['total_files']}, Total lines: {res_all['total_lines']}, Size: {res_all['file_size']} bytes")
    assert os.path.exists(res_all['output_path']), "Aggregate file not created on disk!"
    assert res_all['total_files'] > 0, "No files found to aggregate!"
    log_lines.append("-> Aggregation (All) Test: PASSED")

    # 3. Content Inspection of Generated Aggregate
    log_lines.append("\n[Test 3] Aggregate Formatting & Line Number Verification:")
    with open(res_all['output_path'], "r", encoding="utf-8") as f:
        content_lines = f.readlines()

    preview_first_50 = content_lines[:40]
    log_lines.append(f"Read {len(content_lines)} lines from output.")
    log_lines.append("Sample lines from start of file:")
    for line in preview_first_50[:15]:
        log_lines.append("  " + line.rstrip())

    # Check for hierarchical tree map at top
    has_tree = any("HIERARCHICAL FILE MAP:" in l for l in content_lines[:30])
    log_lines.append(f"Contains Hierarchical Map at top: {has_tree}")
    assert has_tree, "Hierarchical file map missing at top of aggregate!"

    # Check for file header comment
    has_header = any("// FILE:" in l for l in content_lines)
    has_path = any("// PATH:" in l for l in content_lines)
    has_full_path = any("// FULL PATH:" in l for l in content_lines)
    log_lines.append(f"Contains // FILE: {has_header}, // PATH: {has_path}, // FULL PATH: {has_full_path}")
    assert has_header and has_path and has_full_path, "File header comment format missing!"

    # Check line numbering format: <line_no>::<content>
    line_number_formatted = [l for l in content_lines if "::" in l and not l.startswith("=")]
    log_lines.append(f"Sample formatted lines ({len(line_number_formatted)} total):")
    for l in line_number_formatted[:5]:
        log_lines.append("  " + l.rstrip())
    assert len(line_number_formatted) > 0, "No <num>::<content> formatted lines found!"
    log_lines.append("-> Formatting Verification: PASSED")

    # 4. Test Aggregation for specific type (JSON)
    log_lines.append("\n[Test 4] Aggregate Creation (JSON Files):")
    res_json = create_aggregate_file(
        target_dir=r"E:\DOCU",
        file_type="JSON",
        output_dir=r"E:\DOCU\Reports"
    )
    log_lines.append(f"JSON aggregate files count: {res_json['total_files']}")
    assert res_json['total_files'] >= 1, "Should find at least package.json!"
    log_lines.append("-> Aggregation (JSON) Test: PASSED")

    # 5. UI Integration Test
    log_lines.append("\n[Test 5] UI Integration & Modal Dialog Test:")
    app = FileBrowserApp(initial_dir=r"E:\DOCU")
    app.update()

    # Open modal
    modal = AggregateModal(app, target_dir=r"E:\DOCU")
    modal.update()
    log_lines.append("AggregateModal initialized and updated successfully.")
    assert modal.type_var.get() == "JS", "Default selection should be initialized."

    # Test switching type
    modal.type_var.set("All")
    assert modal.type_var.get() == "All"

    modal.destroy()
    app.destroy()
    log_lines.append("Modal and main app window closed cleanly.")
    log_lines.append("-> UI Integration Test: PASSED")

    log_lines.append("\n=== All Verification Tests Passed Successfully for v0.02 ===")

    # Write log to results/v0.02/operational_log.txt
    res_dir = r"E:\DOCU\results\v0.02"
    os.makedirs(res_dir, exist_ok=True)
    log_file = os.path.join(res_dir, "operational_log.txt")
    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write("\n".join(log_lines))
    print(f"Log written to {log_file}")

if __name__ == "__main__":
    run_diagnostics()
