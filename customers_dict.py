import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json


class User:

    def __init__(self,name, location, address, contact, interests: str):
        self.name = name
        self.location = location
        self.address = address
        self.contact = contact
        self.interests = interests

    def __repr__(self):
        return f"Name: {self.name}, Location: {self.location}, Address: {self.address}, Contact: {self.contact}, Interests: {self.interests}"


class UserManager:
    def __init__(self):
        try:
            self.customers = json.load(open("customers_dict.json"))
        except Exception:
            self.customers = []

    def add_user(self, name, location, address, contact, interests):
        print(interests)
        self.customers.append(User(name, location, address, contact, interests).__dict__)
        self.customers = self.merge_sort(self.customers)
        print(self.customers)
        file = open('customers_dict.json', 'w')
        json.dump(self.customers, file)

    def merge(self, left: list, right: list):
        """Merge 2 arrays"""
        result = []
        left_index = 0
        right_index = 0

        while left_index < len(left) and right_index < len(right):
            if left[left_index]['name'].lower() < right[right_index]['name'].lower():
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

            result += left[left_index:]
            result += right[right_index:]
            return result

    def merge_sort(self, items):
        """Recursively break down and sort the array"""
        if len(items) == 1:
            return items
        else:
            mid = len(items) // 2
            left = items[:mid]
            right = items[mid:]

            left = self.merge_sort(left)
            right = self.merge_sort(right)

            return self.merge(left, right)

    def search(self, key: str, attr):
        results = []

        for customer in self.customers:
            if key.lower() in customer[attr].lower():
                results.append(customer)

        return results


class App:
    def __init__(self, root):
        self.name_entry = None
        self.search_option = None
        self.search_entry = None
        self.interests_entry = None
        self.address_entry = None
        self.location_entry = None
        self.contact_entry = None

        self.root = root
        self.root.title("Customer Registration & Search")
        self.root.geometry("700x500")

        # Configure modern theme
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12), padding=6)
        style.configure("TEntry", font=("Helvetica", 12))
        style.configure("TFrame", background="#f4f4f4")  # Light gray background

        self.manager = UserManager()

        # Frames for different pages
        self.main_frame = ttk.Frame(root)
        self.register_frame = ttk.Frame(root)
        self.search_frame = ttk.Frame(root)

        self.create_main_frame()
        self.create_register_frame()
        self.create_search_frame()

        self.main_frame.pack(fill="both", expand=True)

        print(( 'box' in 'Box, Football'.lower()))

    def create_main_frame(self):
        # Main frame widgets
        ttk.Label(
            self.main_frame,
            text="Welcome to User Registration System",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=20)

        ttk.Button(
            self.main_frame,
            text="Register New Customer",
            command=self.show_register_frame,
            width=30,
        ).pack(pady=10)

        ttk.Button(
            self.main_frame,
            text="Search Customer",
            command=self.show_search_frame,
            width=30,
        ).pack(pady=10)

    def create_register_frame(self):
        # Register frame widgets
        ttk.Label(
            self.register_frame,
            text="Register New Customer",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)

        form_frame = ttk.Frame(self.register_frame)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10)

        ttk.Label(form_frame, text="Location:").grid(row=1, column=0, sticky="w", pady=5)
        self.location_entry = ttk.Entry(form_frame, width=30)
        self.location_entry.grid(row=1, column=1, padx=10)

        ttk.Label(form_frame, text="Address:").grid(row=2, column=0, sticky="w", pady=5)
        self.address_entry = ttk.Entry(form_frame, width=30)
        self.address_entry.grid(row=2, column=1, padx=10)

        ttk.Label(form_frame, text="Contact:").grid(row=3, column=0, sticky="w", pady=5)
        self.contact_entry = ttk.Entry(form_frame, width=30)
        self.contact_entry.grid(row=3, column=1, padx=10)

        ttk.Label(form_frame, text="Interests:").grid(row=4, column=0, sticky="w", pady=5)
        self.interests_entry = ttk.Entry(form_frame, width=30)
        self.interests_entry.grid(row=4, column=1, padx=10)

        ttk.Button(
            self.register_frame,
            text="Register",
            command=self.register_customer,
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
            text="Search Customers",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=10)

        ttk.Label(self.search_frame, text="Search By:").pack(anchor="w", padx=20)

        self.search_option = tk.StringVar(value="name")
        ttk.Radiobutton(
            self.search_frame,
            text="Name",
            variable=self.search_option,
            value="name",
        ).pack(anchor="w", padx=20)
        
        ttk.Radiobutton(
            self.search_frame,
            text="Location",
            variable=self.search_option,
            value="location",
        ).pack(anchor="w", padx=20)
        
        ttk.Radiobutton(
            self.search_frame,
            text="Address",
            variable=self.search_option,
            value="address",
        ).pack(anchor="w", padx=20)

        ttk.Radiobutton(
            self.search_frame,
            text="Contact",
            variable=self.search_option,
            value="contact",
        ).pack(anchor="w", padx=20)

        ttk.Radiobutton(
            self.search_frame,
            text="Interests",
            variable=self.search_option,
            value="interests",
        ).pack(anchor="w", padx=20)

        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.pack(pady=10)

        ttk.Button(
            self.search_frame,
            text="Search",
            command=self.search_customers,
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

    def register_customer(self):
        name = self.name_entry.get()
        location = self.location_entry.get()
        address = self.address_entry.get()
        contact = self.contact_entry.get()
        interests = self.interests_entry.get()

        if not name or not location or not address or not contact or not interests:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.manager.add_user(name=name, location=location, address=address, contact=contact, interests=interests)
        messagebox.showinfo("Success", "User registered successfully!")
        self.name_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.interests_entry.delete(0, tk.END)

    def search_customers(self):
        key = self.search_entry.get()
        attribute = self.search_option.get()
        print(f'key:{key}  attr:{attribute}')

        if not key:
            messagebox.showerror("Error", "Please enter a search query!")
            return

        results = self.manager.search(key, attribute)
        self.search_results.delete(0, tk.END)

        if results:
            for user in results:
                self.search_results.insert(tk.END, user)
        else:
            self.search_results.insert(tk.END, "No matching customers found!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
