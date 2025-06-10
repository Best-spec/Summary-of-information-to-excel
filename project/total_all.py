from tkinter import messagebox
import pandas as pd
import glob
import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import tempfile
from config_graph import ColorConfig


categories = {
    'English' : [
        "General Inquiry",
        "Estimated Cost",
        "Contact My Doctor at Bangkok Hospital Pattaya",
        "Other"
    ],

    'Thai' : [
        "สอบถามทั่วไป",
        "ค่าใช้จ่าย",
        "ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา",
        "อื่นๆ"
    ],

    'Russia' : [
        "Общий запрос",
        "Узнать про цену",
        "Написать врачу",
        "Другое"
    ],
    'Arabic' : [
        "General Inquiry",
        "Estimated Cost",
        "Contact My Doctor at Bangkok Hospital Pattaya",
        "Other"
    ],

    'Chinese' : [
        "普通咨询",
        "预估价格咨询",
        "联系芭提雅曼谷医院医生",
        "其他"
    ],

    'German' : [
        "Allgemeine Anfrage",
        "Vorraussichtliche Kosten",
        "Arzt im Bangkok Hospital Pattaya kontaktieren",
        "Andere"
    ]
}

class TotalMonth:
    def __init__(self, folder_path):
        self.folder_path = folder_path
    
    def inquiry(self):
        folder = self.folder_path
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        summary = defaultdict(lambda: defaultdict(int))
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

        for file in csv_files:
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.replace('\ufeff', '').str.strip('"')
                col_name = df.columns[0]
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            if "-en" in file:
                lang = "English"
            elif "-th" in file:
                lang = "Thai"
            elif "-ru" in file:
                lang = "Russia"
            elif "-de" in file:
                lang = "German"
            elif "-ar" in file:
                lang = "Arabic"
            elif "-zh" in file:
                lang = "Chinese"
            else:
                continue

            for cat in categories.get(lang, []):
                count = df[col_name].astype(str).str.strip().eq(cat).sum()
                summary[lang][cat] += count
                
        return summary
        
    def graph_inquiry(self, summary, root):
        # folder = self.folder_path
        # if not folder or not os.path.isdir(folder):
        #     messagebox.showerror("Error", "Please select a valid folder")
        #     return

        # plot graph Type of Email by month 

        # translations สำหรับแปลงชื่อ category เป็นภาษาอังกฤษ
        translations = {
            # Russian
            "Общий запрос": "General Inquiry",
            "Узнать про цену": "Estimated Cost",
            "Написать врачу": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Другое": "Other",
            # German
            "Allgemeine Anfrage": "General Inquiry",
            "Vorraussichtliche Kosten": "Estimated Cost",
            "Arzt im Bangkok Hospital Pattaya kontaktieren": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Andere": "Other",
            # Thai
            "สอบถามทั่วไป": "General Inquiry",
            "ค่าใช้จ่าย": "Estimated Cost",
            "ติดต่อกับหมอประจำตัวที่โรงพยาบาลกรุงเทพพัทยา": "Contact My Doctor at Bangkok Hospital Pattaya",
            "อื่นๆ": "Other",
            # Arabic
            "General Inquiry": "General Inquiry",
            "Estimated Cost": "Estimated Cost",
            "Contact My Doctor at Bangkok Hospital Pattaya": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Other": "Other",
            # Chinese
            "普通咨询": "General Inquiry",
            "预估价格咨询": "Estimated Cost",
            "联系芭提雅曼谷医院医生": "Contact My Doctor at Bangkok Hospital Pattaya",
            "其他": "Other",
            # English already in English
            "General Inquiry": "General Inquiry",
            "Estimated Cost": "Estimated Cost",
            "Contact My Doctor at Bangkok Hospital Pattaya": "Contact My Doctor at Bangkok Hospital Pattaya",
            "Other": "Other",
        }

        # รวม count โดยใช้ชื่อหมวดหมู่ภาษาอังกฤษ
        global_summary = defaultdict(int)

        for lang in summary:
            for cat, count in summary[lang].items():
                eng_cat = translations.get(cat, cat)  # แปลงเป็นอังกฤษ ถ้าไม่มีให้ใช้ชื่อเดิม
                global_summary[eng_cat] += count
            
        global_summary.pop("", None)  # ถ้าไม่มี key จะไม่เกิด error

        # เรียงมากไปน้อย
        sorted_items = sorted(global_summary.items(), key=lambda x: x[1], reverse=True)
        categories_list = [item[0] for item in sorted_items]
        counts = [item[1] for item in sorted_items]


        # วาดกราฟ

        popup = ColorConfig(root, 4)
        color_dict = popup.get_result()
        colorX = popup.get_graph_colors(custom_colors=color_dict)

        plt.figure(figsize=(10, 5))
        bars = plt.bar(categories_list, counts, color=colorX['bar_colors'][:len(categories_list)])

        # ใส่ตัวเลขบนกราฟ
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(height),
                    ha='center', va='bottom', fontsize=10, color=colorX['bar_text_color'])

        plt.ylim(0, max(counts) * 1.2)
        plt.title("Type of Email by month", fontsize=14, color=colorX['title_color'])
        plt.xlabel("ALL language", fontsize=12, color=colorX['ylabel_color'])
        plt.ylabel("Total Count", fontsize=12, color=colorX['xlabel_color'])
        plt.xticks(rotation=45, ha='right', color=colorX['xtick_color'])
        plt.yticks(color=colorX['ytick_color'])  # ใส่ตรงนี้
        plt.tight_layout()

        def get_base_path():
            if getattr(sys, 'frozen', False):
                # 👉 ตอนถูกแปลงเป็น .exe ด้วย pyinstaller
                return sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            else:
                # 👉 ตอนรันแบบ .py ปกติ
                return os.path.dirname(os.path.abspath(__file__))

        # ใช้ path นี้ในการเซฟ
        save_path = os.path.join(get_base_path(), "inquiry.png")

        # วาดกราฟและเซฟ
        plt.savefig(save_path, dpi=300, transparent=True, bbox_inches='tight')

        plt.show()

        # ✅ ปิดหลังแสดงผล
        
    def each_FeedAndPack(self):
        """
        ค้นหาและสรุปข้อมูล Feedback & Suggestion และ Package Inquiry จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        จะอ่านไฟล์ CSV, จัดหมวดหมู่ตามภาษา, นับจำนวนในแต่ละประเภท (Feedback/Package),
        และแสดงผลรวมของแต่ละประเภทแยกตามภาษา.
        """
        folder_path = self.folder_path
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder")
            return
        
        # defaultdict สำหรับเก็บผลรวมของ Feedback และ Package แยกตามภาษา
        feed_counts_by_lang = defaultdict(int)
        pack_counts_by_lang = defaultdict(int)

        # ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์
        all_csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

        for file in all_csv_files:
            lang = None
            # ตรวจสอบภาษาจากชื่อไฟล์
            if "-en" in file:
                lang = "English"
            elif "-th" in file:
                lang = "Thai"
            elif "-ru" in file:
                lang = "Russia"
            elif "-de" in file:
                lang = "German"
            elif "-ar" in file:
                lang = "Arabic"
            elif "-zh" in file:
                lang = "Chinese"
            else:
                continue # ข้ามไฟล์ที่ไม่มี tag ภาษาที่ระบุ

            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                # สมมติว่าคอลัมน์แรกคือคอลัมน์ที่เราต้องการนับจำนวนแถว
                col_name = df.columns[0]
                count = len(df[col_name]) # นับจำนวนแถวทั้งหมดในคอลัมน์แรก
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            # ตรวจสอบว่าเป็นไฟล์ Feedback หรือ Package และเพิ่มจำนวนตามภาษา
            if "feedback-suggestion" in file and lang:
                feed_counts_by_lang[lang] += count
            elif "packages" in file and lang:
                pack_counts_by_lang[lang] += count

        # จัดรูปแบบผลลัพธ์เพื่อแสดงใน Text widget
        output_lines = []
        output_lines.append("\n\n--- Feedback & Package Counts by Language ---")
        
        # รวบรวมภาษาทั้งหมดที่พบในทั้ง Feedback และ Package เพื่อให้แสดงผลครบถ้วน
        all_found_languages = sorted(list(set(feed_counts_by_lang.keys()) | set(pack_counts_by_lang.keys())))

        if not all_found_languages:
            output_lines.append("No feedback or package data found.")
        else:
            for lang in all_found_languages:
                output_lines.append(f"Language: {lang}")
                # แสดงจำนวน Package Inquiry สำหรับภาษานั้นๆ (เป็น 0 ถ้าไม่พบ)
                output_lines.append(f"  📦 Package Inquiry count: {pack_counts_by_lang[lang]}")
                # แสดงจำนวน Feedback & Suggestion สำหรับภาษานั้นๆ (เป็น 0 ถ้าไม่พบ)
                output_lines.append(f"  💬 Feedback & Suggestion count: {feed_counts_by_lang[lang]}")
                output_lines.append("") # เพิ่มบรรทัดว่างเพื่อความอ่านง่าย

        readable_text = "\n".join(output_lines)

        # ล้าง Text widget ก่อนแสดงผลลัพธ์ใหม่
        # self.result_text.delete(1.0, tk.END)
        text_to_insert = str(readable_text) 
        return text_to_insert
        # try:
        #     # แสดงผลลัพธ์ใน Text widget
        #     self.result_text.insert(tk.END, text_to_insert)
        # except tk.TclError as e:
        #     # หากเกิด TclError ให้พิมพ์ข้อผิดพลาดในคอนโซลและแสดง messagebox
        #     print(f"Error inserting text into result display: {e}")
        #     print(f"Type of text_to_insert: {type(text_to_insert)}")
        #     print(f"Content of text_to_insert (first 200 chars): {text_to_insert[:200]}...")
        #     messagebox.showerror("UI Update Error", "Could not update the result display. Please check the console for more details.")

        # # สามารถคืนค่าเป็น dictionary ของผลรวมแต่ละภาษาได้ หากต้องการใช้ในส่วนอื่นของแอปพลิเคชัน
        # return dict(feed_counts_by_lang), dict(pack_counts_by_lang)
        #     # # ล้าง Text widget ก่อนแสดงผลลัพธ์ใหม่
        #     # self.result_text.delete(1.0, tk.END)

        #     # # แสดงผลลัพธ์ใน Text widget
        #     # self.result_text.insert(tk.END, readable_text)

    def each_appointment(self):
        """
        ค้นหาและสรุปข้อมูล Appointment และ Appointment Recommended จากไฟล์ CSV ในโฟลเดอร์ที่กำหนด.
        จะอ่านไฟล์ CSV, จัดหมวดหมู่ตามภาษา, นับจำนวนในแต่ละประเภท (Appointment/Appointment Recommended),
        และแสดงผลรวมของแต่ละประเภทแยกตามภาษา.
        """
        folder = self.folder_path
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        # กำหนดรายการภาษาที่รองรับ
        langs = ["ar", "de", "en", "ru", "th", "zh"]
        # defaultdict สำหรับเก็บผลรวมของ Appointment และ Appointment Recommended แยกตามภาษา
        lang_summary = {lang_code: {"appointment count": 0, "appointment recommended count": 0} for lang_code in langs}
        
        # ค้นหาไฟล์ CSV ที่เกี่ยวข้อง
        recommended_files = glob.glob(os.path.join(folder, "*appointment-recommended*.csv"))
        # ไฟล์ appointment ทั่วไป (ไม่รวม recommended)
        normal_files = [f for f in glob.glob(os.path.join(folder, "*appointment*.csv"))
                        if "appointment-recommended" not in os.path.basename(f)]

        # อ่านไฟล์ recommended
        for file in recommended_files:
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                # ใช้คอลัมน์ที่สอง (index 1) สำหรับนับจำนวนแถว
                col_name = df.columns[1] 
                count = len(df[col_name])
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            for lang_code in langs:
                if f"-{lang_code}" in file:
                    lang_summary[lang_code]["appointment recommended count"] += count
                    break # เมื่อเจอภาษาแล้ว ออกจากลูปภาษา

        # อ่านไฟล์ปกติ
        for file in normal_files:
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip().str.replace('\ufeff', '')
                # ใช้คอลัมน์ที่สอง (index 1) สำหรับนับจำนวนแถว
                col_name = df.columns[1]
                count = len(df[col_name])
            except Exception as e:
                print(f"Failed to process {file}: {e}")
                continue

            for lang_code in langs:
                if f"-{lang_code}" in file:
                    lang_summary[lang_code]["appointment count"] += count
                    break # เมื่อเจอภาษาแล้ว ออกจากลูปภาษา

        # จัดรูปแบบผลลัพธ์เพื่อแสดงใน Text widget
        output_lines = []
        output_lines.append("\n\n--- Appointment Counts by Language ---")
        
        # รวบรวมภาษาทั้งหมดที่พบในทั้งสองประเภท
        all_found_languages = sorted(list(lang_summary.keys()))

        if not any(lang_summary[lc]["appointment count"] > 0 or lang_summary[lc]["appointment recommended count"] > 0 for lc in all_found_languages):
            output_lines.append("No appointment data found.")
        else:
            for lang_code in all_found_languages:
                # แปลงรหัสภาษาเป็นชื่อเต็มภาษาที่อ่านง่าย (ถ้ามี)
                full_lang_name = {
                    "en": "English", "th": "Thai", "ru": "Russia", 
                    "de": "German", "ar": "Arabic", "zh": "Chinese"
                }.get(lang_code, lang_code) # ใช้รหัสภาษาถ้าไม่มีชื่อเต็ม

                output_lines.append(f"Language: {full_lang_name}")
                output_lines.append(f"  📅 Appointment count: {lang_summary[lang_code]['appointment count']}")
                output_lines.append(f"  ⭐ Appointment Recommended count: {lang_summary[lang_code]['appointment recommended count']}")
                output_lines.append("") # เพิ่มบรรทัดว่างเพื่อความอ่านง่าย

        # คำนวณผลรวมทั้งหมด
        total_all_col = sum(lang_summary[lc]["appointment count"] for lc in langs)
        total_all_col_rec = sum(lang_summary[lc]["appointment recommended count"] for lc in langs)

        output_lines.append("--- Overall Totals ---")
        output_lines.append(f"Total Appointment count: {total_all_col}")
        output_lines.append(f"Total Appointment Recommended count: {total_all_col_rec}")
        output_lines.append("---")

        readable_text = "\n".join(output_lines)

        # ล้าง Text widget ก่อนแสดงผลลัพธ์ใหม่
        # self.result_text.delete(1.0, tk.END)
        text_to_insert = str(readable_text)
        return text_to_insert        
        