import tkinter as tk
from tkinter import messagebox
import json
import os
import random

# ================== BIẾN TOÀN CỤC ==================
QUESTIONS_FILE = "questions.json"
questions = []
current_question = 0
score = 0


# Tải câu hỏi từ file JSON
def load_questions():
    global questions
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            random.shuffle(data)
            questions = data[:10]  # Lấy tối đa 10 câu
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không đọc được file câu hỏi!\n{e}")
            root.quit()
    else:
        messagebox.showerror("Lỗi", "Không tìm thấy file questions.json!")
        root.quit()

# Hiển thị câu hỏi hiện tại
def show_question():
    if current_question >= len(questions):
        submit_quiz()
        return

    q = questions[current_question]
    question_label.config(text=f"Câu {current_question + 1}: {q['question']}")

    # Xóa lựa chọn cũ
    for widget in options_frame.winfo_children():
        widget.destroy()

    selected_answer.set(-1)

    # Tạo radio buttons
    for i, option in enumerate(q["options"]):
        rb = tk.Radiobutton(
            options_frame,
            text=option,
            variable=selected_answer,
            value=i,
            font=("Arial", 12),
            bg="#f4f6f9",
            anchor="w",
            padx=20
        )
        rb.pack(fill=tk.X, pady=3)

    # Cập nhật nút
    prev_btn.config(state=tk.NORMAL if current_question > 0 else tk.DISABLED)
    next_btn.config(text="Nộp bài" if current_question == len(questions)-1 else "Tiếp")
    progress_label.config(text=f"Câu {current_question + 1}/{len(questions)}")

# Chuyển câu tiếp theo
def next_question():
    global current_question, score
    selected = selected_answer.get()
    if selected != -1 and selected == questions[current_question]["answer"]:
        score += 1

    current_question += 1
    show_question()

# Quay lại câu trước
def prev_question():
    global current_question
    current_question -= 1
    show_question()

# Nộp bài
def submit_quiz():
    global score
    # Kiểm tra câu cuối
    selected = selected_answer.get()
    if selected != -1 and selected == questions[current_question]["answer"]:
        score += 1

    # Hiển thị kết quả
    result_text = f"Điểm: {score}/{len(questions)}\n"
    percent = (score / len(questions)) * 100
    result_text += f"Tỷ lệ đúng: {percent:.1f}%\n\n"

    if percent >= 90:
        result_text += "Xuất sắc!"
    elif percent >= 70:
        result_text += "Tốt!"
    elif percent >= 50:
        result_text += "Khá!"
    else:
        result_text += "Cần cố gắng hơn!"

    messagebox.showinfo("Kết quả Quiz", result_text)
    root.quit()

# ================== GIAO DIỆN ==================
root = tk.Tk()
selected_answer = tk.IntVar(value=-1)
root.title("Quiz Trắc Nghiệm")
root.geometry("600x500")
root.configure(bg="#f4f6f9")
root.resizable(False, False)

# Tiêu đề
tk.Label(
    root, text="Quiz Trắc Nghiệm",
    font=("Helvetica", 20, "bold"), bg="#f4f6f9", fg="#2c3e50"
).pack(pady=20)

# Frame câu hỏi
question_frame = tk.Frame(root, bg="#f4f6f9")
question_frame.pack(pady=10, padx=40, fill=tk.BOTH, expand=True)

# Label câu hỏi
question_label = tk.Label(
    question_frame, text="", font=("Arial", 14),
    bg="#f4f6f9", fg="#2c3e50", wraplength=500, justify="left"
)
question_label.pack(anchor="w", pady=(0, 15))

# Frame đáp án
options_frame = tk.Frame(question_frame, bg="#f4f6f9")
options_frame.pack(fill=tk.BOTH, expand=True)

# Nút điều hướng
nav_frame = tk.Frame(root, bg="#f4f6f9")
nav_frame.pack(pady=15)

prev_btn = tk.Button(
    nav_frame, text="Trước", command=prev_question,
    bg="#95a5a6", fg="white", width=10, state=tk.DISABLED
)
prev_btn.grid(row=0, column=0, padx=5)

next_btn = tk.Button(
    nav_frame, text="Tiếp", command=next_question,
    bg="#3498db", fg="white", width=10
)
next_btn.grid(row=0, column=1, padx=5)

submit_btn = tk.Button(
    nav_frame, text="Nộp bài", command=submit_quiz,
    bg="#e74c3c", fg="white", width=12, font=("Helvetica", 10, "bold")
)
submit_btn.grid(row=0, column=2, padx=5)

# Thanh tiến độ
progress_label = tk.Label(
    root, text="", font=("Helvetica", 10), bg="#f4f6f9", fg="#7f8c8d"
)
progress_label.pack(pady=5)

# ================== KHỞI CHẠY ==================
load_questions()
show_question()

root.mainloop()