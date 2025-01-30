import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vivek24",
    database="BusTicketManagement"
)
cursor = db.cursor()


class BusTicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Ticket Management System")
        self.root.geometry("600x500")
        
        # Set a global theme for the app
        self.bg_color = "#f4f4f4"
        self.accent_color = "#4CAF50"
        self.text_color = "#333"
        
       # Initialize the current frame to None
        self.current_frame = None

        # Load the main menu
        self.load_main_menu()

        # Set the background color for the root window
        self.root.configure(bg=self.bg_color)

    def load_main_menu(self):
        self.switch_frame(MainMenuFrame)

    # Function to switch frames
    def switch_frame(self, frame_class, *args):
        if self.current_frame:
            self.current_frame.pack_forget()
        frame = frame_class(self, *args)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    # Login/Register Frame
    def load_login(self):
        self.switch_frame(LoginFrame)

    def load_register(self):
        self.switch_frame(RegisterFrame)

    # Source-Destination Selection Frame
    def load_source_destination(self):
        self.switch_frame(SourceDestinationFrame)

    # Bus Selection Frame
    def load_bus_selection(self, source, destination):
        self.switch_frame(BusSelectionFrame, source, destination)

    # Seat Matrix Frame
    def load_seat_matrix(self, bus_id, source, destination):
        self.switch_frame(SeatMatrixFrame, bus_id, source, destination)

    # Booking Details Frame
    def load_booking_details(self, seat_id, bus_id, source, destination):
        self.switch_frame(BookingDetailsFrame, seat_id, bus_id, source, destination)

    # Exit Application
    def exit_app(self):
        self.root.quit()

class AdminPanel(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Admin Panel - Manage Buses", font=("Arial", 18, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        tk.Button(self, text="View Buses", command=self.view_buses, bg="#4CAF50", fg="white", width=20).pack(pady=5)
        tk.Button(self, text="Add Bus", command=self.add_bus, bg="#2196F3", fg="white", width=20).pack(pady=5)
        tk.Button(self, text="Edit Bus", command=self.edit_bus, bg="#FFC107", fg="black", width=20).pack(pady=5)
        tk.Button(self, text="Delete Bus", command=self.delete_bus, bg="#F44336", fg="white", width=20).pack(pady=5)
        tk.Button(self, text="Back", command=self.app.load_main_menu, bg="gray", fg="white", width=20).pack(pady=10)

    def view_buses(self):
        cursor.execute("SELECT * FROM buses")
        buses = cursor.fetchall()
        bus_list = "\n".join([f"{bus[0]}: {bus[1]} ({bus[2]} to {bus[3]})" for bus in buses])
        messagebox.showinfo("Available Buses", bus_list if bus_list else "No buses available.")

    def add_bus(self):
        def save_bus():
            name = name_var.get()
            source = source_var.get()
            destination = destination_var.get()
            if name and source and destination:
                cursor.execute("INSERT INTO buses (bus_name, source, destination) VALUES (%s, %s, %s)", (name, source, destination))
                db.commit()
                messagebox.showinfo("Success", "Bus added successfully!")
                add_window.destroy()
            else:
                messagebox.showerror("Error", "All fields are required!")

        add_window = tk.Toplevel(self)
        add_window.title("Add Bus")
        tk.Label(add_window, text="Bus Name:").pack()
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var).pack()
        tk.Label(add_window, text="Source:").pack()
        source_var = tk.StringVar()
        tk.Entry(add_window, textvariable=source_var).pack()
        tk.Label(add_window, text="Destination:").pack()
        destination_var = tk.StringVar()
        tk.Entry(add_window, textvariable=destination_var).pack()
        tk.Button(add_window, text="Save", command=save_bus).pack()

    def edit_bus(self):
        def update_bus():
            bus_id = bus_id_var.get()
            name = name_var.get()
            source = source_var.get()
            destination = destination_var.get()
            cursor.execute("UPDATE buses SET bus_name=%s, source=%s, destination=%s WHERE bus_id=%s", (name, source, destination, bus_id))
            db.commit()
            messagebox.showinfo("Success", "Bus updated successfully!")
            edit_window.destroy()

        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Bus")
        tk.Label(edit_window, text="Bus ID:").pack()
        bus_id_var = tk.StringVar()
        tk.Entry(edit_window, textvariable=bus_id_var).pack()
        tk.Label(edit_window, text="New Name:").pack()
        name_var = tk.StringVar()
        tk.Entry(edit_window, textvariable=name_var).pack()
        tk.Label(edit_window, text="New Source:").pack()
        source_var = tk.StringVar()
        tk.Entry(edit_window, textvariable=source_var).pack()
        tk.Label(edit_window, text="New Destination:").pack()
        destination_var = tk.StringVar()
        tk.Entry(edit_window, textvariable=destination_var).pack()
        tk.Button(edit_window, text="Update", command=update_bus).pack()

    def delete_bus(self):
        def remove_bus():
            bus_id = bus_id_var.get()
            cursor.execute("DELETE FROM buses WHERE bus_id=%s", (bus_id,))
            db.commit()
            messagebox.showinfo("Success", "Bus deleted successfully!")
            delete_window.destroy()

        delete_window = tk.Toplevel(self)
        delete_window.title("Delete Bus")
        tk.Label(delete_window, text="Bus ID:").pack()
        bus_id_var = tk.StringVar()
        tk.Entry(delete_window, textvariable=bus_id_var).pack()
        tk.Button(delete_window, text="Delete", command=remove_bus).pack()

    
