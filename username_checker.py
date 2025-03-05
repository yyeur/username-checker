import requests
import random
import string

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

# CLI Interface
def main():
    print("\n🔍 Username Availability Checker 🔍")
    username = input("Enter username (or press Enter to generate one): ").strip()

    if not username:
        username = generate_username()
        print(f"Generated Username: {username}")

    print("\nChecking availability, please wait...\n")

    available, taken = check_username_availability(username)

    if available:
        print("✅ Available on:")
        for platform in available:
            print(f"  - {platform}")

    if taken:
        print("\n❌ Taken on:")
        for platform in taken:
            print(f"  - {platform}")

if __name__ == "__main__":
    main()