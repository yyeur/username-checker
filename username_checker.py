import requests
import random
import string
import customtkinter as ctk
from bs4 import BeautifulSoup

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

# Search function for the UI
def search_username():
    username = entry.get().strip()
    if not username:
        username = generate_username()
        entry.delete(0, "end")
        entry.insert(0, username)

    result_textbox.configure(state="normal")
    result_textbox.delete("1.0", "end")
    result_textbox.insert("end", f"🔍 Checking: {username}\n\n")

    available, taken = check_username_availability(username)

    if available:
        result_textbox.insert("end", "✅ Available on:\n", "available")
        for platform in available:
            result_textbox.insert("end", f"  - {platform}\n", "available")
    else:
        result_textbox.insert("end", "❌ Not available on any platform.\n", "taken")

    if taken:
        result_textbox.insert("end", "\n🔴 Taken on:\n", "taken")
        for platform in taken:
            result_textbox.insert("end", f"  - {platform}\n", "taken")

    result_textbox.configure(state="disabled")

# Set up the UI
ctk.set_appearance_mode("System")  # Dark/Light mode based on system settings
ctk.set_default_color_theme("blue")  # Change to "dark-blue" for a different look

root = ctk.CTk()
root.title("Username Checker")
root.geometry("400x500")
root.resizable(False, False)

# UI elements
title_label = ctk.CTkLabel(root, text="🔍 Username Availability Checker", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

entry = ctk.CTkEntry(root, placeholder_text="Enter username or leave blank", font=("Arial", 14))
entry.pack(pady=10)

btn_search = ctk.CTkButton(root, text="🔍 Search", font=("Arial", 14), command=search_username)
btn_search.pack(pady=5)

result_textbox = ctk.CTkTextbox(root, font=("Arial", 12), height=250, width=350)
result_textbox.pack(pady=10)
result_textbox.configure(state="disabled")

# Text colors
result_textbox.tag_config("available", foreground="green")
result_textbox.tag_config("taken", foreground="red")

# Run the UI
root.mainloop()