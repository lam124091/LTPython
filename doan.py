import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText  # Thêm import này
import json

# Đọc dữ liệu từ file CSV trên GitHub
def read_data(url):
    return pd.read_csv(url)

# Lưu dữ liệu vào file CSV
def save_data(df, filename='Cleaned_data_for_model.csv'):
    df.to_csv(filename, index=False)

# Giao diện chính
class App:
    def __init__(self, master):
        self.master = master
        master.title("Quản Lý Dữ Liệu CSV")

        # Tính toán vị trí để căn giữa cửa sổ
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        window_width = 400  # Chiều rộng của cửa sổ
        window_height = 450  # Chiều cao của cửa sổ

        # Tính toán vị trí x và y
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Đặt vị trí cho cửa sổ
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        master.configure(bg="#f5f5f5")  # Màu nền sáng

        self.url = 'https://raw.githubusercontent.com/lam124091/LTPython/main/Cleaned_data_for_model.csv'
        self.df = read_data(self.url)

        # Tiêu đề
        self.title_label = tk.Label(master, text="Chọn chức năng:", font=("Helvetica", 16), bg="#f5f5f5")
        self.title_label.pack(pady=10)

        # Tải màu từ file JSON
        self.colors = self.load_colors()

        # Nút chức năng
        self.create_buttons()

    def load_colors(self):
        try:
            with open('colors.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải mã màu: {str(e)}")
            return {}

    def create_buttons(self):
        button_color = self.colors.get("dark_green", "#4CAF50")  # Màu xanh lá cây
        button_hover_color = "#45a049"  # Màu xanh đậm hơn khi hover

        # Danh sách các nút và chức năng tương ứng
        button_commands = [
            ("Đọc dữ liệu", self.read_data),
            ("Thêm dữ liệu mới", self.open_add_data_form),
            ("Cập nhật dữ liệu", self.open_update_data_form),
            ("Xóa dữ liệu", self.open_delete_data_form),
            ("Làm sạch dữ liệu", self.clean_data),
            ("Chuẩn hóa dữ liệu", self.normalize_data),
            ("Trực quan hóa dữ liệu", self.plot_data),
        ]

        for text, command in button_commands:
            button = tk.Button(self.master, text=text, command=command, bg=button_color, fg="white", font=("Helvetica", 12))
            button.pack(pady=8)  # Tăng khoảng cách giữa các nút
            button.bind("<Enter>", lambda event, b=button: b.config(bg=button_hover_color))
            button.bind("<Leave>", lambda event, b=button: b.config(bg=button_color))

        self.quit_button = tk.Button(self.master, text="Thoát", command=self.master.quit, bg="red", fg="white", font=("Helvetica", 12))
        self.quit_button.pack(pady=20)

    def open_add_data_form(self):
        add_data_window = tk.Toplevel(self.master)
        add_data_window.title("Thêm Dữ Liệu Mới")
        add_data_window.geometry("400x300")

        self.entry_fields = {}
        for column in self.df.columns:
            label = tk.Label(add_data_window, text=column)
            label.pack(pady=5)
            entry = tk.Entry(add_data_window)
            entry.pack(pady=5)
            self.entry_fields[column] = entry

        add_button = tk.Button(add_data_window, text="Thêm", command=lambda: self.add_row(add_data_window), bg="#4CAF50", fg="white")
        add_button.pack(pady=10)

        back_button = tk.Button(add_data_window, text="Quay lại", command=add_data_window.destroy, bg="red", fg="white")
        back_button.pack(pady=10)

    def add_row(self, add_data_window):
        new_data = {}
        for column, entry in self.entry_fields.items():
            new_data[column] = entry.get()
        self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
        save_data(self.df)
        messagebox.showinfo("Thông báo", "Dữ liệu mới đã được thêm.")
        add_data_window.destroy()

    def open_update_data_form(self):
        update_data_window = tk.Toplevel(self.master)
        update_data_window.title("Cập nhật Dữ Liệu")
        update_data_window.geometry("400x250")

        condition_label = tk.Label(update_data_window, text="Nhập tên cột để làm điều kiện:")
        condition_label.pack(pady=5)

        condition_entry = tk.Entry(update_data_window)
        condition_entry.pack(pady=5)

        value_label = tk.Label(update_data_window, text="Nhập giá trị cho điều kiện:")
        value_label.pack(pady=5)

        value_entry = tk.Entry(update_data_window)
        value_entry.pack(pady=5)

        # Khung để cập nhật dữ liệu
        self.update_fields = {}
        for column in self.df.columns:
            label = tk.Label(update_data_window, text=f"Cập nhật giá trị cho {column}:")
            label.pack(pady=5)
            entry = tk.Entry(update_data_window)
            entry.pack(pady=5)
            self.update_fields[column] = entry

        update_button = tk.Button(update_data_window, text="Cập nhật", command=lambda: self.update_row(condition_entry.get(), value_entry.get(), update_data_window), bg="#4CAF50", fg="white")
        update_button.pack(pady=10)

        back_button = tk.Button(update_data_window, text="Quay lại", command=update_data_window.destroy, bg="red", fg="white")
        back_button.pack(pady=10)

    def update_row(self, condition_column, condition_value, update_data_window):
        condition = (self.df[condition_column] == condition_value)
        if self.df[condition].empty:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu thỏa mãn điều kiện.")
            return

        updated_data = {}
        for column, entry in self.update_fields.items():
            if entry.get():  # Chỉ cập nhật nếu có giá trị mới
                updated_data[column] = entry.get()
        
        self.df.loc[condition, list(updated_data.keys())] = list(updated_data.values())
        save_data(self.df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật.")
        update_data_window.destroy()

    def open_delete_data_form(self):
        delete_data_window = tk.Toplevel(self.master)
        delete_data_window.title("Xóa Dữ Liệu")
        delete_data_window.geometry("400x200")

        condition_label = tk.Label(delete_data_window, text="Nhập tên cột để xóa:")
        condition_label.pack(pady=5)

        condition_entry = tk.Entry(delete_data_window)
        condition_entry.pack(pady=5)

        value_label = tk.Label(delete_data_window, text="Nhập giá trị để xóa:")
        value_label.pack(pady=5)

        value_entry = tk.Entry(delete_data_window)
        value_entry.pack(pady=5)

        delete_button = tk.Button(delete_data_window, text="Xóa", command=lambda: self.delete_row(condition_entry.get(), value_entry.get(), delete_data_window), bg="#4CAF50", fg="white")
        delete_button.pack(pady=10)

        back_button = tk.Button(delete_data_window, text="Quay lại", command=delete_data_window.destroy, bg="red", fg="white")
        back_button.pack(pady=10)

    def delete_row(self, condition_column, condition_value, delete_data_window):
        condition = (self.df[condition_column] == condition_value)
        if self.df[condition].empty:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu thỏa mãn điều kiện.")
            return

        self.df = self.df.drop(self.df[condition].index)
        save_data(self.df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa.")
        delete_data_window.destroy()

    def read_data(self):
        self.df = read_data(self.url)
        self.show_data_window(self.df)

    def show_data_window(self, df):
        data_window = tk.Toplevel(self.master)
        data_window.title("Dữ liệu hiện tại")
        data_window.geometry("600x400")

        text_area = ScrolledText(data_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill='both')

        text_area.insert(tk.END, df.to_string())
        text_area.configure(state='disabled')  # Chỉ cho phép xem

    def clean_data(self):
        self.df = self.df.dropna().drop_duplicates()
        save_data(self.df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được làm sạch.")

    def normalize_data(self):
        if 'numeric_column' in self.df.columns:  # Thay 'numeric_column' bằng tên cột thực tế
            self.df['numeric_column'] = pd.to_numeric(self.df['numeric_column'], errors='coerce')
        save_data(self.df)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được chuẩn hóa.")

    def plot_data(self):
        if 'column_x' in self.df.columns and 'column_y' in self.df.columns:  # Thay 'column_x' và 'column_y' bằng tên cột thực tế
            plt.scatter(self.df['column_x'], self.df['column_y'])
            plt.title("Biểu đồ phân tán")
            plt.xlabel("Column X")
            plt.ylabel("Column Y")
            plt.show()
        else:
            messagebox.showerror("Lỗi", "Các cột để vẽ biểu đồ không tồn tại.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
