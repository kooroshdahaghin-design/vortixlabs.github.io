from media_runner import MediaRunner

# روش ۱: بی‌نهایت با استفاده از "A"
runner1 = MediaRunner("my_gif.gif", "image.jpg")
runner1.set_repeat("A")  # "A" یعنی بی‌نهایت
runner1.set_interval("1s")
runner1.set_mode("replace")
runner1.run()

# روش ۲: بی‌نهایت با "a" کوچک هم کار می‌کنه
runner2 = MediaRunner("video.mp4")
runner2.set_repeat("a")  # "a" هم یعنی بی‌نهایت
runner2.run()

# روش ۳: تعداد مشخص با عدد
runner3 = MediaRunner("ad.gif")
runner3.set_repeat(10)  # ۱۰ بار تکرار
runner3.run()

# روش ۴: مستقیم تو یه خط با "A"
MediaRunner("popup.gif").set_repeat("A").set_interval("500ms").run()

# روش ۵: ترکیب با تنظیمات دیگه
MediaRunner("gif1.gif", "gif2.gif").set_repeat("A").set_interval("2s").set_unclosable(True).set_random_position(True).run()
