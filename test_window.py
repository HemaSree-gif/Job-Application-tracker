import tkinter as tk

window = tk.Tk()
window.title("CareerTrack Test")
window.geometry("600x400")
window.configure(bg="white")

label = tk.Label(
    window,
    text="CAREERTRACK",
    font=("Arial", 28, "bold"),
    bg="white",
    fg="blue"
)
label.pack(pady=80)

button = tk.Button(
    window,
    text="CLICK ME",
    font=("Arial", 15),
    command=lambda: label.config(text="IT IS WORKING!")
)
button.pack()

window.mainloop()
