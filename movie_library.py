import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'movies.json'
MAX_TITLE_LEN = 100
MAX_GENRE_LEN = 50

def load_movies():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except (json.JSONDecodeError, OSError) as e:
        messagebox.showerror("Ошибка файла", f"Не удалось загрузить данные: {e}")
        return []

def save_movies(movies):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
    except OSError as e:
        messagebox.showerror("Ошибка файла", f"Не удалось сохранить данные: {e}")

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x600")
        self.movies = load_movies()
        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # --- Поля ввода ---
        frame_input = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        frame_input.pack(pady=10, fill='x')

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, sticky='e')
        self.entry_title = tk.Entry(frame_input, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Жанр:").grid(row=1, column=0, sticky='e')
        self.entry_genre = tk.Entry(frame_input, width=40)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Год выпуска:").grid(row=2, column=0, sticky='e')
        self.entry_year = tk.Entry(frame_input, width=10)
        self.entry_year.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        tk.Label(frame_input, text="Рейтинг (0-10):").grid(row=3, column=0, sticky='e')
        self.entry_rating = tk.Entry(frame_input, width=10)
        self.entry_rating.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        tk.Button(frame_input, text="Добавить фильм", command=self.add_movie).grid(
            row=4, column=0, columnspan=2, pady=10)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(self.root, text="Фильтр", padx=10, pady=10)
        frame_filter.pack(pady=10, fill='x')

        tk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, sticky='e')
        self.filter_genre = tk.Entry(frame_filter, width=30)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filter, text="Год выпуска:").grid(row=1, column=0, sticky='e')
        self.filter_year = tk.Entry(frame_filter, width=10)
        self.filter_year.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter).grid(
            row=2, column=0, columnspan=2, pady=10)

        # --- Таблица фильмов ---
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text={"title": "Название", "genre": "Жанр", "year": "Год", "rating": "Рейтинг"}[col])
            self.tree.column(col, minwidth=0, width=180)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        if not (title and genre and year_str and rating_str):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        if len(title) > MAX_TITLE_LEN or len(genre) > MAX_GENRE_LEN:
            messagebox.showerror("Ошибка", "Превышена максимальная длина строки.")
            return

        if not year_str.isdigit() or int(year_str) < 1895:  # Первый фильм был в 1895 году
            messagebox.showerror("Ошибка", "Год должен быть числом и не раньше 1895.")
            return

        if not rating_str.replace('.', '', 1).isdigit():
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return

        rating = float(rating_str)
        if not (0 <= rating <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year_str),
            "rating": rating
        }

        self.movies.append(movie)
        save_movies(self.movies)
        self.update_treeview()
        
    def apply_filter(self):
        genre = self.filter_genre.get().strip().lower()
        
        year_str = self.filter_year.get().strip()
        
        filter_year = None
        
        if year_str:
            if not year_str.isdigit() or int(year_str) < 1895:
                messagebox.showerror("Ошибка", "Год должен быть числом и не раньше 1895.")
                return
            filter_year = int(year_str)
