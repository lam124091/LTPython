from config import COLORS

class Styles:
    def __init__(self):
        # Kiểm tra các màu có tồn tại
        required_colors = {
            'turquoise', 'navy', 'skyBlue', 'mint', 'peach', 
            'crimson', 'white', 'maroon', 'green', 'pink'
        }
        
        missing_colors = required_colors - set(COLORS.keys())
        if missing_colors:
            raise KeyError(f"Missing colors in config: {missing_colors}")

    # Style cho buttons
    BUTTON_STYLE = {
        'font': ('Helvetica', 12, 'bold'),
        'width': 25,
        'height': 2,
        'bd': 3,
        'relief': 'raised',
        'cursor': 'hand2'
    }

    # Màu sắc cho từng loại button
    BUTTON_COLORS = {
        'view': {
            'bg': COLORS['blue'],        # Đổi tạm thành blue
            'fg': COLORS['white'],
            'hover_bg': COLORS['cyan']
        },
        'explore': {
            'bg': COLORS['green'],
            'fg': COLORS['white'],
            'hover_bg': COLORS['cyan']
        },
        'add': {
            'bg': COLORS['mint'],
            'fg': COLORS['navy'],
            'hover_bg': COLORS['green']
        },
        'update': {
            'bg': COLORS['peach'],
            'fg': COLORS['navy'],
            'hover_bg': COLORS['pink']
        },
        'delete': {
            'bg': COLORS['crimson'],
            'fg': COLORS['white'],
            'hover_bg': COLORS['maroon']
        }
    }

    # Style cho frames
    FRAME_STYLE = {
        'bg': COLORS['beige'],
        'padx': 20,
        'pady': 20,
        'relief': 'flat'
    }

    # Style cho labels
    LABEL_STYLE = {
        'font': ('Helvetica', 16, 'bold'),
        'bg': COLORS['beige'],
        'fg': COLORS['purple'],
        'pady': 10
    }

    # Style cho text widgets
    TEXT_STYLE = {
        'font': ('Helvetica', 10),
        'bg': COLORS['white'],
        'fg': COLORS['black'],
        'padx': 10,
        'pady': 10,
        'relief': 'sunken'
    }

    # Style cho treeview
    TREEVIEW_STYLE = {
        'font': ('Helvetica', 10),
        'rowheight': 25,
        'background': COLORS['white'],
        'foreground': COLORS['black'],
        'selected_bg': COLORS['skyBlue'],
        'selected_fg': COLORS['white']
    }

    @staticmethod
    def lighten_color(color):
        """Tạo màu sáng hơn cho hiệu ứng hover"""
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
        factor = 1.2
        r = min(int(r * factor), 255)
        g = min(int(g * factor), 255)
        b = min(int(b * factor), 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def create_shadow_frame(parent, width):
        """Tạo frame đổ bóng"""
        return {
            'bg': COLORS['grey'],
            'width': width,
            'height': 2,
            'pady': 10
        }
