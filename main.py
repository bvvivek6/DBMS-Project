import mysql.connector
from tkinter import *
import tkinter as tk
from tkinter import messagebox


# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vivek24",
    database="BusTicketManagement"
)
cursor = db.cursor()


current_user_id = None

def view_buses():
    def search_buses():
        source = entry_source.get()
        destination = entry_destination.get()

        cursor.execute("SELECT * FROM Buses WHERE source = %s AND destination = %s", (source, destination))
        buses = cursor.fetchall()

        if not buses:
            messagebox.showinfo("Info", "No buses available for this route.")
        else:
            for bus in buses:
                listbox_buses.insert(END, f"Bus ID: {bus[0]}, Name: {bus[1]}, Seats: {bus[4]}, Fare: {bus[5]}")

    def select_bus():
        selected = listbox_buses.get(ACTIVE)
        if not selected:
            messagebox.showerror("Error", "Please select a bus!")
        else:
            bus_id = int(selected.split(",")[0].split(":")[1].strip())
            book_seats(bus_id)

    # Bus search window
    bus_window = Toplevel(root)
    bus_window.title("View Buses")
    bus_window.geometry("500x500")

    Label(bus_window, text="Source", font=("Arial", 12)).pack(pady=5)
    entry_source = Entry(bus_window, font=("Arial", 12), width=25)
    entry_source.pack(pady=5)

    Label(bus_window, text="Destination", font=("Arial", 12)).pack(pady=5)
    entry_destination = Entry(bus_window, font=("Arial", 12), width=25)
    entry_destination.pack(pady=5)

    Button(
        bus_window,
        text="Search Buses",
        command=search_buses,
        font=("Arial", 12),
        bg="#28a745",
        fg="white",
        activebackground="#218838",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=10)

    # Initialize listbox_buses here
    listbox_buses = Listbox(bus_window, font=("Arial", 12), width=40, height=10)
    listbox_buses.pack(fill=BOTH, expand=True)

    Button(
        bus_window,
        text="Select Bus",
        command=select_bus,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=10)

    
