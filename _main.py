from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pytube import Playlist, YouTube
from PIL import Image, ImageTk

import os
import threading

def clear_default_text(event):
    if url_entry.get() == "https://youtube.com":
        url_entry.delete(0, "end")
    url_entry.configure(highlightthickness=2, highlightcolor="#00FFFF", highlightbackground="blue")
def on_hover(event):
    download_button.config(bd=3)

def on_leave(event):
    download_button.config(relief="flat", bd=0)

def focus_out(event):
    url_entry.configure(highlightthickness=1, highlightcolor="gray", highlightbackground="gray")

def create_roundrect(self, x1, y1, x2, y2, **kwargs):
    if 'canvas' in kwargs:
        canvas = kwargs.pop('canvas')
        kwargs['canvas'] = self
    else:
        canvas = self
    return canvas.create_polygon(x1, y1, x2, y1, x2, y2, x1, y2, 
                                 fill=kwargs.get('fill', ''), 
                                 outline=kwargs.get('outline', ''), 
                                 width=kwargs.get('width', 1), 
                                 smooth=True)

Canvas.create_roundrect = create_roundrect

def download_video():
    def download_all(url, path):
        try:
            for (index, video) in enumerate(url):
                video = YouTube(video)
                video_hd = video.streams.get_highest_resolution()
                video_hd.download(path)
                progress_label.config(text=f"Downloading video {index+1} of {len(url)}")
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Download failed: {e}")

    url = url_entry.get()
    if not url or url == "https://youtube.com":
        messagebox.showerror("Error", "Please enter a valid YouTube Playlist URL")
        return
    download_directory = filedialog.askdirectory(title="Select Download Directory")
    if not download_directory:
        messagebox.showerror("Error", "Please select a download directory")
        return
    url_obj = Playlist(url)
    path = os.path.join(download_directory, url_obj.title)
    os.mkdir(path)

    progress_label = Label(bottom_frame, text="", font=("Segoe UI", 12), fg="#3498db")
    progress_label.pack(pady=20)

    threading.Thread(target=download_all, args=(url_obj, path)).start()

root = Tk()
root.title("YouTube Downloader")
root.geometry("650x650")

image = Image.open("youtube_logo.png")
image = image.resize((650, 300), Image.BICUBIC) 
youtube_logo = ImageTk.PhotoImage(image)

canvas = Canvas(root, width=650, height=200, highlightthickness=0,background="black")
canvas.pack(padx=10, pady=10)
canvas.create_image(325, 100, image=youtube_logo)

top_margin = Frame(root, bg="black", height=3)
top_margin.pack(padx=10,pady=10, fill=X)

app_image = Image.open("app_logo.png")
app_image = app_image.resize((150, 100), Image.BICUBIC)  
app_logo = ImageTk.PhotoImage(app_image)

app_canvas = Canvas(root, width=200, height=100, highlightthickness=0)
app_canvas.place(x=410,y=270)
app_canvas.create_image(100, 50, image=app_logo)
top_frame = Frame(root, bg="#f1f1f1")
top_frame.pack(side=RIGHT,padx=10, pady=10)

top_label = Label(top_frame, text="YouTube Downloader", font=("Segoe UI", 12, "bold"), fg="red", 
                   bg="#f1f1f1", bd=0, highlightthickness=0, relief="solid")

top_label.pack()
border_canvas = Canvas(top_frame, width=250, height=30, highlightthickness=0, bg="#f1f1f1")
border_canvas.pack()

border_canvas.create_roundrect(10, 10, 240, 30, fill="#2ecc71", outline="#2ecc71", width=2)


middle_frame = Frame(root, bg="#f1f1f1")
middle_frame.pack(padx=10, pady=20)

url_label = Label(middle_frame, text="Enter YouTube URL:", font=("Arial", 14, "bold"), fg="#3498db", 
                   bg="#f1f1f1", bd=5, relief="ridge")
url_label.pack(pady=15, ipady=5, ipadx=5)

url_entry = Entry(middle_frame, width=40, font=("Arial", 14), fg="#808080", 
                   bg="white", bd=1, relief="ridge", highlightthickness=1, highlightcolor="#000", 
                   highlightbackground="#000")
url_entry.insert(0, "https://youtube.com")
url_entry.bind("<FocusIn>", clear_default_text)
url_entry.bind("<FocusOut>", focus_out)
url_entry.pack(pady=15, ipady=5, ipadx=5)
download_image = PhotoImage(file = "download_button.png") 
  
download_button = Button(middle_frame,command=download_video, image = download_image,width=210,height=55,
             borderwidth = 0) 
  
download_button.pack(pady=20) 
download_button.bind("<Enter>", on_hover)
download_button.bind("<Leave>", on_leave)
download_button.bind("<Button-1>", on_hover)
download_button.bind("<ButtonRelease-1>", on_leave)  



bottom_frame = Frame(root, bg="#f1f1f1")
bottom_frame.pack(padx=10, pady=20, fill=X)

root.mainloop()