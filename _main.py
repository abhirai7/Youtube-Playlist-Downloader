from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pytube import Playlist,YouTube
import os


def download_video():
    def downloadAll(url,path):
        try:
            for (index,video) in enumerate(url):
                video = YouTube(video)
                videoHd = video.streams.get_highest_resolution()
                videoHd.download(path)
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")


        
    url = url_entry.get()
    print(url)
    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube Playlist URL")
        return
    download_directory = filedialog.askdirectory(title="Select Download Directory")
    if not download_directory:
        messagebox.showerror("Error", "Please select a download directory")
        return
    url_obj = Playlist(url)
    path = os.path.join(download_directory,url_obj.title)
    os.mkdir(path)
    downloadAll(url_obj,path)


root = Tk()
root.title("YouTube Downloader")
root.geometry("500x500")  

font_family = "Segoe UI"
font_size = 12
primary_color = "#3498db"  # Blue
secondary_color = "#f1f1f1"  # Light gray
accent_color = "#2ecc71"  # Green
background_color = "#212121"  # Dark gray
title_color = "red"  # Red title color


canvas = Canvas(root, width=500, height=500, bg=background_color, highlightthickness=0)
canvas.pack()

top_frame = Frame(canvas, bg=primary_color)
canvas.create_window(250, 50, window=top_frame)

top_label = Label(top_frame, text="YouTube Downloader", font=(font_family, font_size, "bold"), fg="red")
top_label.pack(pady=10)

middle_frame = Frame(canvas, bg=secondary_color)
canvas.create_window(250, 150, window=middle_frame)

url_label = Label(middle_frame, text="Enter YouTube URL:", font=(font_family, font_size), fg=primary_color)
url_label.pack(pady=10)

url_entry = Entry(middle_frame, width=40, font=(font_family, font_size), fg=primary_color)
url_entry.pack(pady=10)

download_button = Button(middle_frame, text="Download", command=download_video, 
                          font=(font_family, font_size, "bold"), bg=accent_color, fg="white")
download_button.pack(pady=10)

bottom_frame = Frame(canvas, bg=secondary_color)
canvas.create_window(250, 250, window=bottom_frame)


root.mainloop()