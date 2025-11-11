import tkinter as tk
from tkinter import messagebox
def save_note():
    note = text_box.get("1.0", "end-1c").strip()
    if not note:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung ghi chú trước khi lưu!")
        return
    try:
        with open('note.txt', "w", encoding="utf-8") as f:
            f.write(note)
    except Exception as e:
        messagebox.showerror("Lỗi lưu", f"Không thể lưu ghi chú:\n{e}")
        return
    messagebox.showinfo("Lưu thành công", "Ghi chú đã được lưu vào 'note.txt'.")

def clear_text():
    text_box.delete("1.0", "end")

root = tk.Tk()
root.title("📘 Ứng dụng Ghi Chú Học Tập")
root.geometry("500x600")
root.config(bg="#eaf4fc")

frame_title = tk.Frame(root, bg="#cde4f7", pady=10)
frame_title.pack(fill="x")

tk.Label(frame_title, text="📝 Ghi chú học tập", font=("Arial", 16, "bold"), bg="#cde4f7").pack()

frame_text = tk.Frame(root, bg="#eaf4fc", padx=10, pady=10)
frame_text.pack(fill="both", expand=True)

preferred_font = ("Segoe UI", 12)
text_box = tk.Text(
    frame_text,
    wrap="word",
    font=preferred_font,
    width=60,
    height=15,
    fg="#222",
    bg="#ffffff",
    insertbackground="#111",  # caret color
    selectbackground="#cfe8ff",
    selectforeground="#000",
    relief="flat",
)
text_box.pack(fill="both", expand=True, padx=4, pady=4)

frame_buttons = tk.Frame(root, bg="#eaf4fc", pady=10)
frame_buttons.pack()

btn_save = tk.Button(frame_buttons, text="💾 Lưu ghi chú", bg="#4CAF50", fg="white",
                     font=("Arial", 11), width=15, command=save_note)
btn_save.grid(row=0, column=0, padx=10)
btn_clear = tk.Button(frame_buttons, text="🧹 Xóa nội dung", bg="#f44336", fg="white",
                      font=("Arial", 11), width=15, command=clear_text)
btn_clear.grid(row=0, column=1, padx=10)
root.mainloop()
