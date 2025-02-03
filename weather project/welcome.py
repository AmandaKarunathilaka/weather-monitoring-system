import tkinter as tk
from PIL import ImageTk, Image
from login import show_login_page
from new_account import show_sign_up

def main_window():
    # Main window
    window = tk.Tk()
    window.title("Weather Monitoring System")
    window.geometry("700x600")

    #bg se up
    bg_pic = ImageTk.PhotoImage(file='pexels-enginakyurt-2104848.jpg') # photoimage is an object
    canvas =tk.Canvas(window, width=1920, height=1080) # create an area to display image
    canvas.create_image(0,0, image=bg_pic, anchor="nw") # x=0 y=0
    canvas.pack()

    welcome = tk.Frame(window, bg="#C2FDFF", bd=0) #0 is used to better transparency
    welcome.place(relx=0.5, rely=0.5, anchor="center") #rel:-position the widgets relative to the width/height of parent
    welcome.configure(width=400, height=600)

    window.image_references = {}# image prevent from being garbage collector

    head=tk.Label(welcome, text="Weather Monitoring System",bg="#385CED", fg="white", font=["Arial", 20])
    head.place(x=0, y=20, width=400)

    welcome_icon = ImageTk.PhotoImage(Image.open('banner.png').resize((256, 256), Image.Resampling.LANCZOS))# 1
    window.image_references['welcome_icon'] = welcome_icon
    welcome_text = tk.Label(welcome, image=welcome_icon, bg="#C2FDFF", fg="black", font=["Arial", 35])
    welcome_text.place(x=80, y=80)

    login = tk.Button(welcome, text="Login", bg="#ff9b83", fg="black", width=8,border=0, font=["Arial", 25],
                      command=lambda: show_login_page(window))
    login.place(x=120, y=350)
    new_user = tk.Button(welcome, text="Sign Up", bg="#ff9b83", fg="black", width=8, border=0, font=["Arial", 25],
                         command=lambda: show_sign_up(window))
    new_user.place(x=120, y=450)

    # Run the application
    window.mainloop()

#1 Resize the image with ensure the high-quality resize with apply LANCZOS resampling algorithm

if __name__ == "__main__":
    main_window()