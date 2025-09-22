import tkinter as tk
from tkinter import filedialog, messagebox
from bin.processor import CSVProcessor
from hexify.Hexify import HexyAPP


if __name__ == "__main__":
    root = tk.Tk()
    app = HexyAPP(root)
    root.mainloop()
