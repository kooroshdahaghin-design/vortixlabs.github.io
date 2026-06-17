import subprocess
import threading
import time
import re
import os
import shutil
import sys
import psutil

class Pester:
    def __init__(self):
        self._launch_tasks = []   # هر عضو: (program, interval_seconds)
        self._block_tasks = []    # هر عضو: process_name_substring
        self._stop_event = threading.Event()

    def launch_every(self, program: str, interval: str):
        """
        اضافه کردن یک برنامه برای اجرای مکرر.
        program: اسم یا مسیر فایل اجرایی (مثل 'firefox', 'notepad', '/usr/bin/gedit')
        interval: رشته‌ای مثل '2 seconds', '1 minute', '500 milliseconds', '1 hour'
        """
        seconds = self._parse_interval(interval)
        self._launch_tasks.append((program, seconds))

    def block(self, process_name_substring: str):
        """
        اضافه کردن یک برنامه به لیست سیاه.
        هر پروسه‌ای که اسمش شامل این رشته باشد (بدون حساسیت به بزرگی/کوچکی حروف) kill می‌شود.
        مثال: 'firefox' هم 'firefox.exe' و هم 'FirefoxPortable.exe' را می‌گیرد.
        """
        self._block_tasks.append(process_name_substring)

    def start(self):
        print("[Pester] شروع آزار و اذیت! برای توقف Ctrl+C را بزن.")
        threads = []

        for prog, sec in self._launch_tasks:
            t = threading.Thread(target=self._launch_loop, args=(prog, sec), daemon=True)
            t.start()
            threads.append(t)

        for pname in self._block_tasks:
            t = threading.Thread(target=self._block_loop, args=(pname,), daemon=True)
            t.start()
            threads.append(t)

        try:
            while not self._stop_event.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[Pester] دریافت Ctrl+C. در حال توقف...")
        finally:
            self._stop_event.set()
            for t in threads:
                t.join(timeout=2)
            print("[Pester] متوقف شد.")

    def _resolve_executable(self, program: str) -> str | None:
        """
        تلاش می‌کند مسیر کامل فایل اجرایی را پیدا کند.
        ابتدا از shutil.which استفاده می‌کند، سپس روی ویندوز .exe را هم می‌افزاید.
        در صورت پیدا نشدن None برمی‌گرداند.
        """
        # اگر کاربر مسیر کامل داده (شامل / یا \ باشد)، همون رو برگردون.
        if os.path.sep in program:
            return program if os.path.isfile(program) else None

        # جستجوی معمولی
        path = shutil.which(program)
        if path:
            return path

        # روی ویندوز اگر پسوند داده نشده، .exe را اضافه کن
        if sys.platform == "win32" and not program.lower().endswith(".exe"):
            path = shutil.which(program + ".exe")
            if path:
                return path

        return None

    def _launch_loop(self, program, interval_seconds):
        # یک بار مسیر را حل کن
        exec_path = self._resolve_executable(program)
        if not exec_path:
            # اگر پیدا نشد، برنامه اصلی را با shell=True امتحان می‌کنیم
            print(f"[Pester] !{program} پیدا نشد. با shell=True اجرا می‌کنم، یا مسیر کامل بدهید.")
            exec_path = program  # به shell=True تحویل داده می‌شود

        while not self._stop_event.is_set():
            try:
                if exec_path == program:
                    # استفاده از shell=True وقتی مسیر حل نشده
                    subprocess.Popen(program, shell=True)
                else:
                    subprocess.Popen([exec_path], shell=False)
            except Exception as e:
                print(f"[Pester] خطا در اجرای {program}: {e}")

            self._stop_event.wait(interval_seconds)

    def _block_loop(self, substring):
        while not self._stop_event.is_set():
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    pname = proc.info['name']
                    if pname and substring.lower() in pname.lower():
                        if proc.pid != os.getpid():
                            proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            self._stop_event.wait(0.3)

    @staticmethod
    def _parse_interval(interval_str: str) -> float:
        interval_str = interval_str.strip().lower()
        match = re.match(r'([\d.]+)\s*(milliseconds?|ms|seconds?|sec|s|minutes?|min|m|hours?|hr|h)', interval_str)
        if not match:
            raise ValueError(f"فرمت بازه نامعتبر: {interval_str}")
        value = float(match.group(1))
        unit = match.group(2)

        if unit in ('milliseconds', 'millisecond', 'ms'):
            return value / 1000.0
        elif unit in ('seconds', 'second', 'sec', 's'):
            return value
        elif unit in ('minutes', 'minute', 'min', 'm'):
            return value * 60
        elif unit in ('hours', 'hour', 'hr', 'h'):
            return value * 3600
        else:
            raise ValueError(f"واحد ناشناخته: {unit}")
