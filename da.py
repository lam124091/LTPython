import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import ttk, Menu
# Đọc dữ liệu từ file CSV
def read_data(filename):
    df = pd.read_csv(filename)
    if 'Unnamed: 0' in df.columns:
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
    return df

def add_row(filename):
    df = read_data(filename)
    print("Nhập dữ liệu mới:")
    new_data = {}
    columns = [col for col in df.columns if not col.startswith('Unnamed')]
    for column in columns:
        value = input(f"Nhập giá trị cho {column}: ")
        new_data[column] = value
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(filename)
    print("Dữ liệu mới đã được thêm.")

# Update - cập nhật data theo yêu cầu từ người dùng
def update_row(filename):
    df = read_data(filename)
    print("Nhập thông tin cần cập nhật:")
    condition_value = input(f"Nhập giá trị cập nhật 'property_type': ")

    # Tìm các hàng có property_type match với giá trị nhập vào
    condition = (df['property_type'] == condition_value)
    matching_rows = df[condition]
    
    if matching_rows.empty:
        print("Không tìm thấy dữ liệu thỏa mãn.")
        return

    # Hiển thị các dòng thỏa mãn
    print("\nCác dòng thỏa mãn điều kiện:")
    print(matching_rows)
    
    # Cho người dùng chọn dòng cụ thể
    row_index = input("\nNhập số thứ tự dòng cần cập nhật: ")
    try:
        row_index = int(row_index)
        if row_index not in matching_rows.index:
            print("Số thứ tự không hợp lệ")
            return
    except ValueError:
        print("Vui lòng nhập số")
        return

    # Nhập dữ liệu cập nhật cho dòng đã chọn
    print("\nNhập dữ liệu cập nhật:")
    updated_data = {}
    for column in df.columns:
        updated_data[column] = input(f"Nhập giá trị mới cho {column}: ")
    
    # Cập nhật chỉ dòng được chọn
    df.loc[row_index, list(updated_data.keys())] = list(updated_data.values())
    df.to_csv(filename, index=False)
    print("Dữ liệu đã được cập nhật.")

# Delete - Xóa một hàng mà người dùng yêu cầu
def delete_row(filename):
    df = read_data(filename)
    condition_value = input(f"Nhập giá trị xóa 'property_type': ")

    # Tìm các hàng có property_type match với giá trị nhập vào
    condition = (df['property_type'] == condition_value)
    matching_rows = df[condition]
    
    if matching_rows.empty:
        print("Không tìm thấy dữ liệu thỏa mãn điều kiện.")
        return

    # Hiển thị các dòng thỏa mãn
    print("\nCác dòng thỏa mãn điều kiện:")
    print(matching_rows)
    
    # Cho người dùng chọn dòng cụ thể để xóa
    row_index = input("\nNhập số thứ tự dòng cần xóa: ")
    try:
        row_index = int(row_index)
        if row_index not in matching_rows.index:
            print("Số thứ tự không hợp lệ")
            return
            
        # Xóa chỉ dòng được chọn
        df = df.drop(row_index)
        df.to_csv(filename, index=False)
        print("Dữ liệu đã được xóa.")
        
    except ValueError:
        print("Vui lòng nhập số")
        return

# Làm sạch dữ liệu
def clean_data(df):
    # Xử lý giá trị thiếu
    df = df.dropna() # Bất kỳ dữ liệu nào bị thiếu một giá trị trở lên sẽ bị loại bỏ
    
    # Loại bỏ dữ liệu trùng lặp
    df = df.drop_duplicates() # Bất kỳ dữ liệu nào giống hệt nhau sẽ bị loại bỏ
    
    # Làm sạch giá trị số
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df = df[df['price'] > 0]  # loại bỏ giá trị âm hoặc bằng 0
    
    if 'bedrooms' in df.columns:
        df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
        df = df[df['bedrooms'] > 0]  # loại bỏ số phòng âm hoặc bằng 0
    
    if 'Area_in_Marla' in df.columns:
        df['Area_in_Marla'] = pd.to_numeric(df['Area_in_Marla'], errors='coerce')
        df = df[df['Area_in_Marla'] > 0]  # loại bỏ diện tích âm hoặc bằng 0
    
    print("Dữ liệu đã được làm sạch.")
    return df

