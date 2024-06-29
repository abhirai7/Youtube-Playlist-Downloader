import os
import threading
from tkinter import *
from tkinter import messagebox, filedialog
from pytube import Playlist, YouTube
from PIL import Image, ImageTk

class CustomCanvas(Canvas):
    def create_roundrect(self, x1, y1, x2, y2, **kwargs):
        radius = kwargs.pop('radius', 25) 
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("650x650")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.create_images()
        self.create_canvas()
        self.create_frames()
        self.create_labels()
        self.create_entry()
        self.create_buttons()
        
    def create_images(self):
        self.youtube_logo_image = Image.open("youtube_logo.png").resize((650, 300), Image.BICUBIC)
        self.youtube_logo = ImageTk.PhotoImage(self.youtube_logo_image)
        
        self.app_logo_image = Image.open("app_logo.png").resize((150, 100), Image.BICUBIC)
        self.app_logo = ImageTk.PhotoImage(self.app_logo_image)
        
        self.download_button_image = PhotoImage(file="download_button.png")
        
    def create_canvas(self):
        self.canvas = CustomCanvas(self.root, width=650, height=200, highlightthickness=0, background="black")
        self.canvas.pack(padx=10, pady=10)
        self.canvas.create_image(325, 100, image=self.youtube_logo)
        
    def create_frames(self):
        self.top_margin = Frame(self.root, bg="black", height=3)
        self.top_margin.pack(padx=10, pady=10, fill=X)
        
        self.top_frame = Frame(self.root, bg="#f1f1f1")
        self.top_frame.pack(side=RIGHT, padx=10, pady=10)
        
        self.middle_frame = Frame(self.root, bg="#f1f1f1")
        self.middle_frame.pack(padx=10, pady=20)
        
        self.bottom_frame = Frame(self.root, bg="#f1f1f1")
        self.bottom_frame.pack(padx=10, pady=20, fill=X)
        
        self.app_canvas = CustomCanvas(self.root, width=200, height=100, highlightthickness=0)
        self.app_canvas.place(x=410, y=270)
        self.app_canvas.create_image(100, 50, image=self.app_logo)
        
    def create_labels(self):
        self.top_label = Label(self.top_frame, text="YouTube Downloader", font=("Segoe UI", 12, "bold"), fg="red", bg="#f1f1f1")
        self.top_label.pack()
        
        self.border_canvas = CustomCanvas(self.top_frame, width=250, height=40, highlightthickness=0, bg="#f1f1f1")
        self.border_canvas.pack()
        self.border_canvas.create_roundrect(10, 10, 240, 30, fill="#2ecc71", outline="#2ecc71", width=2)
        
        self.url_label = Label(self.middle_frame, text="Enter YouTube URL:", font=("Arial", 14, "bold"), fg="#3498db", bg="#f1f1f1", bd=5, relief="ridge")
        self.url_label.pack(pady=15, ipady=5, ipadx=5)
        
    def create_entry(self):
        self.url_entry = Entry(self.middle_frame, width=40, font=("Arial", 14), fg="#808080", bg="white", bd=1, relief="ridge", highlightthickness=1)
        self.url_entry.insert(0, "https://youtube.com")
        self.url_entry.bind("<FocusIn>", self.clear_default_text)
        self.url_entry.bind("<FocusOut>", self.focus_out)
        self.url_entry.pack(pady=15, ipady=5, ipadx=5)
        
    def create_buttons(self):
        self.download_button = Button(self.middle_frame, command=self.download_video, image=self.download_button_image, width=210, height=55, borderwidth=0)
        self.download_button.pack(pady=20)
        self.download_button.bind("<Enter>", self.on_hover)
        self.download_button.bind("<Leave>", self.on_leave)
        self.download_button.bind("<Button-1>", self.on_hover)
        self.download_button.bind("<ButtonRelease-1>", self.on_leave)
        
    def clear_default_text(self, event):
        if self.url_entry.get() == "https://youtube.com":
            self.url_entry.delete(0, "end")
        self.url_entry.configure(highlightthickness=2, highlightcolor="#00FFFF", highlightbackground="blue")
        
    def focus_out(self, event):
        self.url_entry.configure(highlightthickness=1, highlightcolor="gray", highlightbackground="gray")
        
    def on_hover(self, event):
        self.download_button.config(bd=3)
        
    def on_leave(self, event):
        self.download_button.config(relief="flat", bd=0)
        
    def download_video(self):
        def download_all(url, path):
            try:
                for (index, video) in enumerate(url):
                    video = YouTube(video)
                    video_hd = video.streams.get_highest_resolution()
                    video_hd.download(path)
                    self.progress_label.config(text=f"Downloading video {index+1} of {len(url)}")
                messagebox.showinfo("Success", "Playlist downloaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Download failed: {e}")
                
        url = self.url_entry.get()
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
        
        self.progress_label = Label(self.bottom_frame, text="", font=("Segoe UI", 12), fg="#3498db")
        self.progress_label.pack(pady=20)
        
        threading.Thread(target=download_all, args=(url_obj, path)).start()

if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloader(root)
    root.mainloop()
