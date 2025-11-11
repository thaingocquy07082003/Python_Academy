import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Tên file lưu dữ liệu
DATA_FILE = "todos.json"

# Đọc dữ liệu từ file
def load_todos():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Ghi dữ liệu vào file
def save_todos():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

# Danh sách công việc
todos = load_todos()

# Hàm thêm công việc
def add_todo():
    task = entry.get().strip()
    if task:
        todos.append({"task": task, "done": False})
        update_listbox()
        entry.delete(0, tk.END)
        save_todos()
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung công việc!")

# Hàm xóa công việc
def delete_todo():
    try:
        selected = listbox.curselection()[0]
        todos.pop(selected)
        update_listbox()
        save_todos()
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để xóa!")

# Hàm đánh dấu hoàn thành
def toggle_done():
    try:
        selected = listbox.curselection()[0]
        todos[selected]["done"] = not todos[selected]["done"]
        update_listbox()
        save_todos()
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc!")

# Cập nhật Listbox
def update_listbox():
    listbox.delete(0, tk.END)
    for i, todo in enumerate(todos):
        prefix = "✓ " if todo["done"] else "○ "
        text = f"{prefix}{todo['task']}"
        listbox.insert(tk.END, text)
        # Tô màu xanh nếu hoàn thành
        if todo["done"]:
            listbox.itemconfig(i, {'fg': 'green'})

# Tạo giao diện
root = tk.Tk()
root.title("Todo List App")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Tiêu đề
title = tk.Label(root, text="📝 Todo List", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
title.pack(pady=10)

# Frame nhập liệu
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10, fill=tk.X, padx=20)

entry = tk.Entry(input_frame, font=("Helvetica", 12), relief=tk.FLAT, bg="white")
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

add_button = tk.Button(
    input_frame, text="➕ Thêm", command=add_todo,
    bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"),
    relief=tk.FLAT, cursor="hand2"
)
add_button.pack(side=tk.RIGHT, padx=(5, 0))

# Listbox hiển thị công việc
listbox_frame = tk.Frame(root, bg="#f0f0f0")
listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(
    listbox_frame,
    font=("Consolas", 11),
    selectbackground="#bde0fe",
    yscrollcommand=scrollbar.set,
    activestyle="none",
    bg="white",
    relief=tk.FLAT
)
listbox.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)

# Nút chức năng
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

done_button = tk.Button(
    button_frame, text="✅ Hoàn thành", command=toggle_done,
    bg="#2196F3", fg="white", relief=tk.FLAT, cursor="hand2"
)
done_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(
    button_frame, text="🗑️ Xóa", command=delete_todo,
    bg="#f44336", fg="white", relief=tk.FLAT, cursor="hand2"
)
delete_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(
    button_frame, text="🧹 Xóa hết", command=lambda: [
        todos.clear(), update_listbox(), save_todos()
    ],
    bg="#9E9E9E", fg="white", relief=tk.FLAT, cursor="hand2"
)
clear_button.grid(row=0, column=2, padx=5)

# Hiển thị ban đầu
update_listbox()

# Phím tắt
root.bind('<Return>', lambda e: add_todo())
root.bind('<Delete>', lambda e: delete_todo())

# Chạy ứng dụng
root.mainloop()