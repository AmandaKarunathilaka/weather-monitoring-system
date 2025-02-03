import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def create_table():
    try:
        db = sqlite3.connect('weathermonitoring.db')
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS humidity (
                Station_ID TEXT NOT NULL,
                City_name TEXT NOT NULL,
                Month TEXT NOT NULL,
                Year INTEGER NOT NULL,
                Humidity_day FLOAT ,
                Humidity_night FLOAT,
                longitude FLOAT NOT NULL,
                latitude FLOAT NOT NULL,
                PRIMARY KEY (City_name , Month)
            );
        """)
    except Exception as e:
        print("Error creating table:", e)
    finally:
        db.close()

def connect_to_db():
    return sqlite3.connect('weathermonitoring.db')

def show_humidity(parent_window): # parent is admin dashboard
    parent_window.withdraw()

    # fetch data with tree
    def fetch_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM humidity")
            rows = cursor.fetchall()
            update_output(rows)
        except Exception as e:
            print("Error fetching data:", e)
        finally:
            db.close()

    # Update tree view with fetched data
    def update_output(rows):
        # refresh
        for item in tree.get_children():
            tree.delete(item)
        # if there's no data in rows
        if not rows:
            print("No data to display")
            return
        for row in rows:
            tree.insert("", "end", values=row)

        for col_index, col_name in enumerate(tree["columns"]):
            max_width = max((len(str(row[col_index])) for row in rows), default=10)
            tree.column(col_name, width=max_width * 10)  # Multiply by 10 for better spacing

    # Clear form fields
    def clear():
        ID.set('')
        City.set('')
        Year.set('')
        Month.set('')
        Humidity_day.set('')
        Humidity_night.set(''),
        longitude.set('')
        latitude.set('')

    def go_back():
        root.destroy()
        parent_window.deiconify()

    #submit data to the db
    def submit_data():
        try:
            db = connect_to_db() # connect to db
            cursor = db.cursor()
            cursor.execute("""INSERT INTO humidity (Station_ID, City_name, Month, Year, Humidity_day, 
            Humidity_night, longitude, latitude)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, # ? is used to prevent from sql injection
                (
                    ID.get(),
                    City.get(),
                    Month.get(),
                    Year.get(),
                    Humidity_day.get(),
                    Humidity_night.get(),
                    longitude.get(),
                    latitude.get()
                )
            )
            db.commit()
            fetch_data() # refresh data
            clear()
            messagebox.showinfo("Success", "Submitted data successfully!")
        except Exception as e:
            print("Error submitting data:", e)
        finally:
            db.close()
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            row_data = tree.item(selected_item[0], "values")  # Use first selected item
            if row_data:  # Ensure row_data is not empty
                City.set(row_data[1])
                Month.set(row_data[2])
                Humidity_day.set(row_data[4])
                Humidity_night.set(row_data[5])

    # Update data in db
    def update_data():
        try:
            selected_item = tree.selection()

            if not selected_item:
                messagebox.showwarning("Warning", "Please select a record to update!")
                return

            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE humidity "
                "SET Humidity_day=?,  Humidity_night=?"
                "WHERE City_name=? AND Month=?",
                (
                    Humidity_day.get(),
                    Humidity_night.get(),
                    City.get(),
                    Month.get()
                ))
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success", "Record updated successfully!")
        except Exception as e:
            print("Error updating data:", e)
        finally:
            db.close()

    #delete data in db
    def delete_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "DELETE FROM humidity WHERE City_name = ? AND Month = ?", (City.get(), Month.get())
            )
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success", "Record deleted successfully!")
        except Exception as e:
            print("Error deleting data:", e)
        finally:
            db.close()

    root = tk.Toplevel()
    root.title("Humidity data")
    root.geometry("1000x700")
    root.configure(bg="#8FA5FF")

    # data form frame
    data_form = tk.Frame(root, bg="#8FA5FF", padx=20, pady=20)
    data_form.pack(side="top", fill="both", expand=True)

    #database form
    output_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=6, border=0)
    output_frame.pack(side="bottom", fill="both", expand=False)

    tk.Label(data_form, text="Station_ID", bg="#8FA5FF",
                      font=["Arial", 14]).place(x=50, y=48)
    ID = tk.StringVar()
    tk.Entry(data_form,textvariable=ID, border=0 ,font=["Arial", 12]).place(x=250, y=50)

    tk.Label(data_form, text="City name",bg="#8FA5FF", font=["Arial", 14]
             ).place(x=50, y=100)
    City = tk.StringVar()
    tk.Entry(data_form, textvariable=City, border=0 ,font=["Arial", 12]).place(x=250, y=100)

    tk.Label(data_form, text="Year", bg="#8FA5FF", font=["Arial", 14]
             ).place(x=50, y=150)
    Year =tk.StringVar()
    tk.Entry(data_form, textvariable=Year, border=0 ,font=["Arial", 12], width=8).place(x=250 , y=150)

    tk.Label(data_form, text="Month", bg="#8FA5FF", font=["Arial", 14]
             ).place(x=480, y=150)
    Month = tk.StringVar()
    tk.Entry(data_form, textvariable=Month, border=0 ,font=["Arial", 12], width=8).place(x=660, y=150)

    tk.Label(data_form, text="Humidity_day",bg="#8FA5FF", font=["Arial", 14]
             ).place(x=50, y=200)
    Humidity_day =tk.StringVar()
    tk.Entry(data_form, textvariable=Humidity_day, border=0 ,font=["Arial", 12]).place(x=250, y=200)

    tk.Label(data_form, text="Humidity_night", bg="#8FA5FF", font=["Arial", 14]).place(x=480, y=200)
    Humidity_night= tk.StringVar()
    tk.Entry(data_form, textvariable=Humidity_night, border=0 ,font=["Arial", 12]).place(x=660, y=200)

    tk.Label(data_form, text="Longitude", bg="#8FA5FF", font=["Arial", 14]).place(x=50, y=250)
    longitude = tk.StringVar()
    tk.Entry(data_form, textvariable=longitude, font=["Arial", 12],border=0 , width=8).place(x=250, y=250)

    tk.Label(data_form, text="Latitude", bg="#8FA5FF", font=["Arial", 14]).place(x=480, y=250)
    latitude = tk.StringVar()
    tk.Entry(data_form, textvariable=latitude, font=["Arial", 12], border=0 ,width=8).place(x=660, y=250)

    tk.Button(data_form, text="Submit", bg="#ff9b83", font=["Arial", 16, 'bold'], border=0 ,
              width=8, height=1, command=submit_data).place(x=70, y=310)
    tk.Button(data_form,text="Update", bg="#ff9b83", font=["Arial", 16, 'bold'], border=0 ,
              width=8, height=1, command=update_data).place(x=210, y=310)
    tk.Button(data_form,text="Delete", bg="#ff9b83", font=["Arial", 16, 'bold'], border=0 ,
              width=8, height=1, command=delete_data).place(x=350, y=310)
    tk.Button(data_form, text="Clear", bg="#ff9b83", font=["Arial", 16, 'bold'],border=0 ,
              width=8, height=1, command=clear).place(x=490, y=310)
    tk.Button(data_form,text="Exit", bg="#ff9b83", font=["Arial", 16, 'bold'],border=0 ,
              width=8, height=1, command=go_back).place(x=630,y=310)

    #output
    tk.Label(output_frame, text="Output", font=("Arial", 16), bg="#ffffff").pack(anchor="w", pady=(0,10))

    # tree view
    tree = ttk.Treeview(output_frame, columns=(
        "Station_ID", "City_name", "Month", "Year", "Humidity_Day", "Humidity_Night", "longitude",
        "latitude"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    fetch_data() # retrieve all data
    root.mainloop()

if __name__ == '__main__':
    create_table()