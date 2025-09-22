from bin.processor import CSVProcessor
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading

class ProcessingDialog(tk.Toplevel):
    def __init__(self, parent, message="Processing..."):
        super().__init__(parent)
        self.title("Please Wait")
        self.geometry("300x120")
        self.resizable(False, False)

        self.label = tk.Label(self, text=message, padx=20, pady=10)
        self.label.pack()

        self.progress = ttk.Progressbar(self, mode='indeterminate', length=250)
        self.progress.pack(pady=10)
        self.progress.start(10)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: None)

    def update_message(self, new_message):
        self.label.config(text=new_message)
        self.update_idletasks()



class HexyAPP:
    def __init__(self, root):
        self.root = root
        self.root.title("Hexify: Hex Id to GIS")

        self.input_path = tk.StringVar()
        self.hex_id_col_name = tk.StringVar()
        self.output_layer_name = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # input csv
        tk.Label(self.root, text="Input CSV File Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=10)
        tk.Button(self.root, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=10)
        # hex_id_col Name
        tk.Label(self.root, text="Hex ID Column Name:").grid(row=1, column=0, pady=10)
        tk.Entry(self.root, textvariable=self.hex_id_col_name, width=50).grid(row=1, column=1, padx=10)
        # Output layer name
        tk.Label(self.root, text="Output Layer Name:").grid(row=2, column=0, pady=10)
        tk.Entry(self.root, textvariable=self.output_layer_name, width=50).grid(row=2, column=1, padx=10)
        # submit button
        tk.Button(self.root, text="Process and Save", command=self.process_file).grid(row=3, column=1, pady=20)


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.input_path.set(file_path)

    def process_file(self):
        input_file = self.input_path.get()
        hex_id = self.hex_id_col_name.get()
        output_layer_name = self.output_layer_name.get()
        if not input_file:
            messagebox.showerror("Error", "Please select a CSV file.")
            return

        if not hex_id:
            messagebox.showerror("Error", "Please type Hex id Column Name")
            return

        if not output_layer_name:
            messagebox.showerror("Error", "Please assign layer name")
            return

        dialog = ProcessingDialog(self.root, message="Starting....")

        def run_processing():
            try:
                self.root.after(0, lambda: dialog.update_message("Loading CSV..."))
                processor = CSVProcessor(input_file)
                processor.load_csv()
                len_row = len(processor.df)
                self.root.after(0, lambda: dialog.update_message(f"Creating Geometries using '{hex_id}' for {len_row} number of rows"))
                processor.create_gis_file(hex_id_col_name=hex_id)

                self.root.after(0, lambda: dialog.update_message(f"Saving GIS data"))
                processor.save_gdf(output_layer_name=processor.output_layer_name)

                output_file = processor.gpkg_output_path

                self.root.after(0, lambda: messagebox.showinfo("Success", f"File saved to:\n{output_file}"))
            except Exception as ex:
                error_message = str(ex)
                self.root.after(0, lambda: messagebox.showerror("Processing Error", error_message))

            finally:
                self.root.after(0, dialog.destroy)

        threading.Thread(target=run_processing, daemon=True).start()
