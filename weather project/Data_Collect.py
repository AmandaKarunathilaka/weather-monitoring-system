import tkinter as tk
from PIL import ImageTk, Image
from Temperature import show_temp
from Rainfall import show_rainfall
from Humidity import show_humidity

def show_admin_dashboard(parent_window):
    if parent_window:
        parent_window.withdraw()# parent window is the login

    window=tk.Toplevel()
    window.title("Admin Dashboard")
    window.geometry("600x600")

    # bg setup
    bg_image = Image.open('pexels-talismenas-2038832.jpg').resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_pic = ImageTk.PhotoImage(bg_image)
    window.bg_pic = bg_pic  # Keep a reference to avoid garbage collection

    canvas = tk.Canvas(window, width=600, height=600)
    canvas.create_image(0, 0, image=bg_pic, anchor="nw")
    canvas.pack(fill="both", expand=True) # expand the canvas

    data = tk.Frame(window, bg="#C2FDFF", bd=0)
    data.place(relx=0.5, rely=0.5, anchor="center")
    data.configure(width=400, height=400)

    topic = tk.Label(data, text="Data Collection Forms", fg="black", bg="#385CED",
                     font=["Arial", 20])
    topic.place(x=0, y=0, width=400)
    temp = tk.Button(data,text="Temperature",bg="#ff9b83",font=["Arial", 20],border=0,
                     command=lambda: show_temp(window))
    temp.place(x=100, y=80)
    rain = tk.Button(data,text="Rainfall",bg="#ff9b83", font=["Arial", 20],border=0,
                     command=lambda: show_rainfall(window))
    rain.place(x=130, y=160)
    hum = tk.Button(data,text="Humidity",bg="#ff9b83", font=["Arial", 20],border=0,
                    command=lambda: show_humidity(window)) # window mean the parent window
    hum.place(x=125, y=240)

    def logout():
        window.destroy()
        parent_window.deiconify() # deiconify make the parent window visible

    tk.Button(data, text="Logout", bg="#2F98FF", fg="black", font=["Arial", 18],border=0,
              command=lambda: logout()).place(x=135, y=350)

if __name__ =='__main__':
    window = tk.Tk()
    window.withdraw()
    show_admin_dashboard(window)
    window.mainloop()