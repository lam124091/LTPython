import pandas as pd
from tkinter import messagebox
import os

def read_data(filepath):
    """Đọc dữ liệu từ file CSV local"""
    try:
        # Kiểm tra file tồn tại
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Không tìm thấy file: {filepath}")
            
        # Đọc file CSV
        df = pd.read_csv(filepath, encoding='utf-8')
        
        # Kiểm tra DataFrame
        if df.empty:
            raise ValueError("DataFrame trống")
            
        # Xóa cột Unnamed nếu có
        if 'Unnamed: 0' in df.columns:
            df.drop(['Unnamed: 0'], axis=1, inplace=True)
            
        print("Columns:", df.columns.tolist())
        print("Shape:", df.shape)
        
        return df
        
    except Exception as e:
        print(f"Error details: {str(e)}")
        messagebox.showerror("Lỗi", f"Không thể đọc dữ liệu: {str(e)}")
        return pd.DataFrame()

def save_data(df, filename):
    """Lưu DataFrame vào file CSV"""
    try:
        df.to_csv(filename, index=False)
        return True
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")
        return False
