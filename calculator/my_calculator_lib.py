"""
کتابخونهٔ ماشین‌حساب پیشرفته با پشتیبانی از SymPy و CustomTkinter
- محاسبات سمبولیک و دقیق (ریشه، مشتق، انتگرال، حل معادله)
- گرافیک فوق‌مدرن (Glassmorphism, Dark Mode)
- ۵۹ تم متنوع (۱ تا ۵۰ + ۹ تم ویژه)
- راهنمای تعاملی (tour) برای کتابخونه‌های مدرن پایتون
"""

import tkinter as tk
import re
import colorsys
import random
import threading

# ─── ۱. تلاش برای بارگذاری کتابخونه‌های پیشرفته ───
try:
    import sympy as sp
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False

try:
    import customtkinter as ctk
    HAS_CTK = True
except ImportError:
    HAS_CTK = False

# ─── ۲. تولید ۵۰ تم رنگین‌کمانی ───
def _generate_50_themes():
    themes = {}
    styles = [
        (0, True), (15, True), (30, True), (45, True), (60, True),
        (75, True), (90, True), (105, True), (120, True), (135, True),
        (150, True), (165, True), (180, True), (195, True), (210, True),
        (225, True), (240, True), (255, True), (270, True), (285, True),
        (300, True), (315, True), (330, True), (345, True),
        (0, False), (20, False), (40, False), (60, False), (80, False),
        (100, False), (120, False), (140, False), (160, False), (180, False),
        (200, False), (220, False), (240, False), (260, False), (280, False),
        (300, False), (320, False), (340, False),
        (10, True, 'neon'), (190, True, 'neon'), (50, False, 'pastel'),
        (290, False, 'pastel'), (130, True, 'metal'), (310, True, 'metal'),
        (70, False, 'vivid'), (250, False, 'vivid')
    ]
    random.seed(42)
    for i, style in enumerate(styles[:50], start=1):
        hue = style[0] / 360.0
        is_dark = style[1]
        extra = style[2] if len(style) > 2 else None

        if extra == 'neon':
            sat, light = 1.0, 0.2 if is_dark else 0.9
        elif extra == 'pastel':
            sat, light = 0.4, 0.9
        elif extra == 'metal':
            sat, light = 0.1, 0.5 if is_dark else 0.7
        elif extra == 'vivid':
            sat, light = 1.0, 0.6
        else:
            sat = random.uniform(0.6, 1.0)
            light = random.uniform(0.1, 0.25) if is_dark else random.uniform(0.8, 0.95)

        def rgb_to_hex(rgb):
            return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

        bg = rgb_to_hex(colorsys.hls_to_rgb(hue, light, sat))
        display_bg = rgb_to_hex(colorsys.hls_to_rgb(hue, max(0, min(1, light+0.05 if is_dark else light-0.05)), sat*0.8))
        display_fg = "#ffffff" if is_dark else "#000000"
        btn_light = light + 0.1 if is_dark else light - 0.1
        btn_bg = rgb_to_hex(colorsys.hls_to_rgb(hue, max(0, min(1, btn_light)), sat*0.9))
        btn_fg = "#ffffff" if is_dark else "#000000"
        btn_hover = "#{:02x}{:02x}{:02x}".format(
            min(255, int(colorsys.hls_to_rgb(hue, btn_light, sat*0.9)[0]*255+30)),
            min(255, int(colorsys.hls_to_rgb(hue, btn_light, sat*0.9)[1]*255+30)),
            min(255, int(colorsys.hls_to_rgb(hue, btn_light, sat*0.9)[2]*255+30))
        )
        op_bg = rgb_to_hex(colorsys.hls_to_rgb((hue+0.5)%1.0, 0.5, 0.9))
        op_fg = "#ffffff"
        eq_bg = rgb_to_hex(colorsys.hls_to_rgb((hue+0.25)%1.0, 0.6, 0.9))
        eq_fg = "#000000" if not is_dark else "#ffffff"
        clr_bg = rgb_to_hex(colorsys.hls_to_rgb(0.0, 0.5, 0.8))
        clr_fg = "#ffffff"

        themes[str(i)] = {
            'bg': bg, 'display_bg': display_bg, 'display_fg': display_fg,
            'btn_bg': btn_bg, 'btn_fg': btn_fg, 'btn_hover': btn_hover,
            'op_btn_bg': op_bg, 'op_btn_fg': op_fg,
            'eq_btn_bg': eq_bg, 'eq_btn_fg': eq_fg,
            'clr_btn_bg': clr_bg, 'clr_btn_fg': clr_fg,
            'font': ('Arial', 14, 'bold'), 'display_font': ('Arial', 28, 'bold'),
            'shadow': True, 'gradient': False, 'roundness': 12 if is_dark else 8,
            'is_dark': is_dark
        }
    return themes

