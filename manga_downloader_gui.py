import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from search_manga import search_manga
from fetch_chapters import fetch_chapters
from download_chapter import download_chapter_images
from process_chapter import create_pdf
from clear_downloads import clear_download_folder


class MangaDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manga Downloader")
        self.root.geometry("500x500")
        self.root.resizable(True, True)

        self.dark_mode = False
        self.bg_image = None
        self.language = "en"  # Default language is English

        # Menu Bar for Settings
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="Select Background Image", command=self.select_background)
        self.settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        # Main Frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Background Label
        self.bg_label = tk.Label(self.main_frame)
        self.bg_label.place(relwidth=1, relheight=1)

        # Language Selection
        self.label_language = tk.Label(self.main_frame, text="Select Language:", font=("Arial", 12))
        self.label_language.pack(pady=5)
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self.main_frame, textvariable=self.language_var, state="readonly", font=("Arial", 12))
        self.language_dropdown["values"] = ["en", "es", "fr", "de", "jp"]  # Example languages
        self.language_dropdown.set(self.language)  # Set default selection
        self.language_dropdown.pack(pady=5)

        # Search Entry
        self.label_search = tk.Label(self.main_frame, text="Enter Manga Title:", font=("Arial", 12))
        self.label_search.pack(pady=5)
        self.entry_search = tk.Entry(self.main_frame, width=40, font=("Arial", 12))
        self.entry_search.pack(pady=5)

        # Search Button
        self.btn_search = tk.Button(self.main_frame, text="Search Manga", font=("Arial", 12, "bold"), command=self.search_manga)
        self.btn_search.pack(pady=5)

        # Manga Selection
        self.label_manga = tk.Label(self.main_frame, text="Select Manga:", font=("Arial", 12))
        self.label_manga.pack(pady=5)
        self.manga_var = tk.StringVar()
        self.manga_dropdown = ttk.Combobox(self.main_frame, textvariable=self.manga_var, state="readonly", font=("Arial", 12))
        self.manga_dropdown.pack(pady=5)

        # Fetch Chapters Button
        self.btn_fetch_chapters = tk.Button(self.main_frame, text="Fetch Chapters", font=("Arial", 12, "bold"), command=self.fetch_chapters)
        self.btn_fetch_chapters.pack(pady=5)

        # Chapter Selection
        self.label_chapter = tk.Label(self.main_frame, text="Select Chapter:", font=("Arial", 12))
        self.label_chapter.pack(pady=5)
        self.chapter_var = tk.StringVar()
        self.chapter_dropdown = ttk.Combobox(self.main_frame, textvariable=self.chapter_var, state="readonly", font=("Arial", 12))
        self.chapter_dropdown.pack(pady=5)

        # Download Button
        self.btn_download = tk.Button(self.main_frame, text="Download Chapter", font=("Arial", 12, "bold"), command=self.download_chapter)
        self.btn_download.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        # Read Manga Button (Initially Disabled)
        self.btn_read = tk.Button(self.main_frame, text="Read Manga", font=("Arial", 12, "bold"), state=tk.DISABLED, command=self.read_manga_not_implemented)
        self.btn_read.pack(pady=10)

        # Data Storage
        self.manga_dict = {}  # {manga_title: manga_id}
        self.chapters_dict = {}  # {chapter_title: chapter_id}
        self.selected_manga_title = ""
        self.selected_manga_id = ""
        self.download_folder = "downloads"

        # Manga Reader Data
        self.images = []  # List to store manga images
        self.current_image_index = 0  # Track the current image

    # Update Progress Method
    def update_progress(self, progress):
        """Update the progress bar value during the download."""
        self.progress["value"] = progress  # Update the progress bar with the current value
        self.root.update_idletasks()  # Force the root window to update the UI

    # Search Manga with Language Option
    def search_manga(self):
        self.language = self.language_var.get()  # Get selected language
        title = self.entry_search.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a manga title.")
            return
        manga_list, _ = search_manga(title, self.language)  # Pass the selected language
        if not manga_list:
            messagebox.showerror("Error", "No manga found.")
            return
        self.manga_dict = manga_list  # {manga_title: manga_id}
        self.manga_dropdown["values"] = list(self.manga_dict.keys())  # Set titles as dropdown values
        self.manga_dropdown.set(list(self.manga_dict.keys())[0])  # Set default selection

    # Fetch Chapters
    def fetch_chapters(self):
        self.selected_manga_title = self.manga_var.get()
        if not self.selected_manga_title:
            messagebox.showerror("Error", "Please select a manga first.")
            return
        # Get the manga ID based on selected title
        self.selected_manga_id = self.manga_dict.get(self.selected_manga_title)
        if not self.selected_manga_id:
            messagebox.showerror("Error", "Invalid manga selection.")
            return
        chapters = fetch_chapters(self.selected_manga_id, self.language)  # Use selected language
        if not chapters:
            messagebox.showerror("Error", "No chapters found.")
            return
        self.chapters_dict = {chapter[1]: chapter[0] for chapter in chapters}  # {chapter_title: chapter_id}
        self.chapter_dropdown["values"] = list(self.chapters_dict.keys())  # Set chapter titles in dropdown
        self.chapter_dropdown.set(list(self.chapters_dict.keys())[0])  # Set default chapter selection

    # Download Chapter
    def download_chapter(self):
        selected_chapter_title = self.chapter_var.get()
        if not selected_chapter_title:
            messagebox.showerror("Error", "Please select a chapter first.")
            return
        chapter_id = self.chapters_dict.get(selected_chapter_title)  # Fetch chapter ID from dictionary
        clear_download_folder()
        self.progress["value"] = 0
        self.root.update_idletasks()
        # Pass self.update_progress as a callback to download_chapter_images
        self.images = download_chapter_images(chapter_id, progress_callback=self.update_progress)  # Fetch images and store
        create_pdf(self.download_folder, f"{self.selected_manga_title} - {selected_chapter_title}.pdf")
        messagebox.showinfo("Success", "Download Complete!")
        self.progress["value"] = 100
        self.btn_read["state"] = tk.NORMAL

    # Display Message for "Read Manga" Not Implemented
    def read_manga_not_implemented(self):
        messagebox.showinfo("Feature Not Implemented", "The Read Manga feature is not implemented yet.")

    # Toggle Dark Mode
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    # Apply Dark Mode Theme
    def apply_theme(self):
        if self.dark_mode:
            self.root.config(bg="black")
            self.bg_label.config(bg="black")
            self.label_language.config(bg="black", fg="white")
            self.language_dropdown.config(bg="black", fg="white")
            self.label_search.config(bg="black", fg="white")
            self.entry_search.config(bg="black", fg="white")
            self.btn_search.config(bg="black", fg="white")
            self.label_manga.config(bg="black", fg="white")
            self.manga_dropdown.config(bg="black", fg="white")
            self.btn_fetch_chapters.config(bg="black", fg="white")
            self.label_chapter.config(bg="black", fg="white")
            self.chapter_dropdown.config(bg="black", fg="white")
            self.btn_download.config(bg="black", fg="white")
            self.progress.config(style="TProgressbar")
            self.btn_read.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            self.bg_label.config(bg="white")
            self.label_language.config(bg="white", fg="black")
            self.language_dropdown.config(bg="white", fg="black")
            self.label_search.config(bg="white", fg="black")
            self.entry_search.config(bg="white", fg="black")
            self.btn_search.config(bg="white", fg="black")
            self.label_manga.config(bg="white", fg="black")
            self.manga_dropdown.config(bg="white", fg="black")
            self.btn_fetch_chapters.config(bg="white", fg="black")
            self.label_chapter.config(bg="white", fg="black")
            self.chapter_dropdown.config(bg="white", fg="black")
            self.btn_download.config(bg="white", fg="black")
            self.progress.config(style="TProgressbar")
            self.btn_read.config(bg="white", fg="black")

    # Select Background Image
    def select_background(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.bg_image = Image.open(file_path)
            self.bg_image = self.bg_image.resize((self.root.winfo_width(), self.root.winfo_height()))
            self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)
            self.bg_label.config(image=self.bg_image_tk)
            self.bg_label.image = self.bg_image_tk
            self.bg_label.place(relwidth=1, relheight=1)

# Main Function
def main():
    root = tk.Tk()
    app = MangaDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
