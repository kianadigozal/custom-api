import requests
import time
import os
import uuid
import threading

# آدرس پایه API در ورسل
BASE_URL = "https://custom-api-wheat.vercel.app"

def delete_file_after_delay(filename, delay_seconds):
    """حذف فایل بعد از تاخیر مشخص شده"""
    time.sleep(delay_seconds)
    try:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"فایل {filename} با موفقیت حذف شد")
    except Exception as e:
        print(f"خطا در حذف فایل {filename}:", str(e))

def test_greeting_api(first_name, last_name):
    """تست API سلام"""
    url = f"{BASE_URL}/api/greet"
    params = {
        "firstName": first_name,
        "lastName": last_name
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        print("پاسخ API سلام:", data["message"])
    else:
        print("خطا در دریافت پاسخ:", response.status_code)
        print(response.json())

def test_random_number_api():
    """تست API تولید عدد تصادفی"""
    url = f"{BASE_URL}/api/random"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("عدد تصادفی دریافت شده:", data["number"])
    else:
        print("خطا در دریافت پاسخ:", response.status_code)

def test_image_api(query):
    """تست API دریافت تصویر"""
    print(f"\nدر حال دریافت تصویر برای موضوع: {query}")
    url = f"{BASE_URL}/api/image"
    params = {"q": query}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # ایجاد نام تصادفی برای فایل
        random_filename = f"image_{uuid.uuid4().hex[:8]}_{query}.png"
        
        # ذخیره تصویر در فایل
        with open(random_filename, "wb") as f:
            f.write(response.content)
        print(f"تصویر با موفقیت در فایل {random_filename} ذخیره شد")
        print("این فایل بعد از 120 ثانیه به طور خودکار حذف خواهد شد")
        
        # ایجاد thread جدید برای حذف فایل بعد از 120 ثانیه
        delete_thread = threading.Thread(
            target=delete_file_after_delay,
            args=(random_filename, 120)
        )
        delete_thread.daemon = True  # اجازه می‌دهد برنامه اصلی بدون منتظر ماندن برای این thread بسته شود
        delete_thread.start()
    else:
        print("خطا در دریافت تصویر:", response.status_code)
        try:
            print(response.json())
        except:
            print("پاسخ خطا قابل پردازش نیست")

def main():
    # تست API سلام
    print("در حال تست API سلام...")
    test_greeting_api("علی", "محمدی")
    print("-" * 50)
    
    # تست API اعداد تصادفی
    print("\nدر حال تست API اعداد تصادفی...")
    print("دریافت 5 عدد تصادفی با فاصله 1 ثانیه:")
    for i in range(5):
        test_random_number_api()
        time.sleep(1)
    
    # تست API تصویر
    print("-" * 50)
    test_image_api("cat")  # دریافت تصویر گربه
    test_image_api("dog")  # دریافت تصویر سگ
    
    # صبر می‌کنیم تا فایل‌ها حذف شوند
    print("\nمنتظر حذف فایل‌ها...")
    time.sleep(125)  # کمی بیشتر از 120 ثانیه صبر می‌کنیم

if __name__ == "__main__":
    main() 