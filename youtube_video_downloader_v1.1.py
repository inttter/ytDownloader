from tkinter import Tk, Label, Entry, Button, StringVar, Menu, filedialog
from pytube import YouTube
import os
import webbrowser

def open_tos():
    # Open YouTube ToS in a web browser
    webbrowser.open("https://www.youtube.com/static?gl=GB&template=terms")

def set_video_quality(quality):
    # Set the video quality based on user selection
    global selected_video_quality
    selected_video_quality = quality

def choose_download_location():
    # Allow the user to choose a download location using a file dialog
    selected_download_location = filedialog.askdirectory()
    download_location_var.set(selected_download_location)

def download_video():
    link = url_entry.get()
    try:
        youtube_object = YouTube(link)
        stream = youtube_object.streams.filter(res=selected_video_quality.get()).first()

        # Set the output path
        output_path = download_location_var.get()

        # Download the video to the specified location
        stream.download(output_path)

        status_var.set("YouTube video downloaded successfully!")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")

# Console-based code
print("Please read the YouTube TOS to avoid any legal issues before using this program:")
print("https://www.youtube.com/static?gl=GB&template=terms")
print("----------")
print()
print("Welcome to the YouTube Video Downloader.")
print("----------")  # spaces the text out to format it better
print("Tutorial:")
print("----------")
print("In order to correctly download a YouTube video using this Python program, you must enter a VALID YouTube URL.")
print("----------")
print("For example, when the program asks for a link, do not do this:")
print("Enter the URL of your YouTube video: https://youtube.com/watch?v=linkhere")
print("----------")
print("Instead, you must write:")
print("----------")
print("Enter the URL of your YouTube video:https://youtube.com/watch?v=linkhere")
print()  # leaves blank spaces to space out the text
print("Now you know how to download your video using this program. Try it below:")
print("----------")

# Create the main window
root = Tk()
root.title("YouTube Video Downloader")

# Menu for settings
settings_menu = Menu(root)
root.config(menu=settings_menu)

# Submenu for YouTube ToS
tos_submenu = Menu(settings_menu, tearoff=0)
tos_submenu.add_command(label="Open YouTube ToS", command=open_tos)
settings_menu.add_cascade(label="YouTube ToS", menu=tos_submenu)

# Submenu for video quality
video_quality_submenu = Menu(settings_menu, tearoff=0)
video_quality_options = ["720p", "480p", "360p"]  # You can customize the options
selected_video_quality = StringVar()
selected_video_quality.set(video_quality_options[0])  # Default video quality
for quality in video_quality_options:
    video_quality_submenu.add_radiobutton(label=quality, variable=selected_video_quality, command=lambda q=quality: set_video_quality(q))
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
download_location_var.set("C:\\Users\\geani\\Desktop\\Downloaded YT Vids\\videos")  # Default download location
download_location_entry = Entry(root, textvariable=download_location_var, state="readonly", width=50)
download_location_entry.pack()

choose_location_button = Button(root, text="Choose Location", command=choose_download_location)
choose_location_button.pack(pady=5)

# Status label to display download status
status_var = StringVar()
status_label = Label(root, textvariable=status_var)
status_label.pack()

# Run the Tkinter main loop
root.mainloop()

# Console-based code
again = input("Would you like to download another video? Y/N:")
if again == "Y":
    print("Please run the program again to download another video.")
    print()
if again == "N":
    print("Press X to exit.")

# program end