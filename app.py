import tkinter as tk
from tkinter import ttk, messagebox
import json
from config import WINDOW_SIZES, COLORS, DATA_PATH
from data_viewer import DataViewer
from data_explorer import DataExplorer
from utils import read_data
from styles import Styles
import pandas as pd

class App:
    def __init__(self, master):
        self.master = master
        self.styles = Styles()  # Khởi tạo styles ngay từ đầu
        
        # Cấu hình cửa sổ chính
        master.title("Quản Lý Dữ Liệu CSV")
        master.configure(**self.styles.FRAME_STYLE)  # Dùng style cho frame

        # Đọc dữ liệu
        self.df = read_data(DATA_PATH)

        # Tiêu đề với style
        self.title_label = tk.Label(
            master, 
            text="Chọn chức năng:",
            **self.styles.LABEL_STYLE  # Dùng style cho label
        )
        self.title_label.pack(pady=10)

        # Frame chứa các nút
        self.create_buttons()

    def load_colors(self):
        try:
            with open('colors.json', 'r') as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải mã màu: {str(e)}")
            return {}

    def create_buttons(self):
        # Frame cho buttons với style
        button_frame = tk.Frame(
            self.master,
            **self.styles.FRAME_STYLE
        )
        button_frame.pack(expand=True)

        buttons_info = [
            {
                'text': "Xem dữ liệu",
                'style': 'view',
                'command': self.show_data_viewer
            },
            {
                'text': "Khám phá dữ liệu",
                'style': 'explore',
                'command': self.show_data_explorer
            }
        ]

        for btn_info in buttons_info:
            style = self.styles.BUTTON_COLORS[btn_info['style']]
            btn = tk.Button(
                button_frame,
                text=btn_info['text'],
                command=btn_info['command'],
                **self.styles.BUTTON_STYLE,  # Style cơ bản cho button
                bg=style['bg'],
                fg=style['fg']
            )

            def on_enter(e, btn=btn, style=style):
                btn.config(
                    bg=style['hover_bg'],
                    relief='sunken'
                )

            def on_leave(e, btn=btn, style=style):
                btn.config(
                    bg=style['bg'],
                    relief='raised'
                )

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

            # Tạo shadow frame
            shadow_style = self.styles.create_shadow_frame(button_frame, btn.winfo_reqwidth())
            shadow_frame = tk.Frame(button_frame, **shadow_style)

            btn.pack(pady=5)
            shadow_frame.pack()

    def show_data_viewer(self):
        viewer_window = tk.Toplevel(self.master)
        viewer_window.title("Xem dữ liệu")
        self.data_viewer = DataViewer(viewer_window, self)  # Lưu instance của DataViewer

    def show_data_explorer(self):
        # Tạo cửa sổ mới
        explorer_window = tk.Toplevel(self.master)
        
        # Khởi tạo DataExplorer và truyền vào cả self (app instance)
        DataExplorer(explorer_window, self)  # Thêm self vào đây
        
        # Đặt vị trí cửa sổ
        window_width = int(WINDOW_SIZES['data_explorer'].split('x')[0])
        window_height = int(WINDOW_SIZES['data_explorer'].split('x')[1])
        center_window(explorer_window, window_width, window_height)

    def add_data(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Thêm Dữ liệu")
        add_window.geometry("400x500")

        # Khởi tạo và cấu hình style
        style = ttk.Style()
        style.configure('Custom.TSpinbox', arrowsize=13)  # Điều chỉnh kích thước nút mũi tên
        style.configure('Custom.TCombobox', arrowsize=13)
        
        # Frame cho form nhập liệu
        form_frame = ttk.Frame(add_window)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Tạo các trường nhập liệu
        self.add_fields = {}
        
        # Cố định độ rộng và style cho labels
        label_width = 12
        field_width = 23
        label_style = {
            'font': ('Arial', 10, 'bold'),
            'fg': '#2C3E50',  # Màu xanh đậm
            'anchor': 'w',    # Căn trái
            'width': label_width
        }

        # Property Type
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Loại nhà:", **label_style).pack(side='left')
        property_type = ttk.Combobox(frame, width=field_width-2,
                                    values=["House", "Flat", "Upper Portion", "Lower Portion", 
                                           "Farm House", "Room", "Penthouse"])
        property_type.pack(side='left', padx=(5,0))
        self.add_fields['property_type'] = property_type

        # Price
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Giá:", **label_style).pack(side='left')
        price = ttk.Entry(frame, width=field_width)
        price.pack(side='left', padx=(5,0))
        self.add_fields['price'] = price

        # Location
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Địa điểm:", **label_style).pack(side='left')
        location = ttk.Entry(frame, width=field_width)
        location.pack(side='left', padx=(5,0))
        self.add_fields['location'] = location

        # City
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Thành phố:", **label_style).pack(side='left')
        city = ttk.Entry(frame, width=field_width)
        city.pack(side='left', padx=(5,0))
        self.add_fields['city'] = city

        # Baths
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Phòng tắm:", **label_style).pack(side='left')
        baths = ttk.Spinbox(frame, width=field_width-2, from_=0, to=10)
        baths.pack(side='left', padx=(5,0))
        self.add_fields['bathrooms'] = baths

        # Purpose
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Mục đích:", **label_style).pack(side='left')
        purpose = ttk.Combobox(frame, width=field_width-2, 
                              values=["Để bán", "Cho thuê"])
        purpose.pack(side='left', padx=(5,0))
        self.add_fields['purpose'] = purpose

        # Bedrooms
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Phòng ngủ:", **label_style).pack(side='left')
        bedrooms = ttk.Spinbox(frame, width=field_width-2, from_=0, to=10)
        bedrooms.pack(side='left', padx=(5,0))
        self.add_fields['bedrooms'] = bedrooms

        # Area
        frame = ttk.Frame(form_frame)
        frame.pack(fill='x', pady=5)
        tk.Label(frame, text="Diện tích:", **label_style).pack(side='left')
        area = ttk.Entry(frame, width=field_width)
        area.pack(side='left', padx=(5,0))
        self.add_fields['area'] = area

        # Frame cho buttons
        button_frame = tk.Frame(add_window)
        button_frame.pack(fill='x', padx=20, pady=20)

        # Tạo frame con để căn giữa các nút
        center_frame = tk.Frame(button_frame)
        center_frame.pack(expand=True)

        # Nút Thêm
        add_button = tk.Button(
            center_frame, 
            text="Thêm dữ liệu",
            command=lambda: self.submit_add_data(add_window),
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',  # Màu xanh lá
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            borderwidth=2
        )
        add_button.pack(side='left', padx=10)

        # Nút Quay lại
        back_button = tk.Button(
            center_frame, 
            text="Quay lại",
            command=add_window.destroy,
            font=('Arial', 11, 'bold'),
            bg='#f44336',  # Màu đỏ
            fg='white',
            padx=20,
            pady=10,
            relief='raised',
            borderwidth=2
        )
        back_button.pack(side='left', padx=10)

        # Hover effect
        def on_enter(e, btn, hover_color):
            btn.config(bg=hover_color)
            
        def on_leave(e, btn, normal_color):
            btn.config(bg=normal_color)

        # Bind hover events
        add_button.bind('<Enter>', lambda e: on_enter(e, add_button, '#45a049'))
        add_button.bind('<Leave>', lambda e: on_leave(e, add_button, '#4CAF50'))
        
        back_button.bind('<Enter>', lambda e: on_enter(e, back_button, '#da190b'))
        back_button.bind('<Leave>', lambda e: on_leave(e, back_button, '#f44336'))

    def save_data(self, df):
        try:
            # Lưu DataFrame vào file CSV
            df.to_csv(DATA_PATH, index=False)
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {str(e)}")
            return False

    def submit_add_data(self, window):
        # Thu thập dữ liệu từ form
        new_data = {}
        column_mapping = {
            'property_type': 'property_type',
            'price': 'price',  # Đảm bảo tên cột khớp với DataFrame
            'location': 'location',
            'city': 'city',
            'bathrooms': 'bathrooms',  # Sửa lại tên cột từ 'baths' thành 'bathrooms'
            'purpose': 'purpose',
            'bedrooms': 'bedrooms',
            'area': 'area'  # Sửa lại tên cột từ 'Area_in_Marla' thành 'area'
        }

        # Chuyển đổi tên trường thành tên cột tương ứng
        for field_name, entry in self.add_fields.items():
            column_name = column_mapping.get(field_name, field_name)
            new_data[column_name] = entry.get()
        
        # Thêm dữ liệu mới vào DataFrame
        self.df.loc[len(self.df)] = new_data
        
        # Lưu DataFrame
        if self.save_data(self.df):
            # Thông báo thành công
            messagebox.showinfo("Thành công", "Đã thêm dữ liệu mới!", parent=window)
            
            # Đóng cửa sổ thêm dữ liệu
            window.destroy()
            
            # Cập nhật DataViewer và di chuyển đến dòng mới
            self.data_viewer.df = pd.read_csv(DATA_PATH)  # Đọc lại dữ liệu mới
            
            # Tính toán vị trí trang mới
            total_rows = len(self.data_viewer.df)
            rows_per_page = self.data_viewer.rows_per_page
            new_page = (total_rows - 1) // rows_per_page
            
            # Cập nhật current_index để hiển thị trang chứa dòng mới
            self.data_viewer.current_index = new_page * rows_per_page
            
            # Cập nhật bảng
            self.data_viewer.load_data()
            
            # Lấy item cuối cùng và áp dụng tag màu
            items = self.data_viewer.tree.get_children()
            if items:
                last_item = items[-1]
                self.data_viewer.tree.selection_set(last_item)
                self.data_viewer.tree.see(last_item)
                self.data_viewer.tree.item(last_item, tags=('new_row',))  # Thêm tag cho dòng mới

    def update_data(self):
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển")

    def delete_data(self):
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển")

    def clean_data(self):
        print("Bắt đầu làm sạch dữ liệu...")
        print(f"Số dòng ban đầu: {len(self.df)}")
        
        # Xử lý giá trị thiếu
        self.df = self.df.dropna()
        print(f"Số dòng sau khi xử lý giá trị thiếu: {len(self.df)}")
        
        # Loại bỏ dữ liệu trùng lặp
        self.df = self.df.drop_duplicates()
        print(f"Số dòng sau khi xử lý trùng lặp: {len(self.df)}")
        
        # Tái định dạng dữ liệu text
        text_columns = ['property_type', 'location', 'city', 'purpose']
        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.lower()  # chuyển thành chữ thường
                self.df[col] = self.df[col].str.strip()  # xóa khoảng trắng thừa
        
        print("Dữ liệu đã được làm sạch.")
        return self.df
