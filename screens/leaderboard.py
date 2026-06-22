import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

root = tk.Tk()
root.title("Leaderboard Screen")
root.geometry("500x400")

tk.Label(root, text="LEADERBOARD", font=("Arial", 16, "bold")).pack(pady=20)

columns = ("Rank", "Username", "Score")

tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Rank", text="Rank")
tree.heading("Username", text="Username")
tree.heading("Score", text="Score")

tree.column("Rank", width=50)
tree.column("Username", width=200)
tree.column("Score", width=100)

tree.pack(pady=20)

# for item in data:
#     tree.insert("", tk.END, values=item) MENUNGGU DATABASE

tk.Button(
    root,
    text="Kembali",
    width=20
).pack(pady=20)


root.mainloop()