# Chuẩn hóa dữ liệu
def normalize_data(df):

    # Chuyển đổi kiểu dữ liệu ???
    if 'numeric_column' in df.columns:
        df_normalized['numeric_column'] = pd.to_numeric(df['numeric_column'], errors='coerce')

    # Chuẩn hóa đơn vị
    if 'height_cm' in df.columns:
        df_normalized['height_m'] = df['height_cm'] / 100
    
    # Tạo một bản sao để không ảnh hưởng đến df gốc
    df_normalized = df.copy()
    
    # Chuẩn hóa giá (đơn vị triệu)
    if 'price' in df_normalized.columns:
        df_normalized['price_in_millions'] = df_normalized['price'] / 1000000
    
    # Chuẩn hóa diện tích (đơn vị m2)
    if 'Area_in_Marla' in df_normalized.columns:
        df_normalized['Area_in_m2'] = df_normalized['Area_in_Marla'] * 25.2929  # 1 Marla = 25.2929 m2
    
    # Thêm các chỉ số phân tích
    if 'price' in df_normalized.columns and 'Area_in_Marla' in df_normalized.columns:
        df_normalized['price_per_marla'] = df_normalized['price'] / df_normalized['Area_in_Marla']  # giá/diện tích
    
    print("\nDữ liệu sau khi chuẩn hóa:")
    print(df_normalized)
    print("\nCác cột được thêm vào để phân tích:")
    print("- price_in_millions: Giá theo đơn vị triệu")
    print("- Area_in_m2: Diện tích theo m2")
    print("- price_per_marla: Giá trên mỗi Marla")
    print("\nLưu ý: Dữ liệu này chỉ hiển thị tạm thời và không được lưu vào file!")
    return df_normalized

# Trực quan hóa dữ liệu
def plot_data(df):

  #Biểu đồ cột giá tiền các loại bất động sản
  plt.bar(df['property_type'], df['price'], color='g', width=0.5, label="Price")
  plt.xlabel('Loại bất động sản')
  plt.ylabel('Giá')
  plt.title('Quan hệ giữa loại bất động sản và giá')
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.show()

  #Biểu đồ cột cho số lượng các loại bất động sản
  df['property_type'].value_counts().plot(kind='bar', color='skyblue')
  plt.title("Số lượng các loại bất động sản")
  plt.xlabel("Loại bất động sn")
  plt.ylabel("Số lượng")
  plt.show()

  #Biểu đồ phân tán giữa diện tích và giá
  plt.scatter(df['Area_in_Marla'], df['price'], color='coral')
  plt.title("Mối quan hệ giữa Diện tích và Giá")
  plt.xlabel("Diện tích (Marla)")
  plt.ylabel("Giá (VNĐ)")
  plt.show()
def export_data(df):
    filename = input("Nhập tên file để lưu (ví dụ: output.csv): ")
    df.to_csv(filename, index=False)
    print(f"Dữ liệu đã được xuất vào {filename}.")
