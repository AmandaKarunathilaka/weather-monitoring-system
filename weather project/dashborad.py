import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

def show_dashboard(parent_window):
    parent_window.withdraw() # in here the parent window is the login

    def connect_to_db():
        try:
            return sqlite3.connect('weathermonitoring.db')
        except sqlite3.Error as e:
            messagebox.showerror(f"Error connecting to database: {e}")
            return None

    def validate_db():
        db = connect_to_db()
        if not db:
            return False

        try:
            cursor = db.cursor()

            # Check temperature table and columns
            cursor.execute('PRAGMA table_info(temperature);') # retrieve column details from pragma
            temp_columns = [col[1] for col in cursor.fetchall()]
            if ('City_name' not in temp_columns or 'Month' not in temp_columns or
                    'Temp_Min' not in temp_columns or 'Temp_Max' not in temp_columns):
                messagebox.showerror("Error" ,"'temperature' table is missing required columns.")
                return False

            # Check rainfall table and columns
            cursor.execute('PRAGMA table_info(rainfall);')
            rain_columns = [col[1] for col in cursor.fetchall()]
            if 'City_name' not in rain_columns or 'Month' not in rain_columns or 'Rainfall_mm' not in rain_columns:
                messagebox.showerror("Error","'rainfall' table is missing required columns.")
                return False

            # Check humidity table and columns
            cursor.execute('PRAGMA table_info(humidity);')
            humidity_col = [col[1] for col in cursor.fetchall()]
            if ('City_name' not in humidity_col or 'Month' not in humidity_col or 'Humidity_day' not in humidity_col
                    or 'Humidity_night' not in humidity_col):
                messagebox.showerror("Error:", "'humidity' table is missing required columns.")
                return False

            return True
        finally:
            db.close()

    def fetch_weather_data(city, month):

        db = connect_to_db()
        if db is None:

            # initialize the dic with none value
            return {"Temp_Min": None, "Temp_Max": None, "Rainfall_mm": None, "Humidity_day": None,
                    "Humidity_night":None, "Longitude":None, "Latitude":None}
        cursor = db.cursor()
        try:
            # Fetch temperature
            cursor.execute(
                "SELECT Temp_Min, Temp_Max, longitude, latitude FROM temperature WHERE City_name = ? AND Month = ?",
                (city, month),
            )
            temp = cursor.fetchone()

            # Fetch rainfall
            cursor.execute(
                "SELECT Rainfall_mm FROM rainfall WHERE City_name = ? AND Month = ?",
                (city, month),
            )
            rain = cursor.fetchone()

            # Fetch humidity
            cursor.execute(
                "SELECT Humidity_day, Humidity_night FROM humidity WHERE City_name = ? AND Month = ?",
                (city, month),
            )
            humidity = cursor.fetchone() #retrieve single row

            return {
                "Temp_Min": temp[0] if temp else None, # extract values from temp like a list
                "Temp_Max": temp[1] if temp else None,
                "Rainfall_mm": rain[0] if rain else None,
                "Humidity_day": humidity[0] if humidity else None,
                "Humidity_night": humidity[1] if humidity else None,
                "Longitude": temp[2] if temp else None,
                "Latitude": temp[3] if temp else None,
            }
        finally:
            db.close()

    def logout():
        root.destroy()
        parent_window.deiconify() # show again login

    def search():
        selected_city = city_var.get()
        selected_month = month_var.get()

        # Clear previous output
        for widget in output_frame.winfo_children():
            widget.destroy()

        weather_data = fetch_weather_data(selected_city, selected_month)

        # Display data
        tk.Label(output_frame, text="Weather Data:", font=("Arial", 16), bg="#BAFBAA").grid(row=0,column=0,
                                                                                            columnspan=2, pady=10)
        #temperature
        if (weather_data["Temp_Min"] is not None and weather_data["Temp_Max"] is not None and
                weather_data["Longitude"] is not None and weather_data["Latitude"] is not None):

            tk.Label(output_frame, image=temp_min, bg="#BAFBAA").grid(row=1, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Temperature Min: {round(float(weather_data['Temp_Min']), 2)}°C",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=1, column=1, padx=20, sticky="w")

            tk.Label(output_frame, image=temp_max_icon, bg="#BAFBAA").grid(row=2, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Temperature Max: {round(float(weather_data['Temp_Max']), 2)}°C",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=2, column=1, padx=20, sticky="w")

            tk.Label(output_frame, image=longitude_icon, bg="#BAFBAA").grid(row=3, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Longitude: {round(float(weather_data['Longitude']), 2)}",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=3, column=1, padx=20, sticky="w")


            tk.Label(output_frame, image=latitude_icon, bg="#BAFBAA").grid(row=4, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Latitude: {round(float(weather_data['Latitude']), 2)}",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=4, column=1, padx=20, sticky="w")

        else:
            tk.Label(output_frame, text="Temperature data not available.", font=("Arial", 14),
                     bg="#BAFBAA").grid(row=1, column=0, columnspan=2, padx=20, sticky='w', pady=5)

        #rainfall
        if weather_data["Rainfall_mm"] is not None:
            tk.Label(output_frame, image=rain_icon, bg="#BAFBAA").grid(row=5, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Rainfall: {round(float(weather_data['Rainfall_mm']), 2)} mm",
                     font=("Arial", 14),bg="#BAFBAA").grid(row=5, column=1, padx=20, sticky="w")
        else:
            tk.Label(output_frame, text="Rainfall data not available.", font=("Arial", 14),
                     bg="#BAFBAA").grid(row=2, column=0, columnspan=2, padx=20, sticky="w", pady=5)

        #humidity
        if weather_data["Humidity_day"] is not None and weather_data["Humidity_night"] is not None:
            tk.Label(output_frame, image=hum_d_icon, bg="#BAFBAA").grid(row=6, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Humidity Day: {round(float(weather_data['Humidity_day']),2)}%",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=6, column=1, padx=20, sticky="w")

            tk.Label(output_frame, image=hum_n_icon, bg="#BAFBAA").grid(row=7, column=0, padx=30, sticky="e")
            tk.Label(output_frame, text=f"Humidity Night: {round(float(weather_data['Humidity_night']), 2)}%",
                     font=("Arial", 14), bg="#BAFBAA").grid(row=7, column=1, padx=20, sticky="w")
        else:
            tk.Label(output_frame, text="Humidity data not available.", font=("Arial", 14),
                     bg="#BAFBAA").grid(row=3, column=0, columnspan=2, padx=20, sticky="w", pady=5)

    if not validate_db():
        messagebox.showerror(" Validation Error","Database validation failed. "
                                                 "Please check the database schema.")
        return

    # main window
    root = tk.Toplevel()
    root.title("Dashboard")
    root.geometry("1000x600")
    root.configure(bg="#00aaff")

    #load icons
    global temp_max_icon, temp_min, rain_icon, hum_d_icon,hum_n_icon, latitude_icon , longitude_icon
    temp_max_icon = ImageTk.PhotoImage(Image.open("9045082_temperature_max_icon.png").resize((30,30),
                                                                                        Image.Resampling.LANCZOS))
    temp_min = ImageTk.PhotoImage(Image.open("9045188_temperature_min_icon.png").resize((30, 30),
                                                                                        Image.Resampling.LANCZOS))
    rain_icon = ImageTk.PhotoImage(Image.open("9254138_rain_rainy_heavy_downpour_draughty_icon.png"
                                              ).resize((30,30), Image.Resampling.LANCZOS))
    hum_d_icon = ImageTk.PhotoImage(Image.open("humidity.png"
                                              ).resize((30, 30), Image.Resampling.LANCZOS))
    hum_n_icon = ImageTk.PhotoImage(Image.open("humidity.png"
                                               ).resize((30, 30), Image.Resampling.LANCZOS))
    latitude_icon = ImageTk.PhotoImage(Image.open("9081704_world_latitude_icon.png"
                                              ).resize((30, 30), Image.Resampling.LANCZOS))
    longitude_icon = ImageTk.PhotoImage(Image.open("9081634_world_longitude_icon.png"
                                              ).resize((30, 30), Image.Resampling.LANCZOS))

    # bg setup
    bg_image = Image.open('pexels-bruce-wallace-48492-175854.jpg').resize((1000, 600), Image.Resampling.LANCZOS)
    bg_pic = ImageTk.PhotoImage(bg_image)
    root.bg_pic = bg_pic  # Keep a reference to avoid garbage collection

    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.create_image(0, 0, image=bg_pic, anchor="nw")
    canvas.pack(fill="both", expand=True)

    # Input frame (for city and month)
    input_frame = tk.Frame(canvas, bg="#00aaff")
    input_frame.place(relx=0.5, rely=0.1, anchor="n")

    # Output frame(weather data)
    output_frame = tk.Frame(canvas, bg="#BAFBAA", relief="sunken",border=0) #relief is a border style option
    # widget appear pressed down
    output_frame.place(relx=0.5, rely=0.3, anchor="n", relwidth=0.4, relheight=0.6)

    # Cities dropdown
    cities = ["Jaffna", "Mullaitivu", "Mannar", "Vavuniya", "Trincomalee", "Anuradhapura", "Puttalam",
              "Batticaloa", "Kurunegala", "Katugastota", "Katunayaka", "Colombo", "Nuwara Eliya", "Badulla",
              "Ratnapura", "Galle", "Hambantota", "Pottuvil", "Monaragala", "Polonnaruwa", "Bandarawela"]

    tk.Label(input_frame, text="Select City:", bg="#00aaff", fg="white",
             font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    city_var = tk.StringVar()
    city_var.set(cities[0])
    ttk.Combobox(input_frame, textvariable=city_var, values=cities,
                 font=("Arial", 12)).grid(row=0, column=1, padx=10, pady=5)

    # Months dropdown
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    tk.Label(input_frame, text="Select Month:", bg="#00aaff", fg="white",
             font=("Arial", 14)).grid(row=0, column=2, padx=10, pady=5)
    month_var = tk.StringVar()
    month_var.set(months[0])
    ttk.Combobox(input_frame, textvariable=month_var, values=months,
                 font=("Arial", 12)).grid(row=0, column=3, padx=10, pady=5)

    # Buttons
    tk.Button(input_frame, text="Search", bg="#ff9b83", fg="black",border=0,
              font=("Arial", 15), command=search).grid(row=1, column=1, pady=10)
    tk.Button(input_frame, text="Logout", bg="#ff9b83", fg="black", border=0,
              font=("Arial", 15), command=logout).grid(row=1, column=3, padx=5, pady=10)

    root.mainloop()
