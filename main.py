import tkinter as tk
from tkinter import ttk, messagebox

# --- Core classes (Book, Library, EBook, etc.) ---

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class BookNotAvailableError(Exception):
    pass

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        raise BookNotAvailableError("Book is not available for lending")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.is_lent = False

    def __iter__(self):
        return (book for book in self.books if not book.is_lent)

    def books_by_author(self, author):
        return (book for book in self.books if book.author.lower() == author.lower())

class EBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size

    def __str__(self):
        return f"{super().__str__()} - Download Size: {self.download_size} MB"


# --- GUI class ---

class LibraryGUI:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("650x550")
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Frame for form inputs
        form_frame = ttk.LabelFrame(self.root, text="Book Information", padding=10)
        form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")

        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", pady=5)
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, pady=5, sticky="w")

        # Author
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky="w", pady=5)
        self.author_entry = ttk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, pady=5, sticky="w")

        # ISBN
        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, sticky="w", pady=5)
        self.isbn_entry = ttk.Entry(form_frame, width=40)
        self.isbn_entry.grid(row=2, column=1, pady=5, sticky="w")

        # eBook checkbox
        self.is_ebook_var = tk.BooleanVar()
        self.ebook_check = ttk.Checkbutton(form_frame, text="Is eBook?", variable=self.is_ebook_var, command=self.toggle_ebook)
        self.ebook_check.grid(row=3, column=1, sticky="w")

        # Download size
        ttk.Label(form_frame, text="Download Size (MB):").grid(row=4, column=0, sticky="w", pady=5)
        self.download_entry = ttk.Entry(form_frame, width=40, state="disabled")
        self.download_entry.grid(row=4, column=1, pady=5, sticky="w")

        # Frame for buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, padx=15, pady=10, sticky="ew")

        # Buttons
        btn_width = 15
        self.add_btn = ttk.Button(button_frame, text="Add Book", command=self.add_book, width=btn_width)
        self.add_btn.grid(row=0, column=0, padx=5, pady=5)

        self.remove_btn = ttk.Button(button_frame, text="Remove Book", command=self.remove_book, width=btn_width)
        self.remove_btn.grid(row=0, column=1, padx=5, pady=5)

        self.lend_btn = ttk.Button(button_frame, text="Lend Book", command=self.lend_book, width=btn_width)
        self.lend_btn.grid(row=0, column=2, padx=5, pady=5)

        self.return_btn = ttk.Button(button_frame, text="Return Book", command=self.return_book, width=btn_width)
        self.return_btn.grid(row=0, column=3, padx=5, pady=5)

        self.show_available_btn = ttk.Button(button_frame, text="Show Available Books", command=self.show_available_books, width=btn_width + 10)
        self.show_available_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.show_by_author_btn = ttk.Button(button_frame, text="Show Books by Author", command=self.show_books_by_author, width=btn_width + 10)
        self.show_by_author_btn.grid(row=1, column=2, columnspan=2, padx=5, pady=10)

        # Output area with scroll
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=10)
        output_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")

        self.output_text = tk.Text(output_frame, height=12, wrap="word", state="disabled")
        self.output_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        scrollbar.pack(side="right", fill="y")

        self.output_text.configure(yscrollcommand=scrollbar.set)

        # Configure grid weights to stretch output frame nicely
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def toggle_ebook(self):
        if self.is_ebook_var.get():
            self.download_entry.config(state="normal")
        else:
            self.download_entry.delete(0, tk.END)
            self.download_entry.config(state="disabled")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.download_entry.delete(0, tk.END)
        self.is_ebook_var.set(False)
        self.toggle_ebook()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()

        if not (title and author and isbn):
            messagebox.showerror("Input Error", "Title, Author, and ISBN are required.")
            return

        if self.is_ebook_var.get():
            download_size = self.download_entry.get().strip()
            if not download_size.replace('.', '', 1).isdigit():
                messagebox.showerror("Input Error", "Download size must be a valid number.")
                return
            book = EBook(title, author, isbn, download_size)
        else:
            book = Book(title, author, isbn)

        self.library.add_book(book)
        messagebox.showinfo("Success", "Book added successfully.")
        self.clear_fields()

    def remove_book(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Input Error", "Please enter ISBN to remove a book.")
            return
        self.library.remove_book(isbn)
        messagebox.showinfo("Success", "Book removed successfully.")

    def lend_book(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Input Error", "Please enter ISBN to lend a book.")
            return
        try:
            book = self.library.lend_book(isbn)
            messagebox.showinfo("Success", f"Book '{book.title}' lent successfully.")
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        isbn = self.isbn_entry.get().strip()
        if not isbn:
            messagebox.showerror("Input Error", "Please enter ISBN to return a book.")
            return
        self.library.return_book(isbn)
        messagebox.showinfo("Success", "Book returned successfully.")

    def show_available_books(self):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Available Books:\n\n")
        for book in self.library:
            self.output_text.insert(tk.END, f"{book}\n")
        self.output_text.config(state="disabled")

    def show_books_by_author(self):
        author = self.author_entry.get().strip()
        if not author:
            messagebox.showerror("Input Error", "Please enter author name to search.")
            return
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Books by {author}:\n\n")
        found = False
        for book in self.library.books_by_author(author):
            self.output_text.insert(tk.END, f"{book}\n")
            found = True
        if not found:
            self.output_text.insert(tk.END, "No books found by this author.")
        self.output_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