# Main Menu Frame
class MainMenuFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Bus Ticket Management System", font=("Arial", 20, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=30)
        tk.Button(self, text="Login", command=self.app.load_login, bg=app.accent_color, fg="white", width=30, height=2).pack(pady=10)
        tk.Button(self, text="Register", command=self.app.load_register, bg="#2196F3", fg="white", width=30, height=2).pack(pady=10)
        tk.Button(self, text="Exit", command=self.app.exit_app, bg="red", fg="white", width=30, height=2).pack(pady=10)
        tk.Button(self, text="Login as Admin", command=self.admin_login, bg="#4CAF50", fg="white", width=20).pack(pady=10)
    def admin_login(self):
        def check_login():
            username = user_var.get()
            password = pass_var.get()
            if username == "admin" and password == "password":  # Change as needed
                messagebox.showinfo("Login Success", "Welcome, Admin!")
                self.app.load_admin_panel()
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials!")

        login_window = tk.Toplevel(self)
        login_window.title("Admin Login")
        tk.Label(login_window, text="Username:").pack()
        user_var = tk.StringVar()
        tk.Entry(login_window, textvariable=user_var).pack()
        tk.Label(login_window, text="Password:").pack()
        pass_var = tk.StringVar()
        tk.Entry(login_window, textvariable=pass_var, show='*').pack()
        tk.Button(login_window, text="Login", command=check_login).pack()


# Login Frame
class LoginFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Login", font=("Arial", 18, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Username:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.username_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Password:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.password_var, show="*", font=("Arial", 14)).pack(pady=5)

        tk.Button(self, text="Login", command=self.login_user, bg=app.accent_color, fg="white", width=15, height=1).pack(pady=10)
        tk.Button(self, text="Back", command=self.app.load_main_menu, bg="gray", fg="white", width=15, height=1).pack(pady=10)

    def login_user(self):
        username = self.username_var.get()
        password = self.password_var.get()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Success", "Login Successful!")
            self.app.load_source_destination()
        else:
            messagebox.showerror("Error", "Invalid credentials!")


# Register User Frame
class RegisterFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Register New User", font=("Arial", 18, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(self, text="Name:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.name_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Email:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.email_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Phone Number:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.phone_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Username:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.username_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Password:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.password_var, show="*", font=("Arial", 14)).pack(pady=5)

        tk.Button(self, text="Register", command=self.register_user, bg=app.accent_color, fg="white", width=15, height=1).pack(pady=10)
        tk.Button(self, text="Back", command=self.app.load_main_menu, bg="gray", fg="white", width=15, height=1).pack(pady=10)

    def register_user(self):
        name = self.name_var.get()
        email = self.email_var.get()
        phone = self.phone_var.get()
        username = self.username_var.get()
        password = self.password_var.get()

        if name and email and phone and username and password:
            try:
                cursor.execute("INSERT INTO users (name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s)",
                               (name, email, phone, username, password))
                db.commit()
                messagebox.showinfo("Success", "Registration Successful!")
                self.app.load_login()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
        else:
            messagebox.showerror("Error", "Please enter all fields!")


