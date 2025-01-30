import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database Connection
conn = mysql.connector.connect(host='localhost', user='root', password='vivek24', database='bus_booking')
cursor = conn.cursor()

# User Registration Function
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()
    phone = entry_phone.get()
    
    cursor.execute("INSERT INTO users (username, password, email, phone) VALUES (%s, %s, %s, %s)", (username, password, email, phone))
    conn.commit()
    messagebox.showinfo("Success", "User Registered Successfully")

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Success", "Login Successful")
        user_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# User Dashboard
def user_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("User Dashboard")
    tk.Label(dashboard, text="Source").pack()
    src_entry = tk.Entry(dashboard)
    src_entry.pack()
    
    tk.Label(dashboard, text="Destination").pack()
    dest_entry = tk.Entry(dashboard)
    dest_entry.pack()
    
    tk.Button(dashboard, text="Search Bus", command=lambda: search_bus(src_entry.get(), dest_entry.get())).pack()

# Search Bus Function
def search_bus(source, destination):
    cursor.execute("SELECT * FROM buses WHERE source=%s AND destination=%s", (source, destination))
    buses = cursor.fetchall()
    
    result_window = tk.Toplevel(root)
    result_window.title("Available Buses")
    
    for bus in buses:
        bus_info = f"Bus ID: {bus[0]}, Name: {bus[1]}, Seats: {bus[4]}, Fare: {bus[5]}"
        tk.Button(result_window, text=bus_info, command=lambda b=bus: book_bus(b)).pack()

# Booking Function
def book_bus(bus):
    bus_id = bus[0]
    available_seats = bus[4]
    
    if available_seats > 0:
        cursor.execute("UPDATE buses SET total_seats = total_seats - 1 WHERE bus_id = %s", (bus_id,))
        conn.commit()
        messagebox.showinfo("Success", "Bus Booked Successfully")
    else:
        messagebox.showerror("Error", "No Seats Available")

# Admin Login
def admin_login():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Dashboard")
    
    tk.Button(admin_window, text="Add Bus", command=add_bus).pack()
    tk.Button(admin_window, text="Delete Bus", command=delete_bus).pack()

# Add Bus Function
def add_bus():
    add_window = tk.Toplevel(root)
    tk.Label(add_window, text="Bus Name").pack()
    bus_name_entry = tk.Entry(add_window)
    bus_name_entry.pack()
    
    tk.Label(add_window, text="Source").pack()
    src_entry = tk.Entry(add_window)
    src_entry.pack()
    
    tk.Label(add_window, text="Destination").pack()
    dest_entry = tk.Entry(add_window)
    dest_entry.pack()
    
    tk.Label(add_window, text="Total Seats").pack()
    seats_entry = tk.Entry(add_window)
    seats_entry.pack()
    
    tk.Label(add_window, text="Fare Per Seat").pack()
    fare_entry = tk.Entry(add_window)
    fare_entry.pack()
    
    tk.Button(add_window, text="Add", command=lambda: insert_bus(bus_name_entry.get(), src_entry.get(), dest_entry.get(), seats_entry.get(), fare_entry.get())).pack()

def insert_bus(name, src, dest, seats, fare):
    cursor.execute("INSERT INTO buses (bus_name, source, destination, total_seats, fare_per_seat) VALUES (%s, %s, %s, %s, %s)", (name, src, dest, seats, fare))
    conn.commit()
    messagebox.showinfo("Success", "Bus Added Successfully")

# Delete Bus Function
def delete_bus():
    delete_window = tk.Toplevel(root)
    tk.Label(delete_window, text="Enter Bus ID").pack()
    bus_id_entry = tk.Entry(delete_window)
    bus_id_entry.pack()
    tk.Button(delete_window, text="Delete", command=lambda: remove_bus(bus_id_entry.get())).pack()

def remove_bus(bus_id):
    cursor.execute("DELETE FROM buses WHERE bus_id=%s", (bus_id,))
    conn.commit()
    messagebox.showinfo("Success", "Bus Deleted Successfully")

# GUI Setup
root = tk.Tk()
root.title("Bus Booking System")

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Phone").pack()
entry_phone = tk.Entry(root)
entry_phone.pack()

tk.Button(root, text="Register", command=register_user).pack()
tk.Button(root, text="Login", command=login_user).pack()
tk.Button(root, text="Admin Login", command=admin_login).pack()

root.mainloop()

# Close connection
conn.close()
