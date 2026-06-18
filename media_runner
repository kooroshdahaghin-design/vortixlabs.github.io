"""
Media Runner - یک کتابخانه ساده برای پخش تصاویر، گیف و ویدئو با قابلیت‌های پیشرفته.
قابلیت‌ها: موقعیت تصادفی، بی‌نهایت با "A"، نام‌گذاری پنجره‌ها
"""

import tkinter as tk
from tkinter import Toplevel, Label, Canvas
from PIL import Image, ImageTk, ImageSequence
import threading
import os
import re
import random
from datetime import datetime, timedelta


class MediaRunner:
    def __init__(self, *media_paths):
        """
        مقداردهی اولیه با یک یا چند مسیر فایل.
        مثال:
            runner = MediaRunner("image.gif", "video.mp4")
        """
        self.media_list = list(media_paths)
        self.interval = 1.0         # زمان پیش‌فرض بین باز شدن فایل‌ها (ثانیه)
        self.repeat_count = 1       # تعداد تکرار کل لیست
        self.loop_forever = False   # حلقهٔ بی‌نهایت
        self.mode = 'accumulate'    # 'accumulate' یا 'replace'
        self.unclosable = False     # غیرقابل بسته شدن پنجره‌ها
        self.window_title = "Media Runner"  # عنوان پیش‌فرض پنجره
        self.start_time = None      # زمان شروع برنامه‌ریزی‌شده (datetime)
        self.random_position = True # موقعیت تصادفی پنجره‌ها (پیش‌فرض فعال)
        self.position_range = None  # محدوده سفارشی (x1, y1, x2, y2) یا None برای کل صفحه

        self._root = None
        self._current_windows = []  # نگهداری آخرین پنجره‌ها
        self._play_index = 0
        self._repeat_done = 0

    # ---------- تنظیمات زنجیره‌ای ----------
    def set_interval(self, interval):
        """
        تنظیم فاصلهٔ بین باز شدن فایل‌ها.
        فرمت‌های قابل قبول: عدد (ثانیه)، یا رشته‌های '1s', '500ms', '2m', '1h'
        """
        self.interval = self._parse_interval(interval)
        return self

    def set_repeat(self, count):
        """
        تعداد دفعات تکرار کل لیست فایل‌ها.
        اگر "A" یا "a" داده شود: بی‌نهایت (حلقه)
        اگر عدد داده شود: همان تعداد تکرار
        مثال:
            set_repeat(10)   # ۱۰ بار تکرار
            set_repeat("A")  # بی‌نهایت
            set_repeat("a")  # بی‌نهایت
        """
        # بررسی کن اگر "A" یا "a" بود، بی‌نهایت کن
        if isinstance(count, str) and count.strip().upper() == "A":
            self.loop_forever = True
            self.repeat_count = -1
        elif isinstance(count, (int, float)):
            self.repeat_count = int(count)
            self.loop_forever = False
        else:
            # اگر رشته عددی بود مثلاً "10"
            try:
                self.repeat_count = int(count)
                self.loop_forever = False
            except (ValueError, TypeError):
                raise ValueError(
                    "set_repeat: مقدار باید عدد باشد یا 'A' برای بی‌نهایت. "
                    f"مقدار داده شده: {count}"
                )
        return self

    def loop(self):
        """پخش بی‌نهایت (تا زمانی که برنامه به زور بسته شود)."""
        self.loop_forever = True
        self.repeat_count = -1
        return self

    def set_mode(self, mode: str):
        """
        حالت پخش:
        'accumulate' -> پنجره‌ها روی هم باقی می‌مانند
        'replace'    -> با باز شدن پنجرهٔ جدید، پنجرهٔ قبلی بسته می‌شود
        """
        if mode in ('accumulate', 'replace'):
            self.mode = mode
        else:
            raise ValueError("mode must be 'accumulate' or 'replace'")
        return self

    def set_unclosable(self, flag: bool):
        """اگر True باشد، کاربر نمی‌تواند پنجره‌ها را با ضربدر یا Alt+F4 ببندد."""
        self.unclosable = flag
        return self

    def set_window_title(self, title: str):
        """عنوان پیش‌فرضی که به پنجره‌ها داده می‌شود (نام فایل هم اضافه می‌شود)."""
        self.window_title = title
        return self

    def set_name(self, name: str):
        """
        تنظیم نام ساده برای پنجره‌ها.
        معادل name="عنوان دلخواه"
        مثال:
            runner.set_name("پنجره من")
        """
        self.window_title = name
        return self

    # برای استفاده خیلی ساده: name="عنوان"
    def name(self, title: str):
        """
        روش جایگزین و ساده‌تر برای تنظیم نام پنجره.
        مثال:
            runner.name("پنجره من")
        """
        self.window_title = title
        return self

    def set_random_position(self, flag: bool, position_range=None):
        """
        فعال/غیرفعال کردن موقعیت تصادفی پنجره‌ها.
        position_range: تاپل (x1, y1, x2, y2) برای محدود کردن ناحیهٔ تصادفی.
                        None یعنی کل صفحه.
        مثال:
            set_random_position(True)  # کل صفحه
            set_random_position(True, (100, 100, 800, 600))  # فقط در این مستطیل
        """
        self.random_position = flag
        if position_range:
            self.position_range = position_range
        return self

    def start_at(self, time_str: str):
        """
        زمان‌بندی اجرای خودکار.
        مثال: start_at("16:00") یا "16:00:00"
        """
        try:
            t = datetime.strptime(time_str, "%H:%M")
        except ValueError:
            try:
                t = datetime.strptime(time_str, "%H:%M:%S")
            except ValueError:
                raise ValueError("فرمت زمان باید HH:MM یا HH:MM:SS باشد.")
        now = datetime.now()
        target = now.replace(hour=t.hour, minute=t.minute, second=0, microsecond=0)
        if target < now:
            target += timedelta(days=1)
        self.start_time = target
        return self

    # ---------- اجرای اصلی ----------
    def run(self):
        """برنامه را اجرا می‌کند و پنجرهٔ اصلی مخفی را وارد حلقهٔ رویداد می‌کند."""
        self._root = tk.Tk()
        self._root.withdraw()  # پنجرهٔ اصلی مخفی

        if self.start_time:
            now = datetime.now()
            delay = (self.start_time - now).total_seconds()
            if delay > 0:
                # زمان‌بندی شروع بعد از تأخیر
                self._root.after(int(delay * 1000), self._begin_playback)
            else:
                self._root.after(0, self._begin_playback)
        else:
            self._root.after(0, self._begin_playback)

        self._root.mainloop()

    # ---------- منطق داخلی ----------
    def _begin_playback(self):
        self._play_index = 0
        self._repeat_done = 0
        self._schedule_next()

    def _schedule_next(self):
        if self._stop_condition():
            return

        media_path = self.media_list[self._play_index]
        self._open_media(media_path)

        # حرکت به فایل بعدی
        self._play_index += 1
        if self._play_index >= len(self.media_list):
            self._play_index = 0
            self._repeat_done += 1

        if not self._stop_condition():
            self._root.after(int(self.interval * 1000), self._schedule_next)

    def _stop_condition(self):
        if self.loop_forever:
            return False
        if self.repeat_count > 0 and self._repeat_done >= self.repeat_count:
            return True
        return False

    def _get_random_position(self, window_width, window_height):
        """
        محاسبه موقعیت تصادفی برای پنجره با توجه به اندازه صفحه و محدودهٔ تعیین‌شده.
        """
        if self.position_range:
            x1, y1, x2, y2 = self.position_range
            max_x = max(x1, x2 - window_width)
            max_y = max(y1, y2 - window_height)
            x = random.randint(x1, max_x) if max_x > x1 else x1
            y = random.randint(y1, max_y) if max_y > y1 else y1
        else:
            screen_width = self._root.winfo_screenwidth()
            screen_height = self._root.winfo_screenheight()
            max_x = max(0, screen_width - window_width)
            max_y = max(0, screen_height - window_height)
            x = random.randint(0, max_x) if max_x > 0 else 0
            y = random.randint(0, max_y) if max_y > 0 else 0
        return x, y

    def _open_media(self, path):
        # مدیریت حالت replace: بستن پنجرهٔ قبلی
        if self.mode == 'replace' and self._current_windows:
            last_win = self._current_windows.pop()
            try:
                last_win.destroy()
            except tk.TclError:
                pass

        # ساخت پنجرهٔ جدید
        win = Toplevel(self._root)
        
        # تنظیم نام پنجره: اگر نام سفارشی داده شده فقط همون رو نشون بده
        if self.window_title == "Media Runner":
            # نام پیش‌فرض: نام کتابخانه + نام فایل
            win.title(f"{self.window_title} - {os.path.basename(path)}")
        else:
            # نام سفارشی: فقط همون نام رو نشون بده
            win.title(self.window_title)

        if self.unclosable:
            # غیرفعال کردن دکمهٔ بستن و Alt+F4
            win.protocol("WM_DELETE_WINDOW", lambda: None)
            win.bind('<Alt-F4>', lambda e: 'break')

        # تشخیص نوع فایل و نمایش
        ext = os.path.splitext(path)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'):
            self._display_image(win, path)
        elif ext in ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'):
            self._display_video(win, path)
        else:
            # تلاش برای باز کردن به عنوان تصویر
            self._display_image(win, path)

        self._current_windows.append(win)

    def _display_image(self, win, path):
        img = Image.open(path)
        
        if getattr(img, "is_animated", False):
            # گیف متحرک
            frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(img)]
            gif_width = frames[0].width()
            gif_height = frames[0].height()
            
            # تنظیم موقعیت تصادفی
            if self.random_position:
                win.update_idletasks()  # به‌روزرسانی برای دریافت اندازه واقعی
                x, y = self._get_random_position(gif_width, gif_height)
                win.geometry(f"+{x}+{y}")
            
            label = Label(win)
            label.pack()

            def update(idx):
                frame = frames[idx]
                label.configure(image=frame)
                idx += 1
                if idx >= len(frames):
                    idx = 0
                try:
                    duration = img.info['duration']
                except KeyError:
                    duration = 100
                win.after(duration, update, idx)

            update(0)
        else:
            # تصویر ثابت
            photo = ImageTk.PhotoImage(img)
            img_width = photo.width()
            img_height = photo.height()
            
            # تنظیم موقعیت تصادفی
            if self.random_position:
                win.update_idletasks()
                x, y = self._get_random_position(img_width, img_height)
                win.geometry(f"+{x}+{y}")
            
            label = Label(win, image=photo)
            label.image = photo  # نگه‌داشتن رفرنس
            label.pack()

    def _display_video(self, win, path):
        try:
            import cv2
        except ImportError:
            raise ImportError(
                "برای پخش ویدئو نیاز به opencv-python دارید.\n"
                "نصب: pip install opencv-python"
            )
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise ValueError(f"نمی‌توان ویدئو را باز کرد: {path}")

        # دریافت ابعاد ویدئو
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # تنظیم موقعیت تصادفی
        if self.random_position:
            win.update_idletasks()
            x, y = self._get_random_position(video_width, video_height)
            win.geometry(f"+{x}+{y}")

        canvas = Canvas(win)
        canvas.pack()

        def show_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                canvas.imgtk = imgtk
                canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
                canvas.config(width=img.width, height=img.height)
                win.after(30, show_frame)  # ~33 فریم بر ثانیه
            else:
                cap.release()

        show_frame()

    @staticmethod
    def _parse_interval(val):
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            val = val.strip().lower()
            match = re.match(r'^(\d+\.?\d*)\s*(ms|s|m|h)?$', val)
            if not match:
                raise ValueError(f"فرمت interval نادرست: {val}")
            num = float(match.group(1))
            unit = match.group(2) if match.group(2) else 's'
            if unit == 'ms':
                return num / 1000.0
            elif unit == 's':
                return num
            elif unit == 'm':
                return num * 60
            elif unit == 'h':
                return num * 3600
        return 1.0
