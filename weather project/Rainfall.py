import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_table():
    try:
        db = sqlite3.connect('weathermonitoring.db')
        cursor = db.cursor() # Create cursor object
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rainfall (
                Station_ID TEXT NOT NULL,
                City_name TEXT NOT NULL,
                Month TEXT NOT NULL,
                Year INTEGER NOT NULL,
                Rainfall_mm FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                latitude FLOAT NOT NULL,
                PRIMARY KEY (City_name, Month)
            );
        """
        )
        db.commit()
    except Exception as e:
        print("Error creating table:", e)
    finally:
        db.close() #close db

def show_rainfall(parent_window):
    parent_window.withdraw() # parent is the admin dashboard

    def connect_to_db():
        return sqlite3.connect('weathermonitoring.db')

    # display data
    def fetch_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM rainfall")
            rows = cursor.fetchall() # fetch all rows
            update_output(rows) #update tree view

        except Exception as e:
            print("Error fetching data:", e)
        finally:
            db.close()

    def update_output(rows):
        # refreshment of tree
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row) # insert new data row by row

        for col_index, col_name in enumerate(tree["columns"]):
            max_width = max(len(str(row[col_index])) for row in rows) if rows else 10
            tree.column(col_name, width=max_width * 10)

    def clear():
        ID.set('')
        Station.set('')
        Year.set('')
        Month.set('')
        Rainfall.set('')
        longitude.set('')
        latitude.set('')

    def go_back():
        window.destroy()
        parent_window.deiconify() # show again admin dashboard

    # insert data to db
    def submit_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "SELECT * FROM rainfall WHERE City_name=? AND Month=?",
                (Station.get(), Month.get())
            )
            if cursor.fetchone():
                tk.messagebox.showinfo("Info", "Record already exists.")
            else:
                cursor.execute(
                    """INSERT INTO rainfall (Station_ID, City_name, Month, Year, Rainfall_mm, longitude, latitude)
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        ID.get(),
                        Station.get(),
                        Month.get(),
                        Year.get(),
                        Rainfall.get(),
                        longitude.get(),
                        latitude.get()
                    )
                )
                db.commit()
                fetch_data()
                clear() #refresh and clear input fields
                messagebox.showinfo("Success", "Submitted data Successfully!")
        except Exception as e:
            print("Error submitting data:", e)
        finally:
            db.close()

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            row_data = tree.item(selected_item[0], "values")  # Use first selected item
            if row_data:  # Ensure row_data is not empty
                Station.set(row_data[1])
                Month.set(row_data[2])
                Rainfall.set(row_data[4])

    #updata db data
    def update_data():
        try:
            selected_item = tree.selection()

            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to update!")
                return

            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                """
                UPDATE rainfall SET Rainfall_mm=? WHERE City_name=? AND Month=?
                """,
                (
                    Rainfall.get(),
                    Station.get(),
                    Month.get()
                )
            )
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success", "Data updated Successfully!")
        except Exception as e:
            print("Error updating data:", e)
        finally:
            db.close()

    #delete data
    def delete_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM rainfall WHERE City_name=? AND Month=?",
                (Station.get(), Month.get())
            )
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success", "Record deleted successfully!")
        except Exception as e:
            print("Error deleting data:", e)
        finally:
            db.close()

    window = tk.Toplevel()
    window.title("Rainfall Data")
    window.geometry("1000x700")
    window.configure(bg="#8FA5FF")

    ID = tk.StringVar()
    Station = tk.StringVar()
    Year = tk.StringVar()
    Month = tk.StringVar()
    Rainfall = tk.StringVar()
    longitude = tk.StringVar()
    latitude = tk.StringVar()

    form_frame = tk.Frame(window, bg="#8FA5FF", padx=20, pady=50)
    form_frame.pack(side="top", fill="both", expand=True)

    output_frame = tk.Frame(window, bg="#ffffff", padx=10, pady=6, border=0)
    output_frame.pack(side="bottom", fill="both", expand=True)

    tk.Label(form_frame, text="Station_ID", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=ID, width=15,border=0 , font=["Arial", 12]
             ).grid(row=1, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="City name", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Station, width=25, border=0 ,font=["Arial", 12]
             ).grid(row=2, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Year", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Year, width=15,border=0 , font=["Arial", 12]
             ).grid(row=3, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Month", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=3, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Month, width=15,border=0 , font=["Arial", 12]
             ).grid(row=3, column=3, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Rainfall(mm)", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Rainfall, width=15, border=0 ,font=["Arial", 12]
             ).grid(row=4, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Longitude", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=longitude, width=15, border=0 , font=["Arial", 12]
             ).grid(row=5, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Latitude", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=5, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=latitude, width=15, border=0 ,font=["Arial", 12]
             ).grid(row=5, column=3, sticky="w", padx=10, pady=5)

    button_frame = tk.Frame(form_frame, bg="#8FA5FF")
    button_frame.grid(row=8, column=0, columnspan=2, pady=50)

    tk.Button(button_frame, text="Submit", bg="#ff9b83", border=0 ,
              font=["Arial", 16, "bold"], width=8, command=submit_data).grid(row=0, column=0, padx=15, pady=10)
    tk.Button(button_frame, text="Update", bg="#ff9b83", border=0 ,
              font=["Arial", 16, "bold"], width=8, command=update_data).grid(row=0, column=1, padx=15, pady=10)
    tk.Button(button_frame, text="Delete", bg="#ff9b83", border=0 ,
              font=["Arial", 16, "bold"], width=8, command=delete_data).grid(row=0, column=2, padx=15, pady=10)
    tk.Button(button_frame, text="Clear", bg="#ff9b83", border=0 ,
              font=["Arial", 16, "bold"], width=8, command=clear).grid(row=0, column=3, padx=15, pady=10)
    tk.Button(button_frame, text="Exit", bg="#ff9b83",border=0 ,
              font=["Arial", 16, "bold"], width=8, command=go_back).grid(row=0, column=4, padx=15, pady=10)

    tk.Label(output_frame, text="Output", font=("Arial", 16), bg="#ffffff").pack(anchor="w", pady=(0, 10))

    #tree view
    tree = ttk.Treeview(output_frame, height=25, columns=("Station_ID", "City_name", "Month", "Year",
                                               "Rainfall_mm", "longitude", "latitude"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    fetch_data()
    window.mainloop()

if __name__ == '__main__':
    create_table()
