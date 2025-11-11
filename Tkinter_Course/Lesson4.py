import tkinter as tk
from tkinter import colorchooser
def start_draw(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y
def draw(event):
    global last_x, last_y
    canvas.create_line(last_x, last_y, event.x, event.y,
                       fill=color, width=pen_size.get(), capstyle=tk.ROUND, smooth=True)
    last_x, last_y = event.x, event.y
def choose_color():
    global color
    color = colorchooser.askcolor(title="Chọn màu vẽ")[1]
    if color:
        color_label.config(bg=color)
def clear_canvas():
    canvas.delete("all")
root = tk.Tk()
root.title("🎨 Ứng dụng Vẽ Hình Tự Do")
root.geometry("600x450")
root.resizable(False, False)
color = "black"
last_x, last_y = None, None
canvas = tk.Canvas(root, bg="white", width=580, height=350, relief="sunken", bd=2)
canvas.pack(pady=10)
canvas.bind("<Button-1>", start_draw) 
canvas.bind("<B1-Motion>", draw)        
toolbar = tk.Frame(root)
toolbar.pack(pady=5)
tk.Button(toolbar, text="🎨 Chọn màu", command=choose_color, bg="#ddd").grid(row=0, column=0, padx=5)
color_label = tk.Label(toolbar, bg=color, width=5, height=1, relief="sunken")
color_label.grid(row=0, column=1, padx=5)
tk.Label(toolbar, text="Độ dày:").grid(row=0, column=2, padx=5)
pen_size = tk.Scale(toolbar, from_=1, to=20, orient="horizontal")
pen_size.set(3)
pen_size.grid(row=0, column=3, padx=5)
tk.Button(toolbar, text="🗑️ Xóa tất cả", command=clear_canvas, bg="#f88").grid(row=0, column=4, padx=5)

root.mainloop()
