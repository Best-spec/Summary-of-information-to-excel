import tkinter as tk
from tkinter import ttk, messagebox

class ColorConfig:
    def __init__(self, parent):
        self.parent = parent
        self.result = {}

        self.window = tk.Toplevel(parent)
        self.window.title("Custom Graph Colors")
        self.window.geometry("400x400")
        self.window.grab_set()

        fields = [
            ("สีแต่ละแท่งกราฟ", "bar_colors"),
            ("สีหัวข้อเรื่อง", "title_color"),
            ("สีข้อความแกน X", "xlabel_color"),
            ("สีข้อความแกน Y", "ylabel_color"),
            ("สีชื่อแต่ละประเภทข้อมูล", "xtick_color"),
            ("สีตัวเลขแกน X", "ytick_color"),
            ("สีเลขบนกราฟ", "bar_text_color")
        ]

        catServices = {
            "inquiry": 4,
            "appointment": 2,
            "topcenter": 3,
            "total_month": 6
        }

        self.entries = {}

        for idx, (label, key) in enumerate(fields):
            ttk.Label(self.window, text=label).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(self.window, width=40)
            entry.grid(row=idx, column=1, padx=10)
            self.entries[key] = entry

        ttk.Button(self.window, text="ตกลง", command=self.submit).grid(row=len(fields), column=0, columnspan=2, pady=10)
        ttk.Button(self.window, text="Default Color", command=self.set_default_theme).grid(row=len(fields), column=1, columnspan=2, pady=10)

        self.window.wait_window()

    def submit(self):
        for key, entry in self.entries.items():
            value = entry.get().strip()
            
            # เช็คค่าว่าง
            if not value:
                messagebox.showerror("Error", f"กรุณากรอกค่าของ '{key}'")
                return

            if key == "bar_colors":
                colors = [x.strip() for x in value.split(",") if x.strip()]
                if not colors:
                    messagebox.showerror("Error", "กรุณากรอก bar_colors อย่างน้อย 1 ค่า")
                    return
                self.result[key] = colors
            else:
                self.result[key] = value

        self.window.destroy()

    def get_result(self):
        return self.result
    
    def set_default_theme(self):
        default_colors = {
            "bar_colors": ["lightgray"] * 5 + ["cyan", "cyan", "lightgray"],
            "title_color": "lightgray",
            "xlabel_color": "lightgray",
            "ylabel_color": "lightgray",
            "xtick_color": "lightgray",
            "ytick_color": "lightgray",
            "bar_text_color": "lightgray"
        }
        for key, entry in self.entries.items():
            val = default_colors.get(key, "")
            entry.delete(0, tk.END)
            if isinstance(val, list):
                entry.insert(0, ", ".join(val))
            else:
                entry.insert(0, val)
    
    def get_graph_colors(self, theme="default", custom_colors=None):
        if custom_colors:
            return custom_colors  # ใช้ dict ที่ส่งมาเลย