def register_user():
    def submit_registration():
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()
        phone = entry_phone.get()

        if not username or not password or not email or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Insert user into the database
            cursor.execute(
                "INSERT INTO Users (username, password, email, phone) VALUES (%s, %s, %s, %s)",
                (username, password, email, phone)
            )
            db.commit()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            register_window.destroy()  # Close the registration window
            login_user()  # Redirect to login screen
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

    # Registration window
    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("500x500")

    Label(register_window, text="Register", font=("Arial", 16, "bold")).pack(pady=20)

    Label(register_window, text="Username", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(register_window, font=("Arial", 12), width=25)
    entry_username.pack(pady=5)

    Label(register_window, text="Password", font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(register_window, font=("Arial", 12), width=25, show="*")
    entry_password.pack(pady=5)

    Label(register_window, text="Email", font=("Arial", 12)).pack(pady=5)
    entry_email = Entry(register_window, font=("Arial", 12), width=25)
    entry_email.pack(pady=5)

    Label(register_window, text="Phone", font=("Arial", 12)).pack(pady=5)
    entry_phone = Entry(register_window, font=("Arial", 12), width=25)
    entry_phone.pack(pady=5)

    Button(
        register_window,
        text="Register",
        command=submit_registration,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=20)


def login_user():
    def submit_login():
        username = entry_username.get()
        password = entry_password.get()

        cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            global current_user_id
            current_user_id = user[0]
            messagebox.showinfo("Success", "Login successful!")
            login_window.destroy()  # Close login window
            main_menu()  # Open main menu after login
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    # Login window
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("500x500")

    Label(login_window, text="Login", font=("Arial", 16, "bold")).pack(pady=20)

    Label(login_window, text="Username", font=("Arial", 12)).pack(pady=5)
    entry_username = Entry(login_window, font=("Arial", 12), width=25)
    entry_username.pack(pady=5)

    Label(login_window, text="Password", font=("Arial", 12)).pack(pady=5)
    entry_password = Entry(login_window, font=("Arial", 12), width=25, show="*")
    entry_password.pack(pady=5)

    Button(
        login_window,
        text="Login",
        command=submit_login,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=20)
    
def select_bus():
    selected = listbox_buses.get(ACTIVE)
    if not selected:
        messagebox.showerror("Error", "Please select a bus!")
    else:
        bus_id = int(selected.split(",")[0].split(":")[1].strip())
        book_seats(bus_id)
def get_fare(bus_id):
    cursor.execute("SELECT fare FROM Buses WHERE bus_id = %s", (bus_id,))
    fare = cursor.fetchone()
    if fare:
        return fare[0]
    return 0  # Default fare if not found

def book_seats(bus_id):
    # Fetch seat data from database
    cursor.execute("SELECT seat_number, is_booked FROM Seats WHERE bus_id = %s", (bus_id,))
    seat_data = cursor.fetchall()

    # Get the total number of seats
    total_seats = len(seat_data)
    
    # Assuming a fixed number of columns (e.g., 4), calculate rows
    cols = 4
    rows = total_seats // cols
    if total_seats % cols != 0:
        rows += 1  
    
    # Initialize seat matrix and availability dictionary
    seat_matrix = [[None for _ in range(cols)] for _ in range(rows)]
    seat_availability = {} 

    
    for seat in seat_data:
        seat_number, is_booked = seat
        row = (seat_number - 1) // cols  
        col = (seat_number - 1) % cols   
        
       
        seat_matrix[row][col] = seat_number
        seat_availability[seat_number] = is_booked
    
    # Create booking window
    booking_window = tk.Toplevel(root)
    booking_window.title("Book Seats")
    booking_window.geometry("500x500")
    
    # Function to handle seat selection
    def select_seat(seat_number):
        if seat_availability[seat_number]:
            messagebox.showerror("Error", f"Seat {seat_number} is already booked!")
        else:
            # Book the seat and update database
            cursor.execute("UPDATE Seats SET is_booked = TRUE WHERE bus_id = %s AND seat_number = %s",
                           (bus_id, seat_number))
            db.commit()
            messagebox.showinfo("Success", f"Seat {seat_number} has been booked successfully!")
            # Update seat button color
            seat_buttons[seat_number].config(bg="red")
            seat_availability[seat_number] = True

    # Create a grid of buttons to represent the seat matrix
    seat_buttons = {}
    for i in range(rows):
        for j in range(cols):
            seat_number = seat_matrix[i][j]
            if seat_number:
                if seat_availability[seat_number]:
                    color = "red"  # Booked seat color
                else:
                    color = "green"  # Available seat color
                button = tk.Button(
                    booking_window,
                    text=f"Seat {seat_number}",
                    width=10,
                    height=2,
                    bg=color,
                    command=lambda seat_number=seat_number: select_seat(seat_number)
                )
                button.grid(row=i, column=j, padx=5, pady=5)
                seat_buttons[seat_number] = button

    # Add a button to confirm booking and show total fare
    def confirm_booking():
        booked_seats = [seat for seat, booked in seat_availability.items() if booked]
        total_fare = len(booked_seats) * get_fare(bus_id)  # Calculate total fare based on number of seats
        messagebox.showinfo("Booking Confirmed", f"Total Fare: {total_fare}")
        booking_window.destroy()

    confirm_button = tk.Button(
        booking_window,
        text="Confirm Booking",
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        activeforeground="white",
        command=confirm_booking
    )
    confirm_button.grid(row=rows, column=0, columnspan=cols, pady=20)



def main_menu():
    def view_buses():
        def search_buses():
            source = entry_source.get()
            destination = entry_destination.get()

            cursor.execute("SELECT * FROM Buses WHERE source = %s AND destination = %s", (source, destination))
            buses = cursor.fetchall()

            if not buses:
                messagebox.showinfo("Info", "No buses available for this route.")
            else:
                for bus in buses:
                    listbox_buses.insert(END, f"Bus ID: {bus[0]}, Name: {bus[1]}, Seats: {bus[4]}, Fare: {bus[5]}")

        def select_bus():
            selected = listbox_buses.get(ACTIVE)
            if not selected:
                messagebox.showerror("Error", "Please select a bus!")
            else:
                bus_id = int(selected.split(",")[0].split(":")[1].strip())
                book_seats(bus_id)

        # Bus search window
        bus_window = Toplevel(root)
        bus_window.title("View Buses")
        bus_window.geometry("500x500")

        Label(bus_window, text="Source", font=("Arial", 12)).pack(pady=5)
        entry_source = Entry(bus_window, font=("Arial", 12), width=25)
        entry_source.pack(pady=5)

        Label(bus_window, text="Destination", font=("Arial", 12)).pack(pady=5)
        entry_destination = Entry(bus_window, font=("Arial", 12), width=25)
        entry_destination.pack(pady=5)

        Button(
            bus_window,
            text="Search Buses",
            command=search_buses,
            font=("Arial", 12),
            bg="#28a745",
            fg="white",
            activebackground="#218838",
            activeforeground="white",
            width=15,
            height=2
        ).pack(pady=10)

        listbox_buses = Listbox(bus_window, font=("Arial", 12), width=40, height=10)
        listbox_buses.pack(fill=BOTH, expand=True)

        Button(
            bus_window,
            text="Select Bus",
            command=select_bus,
            font=("Arial", 12),
            bg="#007BFF",
            fg="white",
            activebackground="#0056b3",
            activeforeground="white",
            width=15,
            height=2
        ).pack(pady=10)

    # Main Menu window
    main_menu_window = Toplevel(root)
    main_menu_window.title("Main Menu")
    main_menu_window.geometry("500x500")

    Label(main_menu_window, text="Welcome!", font=("Arial", 16, "bold")).pack(pady=20)

    Button(
        main_menu_window,
        text="View Buses",
        command=view_buses,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        activebackground="#0056b3",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=20)

    Button(
        main_menu_window,
        text="Logout",
        command=main_menu_window.destroy,
        font=("Arial", 12),
        bg="#dc3545",
        fg="white",
        activebackground="#c82333",
        activeforeground="white",
        width=15,
        height=2
    ).pack(pady=10)

def logout(menu_window):
    global current_user_id
    current_user_id = None  # Clear the current user ID
    menu_window.destroy()
    messagebox.showinfo("Logout", "You have successfully logged out.")


# Main Window
root = Tk()
root.title("Bus Ticket Management System")
root.geometry("500x500")

Label(root, text="Bus Ticket Management System", font=("Arial", 16, "bold")).pack(pady=20)

Button(root, text="Register", command=register_user,
       font=("Arial", 12, "bold"), bg="#007BFF", fg="white", activebackground="#0056b3",
       activeforeground="white", width=15, height=2).pack(pady=10)

Button(root, text="Login", command=login_user,
       font=("Arial", 12, "bold"), bg="#28a745", fg="white", activebackground="#218838",
       activeforeground="white", width=15, height=2).pack(pady=10)

Button(root, text="Exit", command=root.destroy,
       font=("Arial", 12, "bold"), bg="#dc3545", fg="white", activebackground="#c82333",
       activeforeground="white", width=15, height=2).pack(pady=10)

root.mainloop()
