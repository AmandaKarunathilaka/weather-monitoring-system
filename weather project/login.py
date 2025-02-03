import tkinter as tk
import tkinter.messagebox
import sqlite3
from tkinter import Label
from PIL import Image, ImageTk

from dashborad import show_dashboard
from Data_Collect import show_admin_dashboard

def connect_to_db():
    conn = sqlite3.connect("weathermonitoring.db")
    cursor = conn.cursor() # open the cursor object
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

# parent window use bcz it open from welcome screen
def show_login_page(parent_window=None):
    if parent_window:
        parent_window.withdraw() # withdraw mean hide the welcome

    # Use Toplevel if a parent window exists, pop up login
    window = tk.Toplevel() if parent_window else tk.Tk()
    window.title("Login Page")
    window.geometry('700x700')  # width and height
    window.configure(bg="#9DE6FD")

    login = tk.Frame(window, bg="#C2FDFF") # frame contain all login widgets
    login.pack()
    login.configure(width=500, height=600)

    # Keep references to images to prevent garbage collection
    window.image_references = {}

    login_icon = ImageTk.PhotoImage(Image.open("login.png").resize((140, 140), Image.Resampling.LANCZOS))
    window.image_references['login_icon'] = login_icon
    head = tk.Label(login, image=login_icon, bg="#C2FDFF")
    head.place(x=185, y=20, width=140, height=140)

    username_icon = ImageTk.PhotoImage(Image.open('user.png').resize((30, 30), Image.Resampling.LANCZOS))
    password_icon = ImageTk.PhotoImage(Image.open('key.png').resize((30, 30), Image.Resampling.LANCZOS))

    window.image_references['username_icon'] = username_icon
    window.image_references['password_icon'] = password_icon

    user_icon = Label(login, image=username_icon, bg="#C2FDFF")
    user_icon.place(x=50, y=200)
    username_tag = tk.Label(login, text="Username", bg="#C2FDFF", fg="black", font=["Arial", 14])
    username_tag.place(x=90, y=200)
    username_area = tk.Entry(login, font=["Arial", 16],border=0)
    username_area.place(x=200, y=200)

    pass_icon = Label(login, image=password_icon, bg="#C2FDFF")
    pass_icon.place(x=50, y=300)
    password_tag = tk.Label(login, text="Password", bg="#C2FDFF", fg="black", font=["Arial", 14])
    password_tag.place(x=90, y=300)
    password_area = tk.Entry(login, font=["Arial", 16], show="*",border=0)
    password_area.place(x=200, y=300)

    def handle_login():
        user_name = username_area.get()
        pass_key = password_area.get()

        if user_name and pass_key:
            conn, cursor = connect_to_db()
            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            cursor.execute(query, (user_name, pass_key))
            users = cursor.fetchone() # retrieve single record
            conn.close()

            if users:
                tk.messagebox.showinfo("Login", "Login Successful!")

                #clear fields
                username_area.delete(0, tk.END)
                password_area.delete(0, tk.END)

                if user_name.lower() == "admin" and pass_key == '123456':
                    window.after(500, lambda: show_admin_dashboard(window))
                else:
                    window.after(500, lambda: show_dashboard(window))
            else:
                tk.messagebox.showinfo("Login Error", "Invalid Credentials!")
        else:
            tk.messagebox.showinfo("Login", "Please fill all the fields.")

    log = tk.Button(login, text="LOG IN", font=["Arial", 18],border=0, bg="#ff9b83", command=handle_login)
    log.place(x=200, y=390)

    def back_to_main():
        window.destroy()
        if parent_window:
            parent_window.deiconify() # show again welcome

    tk.Button(login, text="Back", font=["Arial", 18], bg="#ff9b83",border=0,
              command=back_to_main).place(x=213, y=480)

    window.mainloop()

if __name__ == "__main__":
    show_login_page()