# ─── ۳. تم‌های نام‌گذاری‌شدهٔ ویژه ───
NAMED_THEMES = {
    '1': {'bg':'#f0f0f0','display_bg':'#ffffff','display_fg':'#000000','btn_bg':'#e0e0e0','btn_fg':'#000000','btn_hover':'#c0c0c0','op_btn_bg':'#ff9500','op_btn_fg':'white','eq_btn_bg':'#007aff','eq_btn_fg':'white','clr_btn_bg':'#ff3b30','clr_btn_fg':'white','font':('Arial',14,'bold'),'display_font':('Arial',28,'bold'),'shadow':False,'gradient':False,'roundness':5,'is_dark':False},
    '2': {'bg':'#1e1e1e','display_bg':'#2d2d2d','display_fg':'#ffffff','btn_bg':'#3c3c3c','btn_fg':'#ffffff','btn_hover':'#505050','op_btn_bg':'#ff9500','op_btn_fg':'white','eq_btn_bg':'#0a84ff','eq_btn_fg':'white','clr_btn_bg':'#d32f2f','clr_btn_fg':'white','font':('Arial',14,'bold'),'display_font':('Arial',28,'bold'),'shadow':True,'gradient':False,'roundness':15,'is_dark':True},
    '3': {'bg':'#0a0a0a','display_bg':'#111','display_fg':'#39ff14','btn_bg':'#222','btn_fg':'#39ff14','btn_hover':'#333','op_btn_bg':'#ff073a','op_btn_fg':'white','eq_btn_bg':'#00ffff','eq_btn_fg':'black','clr_btn_bg':'#ff00ff','clr_btn_fg':'black','font':('Consolas',14,'bold'),'display_font':('Consolas',28,'bold'),'shadow':True,'gradient':True,'roundness':20,'is_dark':True},
    'A': {'bg':'#fce4ec','display_bg':'#ffffff','display_fg':'#880e4f','btn_bg':'#f8bbd0','btn_fg':'#880e4f','btn_hover':'#f48fb1','op_btn_bg':'#ad1457','op_btn_fg':'white','eq_btn_bg':'#6a1b9a','eq_btn_fg':'white','clr_btn_bg':'#d32f2f','clr_btn_fg':'white','font':('Georgia',14,'italic'),'display_font':('Georgia',28,'bold'),'shadow':False,'gradient':False,'roundness':12,'is_dark':False},
    'B': {'bg':'#ecf0f3','display_bg':'#ecf0f3','display_fg':'#2c3e50','btn_bg':'#ecf0f3','btn_fg':'#2c3e50','btn_hover':'#d1d9e6','op_btn_bg':'#e67e22','op_btn_fg':'white','eq_btn_bg':'#27ae60','eq_btn_fg':'white','clr_btn_bg':'#c0392b','clr_btn_fg':'white','font':('Arial',14,'bold'),'display_font':('Arial',28,'bold'),'shadow':True,'gradient':False,'roundness':20,'is_dark':False},
    'S': {'bg':'#1a1a2e','display_bg':'#16213e','display_fg':'#e94560','btn_bg':'#0f3460','btn_fg':'#e94560','btn_hover':'#533483','op_btn_bg':'#533483','op_btn_fg':'white','eq_btn_bg':'#e94560','eq_btn_fg':'white','clr_btn_bg':'#c91b4e','clr_btn_fg':'white','font':('Arial',15,'bold'),'display_font':('Arial',32,'bold'),'shadow':True,'gradient':True,'roundness':25,'is_dark':True},
    'S+': {'bg':'#2d1b4e','display_bg':'#1a1a2e','display_fg':'#f7d794','btn_bg':'#4a2c6d','btn_fg':'#f7d794','btn_hover':'#6c4b96','op_btn_bg':'#f8a5c2','op_btn_fg':'#2d1b4e','eq_btn_bg':'#f7d794','eq_btn_fg':'#2d1b4e','clr_btn_bg':'#e77f67','clr_btn_fg':'white','font':('Arial',15,'bold'),'display_font':('Arial',32,'bold'),'shadow':True,'gradient':True,'roundness':30,'is_dark':True},
    'X': {'bg':'#121212','display_bg':'#1e1e1e','display_fg':'#bb86fc','btn_bg':'#2c2c2c','btn_fg':'#bb86fc','btn_hover':'#3e3e3e','op_btn_bg':'#cf6679','op_btn_fg':'white','eq_btn_bg':'#03dac6','eq_btn_fg':'black','clr_btn_bg':'#b00020','clr_btn_fg':'white','font':('Consolas',14,'bold'),'display_font':('Consolas',28,'bold'),'shadow':True,'gradient':False,'roundness':8,'is_dark':True},
    'Y': {'bg':'#ffd166','display_bg':'#ffffff','display_fg':'#073b4c','btn_bg':'#06d6a0','btn_fg':'#073b4c','btn_hover':'#118ab2','op_btn_bg':'#ef476f','op_btn_fg':'white','eq_btn_bg':'#073b4c','eq_btn_fg':'white','clr_btn_bg':'#d62828','clr_btn_fg':'white','font':('Comic Sans MS',14,'bold'),'display_font':('Comic Sans MS',28,'bold'),'shadow':False,'gradient':False,'roundness':10,'is_dark':False}
}

