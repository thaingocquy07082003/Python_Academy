import tkinter as tk
from tkinter import messagebox

# Biến toàn cục
is_running = False
time_left = 0

def start_timer():
    global is_running, time_left
    try:
        seconds = int(entry.get())
        if seconds <= 0:
            messagebox.showerror("Lỗi", "Vui lòng nhập số giây lớn hơn 0!")
            return
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")
        return

    time_left = seconds
    is_running = True
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    entry.config(state="disabled")
    update_timer()

def stop_timer():
    global is_running
    is_running = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    entry.config(state="normal")

def update_timer():
    global time_left, is_running
    if is_running and time_left > 0:
        # Chuyển đổi giây thành phút:giây
        minutes = time_left // 60
        seconds = time_left % 60
        label.config(text=f"{minutes:02d}:{seconds:02d}")
        time_left -= 1
        # Cập nhật sau 1 giây
        root.after(1000, update_timer)
    elif time_left <= 0:
        label.config(text="Hết thời gian!")
        is_running = False
        start_button.config(state="normal")
        stop_button.config(state="disabled")
        entry.config(state="normal")
        messagebox.showinfo("Hoàn thành", "Đã đếm ngược xong!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Đồng hồ đếm ngược")
root.geometry("300x200")

# Nhãn hiển thị thời gian
label = tk.Label(root, text="00:00", font=("Arial", 24), fg="blue")
label.pack(pady=10)

# Nhãn và ô nhập số giây
entry_label = tk.Label(root, text="Nhập số giây:", font=("Arial", 12))
entry_label.pack()
entry = tk.Entry(root, font=("Arial", 12), width=10)
entry.pack(pady=5)

# Nút Bắt đầu
start_button = tk.Button(root, text="Bắt đầu", font=("Arial", 12), command=start_timer)
start_button.pack(pady=5)

# Nút Dừng
stop_button = tk.Button(root, text="Dừng", font=("Arial", 12), command=stop_timer, state="disabled")
stop_button.pack(pady=5)

# Chạy ứng dụng
root.mainloop()