class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Phân tích dữ liệu Bất động sản")
        self.master.geometry("400x200")  # Kích thước cửa sổ chính nhỏ hơn
        
        self.filename = 'Cleaned_data_for_model.csv'

        # Frame cho các nút chức năng chính
        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(self.main_frame, 
                              text="Chọn chức năng phân tích:",
                              font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=20)
        
        # Nút Xem dữ liệu
        ttk.Button(self.main_frame, 
                  text="Xem dữ liệu", 
                  command=self.show_data_viewer,
                  width=30).pack(pady=10)
        
        # Nút Khám phá dữ liệu
        ttk.Button(self.main_frame, 
                  text="Khám phá dữ liệu", 
                  command=self.show_data_explorer,
                  width=30).pack(pady=10)
        menubar = Menu(master)
        
        # Tạo menu chức năng
        function_menu = Menu(menubar, tearoff=0)
        function_menu.add_command(label="1. Đọc dữ liệu", command=self.read_data)
        function_menu.add_command(label="2. Thêm dữ liệu mới", command=self.add_row)
        function_menu.add_command(label="3. Cập nhật dữ liệu", command=self.update_row)
        function_menu.add_command(label="4. Xóa dữ liệu", command=self.delete_row)
        function_menu.add_command(label="5. Làm sạch dữ liệu", command=self.clean_data)
        function_menu.add_command(label="6. Chuẩn hóa dữ liệu", command=self.normalize_data)
        function_menu.add_command(label="7. Trực quan hóa dữ liệu", command=self.plot_data)
        function_menu.add_command(label="8. Xuất dữ liệu", command=self.export_data)
        
        # Thêm menu chức năng vào menubar
        menubar.add_cascade(label="Chức năng", menu=function_menu)
        
        # Gán menubar cho cửa sổ
        master.config(menu=menubar)

        # Frame cho các nút chức năng chính
        self.main_frame = ttk.Frame(master, padding="20")
        self.main_frame.pack(fill='both', expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(self.main_frame, 
                              text="Chọn chức năng phân tích:",
                              font=('Helvetica', 12, 'bold'))
        title_label.pack(pady=20)

    def read_data(self):
        df = read_data(self.filename)
        print("Dữ liệu hiện tại:")
        print(df.head())

    def add_row(self):
        add_row(self.filename)

    def update_row(self):
        update_row(self.filename)

    def delete_row(self):
        delete_row(self.filename)

    def clean_data(self):
        df = read_data(self.filename)
        df = clean_data(df)
        df.to_csv(self.filename, index=False)

    def normalize_data(self):
        df = read_data(self.filename)
        df = normalize_data(df)
        df.to_csv(self.filename, index=False)

    def plot_data(self):
        df = read_data(self.filename)
        plot_data(df)

    def export_data(self):
        df = read_data(self.filename)
        export_data(df)
    def show_data_explorer(self):
        # Tạo cửa sổ mới để khám phá dữ liệu
        explorer_window = tk.Toplevel(self.master)
        DataExplorer(explorer_window)
    def show_data_viewer(self):
        # Tạo cửa sổ mới để xem dữ liệu
        data_window = tk.Toplevel(self.master)
        DataViewer(data_window)

    def show_data_explorer(self):
        # Tạo cửa sổ mới để khám phá dữ liệu
        explorer_window = tk.Toplevel(self.master)
        DataExplorer(explorer_window)

class DataViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Xem dữ liệu")
        self.master.geometry("1200x600")
        
        # Đọc dữ liệu
        self.df = pd.read_csv('Cleaned_data_for_model.csv')
        if 'Unnamed: 0' in self.df.columns:
            self.df.drop(['Unnamed: 0'], axis=1, inplace=True)
        self.current_index = 0
        self.rows_per_page = 1000
        
        # Tạo frame chứa bảng và thanh cuộn
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)
        
        # Tạo Treeview và các thành phần khác như code cũ
        self.setup_treeview()
        self.setup_controls()
        self.load_data()

    def setup_treeview(self):
        # Code cũ của Treeview...
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(side='left', fill='both', expand=True)
        
        # Thanh cuộn dọc
        self.vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        # Thanh cuộn ngang
        self.hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)
        self.hsb.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=self.hsb.set)
        
        # Định nghĩa các cột
        self.tree["columns"] = list(self.df.columns)
        self.tree["show"] = "headings"
        
        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100)

    def setup_controls(self):
        # Frame cho các nút điều khiển
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.pack(fill='x', padx=5, pady=5)
        
        self.prev_btn = ttk.Button(self.control_frame, text="Trang trước", command=self.prev_page)
        self.prev_btn.pack(side='left', padx=5)
        
        self.next_btn = ttk.Button(self.control_frame, text="Trang sau", command=self.next_page)
        self.next_btn.pack(side='left', padx=5)
        
        self.page_label = ttk.Label(self.control_frame, text="")
        self.page_label.pack(side='left', padx=5)

    def load_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lấy dữ liệu cho trang hiện tại
        start = self.current_index
        end = start + self.rows_per_page
        current_data = self.df.iloc[start:end]
        
        # Thêm dữ liệu vào bảng
        for _, row in current_data.iterrows():
            self.tree.insert("", "end", values=list(row))
            
        # Cập nhật label hiển thị trang
        total_pages = (len(self.df) + self.rows_per_page - 1) // self.rows_per_page
        current_page = (self.current_index // self.rows_per_page) + 1
        self.page_label.config(text=f"Trang {current_page}/{total_pages}")
        
        # Cập nhật trạng thái các nút
        self.prev_btn["state"] = "normal" if self.current_index > 0 else "disabled"
        self.next_btn["state"] = "normal" if end < len(self.df) else "disabled"
    
    def next_page(self):
        self.current_index += self.rows_per_page
        self.load_data()
        
    def prev_page(self):
        self.current_index = max(0, self.current_index - self.rows_per_page)
        self.load_data()

class DataExplorer:
    def __init__(self, master):
        self.master = master
        self.master.title("Khám phá dữ liệu")
        self.master.geometry("800x600")
        
        # Đọc dữ liệu
        self.df = pd.read_csv('Cleaned_data_for_model.csv')
        if 'Unnamed: 0' in self.df.columns:
            self.df.drop(['Unnamed: 0'], axis=1, inplace=True)
            
        # Tạo notebook (tab control)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        
        # Tab thông tin cơ bản
        self.create_basic_info_tab()
        
        # Tab phân tích giá trị unique
        self.create_unique_values_tab()

    def create_basic_info_tab(self):
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text='Thông tin cơ bản')
        
        # Hiển thị thông tin cơ bản của DataFrame
        text = tk.Text(basic_frame)
        text.pack(fill='both', expand=True)
        
        info = f"""
        Thông tin Dataset:
        
        Số lượng dòng: {len(self.df)}
        Số lượng cột: {len(self.df.columns)}
        
        Các cột trong dataset:
        {', '.join(self.df.columns)}
        
        Thông tin chi tiết:
        """
        text.insert('1.0', info)
        
        # Thêm thông tin thống kê cơ bản
        text.insert('end', '\n\nThống kê cơ bản:\n')
        text.insert('end', str(self.df.describe()))

    def create_unique_values_tab(self):
        unique_frame = ttk.Frame(self.notebook)
        self.notebook.add(unique_frame, text='Phân tích giá trị unique')
        
        # Tạo figure cho biểu đồ
        fig = plt.Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        # Vẽ biểu đồ số lượng giá trị unique
        unique_counts = self.df.nunique()
        unique_counts.plot(kind='bar', ax=ax)
        ax.set_title('Số lượng giá trị unique của mỗi cột')
        ax.set_xlabel('Tên cột')
        ax.set_ylabel('Số lượng giá trị unique')
        plt.setp(ax.get_xticklabels(), rotation=45)
        
        # Embed biểu đồ vào tkinter
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, unique_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

# Hàm main
def main():
    filename = 'Cleaned_data_for_model.csv'

    while True:
        print("\nChọn chức năng:")
        print("1. Đọc dữ liệu")
        print("2. Thêm dữ liệu mới")
        print("3. Cập nhật dữ liệu")
        print("4. Xóa dữ liệu")
        print("5. Làm sạch dữ liệu")
        print("6. Chuẩn hóa dữ liệu")
        print("7. Trực quan hóa dữ liệu (biểu đồ)")
        print("0. Thoát")

        choice = input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            df = read_data(filename)
            print("Dữ liệu hiện tại:")
            print(df.head())
        elif choice == "2":
            add_row(filename)
        elif choice == "3":
            update_row(filename)
        elif choice == "4":
            delete_row(filename)
        elif choice == "5":
            df = read_data(filename)
            df = clean_data(df)
            df.to_csv(filename, index=False)
        elif choice == "6":
            df = read_data(filename)
            df = normalize_data(df)
            df.to_csv(filename, index=False)
        elif choice == "7":
            df = read_data(filename)
            plot_data(df)
        elif choice == "8":
            export_data(df) 
        elif choice == "0":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

# Chạy hàm chính
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