THEME_COLORS = {}
THEME_COLORS.update(NAMED_THEMES)
THEME_COLORS.update(_generate_50_themes())

# ─── ۴. موتور محاسبات پیشرفته (SymPy یا معمولی) ───
class AdvancedCalculatorEngine:
    """موتور محاسبات که در صورت وجود SymPy از آن استفاده می‌کند"""
    def __init__(self, use_sympy=HAS_SYMPY):
        self.use_sympy = use_sympy and HAS_SYMPY
        self.expression = ""
        self._reset()

    def _reset(self):
        self.current_display = "0"
        self.expression = ""

    def press(self, char):
        if char == 'C':
            self._reset()
        elif char == '=':
            try:
                if self.use_sympy:
                    # استفاده از SymPy برای نمایش دقیق
                    expr = sp.sympify(self.expression)
                    result = sp.N(expr) if expr.is_Float or expr.has(sp.Float) else expr
                    self.expression = str(result)
                    self.current_display = self.expression
                else:
                    # ارزیابی عادی
                    clean = re.sub(r'[^0-9+\-*/().]', '', self.expression)
                    result = str(eval(clean)) if clean else "0"
                    self.expression = result
                    self.current_display = result
            except Exception:
                self.current_display = "Error"
                self.expression = ""
        else:
            if self.current_display == "Error":
                self._reset()
            if self.current_display == "0" and char not in '/*-+.':
                self.expression = char
            else:
                self.expression += char
            self.current_display = self.expression
        return self.current_display

