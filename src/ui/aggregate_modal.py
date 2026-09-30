import os
import subprocess
import customtkinter as ctk
from typing import Optional, Callable
from src.utils.aggregator import create_aggregate_file

class AggregateModal(ctk.CTkToplevel):
    def __init__(self, parent, target_dir: str, on_success_callback: Optional[Callable[[str], None]] = None):
        super().__init__(parent)

        self.target_dir = target_dir
        self.on_success_callback = on_success_callback
        self.output_dir = r"E:\DOCU\Reports"

        self.title("Create Aggregate - Select File Types")
        self.geometry("520x420")
        self.resizable(False, False)

        # Make it modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.after(100, self.lift)

    def _build_ui(self):
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # Title
        lbl_title = ctk.CTkLabel(
            main_frame,
            text="📁 Create Folder Aggregate",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_title.pack(anchor="w", padx=16, pady=(16, 4))

        lbl_desc = ctk.CTkLabel(
            main_frame,
            text="Recursively combine folder files into a single structured report with line numbers and tree map.",
            font=ctk.CTkFont(size=12),
            text_color="gray70",
            wraplength=460,
            justify="left"
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 12))

        # Target Dir Display
        dir_frame = ctk.CTkFrame(main_frame, fg_color="gray20", corner_radius=6)
        dir_frame.pack(fill="x", padx=16, pady=(0, 12))

        lbl_target_title = ctk.CTkLabel(dir_frame, text="Source Folder:", font=ctk.CTkFont(size=11, weight="bold"))
        lbl_target_title.pack(anchor="w", padx=10, pady=(6, 0))

        lbl_target_val = ctk.CTkLabel(dir_frame, text=self.target_dir, font=ctk.CTkFont(size=11), text_color="cyan")
        lbl_target_val.pack(anchor="w", padx=10, pady=(0, 6))

        # File Type Selection
        lbl_select_type = ctk.CTkLabel(main_frame, text="Select File Types to Include:", font=ctk.CTkFont(size=13, weight="bold"))
        lbl_select_type.pack(anchor="w", padx=16, pady=(4, 6))

        self.type_var = ctk.StringVar(value="JS")

        types_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        types_frame.pack(fill="x", padx=16, pady=(0, 8))

        rb_all = ctk.CTkRadioButton(types_frame, text="All Files (*.*)", variable=self.type_var, value="All")
        rb_all.pack(side="left", padx=(0, 16))

        rb_js = ctk.CTkRadioButton(types_frame, text="JS Files (*.js)", variable=self.type_var, value="JS")
        rb_js.pack(side="left", padx=(0, 16))

        rb_json = ctk.CTkRadioButton(types_frame, text="JSON Files (*.json)", variable=self.type_var, value="JSON")
        rb_json.pack(side="left", padx=(0, 16))

        # Custom extension row
        custom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        custom_frame.pack(fill="x", padx=16, pady=(4, 8))

        rb_custom = ctk.CTkRadioButton(custom_frame, text="Custom:", variable=self.type_var, value="Custom")
        rb_custom.pack(side="left", padx=(0, 8))

        self.entry_custom = ctk.CTkEntry(custom_frame, placeholder_text="e.g. .py or .md", width=120)
        self.entry_custom.pack(side="left")

        # Output status/destination
        lbl_out = ctk.CTkLabel(
            main_frame,
            text=f"Destination: Reports\\ in E:\\DOCU",
            font=ctk.CTkFont(size=11),
            text_color="gray60"
        )
        lbl_out.pack(anchor="w", padx=16, pady=(4, 12))

        self.lbl_status = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12))
        self.lbl_status.pack(anchor="w", padx=16, pady=(0, 8))

        # Action Buttons
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(6, 12), side="bottom")

        self.btn_cancel = ctk.CTkButton(
            btn_frame, 
            text="Cancel", 
            width=90, 
            fg_color="gray30", 
            hover_color="gray40",
            command=self.destroy
        )
        self.btn_cancel.pack(side="right", padx=(8, 0))

        self.btn_generate = ctk.CTkButton(
            btn_frame,
            text="Create Aggregate",
            width=140,
            fg_color="#28a745",
            hover_color="#218838",
            command=self._execute_aggregation
        )
        self.btn_generate.pack(side="right")

        self.btn_open_folder = ctk.CTkButton(
            btn_frame,
            text="📂 Open Reports",
            width=120,
            fg_color="#17a2b8",
            hover_color="#138496",
            command=self._open_reports_folder
        )
        # Hidden until success

    def _execute_aggregation(self):
        sel_type = self.type_var.get()
        custom_ext = self.entry_custom.get().strip() if sel_type == "Custom" else None

        self.btn_generate.configure(state="disabled", text="Aggregating...")
        self.lbl_status.configure(text="Scanning files and compiling aggregate report...", text_color="yellow")
        self.update()

        try:
            result = create_aggregate_file(
                target_dir=self.target_dir,
                file_type=sel_type,
                custom_ext=custom_ext,
                output_dir=self.output_dir
            )

            self.created_filepath = result["output_path"]
            msg = f"Success! Created {result['output_filename']} ({result['total_files']} files, {result['total_lines']} lines)"
            self.lbl_status.configure(text=msg, text_color="#4cd137")
            self.btn_generate.configure(state="normal", text="Completed")
            self.btn_open_folder.pack(side="left")

            if self.on_success_callback:
                self.on_success_callback(self.created_filepath)

        except Exception as e:
            self.lbl_status.configure(text=f"Error: {e}", text_color="red")
            self.btn_generate.configure(state="normal", text="Create Aggregate")

    def _open_reports_folder(self):
        if os.path.exists(self.output_dir):
            os.startfile(self.output_dir)
