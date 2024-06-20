import subprocess
import tkinter as tk
from tkinter import PhotoImage
from datetime import date

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def get_wifi_profiles():
    command = "netsh wlan show profiles"
    output = run_command(command)
    profiles = []
    
    for line in output.split('\n'):
        if "All User Profile" in line:
            profile = line.split(":")[1].strip()
            profiles.append(profile)
    
    return profiles

def get_wifi_password(profile):
    command = f'netsh wlan show profile name="{profile}" key=clear'
    output = run_command(command)
    
    for line in output.split('\n'):
        if "Key Content" in line:
            password = line.split(":")[1].strip()
            return password
    return None

def refresh_profiles():
    profiles = get_wifi_profiles()
    profile_listbox.delete(0, tk.END)
    for profile in profiles:
        profile_listbox.insert(tk.END, profile)

def show_password():
    selected_profile = profile_listbox.get(tk.ACTIVE)
    if selected_profile:
        password = get_wifi_password(selected_profile)
        if password:
            password_label.config(text=f"{password}")
        else:
            password_label.config(text=f"No password found for {selected_profile}")
    else:
        password_label.config(text="Please select a Wi-Fi profile")

def search_profiles(*args):
    search_term = search_var.get().lower()
    profiles = get_wifi_profiles()
    profile_listbox.delete(0, tk.END)
    for profile in profiles:
        if search_term in profile.lower():
            profile_listbox.insert(tk.END, profile)

root = tk.Tk()
root.title("Wifi_Extractor")
root.configure(bg="black")
root.iconbitmap("wifi_logo.ico")
root.geometry("450x600")
root.resizable(False, False)
logo = PhotoImage(file="Wifi_Extractor.png")

logo_label = tk.Label(root, image=logo, bg="black")
logo_label.pack(pady=10)

refresh_button = tk.Button(root, text="List Wi-Fi Profiles", command=refresh_profiles, font=("Fixedsys", 12), bg="gray", fg="white", activebackground="lightgray", activeforeground="black")
refresh_button.pack(pady=5)

search_frame = tk.Frame(root, bg="black")
search_frame.pack(pady=5)

search_label = tk.Label(search_frame, text="Search:", font=("Fixedsys", 12), bg="black", fg="white")
search_label.pack(side=tk.LEFT, padx=5)

search_var = tk.StringVar()
search_var.trace("w", search_profiles)
search_entry = tk.Entry(search_frame, textvariable=search_var, width=40, font=("Fixedsys", 12))
search_entry.pack(side=tk.LEFT)

profile_listbox = tk.Listbox(root, width=50, height=15, font=("Fixedsys", 12), bg="black", fg="white")
profile_listbox.pack(pady=10)

show_password_button = tk.Button(root, text="Show Password", command=show_password, font=("Fixedsys", 12), bg="gray", fg="white", activebackground="lightgray", activeforeground="black")
show_password_button.pack(pady=5)

password_label = tk.Label(root, text="", font=("Fixedsys", 12), bg="black", fg="white")
password_label.pack(pady=10)

programmer_name = "Alex Benny"
current_date = "20 Jun 2024"
info_label = tk.Label(root, text=f"{programmer_name}\n{current_date}", font=("Fixedsys", 12), bg="black", fg="white")
info_label.pack(pady=10)


root.mainloop()
