import tkinter as tk
# Hàm xử lý khi bấm nút
def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + value)
# Hàm tính kết quả
def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Lỗi")
# Hàm xóa toàn bộ 
def clear():
    entry.delete(0, tk.END)
# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy tính bỏ túi")
root.geometry("400x500")
root.resizable(False, False)
# Ô hiển thị
entry = tk.Entry(root, font=("Arial", 20), borderwidth=5, relief="ridge", justify="right")
entry.pack(fill="x", padx=10, pady=10, ipady=10)
# Danh sách nút bấm
buttons = [
    ('7', '8', '9', '/'),
    ('4', '5', '6', '*'),
    ('1', '2', '3', '-'),
    ('0', '.', '=', '+'),
]
# Tạo khung chứa nút
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)
# Tạo các nút
for r, row in enumerate(buttons):
    for c, char in enumerate(row):
        if char == "=":
            btn = tk.Button(frame, text=char, width=5, height=2, font=("Arial", 18),
                            bg="#4CAF50", fg="white", command=calculate)
        else:
            btn = tk.Button(frame, text=char, width=5, height=2, font=("Arial", 18),
                            command=lambda ch=char: button_click(ch))
        btn.grid(row=r, column=c, padx=5, pady=5)
# Nút xóa
clear_btn = tk.Button(root, text="Xóa", font=("Arial", 18), bg="#f44336", fg="white", command=clear)
clear_btn.pack(fill="x", padx=10, pady=10)

root.mainloop()
