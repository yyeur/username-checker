import requests
import random
import string
import time

# Generate a unique random username (5 characters)
def generate_username():
    letters = string.ascii_lowercase
    digits = string.digits
    special_chars = "_."  # Allowed special characters
    return random.choice(letters) + ''.join(random.choices(letters + digits + special_chars, k=4))

# Check username availability on different platforms
def check_username_availability(username):
    platforms = {
        "Telegram": f"https://t.me/{username}",
        "Facebook": f"https://www.facebook.com/{username}",
        "Twitter/X": f"https://x.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "LinkedIn": f"https://www.linkedin.com/in/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Snapchat": f"https://www.snapchat.com/add/{username}",
        "YouTube": f"https://www.youtube.com/{username}",
        "Pinterest": f"https://www.pinterest.com/{username}/",
        "GitHub": f"https://github.com/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Discord": f"https://discord.com/users/{username}"
    }

    available = []
    taken = []

    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 404 or "not found" in response.text.lower():
                available.append(platform)
            else:
                taken.append(platform)
        except requests.RequestException:
            taken.append(platform)

    return available, taken

# Keep generating usernames until we find one available on all platforms
def find_available_username():
    while True:
        username = generate_username()
        print(f"\n🔍 Checking username: {username} ...")

        available, taken = check_username_availability(username)

        if len(taken) == 0:  # Username is available on all platforms
            print(f"\n✅ FOUND! Username '{username}' is available on all platforms! 🎉")
            return username
        else:
            print(f"❌ Username '{username}' is taken on {len(taken)} platforms. Retrying...\n")
            time.sleep(1)  # Avoid sending too many requests too fast

# CLI Interface
def main():
    print("\n🔍 Auto Username Generator & Checker 🔍")
    print("🔄 Generating usernames until we find one available on ALL platforms...\n")

    find_available_username()

if __name__ == "__main__":
    main()