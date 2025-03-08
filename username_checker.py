import requests
import random
import string
import time
import concurrent.futures

# توليد اسم مستخدم مميز بأحرف وأرقام ورموز، بطول 3 إلى 6 حروف
def generate_username():
    patterns = [
        "{}{}", "{}_{}", "{}.{}", "{}{}{}", "{}{}{}", "{}_{}{}", "{}{}_.{}", "{}.{}_{}"
    ]
    
    letters = string.ascii_lowercase
    digits = string.digits
    special_chars = "_."

    length = random.randint(3, 6)  # تحديد الطول العشوائي بين 3 و6
    parts = ''.join(random.choices(letters + digits, k=length - 1))  # الحروف والأرقام
    special = random.choice(special_chars) if length > 3 else ""  # إضافة رمز فقط إذا كان الطول أكبر من 3

    pattern = random.choice(patterns)
    return pattern.format(parts, special)

# المنصات التي سيتم فحص توفر الاسم عليها
platforms = {
    "Telegram": "https://t.me/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "LinkedIn": "https://www.linkedin.com/in/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "GitHub": "https://github.com/{}",
    "Discord": "https://discord.com/users/{}"
}

# فحص توفر اسم المستخدم على منصة معينة
def check_single_platform(platform, url):
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 404 or "not found" in response.text.lower():
            return platform, True  # متاح
        else:
            return platform, False  # محجوز
    except requests.RequestException:
        return platform, False  # في حال حدوث خطأ، نعتبره محجوزًا

# فحص اسم المستخدم على جميع المنصات بالتوازي
def check_username_availability(username):
    available = []
    taken = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_platform = {
            executor.submit(check_single_platform, platform, url.format(username)): platform
            for platform, url in platforms.items()
        }
        for future in concurrent.futures.as_completed(future_to_platform):
            platform, is_available = future.result()
            if is_available:
                available.append(platform)
            else:
                taken.append(platform)

    return available, taken

# البحث عن اسم مستخدم متاح على جميع المنصات
def find_available_username():
    while True:
        username = generate_username()
        print(f"\n🔍 Checking username: {username} ...")

        available, taken = check_username_availability(username)

        if not taken:  # إذا كان متاحًا على كل المنصات
            print(f"\n✅ FOUND! Username '{username}' is available on all platforms! 🎉")
            return username
        else:
            print(f"❌ Username '{username}' is taken on {len(taken)} platforms. Retrying...\n")
            time.sleep(0.5)  # تقليل زمن الانتظار بين المحاولات

# الواجهة الرئيسية
def main():
    print("\n🔍 Auto Username Generator & Checker 🔍")
    print("🔄 Generating usernames until we find one available on ALL platforms...\n")

    find_available_username()

if __name__ == "__main__":
    main() 