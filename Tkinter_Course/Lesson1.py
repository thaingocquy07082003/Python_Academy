from tkinter import *
root = Tk()
root.geometry("400x300")  

paned_window = PanedWindow(root, orient='horizontal', sashwidth=5, sashrelief=RAISED)
paned_window.pack(fill=BOTH, expand=True)  
left_pane = Frame(paned_window, bg="lightblue")
right_pane = Frame(paned_window, bg="lightgreen")

paned_window.add(left_pane, minsize=100) 
paned_window.add(right_pane, minsize=100)
Label(left_pane, text="Hello World", font=("Arial", 16, "bold"), bg="lightblue", fg="navy").pack(pady=20)
Label(right_pane, text="Hello World!", font=("Arial", 16, "italic"), bg="lightgreen", fg="darkgreen").pack(pady=20)

root.mainloop()