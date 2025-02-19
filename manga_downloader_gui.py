import tkinter as tk
from tkinter import ttk, messagebox
from search_manga import search_manga
from fetch_chapters import fetch_chapters
from download_chapter import download_chapter_images
from create_pdf import create_pdf
from clear_downloads import clear_download_folder

class MangaDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Manga Downloader")
        self.root.geometry("500x450")

        # ✅ Search Entry
        self.label_search = tk.Label(root, text="Enter Manga Title:")
        self.label_search.pack(pady=5)
        self.entry_search = tk.Entry(root, width=40)
        self.entry_search.pack(pady=5)

        # ✅ Language Selection Dropdown
        self.label_language = tk.Label(root, text="Select Language:")
        self.label_language.pack(pady=5)
        self.language_var = tk.StringVar(value="en")
        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var, state="readonly")
        self.language_dropdown["values"] = ["en", "jp", "es", "fr", "de", "it"]
        self.language_dropdown.pack(pady=5)

        # ✅ Search Button
        self.btn_search = tk.Button(root, text="Search Manga", command=self.search_manga)
        self.btn_search.pack(pady=5)

        # ✅ Dropdown for Manga Selection
        self.label_manga = tk.Label(root, text="Select Manga:")
        self.label_manga.pack(pady=5)
        self.manga_var = tk.StringVar()
        self.manga_dropdown = ttk.Combobox(root, textvariable=self.manga_var, state="readonly")
        self.manga_dropdown.pack(pady=5)

        # ✅ Fetch Chapters Button
        self.btn_fetch_chapters = tk.Button(root, text="Fetch Chapters", command=self.fetch_chapters)
        self.btn_fetch_chapters.pack(pady=5)

        # ✅ Dropdown for Chapter Selection
        self.label_chapter = tk.Label(root, text="Select Chapter:")
        self.label_chapter.pack(pady=5)
        self.chapter_var = tk.StringVar()
        self.chapter_dropdown = ttk.Combobox(root, textvariable=self.chapter_var, state="readonly")
        self.chapter_dropdown.pack(pady=5)

        # ✅ Download Button
        self.btn_download = tk.Button(root, text="Download Chapter", command=self.download_chapter)
        self.btn_download.pack(pady=10)

        # ✅ Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        # Data Storage
        self.manga_dict = {}  # Store manga_id by title
        self.chapters_dict = {}  # Store chapter_id by title
        self.selected_manga_title = ""
        self.selected_manga_id = ""

    # ✅ Search Manga
    def search_manga(self):
        title = self.entry_search.get().strip()
        language = self.language_var.get()

        if not title:
            messagebox.showerror("Error", "Please enter a manga title.")
            return

        manga_list, _ = search_manga(title, language)  # ✅ Ensures language is passed
        if not manga_list:
            messagebox.showerror("Error", "No manga found.")
            return

        # ✅ Store manga data properly
        self.manga_dict = {manga[1]: manga[0] for manga in manga_list}  # {title: id}
        manga_titles = list(self.manga_dict.keys())

        # ✅ Update Dropdown
        self.manga_dropdown["values"] = manga_titles
        if manga_titles:
            self.manga_dropdown.set(manga_titles[0])  # Select first manga by default

    # ✅ Fetch Chapters
    def fetch_chapters(self):
        self.selected_manga_title = self.manga_var.get()
        language = self.language_var.get()

        if not self.selected_manga_title:
            messagebox.showerror("Error", "Please select a manga first.")
            return

        self.selected_manga_id = self.manga_dict.get(self.selected_manga_title)
        chapters = fetch_chapters(self.selected_manga_id, language)  # ✅ Fix: Pass language correctly

        if not chapters:
            messagebox.showerror("Error", "No chapters found.")
            return

        # ✅ Fix: Correct tuple index for chapter title
        self.chapters_dict = {chapter[1]: chapter[0] for chapter in chapters}  # {title: id}
        chapter_titles = list(self.chapters_dict.keys())

        # ✅ Update Dropdown
        self.chapter_dropdown["values"] = chapter_titles
        if chapter_titles:
            self.chapter_dropdown.set(chapter_titles[0])  # Select first chapter by default

    # ✅ Download Chapter with Progress Bar
    def download_chapter(self):
        selected_chapter_title = self.chapter_var.get()
        if not selected_chapter_title:
            messagebox.showerror("Error", "Please select a chapter first.")
            return

        chapter_id = self.chapters_dict.get(selected_chapter_title)
        if not chapter_id:
            messagebox.showerror("Error", "Invalid chapter selection.")
            return

        # Reset Progress Bar
        self.progress["value"] = 0
        self.root.update_idletasks()

        # ✅ Clear previous downloads
        clear_download_folder()

        # ✅ Download Images with Progress
        def update_progress(value):
            self.progress["value"] = value
            self.root.update_idletasks()

        download_chapter_images(chapter_id, progress_callback=update_progress)

        # ✅ Create PDF
        pdf_filename = f"{self.selected_manga_title} - {selected_chapter_title}.pdf"
        create_pdf("downloads", pdf_filename)

        messagebox.showinfo("Success", f"Download Complete!\nSaved as {pdf_filename}")
        self.progress["value"] = 100  # Ensure full progress on completion

# ✅ Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = MangaDownloaderGUI(root)
    root.mainloop()
