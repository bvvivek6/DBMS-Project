import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime


def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="vivek24",  
        database="dbmsproject2"  # Database name
    )

class BusTicketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bus Booking System")
        self.root.geometry("700x500")
        self.current_page = None
        self.user_id = None
        self.admin_id = None
        self.show_login_or_register_page()
    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_or_register_page(self):
        self.clear_page()
        # Title label with a larger font, bold style, and a color
        login_label = tk.Label(self.root, text="Bus SBooking System", font=("Arial", 24, "bold"), fg="#4CAF50")
        login_label.pack(pady=20)
        login_label = tk.Label(self.root, text="Login to continue", font=("Arial", 12, "bold"), fg="#9CAF10")
        login_label.pack(pady=20)
        # Username entry with padding and a border color
        self.username_entry = tk.Entry(self.root, width=40, font=("Arial", 14))
        self.username_entry.insert(0, "Username")
        self.username_entry.pack(pady=10, padx=20)

        # Password entry with padding and a border color
        self.password_entry = tk.Entry(self.root, show="*", width=40, font=("Arial", 14))
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=10, padx=20)

        # Login button with a green background, white text, and larger padding
        login_button = tk.Button(self.root, text="Login", command=self.login, width=20, height=1, bg="#4CAF50", fg="white", font=("Arial", 14))
        login_button.pack(pady=15)

        # Register button with an orange background, white text, and larger padding
        register_button = tk.Button(self.root, text="Register", command=self.register, width=20, height=1, bg="#ffa500", fg="white", font=("Arial", 14))
        register_button.pack(pady=15)

        # Admin login button with a blue background, white text, and larger padding
        admin_button = tk.Button(self.root, text="Login as Admin", command=self.admin_login, width=20, height=1, bg="#1e90ff", fg="white", font=("Arial", 14))
        admin_button.pack(pady=15)

    def register(self):
        self.clear_page()
        register_label = tk.Label(self.root, text="Register", font=("Arial", 20))
        register_label.pack(pady=10)

        self.username_entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.username_entry.insert(0, "Username")
        self.username_entry.pack(pady=5, ipady=5)

        self.password_entry = tk.Entry(self.root, show="*", width=30, font=("Arial", 14))
        self.password_entry.insert(0, "Password")
        self.password_entry.pack(pady=5, ipady=5)

        self.email_entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.email_entry.insert(0, "Email")
        self.email_entry.pack(pady=5, ipady=5)

        register_button = tk.Button(self.root, text="Register", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, relief="raised", command=self.create_account)
        register_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", font=("Arial", 14, "bold"), bg="#f44336", fg="white", padx=10, pady=5, relief="raised", command=self.show_login_or_register_page)
        back_button.pack(pady=5)


    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        connection.commit()
        connection.close()

        messagebox.showinfo("Registration Successful", "Account created successfully. Please login.")
        self.show_login_or_register_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        connection.close()

        if result:
            self.user_id = result[0]
            self.show_bus_search_page()
        else:
            messagebox.showerror("Login Error", "Invalid credentials. Please try again.")

    def admin_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT admin_id FROM admins WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        connection.close()

        if result:
            self.admin_id = result[0]
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Login Error", "Invalid admin credentials. Please try again.")

    def show_bus_search_page(self):
        self.clear_page()

        search_label = tk.Label(self.root, text="Search Buses", font=("Arial", 22, "bold"), fg="#333")
        search_label.pack(pady=15)

        self.source_entry = tk.Entry(self.root, width=30, font=("Arial", 14), fg="#555")
        self.source_entry.insert(0, "Source")
        self.source_entry.pack(pady=5, ipady=5)

        self.destination_entry = tk.Entry(self.root, width=30, font=("Arial", 14), fg="#555")
        self.destination_entry.insert(0, "Destination")
        self.destination_entry.pack(pady=5, ipady=5)

        search_button = tk.Button(self.root, text="Search", command=self.search_buses)
        search_button.pack(pady=10)

        profile_label = tk.Label(self.root, text="User Profile", font=("Arial", 20))
        profile_label.pack(pady=10)

        search_label = tk.Label(self.root, text="Your Booking history", font=("Arial", 20))
        search_label.pack(pady=10)
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT booking_id, bus_id, total_amount, booking_date FROM bookings WHERE user_id = %s", (self.user_id,))
        bookings = cursor.fetchall()

        for booking in bookings:
            booking_id, bus_id, amount, date = booking
            booking_info = f"Booking ID: {booking_id}, Bus ID: {bus_id}, Amount: {amount}, Date: {date}"

            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            booking_label = tk.Label(frame, text=booking_info)
            booking_label.pack(side=tk.LEFT, padx=10)

            cancel_button = tk.Button(frame, text="Cancel Booking", bg="red", fg="white", command=lambda b_id=booking_id: self.cancel_booking(b_id))
            cancel_button.pack(side=tk.RIGHT, padx=5)

        back_button = tk.Button(self.root, text="Back", command=self.show_login_or_register_page)
        back_button.pack(pady=5)

    def search_buses(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT bus_id, bus_name, total_seats, fare_per_seat FROM buses WHERE source = %s AND destination = %s", (source, destination))
        buses = cursor.fetchall()
        connection.close()

        self.show_bus_selection_page(buses)

    def show_bus_selection_page(self, buses):
        self.clear_page()

        bus_list_label = tk.Label(self.root, text="Select a Bus", font=("Arial", 22, "bold"), fg="#333")
        bus_list_label.pack(pady=15)

        bus_frame = tk.Frame(self.root)
        bus_frame.pack(pady=5)

        self.bus_buttons = []
        for bus in buses:
            bus_info = f"{bus[1]} | Seats: {bus[2]} | Fare: ₹{bus[3]}"
            bus_button = tk.Button(
                bus_frame, text=bus_info, font=("Arial", 14), fg="white", bg="#007BFF", 
                activebackground="#0056b3", activeforeground="white", 
                relief="raised", padx=10, pady=5,
                command=lambda bus_id=bus[0]: self.book_bus(bus_id)
            )
            bus_button.pack(pady=5, fill="x", padx=20)
            self.bus_buttons.append(bus_button)

        back_button = tk.Button(self.root, text="🔙 Back", font=("Arial", 14), fg="white", bg="#dc3545",
                                activebackground="#a71d2a", activeforeground="white",
                                relief="raised", padx=10, pady=5,
                                command=self.show_bus_search_page)
        back_button.pack(pady=15, ipadx=10)

    def book_bus(self, bus_id):
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT total_seats FROM buses WHERE bus_id = %s", (bus_id,))
        total_seats = cursor.fetchone()[0]

        seat_numbers = [i for i in range(1, total_seats + 1)]

        cursor.execute("SELECT total_seats FROM buses WHERE bus_id = %s", (bus_id,))
        booked_seats = cursor.fetchone()[0]

        seat_numbers_label = tk.Label(self.root, text="Seats Booked: ")

        seat_numbers_label = tk.Label(self.root, text="Enter seat numbers to book (comma separated):")
        seat_numbers_label.pack(pady=5)

        self.seat_entry = tk.Entry(self.root, width=30)
        self.seat_entry.pack(pady=5)

        book_button = tk.Button(self.root, text="Book Seats", command=lambda: self.book_seats(bus_id, seat_numbers))
        book_button.pack(pady=5)

        back_button = tk.Button(self.root, text="Back", command=self.show_bus_selection_page)
        back_button.pack(pady=5)

    def book_seats(self, bus_id, username):
        selected_seats = list(map(int, self.seat_entry.get().split(',')))
        print(f"Selected seats: {selected_seats}")  # Debugging line

        connection = db_connection()
        cursor = connection.cursor()
        available_seats = []

        # Check available seats
        for seat in selected_seats:
            cursor.execute("SELECT is_booked FROM seats WHERE bus_id = %s AND seat_number = %s", (bus_id, seat))
            result = cursor.fetchone()
            if result and result[0] == 0:
                available_seats.append(seat)

        if len(available_seats) == len(selected_seats):
            total_amount = len(selected_seats) * 100  # Assuming 100 is the fare per seat
            print(f"Total amount: {total_amount}")  # Debugging line

            cursor.execute("INSERT INTO bookings (user_id, bus_id, total_amount) VALUES (%s, %s, %s)", (self.user_id, bus_id, total_amount))
            booking_id = cursor.lastrowid
            print(f"Booking ID: {booking_id}")  # Debugging line

            # Update the seat booking status
            for seat in selected_seats:
                cursor.execute("UPDATE seats SET is_booked = 1 WHERE bus_id = %s AND seat_number = %s", (bus_id, seat))
                #cursor.execute("UPDATE seats SET is_booked_by = %s WHERE bus_id = %s AND seat_number = %s", (username, bus_id,seat))
                cursor.execute("INSERT INTO bookings_details (booking_id, seat_number, fare) VALUES (%s, %s, %s)", (booking_id, seat, 100))

            connection.commit()
            connection.close()

            messagebox.showinfo("Booking Confirmed", "Your booking has been confirmed.")
            self.show_user_profile_page()
        else:
            messagebox.showerror("Booking Error", "One or more selected seats are already booked.")


    def show_user_profile_page(self):
        self.clear_page()

        profile_label = tk.Label(self.root, text="User Profile", font=("Arial", 20))
        profile_label.pack(pady=10)

        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT booking_id, bus_id, total_amount, booking_date FROM bookings WHERE user_id = %s", (self.user_id,))
        bookings = cursor.fetchall()

        for booking in bookings:
            booking_id, bus_id, amount, date = booking
            booking_info = f"Booking ID: {booking_id}, Bus ID: {bus_id}, Amount: {amount}, Date: {date}"

            frame = tk.Frame(self.root)
            frame.pack(pady=5)

            booking_label = tk.Label(frame, text=booking_info)
            booking_label.pack(side=tk.LEFT, padx=10)

            cancel_button = tk.Button(frame, text="Cancel Booking", bg="red", fg="white", command=lambda b_id=booking_id: self.cancel_booking(b_id))
            cancel_button.pack(side=tk.RIGHT, padx=5)

        back_button = tk.Button(self.root, text="Back", command=self.show_bus_search_page)
        back_button.pack(pady=10)


    def cancel_booking(self, booking_id):
       
        connection = db_connection()
        cursor = connection.cursor()

        # Find seats booked for this booking
        cursor.execute("SELECT seat_number FROM bookings_details WHERE booking_id = %s", (booking_id,))
        booked_seats = cursor.fetchall()

        # Release the seats
        for seat in booked_seats:
            seat_number = seat[0]
            cursor.execute("UPDATE seats SET is_booked = 0 WHERE seat_number = %s", (seat_number,))

        # Remove booking details first
        cursor.execute("DELETE FROM bookings_details WHERE booking_id = %s", (booking_id,))

        # Remove the booking
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))

        connection.commit()
        connection.close()

        messagebox.showinfo("Booking Canceled", "Your booking has been successfully canceled.")

        # Refresh the profile page
        self.show_user_profile_page()


    def show_admin_dashboard(self):

        self.clear_page()
        admin_dashboard_label = tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20))
        admin_dashboard_label.pack(pady=10)

        
        add_bus_button = tk.Button(self.root, text="Add Bus", command=self.add_bus, font=("Arial", 14), 
                                    bg="#4CAF50", fg="white", width=20, height=2, relief="solid", borderwidth=2)
        add_bus_button.pack(pady=10)

        # Delete Bus Button
        delete_bus_button = tk.Button(self.root, text="Delete Bus", command=self.delete_bus, font=("Arial", 14), 
                                    bg="#f44336", fg="white", width=20, height=2, relief="solid", borderwidth=2)
        delete_bus_button.pack(pady=10)

        # Modify Bus Button
        modify_bus_button = tk.Button(self.root, text="Modify", command=self.modify_bus, font=("Arial", 14), 
                                    bg="#ff9800", fg="white", width=20, height=2, relief="solid", borderwidth=2)
        modify_bus_button.pack(pady=10)
    
        back_button = tk.Button(self.root, text="Back", command=self.show_login_or_register_page, font=("Arial", 14), 
                                bg="#2196F3", fg="white", width=20, height=2, relief="solid", borderwidth=2)
        back_button.pack(pady=15)
        
    def add_bus(self):
    
        self.add_bus_window = tk.Toplevel(self.root)
        self.add_bus_window.title("Add New Bus")
        self.add_bus_window.geometry("500x4500")
        self.add_bus_window.configure(bg="#f4f4f4")

        title_label = tk.Label(self.add_bus_window, text="🚌 Add New Bus", font=("Arial", 18, "bold"), fg="#333", bg="#f4f4f4")
        title_label.pack(pady=15)

        # Create a frame for inputs
        form_frame = tk.Frame(self.add_bus_window, bg="#f4f4f4")
        form_frame.pack(pady=5)

        # Function to create styled labels and entries
        def create_input_row(label_text):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 12), bg="#f4f4f4")
            label.pack(anchor="w", pady=2)
            entry = tk.Entry(form_frame, width=30, font=("Arial", 12), relief="solid", bd=1)
            entry.pack(pady=5, ipady=3)
            return entry

        # Bus Name
        self.bus_name_entry = create_input_row("🚌 Bus Name:")

        # Source
        self.source_entry = create_input_row("📍 Source:")

        # Destination
        self.destination_entry = create_input_row("🚏 Destination:")

        # Total Seats
        self.total_seats_entry = create_input_row("💺 Total Seats:")

        # Fare per Seat
        self.fare_entry = create_input_row("💰 Fare per Seat:")

        # Add Bus Button
        add_button = tk.Button(self.add_bus_window, text="➕ Add Bus", font=("Arial", 14, "bold"), fg="white", bg="#28a745",
                            activebackground="#218838", activeforeground="white",
                            relief="raised", padx=10, pady=5, command=self.save_bus)
        add_button.pack(pady=15, ipadx=10)


    def save_bus(self):
        # Get the input values from the fields
        bus_name = self.bus_name_entry.get()
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        total_seats = int(self.total_seats_entry.get())
        fare_per_seat = float(self.fare_entry.get())

        # Database connection
        connection = db_connection()
        cursor = connection.cursor()

        # Insert bus details into the buses table
        cursor.execute(
            "INSERT INTO buses (bus_name, source, destination, total_seats, fare_per_seat) "
            "VALUES (%s, %s, %s, %s, %s)",
            (bus_name, source, destination, total_seats, fare_per_seat)
        )

        connection.commit()
        connection.close()

        # Show success message
        messagebox.showinfo("Success", "New bus added successfully.")
        self.add_bus_window.destroy()  # Close the add bus window
        self.show_admin_dashboard()  # Refresh admin dashboard or bus list


    def delete_bus(self):
    # Open a new window to select the bus to delete
        self.delete_bus_window = tk.Toplevel(self.root)
        self.delete_bus_window.title("🗑️ Delete Bus")
        self.delete_bus_window.geometry("500x500")
        self.delete_bus_window.configure(bg="#f8f9fa")

        # Title Label
        title_label = tk.Label(self.delete_bus_window, text="🚌 Delete a Bus", font=("Arial", 16, "bold"), fg="#dc3545", bg="#f8f9fa")
        title_label.pack(pady=15)

        # Fetch bus list from the database
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT bus_id, bus_name FROM buses")
        buses = cursor.fetchall()
        connection.close()

        # Create a frame for the listbox
        list_frame = tk.Frame(self.delete_bus_window, bg="#f8f9fa")
        list_frame.pack(pady=5)

        # Styled Listbox for displaying buses
        self.bus_listbox = tk.Listbox(list_frame, width=45, height=10, font=("Arial", 12), relief="solid", bd=1, fg="#333")
        for bus in buses:
            self.bus_listbox.insert(tk.END, f"ID: {bus[0]} - {bus[1]}")
        self.bus_listbox.pack(side=tk.LEFT, padx=5)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.bus_listbox.yview)
        self.bus_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Delete Button with styling
        delete_button = tk.Button(self.delete_bus_window, text="🗑️ Delete Selected Bus", font=("Arial", 12, "bold"),
                                fg="white", bg="#dc3545", activebackground="#c82333", activeforeground="white",
                                relief="raised", padx=10, pady=5, command=self.confirm_delete)
        delete_button.pack(pady=15, ipadx=10)

    def confirm_delete(self):
        try:
            # Get the selected bus from the listbox
            selected_bus = self.bus_listbox.get(tk.ACTIVE)
            print(f"Selected Bus: '{selected_bus}'")  # Show the full selected string for debugging

            # Try to extract the bus_id based on multiple possible formats
            bus_id_str = ""
            if "ID:" in selected_bus:
                # Format like "ID: 16 - Bus Name"
                bus_id_str = selected_bus.split('ID:')[1].split()[0].strip()  # Get the number after "ID:"
            elif " - " in selected_bus:
                # Format like "16 - Bus Name"
                bus_id_str = selected_bus.split(' - ')[0].strip()  # Get the number before the dash
            else:
                raise ValueError(f"Invalid bus format: {selected_bus}")

            print(f"Extracted bus_id string: '{bus_id_str}'")  # Debugging line

            # Ensure the bus_id_str is a valid number before trying to convert it
            if not bus_id_str.isdigit():
                raise ValueError(f"Invalid bus_id format: '{bus_id_str}'")

            # Convert the bus_id to an integer
            bus_id = int(bus_id_str)
            print(f"Converted bus_id: {bus_id}")  # Debugging line

            # Database connection
            connection = db_connection()
            cursor = connection.cursor()

            # Delete bus from the buses table
            cursor.execute("DELETE FROM buses WHERE bus_id = %s", (bus_id,))
            connection.commit()

            # Check if any rows were affected
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Bus deleted successfully.")
            else:
                messagebox.showwarning("No Rows Affected", "No bus found with the given ID.")

            # Close the connection
            connection.close()

            # Close the delete window and refresh the dashboard
            self.delete_bus_window.destroy()
            self.show_admin_dashboard()

        except Exception as e:
        # Display any error that occurred
            messagebox.showerror("Error", f"An error occurred: {e}")





    def modify_bus(self):
        # Open a new window to select the bus to modify
        self.modify_bus_window = tk.Toplevel(self.root)
        self.modify_bus_window.title("Modify Bus")
        self.modify_bus_window.configure(bg="#f7f7f7")  # Light background color for the window

        # Get list of buses from the database
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT bus_id, bus_name FROM buses")
        buses = cursor.fetchall()
        connection.close()

        # Create a frame to organize widgets
        frame = tk.Frame(self.modify_bus_window, padx=20, pady=20, bg="#f7f7f7")
        frame.pack(padx=10, pady=10)

        # Create a listbox to show buses
        self.bus_listbox = tk.Listbox(frame, width=50, height=10, font=("Arial", 12), selectmode=tk.SINGLE)
        for bus in buses:
            self.bus_listbox.insert(tk.END, f"ID: {bus[0]}, {bus[1]}")
        self.bus_listbox.pack(pady=10)

        # Modify button
        modify_button = tk.Button(frame, text="Modify Selected Bus", command=self.show_modify_fields, 
                                  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", width=20, height=2)
        modify_button.pack(pady=10)

    def show_modify_fields(self):
       
        selected_bus = self.bus_listbox.get(tk.ACTIVE)
        bus_id = int(selected_bus.split(',')[0].split(':')[1].strip())

      
        self.modify_details_window = tk.Toplevel(self.root)
        self.modify_details_window.title("Modify Bus Details")

        # Get bus details from the database
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM buses WHERE bus_id = %s", (bus_id,))
        bus = cursor.fetchone()
        connection.close()

        # Bus name
        bus_name_label = tk.Label(self.modify_details_window, text="Bus Name:")
        bus_name_label.pack(pady=5)
        self.bus_name_entry = tk.Entry(self.modify_details_window, width=30)
        self.bus_name_entry.insert(0, bus[1])  # Default value is current bus name
        self.bus_name_entry.pack(pady=5)

        # Source
        source_label = tk.Label(self.modify_details_window, text="Source:")
        source_label.pack(pady=5)
        self.source_entry = tk.Entry(self.modify_details_window, width=30)
        self.source_entry.insert(0, bus[2])  # Default value is current source
        self.source_entry.pack(pady=5)

        # Destination
        destination_label = tk.Label(self.modify_details_window, text="Destination:")
        destination_label.pack(pady=5)
        self.destination_entry = tk.Entry(self.modify_details_window, width=30)
        self.destination_entry.insert(0, bus[3])  # Default value is current destination
        self.destination_entry.pack(pady=5)

        # Total seats
        total_seats_label = tk.Label(self.modify_details_window, text="Total Seats:")
        total_seats_label.pack(pady=5)
        self.total_seats_entry = tk.Entry(self.modify_details_window, width=30)
        self.total_seats_entry.insert(0, bus[4])  # Default value is current total seats
        self.total_seats_entry.pack(pady=5)

        # Fare per seat
        fare_label = tk.Label(self.modify_details_window, text="Fare per Seat:")
        fare_label.pack(pady=5)
        self.fare_entry = tk.Entry(self.modify_details_window, width=30)
        self.fare_entry.insert(0, bus[5])  # Default value is current fare
        self.fare_entry.pack(pady=5)

        # Save changes button
        save_button = tk.Button(self.modify_details_window, text="Save Changes", command=lambda: self.save_modified_bus(bus_id))
        save_button.pack(pady=5)

    def save_modified_bus(self, bus_id):
        # Get the modified values from the fields
        bus_name = self.bus_name_entry.get()
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        total_seats = int(self.total_seats_entry.get())
        fare_per_seat = float(self.fare_entry.get())

        # Database connection
        connection = db_connection()
        cursor = connection.cursor()

        # Update bus details in the buses table
        cursor.execute(
            "UPDATE buses SET bus_name = %s, source = %s, destination = %s, total_seats = %s, fare_per_seat = %s "
            "WHERE bus_id = %s",
            (bus_name, source, destination, total_seats, fare_per_seat, bus_id)
        )

        connection.commit()
        connection.close()

        # Show success message
        messagebox.showinfo("Success", "Bus details updated successfully.")
        self.modify_details_window.destroy()  # Close the modify bus window
        self.show_admin_dashboard()  # Refresh admin dashboard or bus list

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BusTicketApp(root)
    root.mainloop()
