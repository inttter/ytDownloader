from tkinter import Tk, Label, Entry, Button, StringVar, Menu, filedialog, Radiobutton, simpledialog
from pytube import YouTube
import os
import webbrowser
import requests
import tkinter.messagebox as messagebox

# Function to open the documentation (GitHub page)
def open_documentation():
    webbrowser.open("https://github.com/inttter/ytdownloader")

# Function to check for updates
def check_for_updates():
    try:
        releases_url = "https://api.github.com/repos/inttter/ytdownloader/releases/latest"
        response = requests.get(releases_url)
        if response.status_code == 200:
            latest_version = response.json()["tag_name"]
            if latest_version != "V1.":
                # notify user about the update and provide a link to the download page
                message = f"A newer version ({latest_version}) is available! Would you like to download it?"
                if messagebox.askyesno("Update Available", message):
                    webbrowser.open("https://github.com/inttter/ytdownloader/releases")
            else:
                messagebox.showinfo("No Updates", "You are already using the latest version.")
        else:
            messagebox.showerror("Error", "Failed to check for updates.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def open_tos():
    # Open YouTube ToS in a web browser
    webbrowser.open("https://www.youtube.com/static?gl=GB&template=terms")

def set_video_quality(quality):
    # Set the video quality based on user selection
    global selected_video_quality


def set_download_type(download_type):
    # Set the download type (video)
    global selected_download_type
    selected_download_type = download_type

def choose_download_location():
    # Allow the user to choose a download location using a file dialog
    selected_download_location = filedialog.askdirectory()
    download_location_var.set(selected_download_location)

def download_video():
    link = url_entry.get()
    try:
        youtube_object = YouTube(link)
        available_streams = youtube_object.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().all()

        selected_quality = selected_video_quality.get()

        selected_stream = None
        for stream in available_streams:
            if stream.resolution == selected_quality:
                selected_stream = stream
                break

        if not selected_stream and selected_quality == '480p':
            for stream in available_streams:
                if int(stream.resolution[:-1]) <= 480:  # Look for a stream equal to or less than 480p
                    selected_stream = stream
                    break

        if selected_stream:
            output_path = download_location_var.get()
            selected_stream.download(output_path)
            status_var.set("YouTube video downloaded successfully!")
        else:
            status_var.set(f"No {selected_quality} stream available.")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")

def limit_bandwidth():
    # Function to set download speed limit
    try:
        speed_limit = simpledialog.askinteger("Set Speed Limit", "Enter download speed limit (in KB/s):", parent=root, minvalue=1)
        if speed_limit is not None:
            os.system(f'wget --limit-rate={speed_limit}k {url_entry.get()}')
            status_var.set(f"Download speed limited to {speed_limit} KB/s")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")

# Create the main window
root = Tk()
root.title("YouTube Video Downloader")

# StringVar for video quality
video_quality_options = ["720p", "480p", "360p"]  # You can customize the options 
selected_video_quality = StringVar()
selected_video_quality.set(video_quality_options[0])  # Default video quality

# Menu for settings
settings_menu = Menu(root)
root.config(menu=settings_menu)

# Submenu for Documentation (GitHub)
documentation_submenu = Menu(settings_menu, tearoff=0)
documentation_submenu.add_command(label="Documentation", command=open_documentation)
settings_menu.add_cascade(label="Documentation", menu=documentation_submenu)

# Submenu for YouTube ToS
tos_submenu = Menu(settings_menu, tearoff=0)
tos_submenu.add_command(label="Open YouTube ToS", command=open_tos)
settings_menu.add_cascade(label="YouTube ToS", menu=tos_submenu)

# Submenu for video quality
video_quality_submenu = Menu(settings_menu, tearoff=0)
for quality in video_quality_options:
    video_quality_submenu.add_radiobutton(label=quality, variable=selected_video_quality, value=quality, command=lambda q=quality: set_video_quality(q))
settings_menu.add_cascade(label="Video Quality", menu=video_quality_submenu)

# Label and Entry for the YouTube URL
url_label = Label(root, text="Enter the URL of your YouTube video:")
url_label.pack(pady=10)
url_entry = Entry(root, width=50)
url_entry.pack()

# Button to trigger the download
download_button = Button(root, text="Download Video", command=download_video)
download_button.pack(pady=10)

# Label and Button for the download location
download_location_label = Label(root, text="Download Location:")
download_location_label.pack(pady=5)

download_location_var = StringVar()
download_location_var.set("C:")  # Default download location
download_location_entry = Entry(root, textvariable=download_location_var, state="readonly", width=50)
download_location_entry.pack()

choose_location_button = Button(root, text="Choose Location", command=choose_download_location)
choose_location_button.pack(pady=5)

# Button to check for updates
check_updates_button = Button(root, text="Check for Updates", command=check_for_updates)
check_updates_button.pack(pady=10)

# Status label to display download status
status_var = StringVar()
status_label = Label(root, textvariable=status_var)
status_label.pack()

# Run the Tkinter main loop
root.mainloop()