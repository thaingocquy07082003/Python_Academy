import tkinter as tk
from tkinter import messagebox
def submit_form():
    name = entry_name.get()
    dob = entry_dob.get()
    gender = gender_var.get()
    selected_index = listbox_age.curselection()
    age = listbox_age.get(selected_index) if selected_index else "Chưa chọn"
    hobbies = []
    if hobby_reading.get(): hobbies.append("Đọc sách")
    if hobby_travel.get(): hobbies.append("Du lịch")
    if hobby_music.get(): hobbies.append("Nghe nhạc")
    if hobby_sport.get(): hobbies.append("Thể thao")
    if not name or not dob:
        messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ họ tên và ngày sinh!")
        return
    # Chuẩn bị nội dung hiển thị
    result_text = (
        f"Họ tên: {name}\n"
        f"Ngày sinh: {dob}\n"
        f"Tuổi: {age}\n"
        f"Giới tính: {gender}\n"
        f"Sở thích: {', '.join(hobbies) if hobbies else 'Không có'}"
    )
    label_result.config(text=result_text, justify="left")

root = tk.Tk()
root.title("Form Đăng Ký Thông Tin")
root.geometry("420x750")
root.config(bg="#f2f2f2")

frame_result = tk.Frame(root, bg="#fff5cc", padx=10, pady=10)
frame_result.pack(fill="x", pady=5, padx=10)

tk.Label(frame_result, text="THÔNG TIN ĐÃ ĐĂNG KÝ", bg="#fff5cc", font=("Arial", 12, "bold")).pack()
label_result = tk.Label(frame_result, text="Chưa có thông tin", bg="#fff5cc", justify="left", fg="blue")
label_result.pack(anchor="w", pady=5)

frame_info = tk.Frame(root, bg="#d9eaf7", padx=10, pady=10)
frame_info.pack(fill="x", pady=5, padx=10)

tk.Label(frame_info, text="Họ và tên:", bg="#d9eaf7").grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(frame_info, width=30)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame_info, text="Ngày sinh:", bg="#d9eaf7").grid(row=1, column=0, sticky="w", pady=5)
entry_dob = tk.Entry(frame_info, width=30)
entry_dob.grid(row=1, column=1, pady=5)

frame_age = tk.Frame(root, bg="#f7e6d9", padx=10, pady=10)
frame_age.pack(fill="x", pady=5, padx=10)

tk.Label(frame_age, text="Chọn tuổi:", bg="#f7e6d9").pack(anchor="w")

listbox_age = tk.Listbox(frame_age, height=5, exportselection=False)
listbox_age.pack(fill="x", padx=20)
for i in range(18, 61):
    listbox_age.insert(tk.END, str(i))

frame_gender = tk.Frame(root, bg="#f7ecd9", padx=10, pady=10)
frame_gender.pack(fill="x", pady=5, padx=10)

tk.Label(frame_gender, text="Giới tính:", bg="#f7ecd9").pack(anchor="w")

gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_gender, text="Nam", variable=gender_var, value="Nam", bg="#f7ecd9").pack(anchor="w")
tk.Radiobutton(frame_gender, text="Nữ", variable=gender_var, value="Nữ", bg="#f7ecd9").pack(anchor="w")
tk.Radiobutton(frame_gender, text="Khác", variable=gender_var, value="Khác", bg="#f7ecd9").pack(anchor="w")

frame_hobby = tk.Frame(root, bg="#e2f7d9", padx=10, pady=10)
frame_hobby.pack(fill="x", pady=5, padx=10)

tk.Label(frame_hobby, text="Sở thích:", bg="#e2f7d9").pack(anchor="w")

hobby_reading = tk.BooleanVar()
hobby_travel = tk.BooleanVar()
hobby_music = tk.BooleanVar()
hobby_sport = tk.BooleanVar()

tk.Checkbutton(frame_hobby, text="Đọc sách", variable=hobby_reading, bg="#e2f7d9").pack(anchor="w")
tk.Checkbutton(frame_hobby, text="Du lịch", variable=hobby_travel, bg="#e2f7d9").pack(anchor="w")
tk.Checkbutton(frame_hobby, text="Nghe nhạc", variable=hobby_music, bg="#e2f7d9").pack(anchor="w")
tk.Checkbutton(frame_hobby, text="Thể thao", variable=hobby_sport, bg="#e2f7d9").pack(anchor="w")

frame_btn = tk.Frame(root, bg="#f2f2f2", pady=10)
frame_btn.pack()

tk.Button(frame_btn, text="Đăng ký", command=submit_form, bg="#4CAF50", fg="white", width=15).pack()

root.mainloop()
