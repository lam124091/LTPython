import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS
from app import App
import json

def center_window(window, width, height):
    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Tính toán vị trí x, y
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Đặt vị trí cho cửa sổ
    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    try:
        # Khởi tạo cửa sổ chính
        root = tk.Tk()
        root.title("Quản Lý Dữ Liệu CSV")
        
        # Căn giữa cửa sổ
        window_width = 400
        window_height = 450
        center_window(root, window_width, window_height)
        
        # Đặt màu nền
        root.configure(bg=COLORS['beige'])
        
        # Khởi tạo ứng dụng
        app = App(root)
        
        # Chạy ứng dụng
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
