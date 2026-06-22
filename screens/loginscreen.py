import tkinter as tk
from tkinter import messagebox


def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror(
            "Error", "Mohon untuk mengisi Username dan Password")
        return

    messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")


def register():

    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror(
            "Error", "Mohon untuk mengisi Username dan Password")
        return

    messagebox.showinfo("Registrasi Berhasil",
                        f"Selamat datang, {username}! Akun Anda telah berhasil dibuat.")


def password():

    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


root = tk.Tk()
root.title("Login Screen")
root.geometry("400x350")

tk.Label(root, text="COLOR BALL SORT PUZZLE",
         font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

show_password_var = tk.BooleanVar()

tk.Checkbutton(root, text="Show Password",
               variable=show_password_var, command=password).pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=10)
tk.Button(root, text="Register", command=register).pack(pady=5)

root.mainloop()
