import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import DATA_PATH
from utils import read_data

class DataExplorer:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("Khám phá dữ liệu")
        self.master.geometry("1400x800")
        
        # Style cho giao diện
        self.style = ttk.Style()
        self.setup_styles()
        
        # Frame chính
        self.main_frame = ttk.Frame(self.master, style='Main.TFrame', padding="10")
        self.main_frame.pack(fill='both', expand=True)
        
        # Notebook cho các tab
        self.notebook = ttk.Notebook(self.main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tạo các tab
        self.create_basic_info_tab()
        self.create_visualization_tab()
        self.create_correlation_tab()
        
    def setup_styles(self):
        # Style cho frame chính
        self.style.configure('Main.TFrame', background='#F0F0F0')
        
        # Style cho Notebook
        self.style.configure('Custom.TNotebook', background='#FFFFFF')
        self.style.configure('Custom.TNotebook.Tab',
            padding=[12, 8],
            background='#E1E1E1',
            foreground='#333333',
            font=('Arial', 10, 'bold')
        )
        self.style.map('Custom.TNotebook.Tab',
            background=[('selected', '#4CAF50')],
            foreground=[('selected', '#FFFFFF')]
        )
        
        # Style cho các label
        self.style.configure('Title.TLabel',
            font=('Arial', 14, 'bold'),
            foreground='#2196F3',
            background='#FFFFFF',
            padding=10
        )
        
        # Style cho các frame con
        self.style.configure('SubFrame.TFrame',
            background='#FFFFFF',
            relief='solid',
            borderwidth=1
        )

    def create_basic_info_tab(self):
        basic_frame = ttk.Frame(self.notebook, style='SubFrame.TFrame', padding="20")
        self.notebook.add(basic_frame, text='Thông tin cơ bản')
        
        # Tiêu đề
        title = ttk.Label(basic_frame, 
                         text="Thống kê dữ liệu", 
                         style='Title.TLabel')
        title.pack(fill='x', pady=(0,20))
        
        # Frame cho thống kê
        stats_frame = ttk.Frame(basic_frame, style='SubFrame.TFrame')
        stats_frame.pack(fill='both', expand=True)
        
        # Hiển thị thông tin cơ bản
        self.display_basic_stats(stats_frame)

    def create_visualization_tab(self):
        viz_frame = ttk.Frame(self.notebook, style='SubFrame.TFrame', padding="20")
        self.notebook.add(viz_frame, text='Biểu đồ phân tích')
        
        # Tiêu đề
        title = ttk.Label(viz_frame, 
                         text="Phân tích trực quan", 
                         style='Title.TLabel')
        title.pack(fill='x', pady=(0,20))
        
        # Frame cho controls
        control_frame = ttk.Frame(viz_frame, style='SubFrame.TFrame')
        control_frame.pack(fill='x', pady=(0,10))
        
        # Dropdown chọn loại biểu đồ
        ttk.Label(control_frame, text="Loại biểu đồ:").pack(side='left', padx=5)
        plot_types = ['Histogram', 'Box Plot', 'Scatter Plot', 'Bar Chart']
        self.plot_type = ttk.Combobox(control_frame, values=plot_types, state='readonly')
        self.plot_type.set(plot_types[0])
        self.plot_type.pack(side='left', padx=5)
        
        # Frame cho biểu đồ
        self.plot_frame = ttk.Frame(viz_frame, style='SubFrame.TFrame')
        self.plot_frame.pack(fill='both', expand=True, pady=10)

    def create_correlation_tab(self):
        corr_frame = ttk.Frame(self.notebook, style='SubFrame.TFrame', padding="20")
        self.notebook.add(corr_frame, text='Tương quan')
        
        # Tiêu đề
        title = ttk.Label(corr_frame, 
                         text="Ma trận tương quan", 
                         style='Title.TLabel')
        title.pack(fill='x', pady=(0,20))
        
        # Frame cho heatmap
        self.heatmap_frame = ttk.Frame(corr_frame, style='SubFrame.TFrame')
        self.heatmap_frame.pack(fill='both', expand=True)

    def display_basic_stats(self, parent_frame):
        # Tạo Text widget với scrollbar
        text_frame = ttk.Frame(parent_frame)
        text_frame.pack(fill='both', expand=True)
        
        text_widget = tk.Text(text_frame, 
                            wrap=tk.WORD, 
                            font=('Consolas', 11),
                            bg='#FFFFFF',
                            fg='#333333')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Thêm thông tin thống kê
        text_widget.tag_configure('header', 
                                font=('Arial', 12, 'bold'),
                                foreground='#2196F3')
        
        # Thêm nội dung
        text_widget.insert('end', "THÔNG TIN CƠ BẢN\n\n", 'header')
        text_widget.insert('end', f"Số lượng bản ghi: {len(self.app.df)}\n")
        text_widget.insert('end', f"Số lượng cột: {len(self.app.df.columns)}\n\n")
        
        text_widget.insert('end', "THỐNG KÊ MÔ TẢ\n\n", 'header')
        text_widget.insert('end', str(self.app.df.describe()))
        
        text_widget.configure(state='disabled')  # Làm cho text widget chỉ đọc