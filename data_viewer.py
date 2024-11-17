import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from config import WINDOW_SIZES, ROWS_PER_PAGE, DATA_PATH, COLORS
from utils import read_data

class DataViewer:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        
        # Thiết lập cửa sổ
        self.master.title("Xem Dữ liệu")
        self.master.geometry(WINDOW_SIZES['data_viewer'])
        
        # Khởi tạo style
        self.style = ttk.Style()
        self.setup_styles()
        
        # Khởi tạo các biến
        self.df = pd.read_csv(DATA_PATH)
        self.current_index = 0
        self.rows_per_page = ROWS_PER_PAGE
        self.panel_width = 400
        self.panel_visible = False
        
        # Tạo main container
        self.main_container = ttk.Frame(self.master)
        self.main_container.pack(fill='both', expand=True)
        
        # Tạo left frame với kích thước phù hợp
        self.left_frame = ttk.Frame(self.main_container, width=100)  # Giảm xuống 100 để cân đối hơn
        self.left_frame.pack(side='left', fill='y')
        self.left_frame.pack_propagate(False)
        
        # Tạo toggle button lớn hơn
        self.toggle_btn = tk.Button(
            self.left_frame,
            text="☰",
            command=self.toggle_panel,
            font=('Arial', 28, 'bold'),
            bg=COLORS['beige'],
            fg='#333333',
            width=3,
            height=2,
            relief='flat',
            cursor='hand2',
            padx=25
        )
        self.toggle_btn.pack(pady=20)
        
        # Tạo panel frame
        self.panel_frame = ttk.Frame(self.main_container, width=self.panel_width)
        self.panel_frame.pack_propagate(False)
        
        # Tạo spacer frame để tạo khoảng cách
        self.spacer = ttk.Frame(self.main_container, width=100)  # Thêm frame tạo khoảng cách
        self.spacer.pack(side='left', fill='y')
        self.spacer.pack_propagate(False)
        
        # Tạo data frame bên phải
        self.data_frame = ttk.Frame(self.main_container)
        self.data_frame.pack(side='left', fill='both', expand=True, padx=(50, 10))  # Tăng padding bên trái
        
        # Tạo sẵn các buttons trong panel_frame
        self.create_panel_buttons()  # Tạo buttons ngay từ đầu
        
        # Ẩn panel frame ban đầu
        self.panel_frame.pack_forget()
        
        # Tạo content frame cho data
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(fill='both', expand=True)
        
        # Tạo giao diện
        self.create_panel_buttons()
        self.setup_tree()
        self.setup_controls()
        self.load_data()

    def setup_styles(self):
        # Style cho frame nội dung
        self.style.configure('Content.TFrame', background='white')
        
        # Style cho Treeview
        self.style.configure("Treeview",
            background="#FFFFFF",
            foreground="black", 
            rowheight=28,
            fieldbackground="#FFFFFF",
            bordercolor="#FF69B4",
            borderwidth=2,
            font=('Arial', 10, 'bold')
        )
        
        # Style cho header
        self.style.configure("Treeview.Heading",
            background="#FF69B4",
            foreground="black",
            relief="flat",
            font=('Arial', 11, 'bold')
        )
        
        # Style cho hàng được chọn
        self.style.map('Treeview',
            background=[('selected', '#FF1493')],
            foreground=[('selected', 'white')]
        )

        # Cấu hình màu cho các hàng
        if hasattr(self, 'tree'):
            self.tree.tag_configure('oddrow', background='#E6E6FA')  # Tím nhạt
            self.tree.tag_configure('evenrow', background='#FFE4E1')  # Hồng phấn

    def setup_tree(self):
        # Tạo frame container cho tree và scrollbar
        tree_frame = ttk.Frame(self.data_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Tạo và cấu hình Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            style="Custom.Treeview",
            columns=list(self.df.columns),
            show='headings',
            selectmode='extended'
        )
        
        # Tạo scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        # Configure grid weights
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Định dạng các cột
        for col in self.df.columns:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center', width=100, minwidth=100)
        
        # Tạo tags cho màu sắc xen kẽ và các trường hợp đặc biệt
        self.tree.tag_configure('oddrow', background='#f5f5f5')
        self.tree.tag_configure('evenrow', background='#ffffff')
        self.tree.tag_configure('high_price', background='#e8f5e9', foreground='#2e7d32')
        self.tree.tag_configure('low_price', background='#ffebee', foreground='#c62828')

    def setup_controls(self):
        # Frame cho điều khiển với padding
        control_frame = ttk.Frame(self.master, padding="5 10 5 10")
        control_frame.pack(fill='x')
        
        # Style cho buttons
        self.style.configure("Nav.TButton",
            font=('Arial', 11, 'bold'),
            padding=8,
            background=COLORS["skyBlue"],
            foreground=COLORS["navy"]
        )
        
        # Style cho label trang
        self.style.configure("Page.TLabel",
            font=('Arial', 13, 'bold'),
            foreground=COLORS["navy"],
            padding=10
        )
        
        # Frame con để căn giữa các elements
        center_frame = ttk.Frame(control_frame)
        center_frame.pack(expand=True, fill='x')
        
        # Căn các elements theo tỷ lệ
        center_frame.grid_columnconfigure(0, weight=1)  # Khoảng trống bên trái
        center_frame.grid_columnconfigure(1, minsize=100)  # Nút trước
        center_frame.grid_columnconfigure(2, minsize=200)  # Label trang
        center_frame.grid_columnconfigure(3, minsize=100)  # Nút sau
        center_frame.grid_columnconfigure(4, weight=1)  # Khoảng trống bên phải
        
        # Nút trang trước
        self.prev_btn = ttk.Button(
            center_frame, 
            text="◄ Trang trước",
            command=self.prev_page,
            style="Nav.TButton"
        )
        self.prev_btn.grid(row=0, column=1, padx=10)
        
        # Label hiển thị trang
        total_pages = (len(self.df) - 1)//self.rows_per_page + 1
        self.page_label = ttk.Label(
            center_frame,
            text=f"Trang {self.current_index//self.rows_per_page + 1}/{total_pages}",
            style="Page.TLabel"
        )
        self.page_label.grid(row=0, column=2)
        
        # Nút trang sau
        self.next_btn = ttk.Button(
            center_frame,
            text="Trang sau ►",
            command=self.next_page,
            style="Nav.TButton"
        )
        self.next_btn.grid(row=0, column=3, padx=10)

    def load_data(self):
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Lấy dữ liệu cho trang hiện tại
        start = self.current_index
        end = start + self.rows_per_page
        current_data = self.df.iloc[start:end]
        
        # Tính giá trung bình để làm mốc so sánh
        avg_price = self.df['price'].mean()
        
        # Thêm dữ liệu vào bảng với màu sắc
        for idx, row in current_data.iterrows():
            # Xác định tag cho hàng
            tags = ('evenrow',) if idx % 2 == 0 else ('oddrow',)
            
            # Thêm tag cho giá
            if row['price'] > avg_price * 1.5:
                tags = tags + ('high_price',)
            elif row['price'] < avg_price * 0.5:
                tags = tags + ('low_price',)
            
            # Chèn dữ liệu với tags
            self.tree.insert("", "end", values=list(row), tags=tags)
        
        # Cập nhật label hiển thị trang
        total_pages = (len(self.df) + self.rows_per_page - 1) // self.rows_per_page
        current_page = (self.current_index // self.rows_per_page) + 1
        self.page_label.config(text=f"Trang {current_page}/{total_pages}")
        
        # Cập nhật trạng thái các nút
        self.prev_btn["state"] = "normal" if self.current_index > 0 else "disabled"
        self.next_btn["state"] = "normal" if end < len(self.df) else "disabled"

    def prev_page(self):
        if self.current_index > 0:
            self.current_index -= self.rows_per_page
            self.load_data()
            self.update_page_label()

    def next_page(self):
        if self.current_index + self.rows_per_page < len(self.df):
            self.current_index += self.rows_per_page
            self.load_data()
            self.update_page_label()

    def update_page_label(self):
        current_page = self.current_index//self.rows_per_page + 1
        total_pages = (len(self.df) - 1)//self.rows_per_page + 1
        self.page_label.config(
            text=f"Trang {current_page}/{total_pages}",
            style="Page.TLabel"
        )

    # Thêm các phưng thức xử lý chức năng
    def add_data(self):
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển")

    def edit_data(self):
        # Kiểm tra xem có dòng nào được chọn không
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return
        
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Sửa dữ liệu")
        edit_window.geometry("600x400")
        # TODO: Thêm form sửa dữ liệu

    def delete_data(self):
        # Kiểm tra xem có dòng nào được chn không
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
        
        # Xác nhận xóa
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dữ liu này?"):
            # TODO: Thực hiện xóa dữ liệu
            pass

    def validate_number(self, value):
        """Chỉ cho phép nhập số và dấu chấm"""
        if value == "":  # Cho phép trường rỗng
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def handle_click(self, event):
        # Lấy vị trí click
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            
            # Lấy số cột (từ 1)
            col_num = int(column[1]) - 1
            
            # Nếu click vào cột edit
            if col_num == len(self.df.columns):
                self.edit_row(item)
            # Nếu click vào cột delete    
            elif col_num == len(self.df.columns) + 1:
                self.delete_row(item)

    def edit_row(self, item):
        # Lấy dữ liệu của dòng được chọn
        values = self.tree.item(item)['values']
        tags = self.tree.item(item)['tags']
        
        # Lấy index từ tags
        row_index = int(tags[1].split('_')[1])
        
        # Tạo cửa sổ edit
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Chỉnh sửa dữ liệu")
        edit_window.geometry("400x500")
        
        # Frame cho form
        form_frame = ttk.Frame(edit_window)
        form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tạo các trường nhập liệu
        entries = {}
        for i, col in enumerate(self.df.columns):
            frame = ttk.Frame(form_frame)
            frame.pack(fill='x', pady=5)
            ttk.Label(frame, text=f"{col}:", width=15).pack(side='left')
            entry = ttk.Entry(frame, width=30)
            entry.insert(0, str(values[i]))
            entry.pack(side='left', padx=5)
            entries[col] = entry
            
        # Nút lưu
        ttk.Button(
            form_frame,
            text="Lưu",
            command=lambda: self.save_edit(row_index, entries, edit_window)
        ).pack(pady=20)

    def save_edit(self, row_index, entries, window):
        # Cập nhật DataFrame
        for col, entry in entries.items():
            self.df.at[row_index, col] = entry.get()
        
        # Lưu vào file
        self.app.save_data(self.df)
        
        # Cập nht hiển thị
        self.load_data()
        
        # Đóng cửa sổ edit
        window.destroy()
        messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu!")

    def delete_row(self, item):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng này?"):
            # Lấy index từ tags
            tags = self.tree.item(item)['tags']
            row_index = int(tags[1].split('_')[1])
            
            # Xóa khỏi DataFrame
            self.df = self.df.drop(row_index)
            
            # Lưu vào file
            self.app.save_data(self.df)
            
            # Cập nhật hiển thị
            self.load_data()
            messagebox.showinfo("Thành công", "Đã xóa dữ liệu!")

    def toggle_panel(self):
        if not self.panel_visible:
            # Hiện panel 
            self.panel_frame.pack(fill='y', expand=True, after=self.toggle_btn)
            self.toggle_btn.configure(text="◀")
            self.panel_visible = True
        else:
            # Ẩn panel
            self.panel_frame.pack_forget()
            self.toggle_btn.configure(text="☰")
            self.panel_visible = False

    def create_panel_buttons(self):
        # Xóa các buttons cũ nếu có
        for widget in self.panel_frame.winfo_children():
            widget.destroy()
        
        buttons_config = [
            {
                'text': "➕ Thêm",
                'command': self.app.add_data,
                'bg': '#4CAF50',
                'hover': '#45a049'
            },
            {
                'text': "🧹 Dọn", 
                'command': self.clean_data,
                'bg': '#2196F3',
                'hover': '#1976D2'
            },
            {
                'text': "✏️ Sửa",
                'command': self.edit_selected,
                'bg': '#FFA500',
                'hover': '#FF8C00'
            },
            {
                'text': "🗑️ Xóa",
                'command': self.delete_selected,
                'bg': '#FF4444',
                'hover': '#FF0000'
            }
        ]
        
        # Tạo container frame cho các buttons
        container = ttk.Frame(self.panel_frame)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        for config in buttons_config:
            # Frame cho mỗi button
            btn_frame = ttk.Frame(container)
            btn_frame.pack(fill='x', pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=config['text'],
                command=config['command'],
                font=('Arial', 12),  # Giảm font size
                bg=config['bg'],
                fg='white',
                padx=10,           # Giảm padding
                pady=5,            # Giảm padding
                relief='raised',
                borderwidth=2,
                cursor='hand2'
            )
            btn.pack(fill='x', padx=5)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn, h=config['hover']: b.config(bg=h))
            btn.bind('<Leave>', lambda e, b=btn, c=config['bg']: b.config(bg=c))

    def clean_data(self):
        # Lưu số dòng ban đầu để thống kê
        rows_before = len(self.df)
        
        # 1. Xử lý giá trị trống (NaN)
        self.df = self.df.dropna()
        print(f"Số dòng sau khi xử lý giá trị trống: {len(self.df)}")
        
        # 2. Xử lý giá trị số không hợp lệ
        numeric_columns = ['bedrooms', 'baths', 'area']
        for col in numeric_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                self.df = self.df[self.df[col] >= 0]
        
        print(f"Số dòng sau khi xử lý giá trị số không hợp lệ: {len(self.df)}")
        
        # 3. Loại bỏ dữ liệu trùng lặp
        self.df = self.df.drop_duplicates()
        print(f"S dòng sau khi xử lý trùng lặp: {len(self.df)}")
        
        # Cập nhật DataFrame trong app
        self.app.df = self.df
        
        # Lưu DataFrame đã clean vào file
        self.app.save_data(self.df)
        
        # Cập nhật hiển thị
        self.load_data()
        
        # Tính số dòng đã xóa
        rows_removed = rows_before - len(self.df)
        
        # Thông báo hoàn thành với thống kê
        messagebox.showinfo(
            "Hoàn thành", 
            f"Dữ liệu đã được làm sạch!\n\n"
            f"- Số dòng ban đầu: {rows_before:,}\n"
            f"- Số dòng đã xóa: {rows_removed:,}\n"
            f"- Số dòng còn lại: {len(self.df):,}\n\n"
            f"Đã xóa:\n"
            f"- Các dòng có giá trị trống\n"
            f"- Các dòng có số phòng, diện tích âm\n"
            f"- Các dòng trng lặp"
        )
        
        # Quay về DataViewer
        self.master.lift()  # Đưa cửa s DataViewer lên trên
        self.master.focus_force()  # Focus vào DataViewer

    def edit_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần sửa!")
            return
        self.edit_row(selected_items[0])
        self.hide_menu()

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dòng cần xóa!")
            return
        self.delete_row(selected_items[0])
        self.hide_menu()

    def toggle_menu(self):
        if hasattr(self, 'menu_visible') and self.menu_visible:
            self.hide_menu()
        else:
            self.show_menu()

    def show_menu(self):
        # Tính toán vị trí menu dựa trên vị trí toggle button
        x = self.corner_frame.winfo_x()
        y = self.corner_frame.winfo_y() + self.corner_frame.winfo_height()
        
        self.menu_frame.place(x=x, y=y)
        self.menu_visible = True
        
        # Bind click outside để ẩn menu
        self.master.bind('<Button-1>', self.check_mouse_click)

    def hide_menu(self):
        self.menu_frame.place_forget()
        self.menu_visible = False
        self.master.unbind('<Button-1>')

    def check_mouse_click(self, event):
        # Kiểm tra click có nằm ngoài menu không
        if not self.menu_frame.winfo_containing(event.x_root, event.y_root):
            self.hide_menu()

