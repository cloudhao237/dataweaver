import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from dataweaver.core import BatchMerger, TextNormalizer, PATTERNS
from dataweaver import __version__

class DataWeaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"DataWeaver Desktop v{__version__} - Fast Local Data Processing")
        self.root.geometry("720x520")
        self.root.minsize(650, 480)

        # Style configuration
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self._create_widgets()

    def _create_widgets(self):
        # Header banner
        header_frame = tk.Frame(self.root, bg="#1e293b", height=70)
        header_frame.pack(fill="x", side="top")
        
        lbl_title = tk.Label(header_frame, text="⚡ DataWeaver Studio", font=("Helvetica", 18, "bold"), fg="#38bdf8", bg="#1e293b")
        lbl_title.pack(anchor="w", padx=20, pady=(12, 2))
        
        lbl_sub = tk.Label(header_frame, text="Privacy-First Batch Data Merger & Entity Extractor • 100% Offline", font=("Helvetica", 10), fg="#94a3b8", bg="#1e293b")
        lbl_sub.pack(anchor="w", padx=20, pady=(0, 10))

        # Notebook tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Tab 1: Batch Merger
        self.tab_merge = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_merge, text=" 📂 Batch File Merger ")
        self._build_merge_tab()

        # Tab 2: Entity Extractor
        self.tab_extract = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_extract, text=" 🔍 Regex Entity Extractor ")
        self._build_extract_tab()

        # Status Bar
        self.status_var = tk.StringVar(value="Ready. All operations run 100% locally on your computer.")
        status_bar = tk.Label(self.root, textvariable=self.status_var, font=("Helvetica", 9), bd=1, relief="sunken", anchor="w", fg="#475569", bg="#f1f5f9")
        status_bar.pack(side="bottom", fill="x")

    def _build_merge_tab(self):
        frame = ttk.Frame(self.tab_merge, padding=15)
        frame.pack(fill="both", expand=True)

        lbl = ttk.Label(frame, text="Select multiple CSV or TSV files to merge into one clean dataset:")
        lbl.pack(anchor="w", pady=(0, 8))

        btn_select = ttk.Button(frame, text="📁 Select Files...", command=self._select_merge_files)
        btn_select.pack(anchor="w")

        self.listbox_files = tk.Listbox(frame, height=8, selectmode="extended")
        self.listbox_files.pack(fill="both", expand=True, pady=10)

        # Options
        self.dedup_var = tk.BooleanVar(value=True)
        chk_dedup = ttk.Checkbutton(frame, text="Automatically deduplicate identical rows", variable=self.dedup_var)
        chk_dedup.pack(anchor="w", pady=(0, 10))

        # Run Button
        btn_run = tk.Button(frame, text="🚀 Merge & Export Consolidated CSV", bg="#0284c7", fg="white", font=("Helvetica", 11, "bold"), relief="flat", padx=15, pady=8, command=self._run_merge)
        btn_run.pack(fill="x")

    def _build_extract_tab(self):
        frame = ttk.Frame(self.tab_extract, padding=15)
        frame.pack(fill="both", expand=True)

        lbl = ttk.Label(frame, text="Select raw unformatted text file to extract emails, phones, URLs:")
        lbl.pack(anchor="w", pady=(0, 8))

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", pady=(0, 10))

        self.extract_path_var = tk.StringVar()
        entry_path = ttk.Entry(input_frame, textvariable=self.extract_path_var)
        entry_path.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_browse = ttk.Button(input_frame, text="Browse...", command=self._select_extract_file)
        btn_browse.pack(side="right")

        # Result preview box
        lbl_prev = ttk.Label(frame, text="Extraction Output Log:")
        lbl_prev.pack(anchor="w", pady=(5, 5))

        self.txt_extract_log = tk.Text(frame, height=10, state="disabled", bg="#f8fafc")
        self.txt_extract_log.pack(fill="both", expand=True, pady=(0, 10))

        # Run Button
        btn_extract = tk.Button(frame, text="🔍 Start Extraction to CSV", bg="#059669", fg="white", font=("Helvetica", 11, "bold"), relief="flat", padx=15, pady=8, command=self._run_extract)
        btn_extract.pack(fill="x")

    def _select_merge_files(self):
        files = filedialog.askopenfilenames(
            title="Select CSV/TSV Files",
            filetypes=[("Data Files", "*.csv *.tsv *.txt"), ("All Files", "*.*")]
        )
        if files:
            self.listbox_files.delete(0, tk.END)
            for f in files:
                self.listbox_files.insert(tk.END, f)
            self.status_var.set(f"Selected {len(files)} files for merging.")

    def _select_extract_file(self):
        f = filedialog.askopenfilename(
            title="Select Text Dump File",
            filetypes=[("Text / Log Files", "*.txt *.log *.csv *.json"), ("All Files", "*.*")]
        )
        if f:
            self.extract_path_var.set(f)

    def _run_merge(self):
        files = list(self.listbox_files.get(0, tk.END))
        if not files:
            messagebox.showwarning("No Files", "Please select at least one file to merge.")
            return

        out_path = filedialog.asksaveasfilename(
            title="Save Merged CSV As",
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )
        if not out_path:
            return

        self.status_var.set("Merging files, please wait...")
        
        def task():
            try:
                res = BatchMerger.merge_csv_files(files, out_path, deduplicate=self.dedup_var.get())
                self.root.after(0, lambda: self._on_merge_done(res))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Merge Error", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _on_merge_done(self, res):
        self.status_var.set(f"Done! {res['processed_files']} files merged into {res['total_records']} rows.")
        messagebox.showinfo(
            "Success",
            f"Successfully merged {res['processed_files']} files!\n\n"
            f"Total records: {res['total_records']}\n"
            f"Columns: {res['columns']}\n\n"
            f"Saved to: {res['output_path']}"
        )

    def _run_extract(self):
        inp_file = self.extract_path_var.get().strip()
        if not inp_file or not os.path.exists(inp_file):
            messagebox.showwarning("Invalid File", "Please select an existing text or dump file.")
            return

        out_path = filedialog.asksaveasfilename(
            title="Save Extracted Entities CSV As",
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )
        if not out_path:
            return

        self.status_var.set("Extracting entities...")

        def task():
            try:
                res = BatchMerger.extract_entities_to_csv(inp_file, out_path)
                self.root.after(0, lambda: self._on_extract_done(res))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Extraction Error", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def _on_extract_done(self, res):
        summary_lines = ["Extraction Summary:"]
        for k, v in res["total_extracted"].items():
            summary_lines.append(f"  • {k}: {v} items")
        summary_lines.append(f"\nSaved to: {res['output_path']}")
        
        self.txt_extract_log.config(state="normal")
        self.txt_extract_log.delete("1.0", tk.END)
        self.txt_extract_log.insert(tk.END, "\n".join(summary_lines))
        self.txt_extract_log.config(state="disabled")
        
        self.status_var.set("Extraction finished successfully.")
        messagebox.showinfo("Extraction Complete", f"Entities successfully saved to:\n{res['output_path']}")

def launch_gui():
    root = tk.Tk()
    app = DataWeaverApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
