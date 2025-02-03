import tkinter as tk
import tkinter.messagebox
import sqlite3
from tkinter import Label
from PIL import ImageTk, Image

def connect_to_db():
    conn = sqlite3.connect("weathermonitoring.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn, cursor

def show_sign_up(parent_window=None):
    parent_window.withdraw() # parent window is the welcome screen , it will hide in here

    window = tk.Toplevel()
    window.title("Create New Account")
    window.geometry('800x800')
    window.configure(bg="#9DE6FD")

    new = tk.Frame(window, bg="#91cfec", bd=0) # frame is like a small container
    new.place(relx=0.5, rely=0.5, anchor="center")
    new.configure(width=500, height=600)

    #store references for images
    window.image_references={}

    signup_icon = ImageTk.PhotoImage(Image.open("add-user.png").resize((140,140), Image.Resampling.LANCZOS))
    window.image_references['signup_icon'] = signup_icon
    tk.Label(new,image=signup_icon, bg="#91cfec").place(x=185, y=20, width=140, height=140)

    username_icon = ImageTk.PhotoImage(Image.open('user.png').resize((30, 30), Image.Resampling.LANCZOS))
    password_icon = ImageTk.PhotoImage(Image.open('key.png').resize((30, 30), Image.Resampling.LANCZOS))

    window.image_references['username_icon'] = username_icon
    window.image_references['password_icon'] = password_icon

    user_icon = Label(new, image=username_icon, bg="#91cfec")
    user_icon.place(x=50, y=200)
    username = tk.Label(new,text="Username", bg="#91cfec", font=["Arial", 16])
    username.place(x=90, y=200)
    enter = tk.Entry(new,font=["Arial", 14], border=0,)
    enter.place(x=200, y=200)

    pass_icon = Label(new, image=password_icon, bg="#91cfec")
    pass_icon.place(x=50, y=300)
    password = tk.Label(new,text="Password", bg="#91cfec", font=["Arial", 16])
    password.place(x=90, y=300)
    enter_key = tk.Entry(new,font=["Arial", 14], show="*",border=0)
    enter_key.place(x=200, y=300)

    # save account
    def save_account():
        user_id =enter.get()
        pass_key =enter_key.get()

        if user_id and pass_key:
            if len(pass_key) < 6:
                tk.messagebox.showinfo("Sign Up", "Password must have at \n least 6 characters")
                return

            try:
                conn, cursor = connect_to_db()
                query = "INSERT INTO users (username, password) VALUES(? , ?)"
                cursor.execute(query,(user_id, pass_key))
                conn.commit() # save changes
                conn.close()
                tk.messagebox.showinfo("Sign Up", "Account Created Successfully !")

            except Exception as e:
                tk.messagebox.showinfo("Sign Up", "Error Creating Account!")
                tk.messagebox.showerror("Error",f"Database error: {e}")

        else:
            tk.messagebox.showinfo("Sign Up", "Please fill all the fields")

    save = tk.Button(new, text="Sign Up",bg="#ff9b83",font=["Arial", 18],border=0, command=save_account)
    save.place(x=210, y=390)

    def back_to_main():
        window.destroy() # signup close
        parent_window.deiconify() # previously hidden welcome will be show

    #backward button
    tk.Button(new, text="Back", bg="#ff9b83", font=["Arial", 18],border=0
              , command=back_to_main).place(x=217, y=480)

    window.mainloop()

