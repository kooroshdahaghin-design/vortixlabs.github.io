from my_calculator_lib import run_calculator

# رنگ‌های دلخواه خودت رو بده
my_colors = {
    'bg': '#0d0d0d',           # background - پس‌زمینه
    'display_bg': '#1a1a1a',   # display bg - پس‌زمینهٔ نمایشگر
    'display_fg': '#ffd700',   # display fg - رنگ متن نمایشگر (طلایی)
    'btn_bg': '#2a2a0000002a',       # button bg - رنگ دکمه‌ها
    'btn_fg': '#ffffff',       # button fg - متن دکمه‌ها
    'btn_hover': '#4a4a4a',    # button hover - افکت موس
    'op_btn_bg': '#ff8c00',    # operator bg - دکمه‌های + - * /
    'op_btn_fg': '#000000',    # operator fg
    'eq_btn_bg': '#00ff88',    # equal bg - دکمهٔ =
    'eq_btn_fg': '#000000',    # equal fg
    'clr_btn_bg': '#ff3366',   # clear bg - دکمهٔ C
    'clr_btn_fg': '#ffffff',   # clear fg
    'roundness': 25,           # گردی گوشه‌ها
    'is_dark': True            # تم تاریک
}

run_calculator(
    title="حسابگر شخصی من",
    width=420,
    height=700,
    custom_colors=my_colors
)
