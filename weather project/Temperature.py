import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Function to create the temperature table
def create_table():
    try:
        db = sqlite3.connect('weathermonitoring.db')
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temperature (
                Station_ID INTEGER NOT NULL,
                City_name TEXT NOT NULL,
                Month TEXT NOT NULL,
                Year INTEGER NOT NULL,
                Temp_Min FLOAT NOT NULL,
                Temp_Max FLOAT NOT NULL,
                longitude FLOAT NOT NULL,
                latitude FLOAT NOT NULL, 
                PRIMARY KEY (City_name, Month)
            );
        """)
        db.commit() # save changes permanently
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        db.close()

def show_temp(parent_window): #parent window = admin dashboard
    # Connect to the database
    def connect_to_db():
        return sqlite3.connect('weathermonitoring.db')

    # Fetch data from the database
    def fetch_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM temperature")
            rows = cursor.fetchall()
            update_output(rows)
        except Exception as e:
            print("Error fetching data:", e)
        finally:
            db.close()

    # Update tree view with fetched data
    def update_output(rows):
        #refresh with latest data
        for item in tree.get_children():
            tree.delete(item) # clear existing data in tree
        for row in rows:
            tree.insert("", "end", values=row) # insert new row

        # Adjust column width based on length of content
        for col_index, col_name in enumerate(tree["columns"]): # enumerate is assign an index to each col.
            max_width = max(len(str(row[col_index])) for row in rows) if rows else 10 # default width is 10
            tree.column(col_name, width=max_width * 10)

    # Clear form fields and reset fields
    def clear():
        IDValue.set('')
        Station_NameValue.set('')
        YearValue.set('')
        Month_of_year.set('')
        Temperature_MinValue.set('')
        Temperature_MaxValue.set('')
        longitude_Value.set('')
        latitude_Value.set('')

    # Go back to the parent window
    def go_back():
        root.destroy()
        parent_window.deiconify() # again show the data collect

    # Submit data to the database
    def submit_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO temperature (Station_ID, City_name, Month, Year, Temp_Min, Temp_Max,"
                " longitude, latitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    IDValue.get(),
                    Station_NameValue.get(),
                    Month_of_year.get(),
                    YearValue.get(),
                    Temperature_MinValue.get(),
                    Temperature_MaxValue.get(),
                    longitude_Value.get(),
                    latitude_Value.get()
                )
            )
            db.commit()
            fetch_data() # update display
            clear() # clear after insertion
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

                Station_NameValue.set(row_data[1])
                Month_of_year.set(row_data[2])

                Temperature_MinValue.set(row_data[4])
                Temperature_MaxValue.set(row_data[5])


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
                UPDATE temperature 
                SET Temp_Min = ?, Temp_Max = ? 
                WHERE City_name = ? AND Month = ?
                """,
                (
                    Temperature_MinValue.get(),
                    Temperature_MaxValue.get(),
                    Station_NameValue.get(),
                    Month_of_year.get(),
                )
            )
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success","Data updated successfully!")
        except Exception as e:
            print("Error updating data:", e)
        finally:
            db.close()

    # Delete data from the database
    def delete_data():
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM temperature WHERE City_name=? AND Month=?",
                           (Station_NameValue.get(), Month_of_year.get())
            )
            db.commit()
            fetch_data()
            clear()
            messagebox.showinfo("Success", "Record deleted successfully!")
        except Exception as e:
            print("Error deleting data:", e)
        finally:
            db.close()

    # Create the form window
    root = tk.Toplevel()
    root.title("Temperature Data Entry")
    root.geometry("1000x700")
    root.configure(bg="#8FA5FF")

    # Variables
    IDValue = tk.StringVar()
    Station_NameValue = tk.StringVar()
    YearValue = tk.StringVar()
    Month_of_year = tk.StringVar()
    Temperature_MinValue = tk.StringVar()
    Temperature_MaxValue = tk.StringVar()
    longitude_Value = tk.StringVar()
    latitude_Value = tk.StringVar()

    # Main Frame
    form_frame = tk.Frame(root, bg="#8FA5FF", padx=20, pady=50)
    form_frame.pack(side="top", fill="both", expand=True)

    output_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=6, border=0)
    output_frame.pack(side="bottom", fill="both", expand=False)

    # Labels and Entries
    tk.Label(form_frame, text="Station_ID", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=IDValue, width=15, border=0, font=("Arial", 12)
             ).grid(row=1, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="City Name", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Station_NameValue, width=25, border=0, font=("Arial", 12)
             ).grid(row=2, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Year", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=YearValue, width=15, border=0, font=("Arial", 12)
             ).grid(row=3, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Month", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=3, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Month_of_year, width=15, border=0, font=("Arial", 12)
             ).grid(row=3, column=3, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Temperature (Min)", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Temperature_MinValue, width=15, border=0, font=("Arial", 12)
             ).grid(row=4, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Temperature (Max)", font=("Arial", 14), bg="#8FA5FF"
             ).grid(row=4, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, textvariable=Temperature_MaxValue, width=15, border=0, font=("Arial", 12)
             ).grid(row=4, column=3, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Longitude", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, font=["Arial", 12], width=8, border=0,textvariable=longitude_Value
             ).grid(row=5, column=1, sticky="w", padx=10, pady=5)

    tk.Label(form_frame, text="Latitude", bg="#8FA5FF", font=["Arial", 14]
             ).grid(row=5, column=2, sticky="w", padx=10, pady=5)
    tk.Entry(form_frame, font=["Arial", 12],  border=0 ,textvariable=latitude_Value, width=8
             ).grid(row=5, column=3, sticky="w", padx=10, pady=5)

    # Buttons
    button_frame = tk.Frame(form_frame, bg="#8FA5FF")
    button_frame.grid(row=7, column=0, columnspan=4, pady=50)

    tk.Button(button_frame, text="Submit", bg="#ff9b83",border=0,
              font=("Arial", 16, "bold"), width=10, command=submit_data).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Update", bg="#ff9b83", border=0 ,
              font=("Arial", 16, "bold"), width=10, command=update_data).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Delete", bg="#ff9b83", border=0 ,
              font=("Arial", 16, "bold"), width=10, command=delete_data).grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Clear", bg="#ff9b83", border=0 ,
              font=("Arial", 16, "bold"), width=10, command=clear).grid(row=0, column=3, padx=10)
    tk.Button(button_frame, text="Exit", bg="#ff9b83", border=0 ,
              font=("Arial", 16, "bold"), width=10, command=go_back).grid(row=0, column=4, padx=10)

    # Output Frame Content
    tk.Label(output_frame, text="Output", font=("Arial", 16), bg="#ffffff").pack(anchor="w", pady=(0, 10))

    # display db records
    tree = ttk.Treeview(output_frame, columns=("Station_ID", "City_name", "Month", "Year",
                                               "Temp_Min", "Temp_Max", "longitude", "latitude"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Fetch and display data
    fetch_data()
    root.mainloop()

if __name__ == '__main__':
    create_table()
