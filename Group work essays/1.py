import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class User:
    def __init__(self, username, location, dob, password):
        self.username = username
        self.location = location
        self.dob = dob
        self.password = password

    def __repr__(self):
        return f"Username: {self.username}, Location: {self.location}, DOB: {self.dob}"


class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, username, location, dob, password):
        self.users.append(User(username, location, dob, password))
        self.bubble_sort()

    def bubble_sort(self):
        n = len(self.users)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.users[j].username > self.users[j + 1].username:
                    self.users[j], self.users[j + 1] = self.users[j + 1], self.users[j]

    def get_all_users(self):
        return self.users

    def binary_search(self, key, attribute):
        low, high = 0, len(self.users) - 1
        results = []

        while low <= high:
            mid = (low + high) // 2
            value = getattr(self.users[mid], attribute)

            if key.lower() in value.lower():
                results.append(self.users[mid])
                left, right = mid - 1, mid + 1
                while left >= 0 and key.lower() in getattr(self.users[left], attribute).lower():
                    results.append(self.users[left])
                    left -= 1
                while right < len(self.users) and key.lower() in getattr(self.users[right], attribute).lower():
                    results.append(self.users[right])
                    right += 1
                break
            elif value.lower() < key.lower():
                low = mid + 1
            else:
                high = mid - 1

        return results


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration & Search")
        self.root.geometry("700x500")

        # Configure modern theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TFrame", background="#f4f4f4")

        self.manager = UserManager()

        # Frames for different pages
        self.main_frame = ttk.Frame(root)
        self.register_frame = ttk.Frame(root)
        self.search_frame = ttk.Frame(root)
        self.view_customers_frame = ttk.Frame(root)  # New frame for viewing customers

        self.create_main_frame()
        self.create_register_frame()
        self.create_search_frame()
        self.create_view_customers_frame()  # Create the new frame

        self.main_frame.pack(fill="both", expand=True)

    def create_main_frame(self):
        # Main frame widgets
        ttk.Label(
            self.main_frame,
            text="Welcome to User Registration System",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=20)

        ttk.Button(
            self.main_frame,
            text="Register New User",
            command=self.show_register_frame,
            width=30,
        ).pack(pady=10)

        ttk.Button(
            self.main_frame,
            text="Search Users",
            command=self.show_search_frame,
            width=30,
        ).pack(pady=10)

        ttk.Button(
            self.main_frame,
            text="View All Customers",
            command=self.show_view_customers_frame,
            width=30,
        ).pack(pady=10)

    def create_view_customers_frame(self):
        # View customers frame widgets
        ttk.Label(
            self.view_customers_frame,
            text="All Customers",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)

        # Create a treeview for better display of customer information
        self.customer_tree = ttk.Treeview(
            self.view_customers_frame,
            columns=("Username", "Location", "DOB"),
            show="headings",
            height=15
        )

        # Define columns
        self.customer_tree.heading("Username", text="Username")
        self.customer_tree.heading("Location", text="Location")
        self.customer_tree.heading("DOB", text="Date of Birth")

        # Configure column widths
        self.customer_tree.column("Username", width=200)
        self.customer_tree.column("Location", width=200)
        self.customer_tree.column("DOB", width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.view_customers_frame,
            orient="vertical",
            command=self.customer_tree.yview
        )
        self.customer_tree.configure(yscrollcommand=scrollbar.set)

        # Pack the treeview and scrollbar
        self.customer_tree.pack(side="left", pady=10, padx=10, fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Add refresh button
        ttk.Button(
            self.view_customers_frame,
            text="Refresh List",
            command=self.refresh_customer_list,
            width=20,
        ).pack(pady=10)

        ttk.Button(
            self.view_customers_frame,
            text="Return to Main Page",
            command=self.show_main_frame,
            width=20,
        ).pack(pady=10)

    def refresh_customer_list(self):
        # Clear the current items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        # Get all users and insert them into the treeview
        users = self.manager.get_all_users()
        for user in users:
            self.customer_tree.insert(
                "",
                "end",
                values=(user.username, user.location, user.dob)
            )

    def show_view_customers_frame(self):
        self.clear_frames()
        self.view_customers_frame.pack(fill="both", expand=True)
        self.refresh_customer_list()  # Refresh the list when showing the frame

    def create_register_frame(self):
        # Register frame widgets
        ttk.Label(
            self.register_frame,
            text="Register New User",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)

        form_frame = ttk.Frame(self.register_frame)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=10)

        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=5)
        self.location_entry = ttk.Entry(form_frame, width=30)
        self.location_entry.grid(row=1, column=1, padx=10)

        ttk.Label(form_frame, text="Date of Birth:").grid(row=2, column=0, sticky="w", pady=5)
        self.dob_entry = ttk.Entry(form_frame, width=30)
        self.dob_entry.grid(row=2, column=1, padx=10)

        ttk.Label(form_frame, text="Password:").grid(row=3, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=3, column=1, padx=10)

        ttk.Button(
            self.register_frame,
            text="Register",
            command=self.register_user,
            width=20,
        ).pack(pady=10)

        ttk.Button(
            self.register_frame,
            text="Return to Main Page",
            command=self.show_main_frame,
            width=20,
        ).pack(pady=10)

    def create_search_frame(self):
        # Search frame widgets
        ttk.Label(
            self.search_frame,
            text="Search Users",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)

        ttk.Label(self.search_frame, text="Search By:").pack(anchor="w", padx=20)

        self.search_option = tk.StringVar(value="username")
        ttk.Radiobutton(
            self.search_frame,
            text="Username",
            variable=self.search_option,
            value="username",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            self.search_frame,
            text="Location",
            variable=self.search_option,
            value="location",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            self.search_frame,
            text="Date of Birth",
            variable=self.search_option,
            value="dob",
        ).pack(anchor="w", padx=20)

        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.pack(pady=10)

        ttk.Button(
            self.search_frame,
            text="Search",
            command=self.search_users,
            width=20,
        ).pack(pady=10)

        self.search_results = tk.Listbox(self.search_frame, width=50, height=10, font=("Helvetica", 12))
        self.search_results.pack(pady=10)

        ttk.Button(
            self.search_frame,
            text="Return to Main Page",
            command=self.show_main_frame,
            width=20,
        ).pack(pady=10)

    def show_main_frame(self):
        self.clear_frames()
        self.main_frame.pack(fill="both", expand=True)

    def show_register_frame(self):
        self.clear_frames()
        self.register_frame.pack(fill="both", expand=True)

    def show_search_frame(self):
        self.clear_frames()
        self.search_frame.pack(fill="both", expand=True)

    def clear_frames(self):
        self.main_frame.pack_forget()
        self.register_frame.pack_forget()
        self.search_frame.pack_forget()
        self.view_customers_frame.pack_forget()

    def register_user(self):
        username = self.username_entry.get()
        location = self.location_entry.get()
        dob = self.dob_entry.get()
        password = self.password_entry.get()

        if not username or not location or not dob or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.manager.add_user(username, location, dob, password)
        messagebox.showinfo("Success", "User registered successfully!")
        self.username_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def search_users(self):
        key = self.search_entry.get()
        attribute = self.search_option.get()

        if not key:
            messagebox.showerror("Error", "Please enter a search query!")
            return

        results = self.manager.binary_search(key, attribute)
        self.search_results.delete(0, tk.END)

        if results:
            for user in results:
                self.search_results.insert(tk.END, user)
        else:
            self.search_results.insert(tk.END, "No matching users found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()