# Source-Destination Frame
class SourceDestinationFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Select Source and Destination", font=("Arial", 16, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        self.source_var = tk.StringVar()
        self.destination_var = tk.StringVar()

        tk.Label(self, text="Source:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.source_var, font=("Arial", 14)).pack(pady=5)

        tk.Label(self, text="Destination:", bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Entry(self, textvariable=self.destination_var, font=("Arial", 14)).pack(pady=5)

        tk.Button(self, text="Search Buses", command=self.search_buses, bg=app.accent_color, fg="white", width=15, height=1).pack(pady=10)
        tk.Button(self, text="Back", command=self.app.load_main_menu, bg="gray", fg="white", width=15, height=1).pack(pady=10)

    def search_buses(self):
        source = self.source_var.get()
        destination = self.destination_var.get()
        if source and destination:
            self.app.load_bus_selection(source, destination)
        else:
            messagebox.showerror("Error", "Please enter both source and destination!")


class BusSelectionFrame(tk.Frame):
    def __init__(self, app, source, destination):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app
        self.source = source
        self.destination = destination

        tk.Label(self, text=f"Buses from {source} to {destination}", font=("Arial", 16, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        cursor.execute("SELECT * FROM buses WHERE source=%s AND destination=%s", (source, destination))
        buses = cursor.fetchall()

        self.bus_buttons = []
        for bus in buses:
            bus_id, bus_name = bus[0], bus[1]
            bus_button = tk.Button(self, text=bus_name, command=lambda bus_id=bus_id: self.app.load_seat_matrix(bus_id, source, destination),
                                   bg=app.accent_color, fg="white", width=30, height=2)
            bus_button.pack(pady=10)
            self.bus_buttons.append(bus_button)

        tk.Button(self, text="Back", command=self.app.load_source_destination, bg="gray", fg="white", width=15, height=1).pack(pady=10)


class SeatMatrixFrame(tk.Frame):
    def __init__(self, app, bus_id, source, destination):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app
        self.bus_id = bus_id
        self.source = source
        self.destination = destination

        tk.Label(self, text="Seat Availability", font=("Arial", 16, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        # Fetch booked seats for the selected bus
        cursor.execute("SELECT seat_number FROM Seats WHERE bus_id = %s AND is_booked = 'Booked'", (self.bus_id,))
        booked_seats = cursor.fetchall()
        
        # Fetch total seats for the selected bus
        cursor.execute("SELECT total_seats FROM Buses WHERE bus_id = %s", (self.bus_id,))
        total_seats = cursor.fetchone()[0]

        # Convert booked seats list into a set for faster lookup
        booked_seats = set(seat[0] for seat in booked_seats)

        # Available seats will be the seats not in the booked seats set
        available_seats = [seat for seat in range(1, total_seats + 1) if seat not in booked_seats]

        # Debugging: Print the available and booked seats to verify
        print(f"Booked Seats: {booked_seats}")
        print(f"Available Seats: {available_seats}")

        # Display total seats, available seats, and booked seats
        tk.Label(self, text=f"Total Seats: {total_seats}", font=("Arial", 14), bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Label(self, text=f"Booked Seats: {', '.join(map(str, booked_seats))}", font=("Arial", 14), bg=app.bg_color, fg=app.text_color).pack(pady=5)
        tk.Label(self, text=f"Available Seats: {', '.join(map(str, available_seats))}", font=("Arial", 14), bg=app.bg_color, fg=app.text_color).pack(pady=5)

        # Entry for seat numbers to book
        self.seats_to_book_label = tk.Label(self, text="Enter seat numbers to book (comma separated):", font=("Arial", 14), bg=app.bg_color, fg=app.text_color)
        self.seats_to_book_label.pack(pady=5)
        self.seats_to_book_entry = tk.Entry(self, font=("Arial", 12))
        self.seats_to_book_entry.pack(pady=5)

        # Book button to confirm booking
        self.book_button = tk.Button(self, text="Book Selected Seats", command=self.book_selected_seats, bg=app.accent_color, fg="white", width=20, height=1)
        self.book_button.pack(pady=10)

        # Back button to go back to bus selection
        tk.Button(self, text="Back", command=lambda: self.app.load_bus_selection(self.source, self.destination), bg="gray", fg="white", width=15, height=1).pack(pady=10)

    def book_selected_seats(self):
        # Get the seat numbers entered by the user
        seat_numbers = self.seats_to_book_entry.get().split(",")
        booked_seats = []
        
        # Fetch available seats (already calculated earlier)
        cursor.execute("SELECT seat_number FROM Seats WHERE bus_id = %s AND is_booked = 'Booked'", (self.bus_id,))
        booked_seats_set = set(seat[0] for seat in cursor.fetchall())

        # Debugging: Print the current booked seats to verify
        print(f"Current Booked Seats: {booked_seats_set}")

        available_seats = [seat for seat in range(1, self.total_seats + 1) if seat not in booked_seats_set]

        for seat_number in seat_numbers:
            seat_number = seat_number.strip()
            if seat_number.isdigit():
                seat_number = int(seat_number)
                if seat_number in available_seats:
                    # Proceed with booking the seat
                    cursor.execute("SELECT seat_id FROM Seats WHERE bus_id = %s AND seat_number = %s", (self.bus_id, seat_number))
                    seat = cursor.fetchone()
                    if seat:
                        seat_id = seat[0]
                        cursor.execute("UPDATE Seats SET is_booked = 'Booked' WHERE seat_id = %s", (seat_id,))
                        booked_seats.append(seat_number)
                    else:
                        print(f"Seat {seat_number} not found in the database.")
                else:
                    tk.messagebox.showwarning("Seat Not Available", f"Seat {seat_number} is not available.")
            else:
                tk.messagebox.showwarning("Input Error", f"Invalid seat number: {seat_number}. Please enter valid numbers.")

        if booked_seats:
            cursor.connection.commit()  # Commit the booking changes to the database
            tk.messagebox.showinfo("Booking Successful", f"Seats {', '.join(map(str, booked_seats))} have been successfully booked.")
            self.app.load_booking_details(booked_seats, self.bus_id, self.source, self.destination)


if __name__ == "__main__":
    root = tk.Tk()
    app = BusTicketApp(root)
    root.mainloop()
