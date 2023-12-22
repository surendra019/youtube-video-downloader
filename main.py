from asyncio import streams
from cgitb import text
from hmac import new
import tkinter as tk
import time
from turtle import screensize
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
from tkinter import messagebox
import threading
from tkinter import ttk
import urllib.request
from PIL import Image, ImageTk
from io import BytesIO

def center_window(window, x, y):
    window.geometry(f"{x}x{y}+{int(window.winfo_screenwidth()/2-x/2)}+{int(window.winfo_screenheight()/2-y/2)}")
    

root = tk.Tk()
root.title("YouTube Downloader") 


center_window(root, 300,200)

new_window = tk.Toplevel(root)
center_window(new_window, 400, 400)
new_window.title("Select Quality")
new_window.withdraw()

link_label = tk.Label(root, text="Enter YouTube Link:")
link_label.pack(pady= 20)


frame = ttk.Frame(root, style='RoundedEntry.TFrame', padding=(5, 5, 5, 5))
frame.pack()

link_entry = ttk.Entry(frame, font=('Arial', 12))
link_entry.pack(expand=True, fill='both')

style = ttk.Style()


# Configure the style for the rounded button
style.configure(
    'RoundedButton.TButton',
    border=10, 
    relief=tk.RAISED
)


def check_video():
    
    video_url = link_entry.get()
    status_label.config(text="")
    print(video_url)
    try:
        global yt
        yt = YouTube(video_url, on_progress_callback=download_progress, on_complete_callback=on_download_completed)
        global image_url
        image_url = yt.thumbnail_url

        global stream
        stream = yt.streams.get_highest_resolution()
        
        for i in yt.streams:
            if i.mime_type=="video/mp4":
                available_streams.append(i.resolution)
      
        open_new_window()
    except VideoUnavailable:
        status_label.config(text="not a valid link")
    except RegexMatchError:
        status_label.config(text="wrong link")


def clear_input():
    link_entry.delete(0, tk.END)


btn_frame = ttk.Frame(root)
btn_frame.pack()

check_btn = ttk.Button(btn_frame, text="check",style='RoundedButton.TButton', command=check_video)
check_btn.pack(side="left", pady=5)


clear_btn = ttk.Button(btn_frame, text="clear",style='RoundedButton.TButton', command=clear_input)
clear_btn.pack(side="right", pady=5)

status_label = tk.Label(root, pady=10)
status_label.pack()

video_url = ""
available_streams = []
global progress_bar

def download_progress(chunk, fileHandler, bytesRemaining):
    if file_size!=None:
        completed = file_size-bytesRemaining
        percentage_completed = completed/file_size * 100
        progress_bar['value']= percentage_completed

def on_download_completed(stream, file_handle):
    status_lbl.config(text="Download completed!")
    pass

def open_new_window():
    video_title = tk.Label(new_window, text=stream.title)
    video_title.pack(pady=8)

    with urllib.request.urlopen(image_url) as response:
        try:
            
            # Read the image data from the response content
            image_data = response.read()
            image = Image.open(BytesIO(image_data))
            img = image.resize((240, 180))
            global img_tk
            img_tk = ImageTk.PhotoImage(img)

        except Exception as e:
            print("an error occured!"+ str(e))
    if img_tk:
        label = tk.Label(new_window, image=img_tk)
        label.pack(pady=8)
    

    global value_inside
    value_inside = tk.StringVar(root) 
    
    value_inside.set("Select Quality") 

    new_frame = ttk.Frame(new_window)
    new_frame.pack(pady=5)

    option_menu = ttk.OptionMenu(new_frame, value_inside, *available_streams)
    option_menu.pack(side="left")

    download_btn = ttk.Button(new_frame, text="Download", command=download_video)
    download_btn.pack(side="right")

    global status_lbl
    status_lbl = tk.Label(new_window, text="")
    status_lbl.pack(pady=5)

    global progress_bar
    progress_bar = ttk.Progressbar(new_window, mode="determinate")

    new_window.deiconify()

def download_video():
    if value_inside.get()=="Select Quality":
        print("please select a quality!")
    else:
        
        st = yt.streams.get_by_resolution(value_inside.get())

        if st==None:
            status_lbl.config(text="Not available")
        else:
            progress_bar.pack()
            status_lbl.config(text="Downloading....")
            global file_size
            file_size=  st.filesize
            
            st.download("./Videos/") 
            

root.mainloop()
