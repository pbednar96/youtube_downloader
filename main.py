import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import os


def download_video():
    url = url_entry.get()
    folder = folder_path.get()
    download_type = download_type_var.get()

    if not url or not folder:
        messagebox.showerror("Error", "No URL or folder")
        return

    try:
        yt = YouTube(url)
        if download_type == "video":
            stream = yt.streams.get_highest_resolution()
        else:  # audio
            stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            out_file = stream.download(output_path=folder)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            messagebox.showinfo("Success", "Audio downloaded successfully!")
            return

        stream.download(output_path=folder)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")


def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)


# Create the main window
root = tk.Tk()
root.title("YouTube Video/Audio Downloader")

# URL Entry
tk.Label(root, text="YouTube URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Folder Path
folder_path = tk.StringVar()
tk.Label(root, text="Download Folder:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=folder_path, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=10, pady=10)

# Download Type
download_type_var = tk.StringVar(value="video")
tk.Label(root, text="Download Type:").grid(row=2, column=0, padx=10, pady=10)
tk.Radiobutton(root, text="Video", variable=download_type_var, value="video").grid(row=2, column=1, sticky="w", padx=10,
                                                                                   pady=10)
tk.Radiobutton(root, text="Audio", variable=download_type_var, value="audio").grid(row=2, column=1, sticky="e", padx=10,
                                                                                   pady=10)

# Download Button
tk.Button(root, text="Download", command=download_video).grid(row=3, column=1, padx=10, pady=10)

# Run the application
root.mainloop()