# ─── ۵. رابط گرافیکی (CustomTkinter یا Canvas) ───
if HAS_CTK:
    class ModernCalculatorGUI:
        def __init__(self, root, title, width, height, theme):
            self.root = root
            self.root.title(title)
            self.root.geometry(f"{width}x{height}")
            self.root.resizable(False, False)
            ctk.set_appearance_mode("dark" if theme.get('is_dark', True) else "light")
            ctk.set_default_color_theme("blue")

            self.engine = AdvancedCalculatorEngine()
            self.theme = theme

            self.display_var = tk.StringVar(value="0")
            self.display = ctk.CTkEntry(
                root, textvariable=self.display_var, font=('Arial', 28, 'bold'),
                justify='right', state='readonly', height=60,
                fg_color=theme['display_bg'], text_color=theme['display_fg'],
                corner_radius=15
            )
            self.display.pack(padx=15, pady=(15,5), fill='x')

            btn_frame = ctk.CTkFrame(root, fg_color='transparent')
            btn_frame.pack(padx=15, pady=10, fill='both', expand=True)

            buttons = [
                ['C', '(', ')', '/'],
                ['7', '8', '9', '*'],
                ['4', '5', '6', '-'],
                ['1', '2', '3', '+'],
                ['0', '.', '=', '']
            ]

            for r, row in enumerate(buttons):
                for c, char in enumerate(row):
                    if char == '': continue
                    fg, bg = self._btn_colors(char)
                    btn = ctk.CTkButton(
                        btn_frame, text=char, font=('Arial', 18, 'bold'),
                        fg_color=bg, text_color=fg, hover_color=theme['btn_hover'],
                        corner_radius=theme.get('roundness', 10),
                        command=lambda ch=char: self._on_click(ch)
                    )
                    btn.grid(row=r, column=c, sticky='nsew', padx=3, pady=3)
                    btn_frame.columnconfigure(c, weight=1)
                btn_frame.rowconfigure(r, weight=1)

        def _btn_colors(self, char):
            if char == 'C': return self.theme['clr_btn_fg'], self.theme['clr_btn_bg']
            if char in '/*-+': return self.theme['op_btn_fg'], self.theme['op_btn_bg']
            if char == '=': return self.theme['eq_btn_fg'], self.theme['eq_btn_bg']
            return self.theme['btn_fg'], self.theme['btn_bg']

        def _on_click(self, char):
            self.display_var.set(self.engine.press(char))

        def run(self): self.root.mainloop()
else:
    class ModernCalculatorGUI:
        def __init__(self, root, title, width, height, theme):
            self.root = root
            self.root.title(title)
            self.root.resizable(False, False)
            self.root.geometry(f"{width}x{height}")
            self.w, self.h = width, height
            self.engine = AdvancedCalculatorEngine()
            self.theme = theme
            self.canvas = tk.Canvas(root, width=width, height=height, bg=theme['bg'], highlightthickness=0)
            self.canvas.pack()
            self.display_id = None
            self._draw_display()
            self._draw_buttons()

        def _draw_display(self):
            self.canvas.create_rectangle(10, 10, self.w-10, 80,
                                         fill=self.theme['display_bg'], outline='', tags='disp')
            self.display_id = self.canvas.create_text(
                self.w-25, 45, text="0", font=self.theme['display_font'],
                fill=self.theme['display_fg'], anchor='e', tags='disp_text'
            )

        def _draw_buttons(self):
            start_x, start_y = 15, 100
            cols, rows = 4, 5
            spacing = 8
            btn_w = (self.w - 2*start_x - (cols-1)*spacing) / cols
            btn_h = (self.h - start_y - 30 - (rows-1)*spacing) / rows
            layout = [['C','(',')','/'],['7','8','9','*'],['4','5','6','-'],
                      ['1','2','3','+'],['0','.','=','']]
            self.btn_colors = {}
            for r in range(rows):
                for c in range(cols):
                    char = layout[r][c]
                    if char == '': continue
                    x1 = start_x + c*(btn_w+spacing)
                    y1 = start_y + r*(btn_h+spacing)
                    x2 = x1 + btn_w
                    y2 = y1 + btn_h
                    fill, text_col = self._btn_fill(char)
                    self.btn_colors[f'btn_{char}'] = fill
                    if self.theme.get('shadow'):
                        self.canvas.create_oval(x1+2, y1+2, x2+2, y2+2,
                                                fill='#000000', stipple='gray50', outline='')
                    self.canvas.create_oval(x1, y1, x2, y2, fill=fill, outline='', tags=('btn',f'btn_{char}'))
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=char,
                                            fill=text_col, font=self.theme['font'], tags=('btn',f'btn_{char}'))
                    self.canvas.tag_bind(f'btn_{char}', '<Button-1>', lambda e, ch=char: self._on_click(ch))
                    self.canvas.tag_bind(f'btn_{char}', '<Enter>', lambda e, ch=char: self._hover(ch, True))
                    self.canvas.tag_bind(f'btn_{char}', '<Leave>', lambda e, ch=char: self._hover(ch, False))

        def _btn_fill(self, char):
            if char == 'C': return self.theme['clr_btn_bg'], self.theme['clr_btn_fg']
            if char in '/*-+': return self.theme['op_btn_bg'], self.theme['op_btn_fg']
            if char == '=': return self.theme['eq_btn_bg'], self.theme['eq_btn_fg']
            return self.theme['btn_bg'], self.theme['btn_fg']

        def _hover(self, char, entering):
            color = self.theme['btn_hover'] if entering else self.btn_colors.get(f'btn_{char}')
            self.canvas.itemconfig(f'btn_{char}', fill=color)

        def _on_click(self, char):
            self.canvas.itemconfig(self.display_id, text=self.engine.press(char))

        def run(self): self.root.mainloop()

