import requests
import time

# آدرس پایه API در ورسل
BASE_URL = "https://custom-api-wheat.vercel.app"

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
        time.sleep(1)  # یک ثانیه صبر می‌کنیم

if __name__ == "__main__":
    main() 