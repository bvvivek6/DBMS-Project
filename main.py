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


# Main Menu Frame
class MainMenuFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app.root, bg=app.bg_color)
        self.app = app

        tk.Label(self, text="Bus Ticket Management System", font=("Arial", 20, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=30)
        tk.Button(self, text="Login", command=self.app.load_login, bg=app.accent_color, fg="white", width=30, height=2).pack(pady=10)
        tk.Button(self, text="Register", command=self.app.load_register, bg="#2196F3", fg="white", width=30, height=2).pack(pady=10)
        tk.Button(self, text="Exit", command=self.app.exit_app, bg="red", fg="white", width=30, height=2).pack(pady=10)


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


# Bus Selection Frame
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

        tk.Label(self, text="Enter Seat Number to Book", font=("Arial", 16, "bold"), bg=app.bg_color, fg=app.text_color).pack(pady=20)

        # Entry field for seat number
        self.seat_entry_label = tk.Label(self, text="Seat Number:", font=("Arial", 14), bg=app.bg_color, fg=app.text_color)
        self.seat_entry_label.pack(pady=5)
        self.seat_entry = tk.Entry(self, font=("Arial", 12))
        self.seat_entry.pack(pady=5)

        # Book button to confirm booking
        self.book_button = tk.Button(self, text="Check Availability & Book", command=self.check_and_book_seat, bg=app.accent_color, fg="white", width=20, height=1)
        self.book_button.pack(pady=10)

        # Back button to go back to bus selection
        tk.Button(self, text="Back", command=lambda: self.app.load_bus_selection(self.source, self.destination), bg="gray", fg="white", width=15, height=1).pack(pady=10)

    def check_and_book_seat(self):
        seat_number = self.seat_entry.get()

        if not seat_number:
            tk.messagebox.showwarning("Input Error", "Please enter a seat number.")
            return

        # Fetch seat details based on the seat number
        cursor.execute("SELECT seat_id, is_booked FROM Seats WHERE bus_id = %s AND seat_number = %s", (self.bus_id, seat_number))
        seat = cursor.fetchone()

        if not seat:
            tk.messagebox.showwarning("Invalid Seat", f"Seat {seat_number} does not exist on this bus.")
            return

        seat_id, is_booked = seat

        if is_booked == 'Booked':
            tk.messagebox.showwarning("Seat Already Booked", f"Seat {seat_number} is already booked.")
        else:
            # Proceed with booking the seat
            cursor.execute("UPDATE Seats SET is_booked = 'Booked' WHERE seat_id = %s", (seat_id,))
            cursor.connection.commit()  # Commit the transaction to the database
            tk.messagebox.showinfo("Booking Successful", f"Seat {seat_number} has been successfully booked.")
            self.app.load_booking_details(seat_id, self.bus_id, self.source, self.destination)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusTicketApp(root)
    root.mainloop()