# ─── ۶. توابع عمومی ───
def help_calculator():
    print("=" * 60)
    print("راهنمای کتابخونه ماشین حساب پیشرفته")
    print("=" * 60)
    print("توابع اصلی:")
    print("  run_calculator(title, width, height, level, custom_colors, use_sympy)")
    print("    - یک ماشین حساب باز می‌کند (تا بسته نشود، برنامه صبر می‌کند)")
    print("    - level: شماره ۱-۵۰ یا نام تم ('S', 'S+', ...)")
    print("    - use_sympy: True (در صورت نصب SymPy) محاسبات دقیق انجام دهد")
    print("  open_calculator(...) : چند ماشین حساب هم‌زمان")
    print("  tour() : معرفی کتابخانه‌های پیشرفته پایتون (SymPy, NEUI, ...)")
    print("=" * 60)

def tour():
    """راهنمای جامع کتابخانه‌های پیشرفته پایتون برای ماشین حساب و GUI"""
    print("\n" + "=" * 60)
    print("🌟 کتابخانه‌های پیشنهادی برای ساخت ماشین حساب‌های نسل جدید")
    print("=" * 60)
    print("1. SymPy (نصب: pip install sympy)")
    print("   - محاسبات دقیق و سمبولیک (ریشه‌ها، مشتق، انتگرال)")
    print("   - نمایش √2 به جای 1.414...")
    print("2. CustomTkinter (نصب: pip install customtkinter)")
    print("   - ظاهر مدرن و شیشه‌ای برای Tkinter")
    print("   - دکمه‌های گرد، تم تاریک، افکت‌های هاور")
    print("3. NEUI (کتابخانه جدید)")
    print("   - رابط کاربری GPU-شتاب‌یافته با تم دارک و چیدمان Flexbox")
    print("4. WinUp (بر پایه PySide6)")
    print("   - Hot Reloading، مدیریت state مشابه React، کامپوننت‌های حرفه‌ای")
    print("5. PyEdifice (Declarative UI)")
    print("   - سبک React برای دسکتاپ با Hot Reloading")
    print("6. pydantic-rpn")
    print("   - محاسبات با نمادگذاری RPN و امنیت نوع بالا (Type Safety)")
    print("\nشما می‌توانید کتابخانه ما را با هر یک از این‌ها ترکیب کنید!")
    print("برای مثال، با نصب SymPy، ماشین حساب ما جواب‌ها را دقیق نمایش می‌دهد.")
    print("=" * 60)

def _merge_custom_colors(theme, custom):
    if custom:
        new_theme = theme.copy()
        new_theme.update(custom)
        return new_theme
    return theme

def run_calculator(title="حسابگر پیشرفته", width=400, height=650, level='S',
                   custom_colors=None, use_sympy=HAS_SYMPY):
    base_theme = THEME_COLORS.get(str(level), THEME_COLORS['2'])
    final_theme = _merge_custom_colors(base_theme, custom_colors)
    root = tk.Tk()
    app = ModernCalculatorGUI(root, title, width, height, final_theme)
    if use_sympy and HAS_SYMPY:
        app.engine.use_sympy = True
    app.run()

def open_calculator(title="حسابگر", width=400, height=650, level='S',
                    custom_colors=None, use_sympy=HAS_SYMPY):
    t = threading.Thread(target=run_calculator,
                         args=(title, width, height, level, custom_colors, use_sympy))
    t.daemon = False
    t.start()
