#https://www.weatherapi.com/docs/
import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
API_KEY = "e0ab5ab50b5449c391192915252710"
BASE_URL = "http://api.weatherapi.com/v1/current.json"
labels = {}
root = tk.Tk()
root.title("Thời tiết Hôm nay")
root.geometry("400x520")
root.configure(bg="#f4f6f9")
root.resizable(False, False)
title = tk.Label(root, text="THỜI TIẾT HÔM NAY", font=("Helvetica", 18, "bold"),
                 bg="#f4f6f9", fg="#2c3e50")
title.pack(pady=15)
search_frame = tk.Frame(root, bg="#f4f6f9")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Nhập thành phố:", font=("Arial", 11),
         bg="#f4f6f9", fg="#34495e").pack(side=tk.LEFT, padx=5)
city_entry = tk.Entry(search_frame, font=("Arial", 11), width=18)
city_entry.pack(side=tk.LEFT, padx=5)
city_entry.focus()

def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Thiếu", "Vui lòng nhập tên thành phố!")
        return

    try:
        params = {'q': city, 'key': API_KEY, 'lang': 'vi'}
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Lỗi", "Không tìm thấy thành phố!")
            return

        labels["city"].config(text=data["location"]["name"])
        labels["country"].config(text=data["location"]["country"])
        labels["temp"].config(text=f"{data['current']['temp_c']:.1f}°C")
        labels["description"].config(text=data["current"]["condition"]["text"].capitalize())
        labels["wind"].config(text=f"{data['current']['wind_kph']} km/h")
        labels["clouds"].config(text=f"{data['current']['cloud']}%")
        now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        labels["updated"].config(text=now)

    except requests.exceptions.RequestException:
        messagebox.showerror("Lỗi mạng", "Không kết nối được Internet!")
    except Exception as e:
        messagebox.showerror("Lỗi", "Đã xảy ra sự cố!")

search_btn = tk.Button(search_frame, text="Tìm", font=("Arial", 10, "bold"),
                       bg="#3498db", fg="white", command=get_weather)
search_btn.pack(side=tk.LEFT, padx=5)
city_entry.bind("<Return>", lambda event: get_weather())
result_frame = tk.Frame(root, bg="#ecf0f1", relief=tk.RAISED, bd=2)
result_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
fields = [
    ("Thành phố", "city"),
    ("Quốc gia", "country"),
    ("Nhiệt độ", "temp"),
    ("Thời tiết", "description"),
    ("Tốc độ gió", "wind"),
    ("Mây", "clouds"),
    ("Cập nhật lúc", "updated")
]

for label_text, key in fields:
    frame = tk.Frame(result_frame, bg="#ecf0f1")
    frame.pack(fill=tk.X, pady=5, padx=10)
    tk.Label(frame, text=label_text + ":", font=("Arial", 11, "bold"),
             bg="#ecf0f1", fg="#2c3e50", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)

    value = tk.Label(frame, text="---", font=("Arial", 11),
                     bg="#ecf0f1", fg="#e74c3c", anchor="w")
    value.pack(side=tk.RIGHT)
    labels[key] = value 

refresh_btn = tk.Button(root, text="Làm mới", font=("Arial", 10, "bold"),
                        bg="#27ae60", fg="white", command=get_weather)
refresh_btn.pack(pady=10)
now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
labels["updated"].config(text=now)

root.mainloop()