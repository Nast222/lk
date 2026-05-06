import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# --- Настройки ---
HISTORY_FILE = 'tasks.json'
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учеба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчет", "type": "работа"},
    {"text": "Посмотреть лекцию", "type": "учеба"},
    {"text": "Сходить на пробежку", "type": "спорт"},
    {"text": "Провести встречу", "type": "работа"}
]

# --- Работа с данными (JSON) ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Основная логика приложения ---
class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")

        self.all_tasks = DEFAULT_TASKS.copy()
        self.history = load_history()
        self.filter_type = tk.StringVar(value="все")

        self.create_widgets()
        self.update_history_list()

    def create_widgets(self):
        # Фильтр по типу
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5, fill=tk.X)
        
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        types = ["все", "учеба", "спорт", "работа"]
        for t in types:
            tk.Radiobutton(filter_frame, text=t.capitalize(), variable=self.filter_type, 
                          value=t, command=self.update_history_list).pack(side=tk.LEFT, padx=5)

        # Кнопка генерации
        btn_gen = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        btn_gen.pack(pady=10)

        # Текущая задача (результат)
        self.current_task_label = tk.Label(self.root, text="Ваша задача появится здесь", wraplength=450)
        self.current_task_label.pack(pady=10)

        # История задач
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(history_frame)
        self.history_listbox = tk.Listbox(history_frame, yscrollcommand=scrollbar.set, width=60, height=10)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Кнопки управления задачами и историей
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="Добавить свою задачу", command=self.add_custom_task).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)

    def generate_task(self):
        task = random.choice(self.all_tasks)
        self.current_task_label.config(text=f"Задача: {task['text']} (Тип: {task['type']})")
        
        # Добавляем в историю
        self.history.append(task)
        save_history(self.history)
        self.update_history_list()

    def add_custom_task(self):
        task_text = simpledialog.askstring("Новая задача", "Введите текст задачи:")
        
        if task_text is None: # Пользователь нажал Отмена
            return

        if not task_text.strip():
            messagebox.showerror("Ошибка", "Текст задачи не может быть пустым!")
            return

        # Выбор типа задачи
        task_type = simpledialog.askstring("Тип задачи", 
                                          "Введите тип задачи (учеба/спорт/работа):",
                                          initialvalue="учеба")
        
        if task_type is None: # Пользователь нажал Отмена
            return

        if task_type.lower() not in ["учеба", "спорт", "работа"]:
            messagebox.showerror("Ошибка", "Допустимые типы: учеба, спорт, работа.")
            return

        new_task = {"text": task_text, "type": task_type.lower()}
        self.all_tasks.append(new_task)
        
    def update_history_list(self):
        """Обновляет список истории с учетом фильтра"""
        self.history_listbox.delete(0, tk.END)
        
        filter_val = self.filter_type.get()
        
        for task in self.history:
            if filter_val == "все" or task["type"] == filter_val:
                self.history_listbox.insert(tk.END, f"{task['text']} | Тип: {task['type']}")

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить всю историю задач?"):
            self.history.clear()
            save_history(self.history)
            self.update_history_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
