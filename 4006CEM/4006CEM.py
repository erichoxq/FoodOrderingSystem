import sqlite3
import tkinter.messagebox as messagebox
from tkinter import ttk, Menu, Radiobutton
from tkinter import Tk, StringVar, Toplevel, Frame, Label, Entry, Button, Text, Scrollbar
from tkinter import END
from datetime import datetime

root = Tk()
root.title("Register and Login System")
root.geometry("1920x1080+0+0")  # window size and position
root.config(bg='light blue')  # used to customize the window (bg colour, title)
root.state("zoomed")  # maximize the root window to fill the entire screen

# Constants
WIDTH = 800
HEIGHT = 700

# Create variables
USERNAME_LOGIN = StringVar()
PASSWORD_LOGIN = StringVar()
USERNAME_REGISTER = StringVar()
PASSWORD_REGISTER = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
DATE_OF_BIRTH = StringVar()
EMAIL_ADDRESS = StringVar()
PHONE_NUMBER = StringVar()

conn = None  # connection to database
cursor = None  # use to execute the sql queries and fetch results from db
conn = sqlite3.connect(':memory:')
# Initialize Cart
cart = []


def Database():
    global conn, cursor
    conn = sqlite3.connect("db_food_ordering_system.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `customer` (customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20), "
        "password TEXT(20), firstname TEXT(20), lastname TEXT(20), date_of_birth DATE, email_address TEXT(30), phone_number TEXT(20))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `food` (food_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, food_name TEXT(30), "
        "description TEXT(50), price float, food_type TEXT(10), admin_id INTEGER, FOREIGN KEY(admin_id) REFERENCES admin(admin_id) )")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `review` (review_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customer_id INTEGER,"
        "review TEXT(20),rating INTEGER, review_date DATE, FOREIGN KEY (customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `payment` (payment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, payment_date DATE, "
        "order_id INTEGER, total_price FLAOT, FOREIGN KEY(order_id) REFERENCES orders(order_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `order` (order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, order_date DATE, "
        "food_id INTEGER, quantity INTEGER, total_price FLAOT, customer_id INTEGER, FOREIGN KEY(food_id) REFERENCES food(food_id), FOREIGN KEY(customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `admin`(admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20), "
        "password TEXT(20), firstname TEXT(20), lastname TEXT(20), date_of_birth DATE, email_address TEXT(30), phone_number TEXT(20))")

def Exit():
    result = messagebox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()

def Home():
    global HomeFrame
    HomeFrame = Frame(root)
    HomeFrame.pack(side='top', pady=60)
    root.withdraw()  # Hide the main login window
    HomeFrame = Toplevel()  # Create a new window
    HomeFrame.title("Home")
    HomeFrame.attributes('-fullscreen', True)

    lbl_home = Label(HomeFrame, text="Welcome to the Home Page", font=('times new roman', 20, 'bold'))
    lbl_home.pack(pady=50)

    btn_view_menu = Button(HomeFrame, text="Food Menu", font=('times new roman', 16), width=20, command=ViewFoodMenu, bg='green', fg='white', relief='raised')
    btn_view_menu.bind("<Enter>", lambda e: btn_view_menu.config(bg="light green"))
    btn_view_menu.bind("<Leave>", lambda e: btn_view_menu.config(bg="green"))
    btn_view_menu.pack(pady=20)

    btn_logout = Button(HomeFrame, text="Logout", font=('times new roman', 16), width=20, command=Logout, bg='#7E84F7', fg='white', relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#B8BEED"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#7E84F7"))
    btn_logout.pack(pady=20)

def AdminPanel():
    global AdminPanelFrame
    AdminPanelFrame = Frame(root)
    AdminPanelFrame.pack(side='top', pady=60)
    root.withdraw()  # Hide the main login window
    AdminPanelFrame = Toplevel()  # Create a new window
    AdminPanelFrame.title("Admin Panel")
    AdminPanelFrame.attributes('-fullscreen', True)

    lbl_admin_panel = Label(AdminPanelFrame, text="Admin Panel", font=('times new roman', 20, 'bold'))
    lbl_admin_panel.pack(pady=20)

    btn_food_dashboard = Button(AdminPanelFrame, text="Food Dashboard", font=('times new roman', 16), width=20, command=FoodDashboard, bg='#65D954', fg='white')
    btn_food_dashboard.bind("<Enter>", lambda e: btn_food_dashboard.config(bg="#77FF63"))
    btn_food_dashboard.bind("<Leave>", lambda e: btn_food_dashboard.config(bg="#65D954"))
    btn_food_dashboard.pack(pady=10)

    btn_view_review_rating = Button(AdminPanelFrame, text="View Review and Rating", font=('times new roman', 16), width=20, command=view_review_rating, bg='#E0B715', fg='white')
    btn_view_review_rating.bind("<Enter>", lambda e: btn_view_review_rating.config(bg="#FACC18"))
    btn_view_review_rating.bind("<Leave>", lambda e: btn_view_review_rating.config(bg="#E0B715"))
    btn_view_review_rating.pack(pady=10)

    btn_view_total_orders = Button(AdminPanelFrame, text="View Total Orders", font=('times new roman', 16), width=20, command=view_total_orders, bg='#840BC7', fg='white')
    btn_view_total_orders.bind("<Enter>", lambda e: btn_view_total_orders.config(bg="#AA0EFF"))
    btn_view_total_orders.bind("<Leave>", lambda e: btn_view_total_orders.config(bg="#840BC7"))
    btn_view_total_orders.pack(pady=10)

    btn_logout_admin = Button(AdminPanelFrame, text="Logout", font=('times new roman', 16), width=20, command=LogoutAdmin, bg='#7E84F7', fg='white')
    btn_logout_admin.bind("<Enter>", lambda e: btn_logout_admin.config(bg="#B8BEED"))
    btn_logout_admin.bind("<Leave>", lambda e: btn_logout_admin.config(bg="#7E84F7"))
    btn_logout_admin.pack(pady=10)

def add_food_window():
    # Create a new window for adding food
    add_food_window = Toplevel()
    add_food_window.title("Add Food")
    add_food_window.geometry("1920x1080+0+0")  # window size and position
    add_food_window.state("zoomed")
    add_food_window.grid_columnconfigure(0, weight=1)
    add_food_window.grid_columnconfigure(1, weight=1)

    # Define the layout of the window
    label_food_name = Label(add_food_window, text="Food Name:", font=('times new roman', 16))
    label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_food_name = Entry(add_food_window, font=('times new roman', 16))
    entry_food_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    label_description = Label(add_food_window, text="Food Description:", font=('times new roman', 16))
    label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_description = Entry(add_food_window, font=('times new roman', 16))
    entry_description.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    label_price = Label(add_food_window, text="Price:", font=('times new roman', 16))
    label_price.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_price = Entry(add_food_window, font=('times new roman', 16))
    entry_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    label_food_type = Label(add_food_window, text="Food Type:", font=('times new roman', 16))
    label_food_type.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    entry_food_type = Entry(add_food_window, font=('times new roman', 16))
    entry_food_type.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    # Create a button to add the food
    btn_add_food = Button(add_food_window, text="Add Food", font=('times new roman', 16), command=lambda: add_food(entry_food_name, entry_description, entry_price, entry_food_type), bg='#E69312', fg='white')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFA314"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.grid(row=5, columnspan=2, pady=20)

    btn_back = Button(add_food_window, text="Back to Dashboard", font=('times new roman', 16), command=FoodDashboard, bg='#7E84F7', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B8BEED"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#7E84F7"))
    btn_back.grid(row=6, columnspan=2, pady=20)

def FoodDashboard():
    global AdminPanelFrame, food_treeview

    def apply_filter(food_type):
        # Clear previous search results
        food_treeview.delete(*food_treeview.get_children())

        try:
            # Construct the SQL query based on the selected food type
            sql_query = "SELECT food_id, food_name, description, price, food_type FROM food"
            if food_type and food_type != "all":
                sql_query += f" WHERE food_type = '{food_type}'"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Populate the treeview with fetched data
            for row in rows:
                food_id, food_name, description, price, food_type = row
                food_treeview.insert("", "end", values=(food_id, food_name, description, price, food_type), tags=(food_id,))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    AdminPanelFrame.withdraw()  # Hide the home window
    FoodFrame = Toplevel()
    FoodFrame.title("Food Dashboard")
    FoodFrame.geometry("1920x1080+0+0")  # window size and position
    FoodFrame.state("zoomed")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), foreground="#148699")

    # Create a frame to contain the food options buttons
    food_options_frame = Frame(FoodFrame)
    food_options_frame.pack(side="top", pady=20)

    # Create the food options buttons
    btn_add_food = Button(food_options_frame, text="Add Food", font=('times new roman', 16), width=15, command=add_food_window, bg='#E69312', fg='white', relief='raised')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFA314"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.pack(side="left", padx=10)

    btn_delete_food = Button(food_options_frame, text="Delete Food", font=('times new roman', 16), width=15, command=delete_food, bg='red', fg='white', relief='raised')
    btn_delete_food.bind("<Enter>", lambda e: btn_delete_food.config(bg="#FF8080"))
    btn_delete_food.bind("<Leave>", lambda e: btn_delete_food.config(bg="red"))
    btn_delete_food.pack(side="left", padx=10)

    btn_update_food = Button(food_options_frame, text="Update Food", font=('times new roman', 16), width=15, command=update_food_window, bg='green', fg='white')
    btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="light green"))
    btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="green"))
    btn_update_food.pack(side="left", padx=10)

    btn_search_food = Button(food_options_frame, text="Search Food", font=('times new roman', 16), width=15, command=search_food_window, bg='#D1D1D1', fg='white')
    btn_search_food.bind("<Enter>", lambda e: btn_search_food.config(bg="#808080"))
    btn_search_food.bind("<Leave>", lambda e: btn_search_food.config(bg="#D1D1D1"))
    btn_search_food.pack(side="left", padx=10)

    btn_back = Button(food_options_frame, text="Back to Admin Panel", font=('times new roman', 16), command=AdminPanel, bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side="left", padx=10)

    btn_Logout = Button(food_options_frame, text="Logout", font=('times new roman', 16), width=15, command=Logout, bg='#7E84F7', fg='white')
    btn_Logout.bind("<Enter>", lambda e: btn_Logout.config(bg="#B8BEED"))
    btn_Logout.bind("<Leave>", lambda e: btn_Logout.config(bg="#7E84F7"))
    btn_Logout.pack(side="left", padx=10)

    # Food type filter buttons
    food_type_frame = Frame(FoodFrame)
    food_type_frame.pack(side="top", pady=20)

    selected_food_type = StringVar(value="all")  # Default to "all"

    btn_all = Radiobutton(food_type_frame, text="All", font=('times new roman', 16), variable=selected_food_type, value="all")
    btn_all.pack(side="left", padx=10)

    btn_spicy = Radiobutton(food_type_frame, text="Spicy", font=('times new roman', 16), variable=selected_food_type, value="spicy")
    btn_spicy.pack(side="left", padx=10)

    btn_normal = Radiobutton(food_type_frame, text="Normal", font=('times new roman', 16), variable=selected_food_type, value="normal")
    btn_normal.pack(side="left", padx=10)

    btn_vegetarian = Radiobutton(food_type_frame, text="Vegetarian", font=('times new roman', 16), variable=selected_food_type, value="vegetarian")
    btn_vegetarian.pack(side="left", padx=10)

    # Apply Filter button
    btn_filter = Button(food_type_frame, text="Apply Filter", font=('times new roman', 16), command=lambda: apply_filter(selected_food_type.get()), bg='#D1D1D1', fg='black')
    btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#808080"))
    btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#D1D1D1"))
    btn_filter.pack(side="left", padx=10)

    # Create a Treeview widget to display food items
    food_treeview = ttk.Treeview(FoodFrame, columns=("Food ID", "Food Name", "Description", "Price", "Food Type"),
                                 show='headings', height=20, style="Treeview")
    food_treeview.heading("Food ID", text="Food ID")
    food_treeview.heading("Food Name", text="Food Name")
    food_treeview.heading("Description", text="Description")
    food_treeview.heading("Price", text="Price")
    food_treeview.heading("Food Type", text="Food Type")
    food_treeview.column("Food ID", width=100, anchor="center")
    food_treeview.column("Food Name", width=150, anchor="center")
    food_treeview.column("Description", width=300, anchor="center")
    food_treeview.column("Price", width=100, anchor="center")
    food_treeview.column("Food Type", width=100, anchor="center")
    food_treeview.pack(pady=20)

    # Populate the treeview with food data from the database
    apply_filter("all")  # Load all data initially

    food_treeview.pack(fill="both", expand=True)
    update_food_treeview()

def add_food(entry_food_name, entry_description, entry_price, entry_food_type):
    # Get the values entered by the user
    food_name = entry_food_name.get()
    description = entry_description.get()
    price = entry_price.get()
    food_type = entry_food_type.get()

    # Check if all fields are filled
    if food_name and description and price and food_type:
        try:
            # Insert the food details into the database
            cursor.execute("INSERT INTO food (food_name, description, price, food_type) VALUES (?, ?, ?, ?)",
                           (food_name, description, price, food_type))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Food successfully added!")

            # Fetch data from the database and update the food_treeview
            update_food_treeview()

            # Destroy the add_food_window
            add_food_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding food: {e}")
    else:
        messagebox.showerror("Error", "Please fill in all fields!")

def update_food_window():
    # Get the selected food_id
    food_id = get_selected_food_id()

    if food_id:
        try:
            # Fetch the selected food details from the database
            cursor.execute("SELECT food_name, description, price, food_type FROM food WHERE food_id=?", (food_id,))
            food_details = cursor.fetchone()
            if food_details:
                # Create a new window for updating food
                update_food_window = Toplevel()
                update_food_window.title("Update Food")

                # Define the layout of the window
                label_food_name = Label(update_food_window, text="Food Name:", font=('times new roman', 16))
                label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="w")
                entry_food_name = Entry(update_food_window, font=('times new roman', 16))
                entry_food_name.grid(row=0, column=1, padx=10, pady=10)
                entry_food_name.insert(0, food_details[0])  # Food name

                label_description = Label(update_food_window, text="Food Description:", font=('times new roman', 16))
                label_description.grid(row=1, column=0, padx=10, pady=10, sticky="w")
                entry_description = Entry(update_food_window, font=('times new roman', 16))
                entry_description.grid(row=1, column=1, padx=10, pady=10)
                entry_description.insert(0, food_details[1])  # Description

                label_price = Label(update_food_window, text="Price:", font=('times new roman', 16))
                label_price.grid(row=2, column=0, padx=10, pady=10, sticky="w")
                entry_price = Entry(update_food_window, font=('times new roman', 16))
                entry_price.grid(row=2, column=1, padx=10, pady=10)
                entry_price.insert(0, food_details[2])  # Price

                label_food_type = Label(update_food_window, text="Food Type:", font=('times new roman', 16))
                label_food_type.grid(row=3, column=0, padx=10, pady=10, sticky="w")
                entry_food_type = Entry(update_food_window, font=('times new roman', 16))
                entry_food_type.grid(row=3, column=1, padx=10, pady=10)
                entry_food_type.insert(0, food_details[3])  # Food Type

                # Create a button to update the food
                btn_update_food = Button(update_food_window, text="Update Food", font=('times new roman', 16), command=lambda: update_food(food_id, entry_food_name.get(), entry_description.get(), entry_price.get(), entry_food_type.get()), bg='blue', fg='white')
                btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="light blue"))
                btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="blue"))
                btn_update_food.grid(row=4, columnspan=2, pady=20)
            else:
                messagebox.showerror("Error", "Selected food details not found.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food details: {e}")

def get_selected_food_id():
    selected_item = food_treeview.selection()
    if selected_item:
        item_values = food_treeview.item(selected_item, 'values')
        cursor.execute("SELECT food_id FROM food WHERE food_id=?", (item_values[0],))
        food_id = cursor.fetchone()
        if food_id:
            return food_id[0]  # Return the food id
        else:
            messagebox.showerror("Error", "Selected food id not found.")
    else:
        messagebox.showerror("Error", "Please select a food item.")

def update_food(food_id, food_name, description, price, food_type):
    try:
        cursor.execute("UPDATE food SET food_name=?, description=?, price=?, food_type=? WHERE food_id=?",
                       (food_name, description, price, food_type, food_id))
        conn.commit()  # Commit the transaction
        messagebox.showinfo("Success", "Food details updated successfully!")

        # Fetch the updated data from the database and update the food treeview
        update_food_treeview()


        # Show the food dashboard
        # Destroy the update window after the user clicks "OK" on the message box
        update_food_window.destroy()
        FoodDashboard()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating food details: {e}")

def update_food_treeview():
    # Clear existing data in the treeview
    for item in food_treeview.get_children():
        food_treeview.delete(item)

    try:
        # Fetch data from the database
        cursor.execute("SELECT food_id, food_name, description, price, food_type FROM food")
        rows = cursor.fetchall()

        # Populate the treeview with fetched data
        for row in rows:
            food_treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching food data: {e}")

def delete_food():
    # Get the selected item from the Treeview
    selected_item = food_treeview.selection()

    if not selected_item:
        messagebox.showerror("Error", "Please select a food item to delete.")
        return

    # Get the item's values
    item_values = food_treeview.item(selected_item, 'values')
    food_name = item_values[0]

    # Prompt the user for confirmation
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{food_name}'?")

    if confirm:
        try:
            # Delete the selected item from the database table
            cursor.execute("DELETE FROM food WHERE food_name=?", (food_name,))
            conn.commit()  # Commit the transaction

            # Delete the selected item from the Treeview
            food_treeview.delete(selected_item)
            messagebox.showinfo("Success", f"'{food_name}' deleted successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting food: {e}")

def search_food_window():
    def search_food():
        # Get the search query from the entry field
        query = entry_search.get()

        # Clear previous search results
        treeview_search.delete(*treeview_search.get_children())

        # Iterate over the items in food_treeview and check for matches
        for item in food_treeview.get_children():
            values = food_treeview.item(item, 'values')
            if values and query.lower() in values[0].lower():  # Assuming food name is in the first column
                treeview_search.insert("", "end", values=values)

        if not treeview_search.get_children():
            messagebox.showinfo("Search Results", "No matching food found.")

    # Create a new Toplevel window for searching food
    search_window = Toplevel()
    search_window.title("Search Food")
    search_window.geometry("1920x1080+0+0")
    search_window.state("zoomed")

    # Create a label and an entry field for entering the search query
    label_search = Label(search_window, text="Enter Food ID:")
    label_search.pack(pady=10)

    entry_search = Entry(search_window, width=30)
    entry_search.pack()

    # Create a button to initiate the search
    btn_search = Button(search_window, text="Search", command=search_food, bg='#D1D1D1', fg='black')
    btn_search.bind("<Enter>", lambda e: btn_search.config(bg="#808080"))
    btn_search.bind("<Leave>", lambda e: btn_search.config(bg="#D1D1D1"))
    btn_search.pack(pady=10)

    btn_back = Button(search_window, text="Back to Food Dashboard", font=('times new roman', 16), command=FoodDashboard, bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='bottom', padx=10)

    # Create a Treeview to display search results
    treeview_search = ttk.Treeview(search_window, columns=("Food ID", "Food Name", "Description", "Price", "Food Type"), show="headings")
    treeview_search.heading("Food ID", text="Food ID")
    treeview_search.heading("Food Name", text="Food Name")
    treeview_search.heading("Description", text="Description")
    treeview_search.heading("Price", text="Price")
    treeview_search.heading("Food Type", text="Food Type")
    treeview_search.pack(pady=10)

    # Run the main loop for the search window
    search_window.mainloop()

def ViewFoodMenu():
    global menu_treeview

    HomeFrame.withdraw()  # Hide the home window
    MenuFrame = Toplevel()
    MenuFrame.title("Food Menu")
    MenuFrame.geometry("1920x1080+0+0")  # window size and position
    MenuFrame.state("zoomed")

    Menu_options_frame = Frame(MenuFrame)
    Menu_options_frame.pack(side="top", pady=20)

    search_frame = Frame(MenuFrame)
    search_frame.pack(side="top", pady=20)

    search_label = Label(search_frame, text="Search Food:", font=('times new roman', 16))
    search_label.pack(side="left", padx=10)

    search_entry = Entry(search_frame, font=('times new roman', 16))
    search_entry.pack(side="left", padx=10)

    search_button = Button(search_frame, text="Search", font=('times new roman', 16), command=lambda: search_food(search_entry.get()),bg='#D1D1D1', fg='black' )
    search_button.bind("<Enter>", lambda e: search_button.config(bg="#808080"))
    search_button.bind("<Leave>", lambda e: search_button.config(bg="#D1D1D1"))
    search_button.pack(side="left", padx=10)

    btn_view_cart = Button(Menu_options_frame, text="View Cart", font=('times new roman', 16), width=15, command=ViewCart, bg='#22B14C', fg='black')
    btn_view_cart.bind("<Enter>", lambda e: btn_view_cart.config(bg="light green"))
    btn_view_cart.bind("<Leave>", lambda e: btn_view_cart.config(bg="#22B14C"))
    btn_view_cart.pack(side="left", padx=10)

    btn_add_to_cart = Button(Menu_options_frame, text="Add to Cart", font=('times new roman', 16), width=15, command=add_to_cart, bg='yellow', fg='black')
    btn_add_to_cart.bind("<Enter>", lambda e: btn_add_to_cart.config(bg="light yellow"))
    btn_add_to_cart.bind("<Leave>", lambda e: btn_add_to_cart.config(bg="yellow"))
    btn_add_to_cart.pack(side="left", padx=10)

    btn_Logout = Button(Menu_options_frame, text="Logout", font=('times new roman', 16), width=15, command=Logout, bg='#7E84F7', fg='black')
    btn_Logout.bind("<Enter>", lambda e: btn_Logout.config(bg="#B8BEED"))
    btn_Logout.bind("<Leave>", lambda e: btn_Logout.config(bg="#7E84F7"))
    btn_Logout.pack(side="left", padx=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 16, 'bold'))  # Change heading font
    style.configure("Treeview", font=('times new roman', 14))  # Change body font

    # Define columns
    columns = ("Food ID", "Food Name", "Description", "Price", "Food Type")

    # Create Treeview widget
    menu_treeview = ttk.Treeview(MenuFrame, columns=columns, show="headings")
    menu_treeview.heading("Food ID", text="Food ID")
    menu_treeview.heading("Food Name", text="Food Name")
    menu_treeview.heading("Description", text="Description")
    menu_treeview.heading("Price", text="Price")
    menu_treeview.heading("Food Type", text="Food Type")

    menu_treeview.pack(fill="both", expand=True)

    # Food type filter buttons
    food_type_frame = Frame(MenuFrame)
    food_type_frame.pack(side="top", pady=20)

    selected_food_type = StringVar(value="all")  # Default to "all"

    btn_all = Radiobutton(food_type_frame, text="All", font=('times new roman', 16), variable=selected_food_type, value="all")
    btn_all.pack(side="left", padx=10)

    btn_spicy = Radiobutton(food_type_frame, text="Spicy", font=('times new roman', 16), variable=selected_food_type, value="spicy")
    btn_spicy.pack(side="left", padx=10)

    btn_normal = Radiobutton(food_type_frame, text="Normal", font=('times new roman', 16), variable=selected_food_type, value="normal")
    btn_normal.pack(side="left", padx=10)

    btn_vegetarian = Radiobutton(food_type_frame, text="Vegetarian", font=('times new roman', 16), variable=selected_food_type, value="vegetarian")
    btn_vegetarian.pack(side="left", padx=10)

    # Apply Filter button
    btn_filter = Button(food_type_frame, text="Apply Filter", font=('times new roman', 16), command=lambda: apply_filter(selected_food_type.get()), bg='#D1D1D1', fg='black')
    btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#808080"))
    btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#D1D1D1"))
    btn_filter.pack(side="left", padx=10)

    def search_food(query):
        # Clear previous search results
        menu_treeview.delete(*menu_treeview.get_children())

        try:
            # Construct the SQL query based on the search query
            sql_query = "SELECT food_id, food_name, description, price, food_type FROM food WHERE food_name LIKE ?"
            cursor.execute(sql_query, ('%' + query + '%',))
            rows = cursor.fetchall()

            # Populate the treeview with fetched data
            for row in rows:
                food_id, food_name, description, price, food_type = row
                menu_treeview.insert("", "end", values=(food_id, food_name, description, price, food_type), tags=(food_id,))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    def apply_filter(food_type):
        # Clear previous search results
        menu_treeview.delete(*menu_treeview.get_children())

        try:
            # Construct the SQL query based on the selected food type
            sql_query = "SELECT food_id, food_name, description, price, food_type FROM food"
            if food_type and food_type != "all":
                sql_query += " WHERE food_type = ?"
                cursor.execute(sql_query, (food_type,))
            else:
                cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Populate the treeview with fetched data
            for row in rows:
                food_id, food_name, description, price, food_type = row
                menu_treeview.insert("", "end", values=(food_id, food_name, description, price, food_type), tags=(food_id,))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    # Populate the treeview with food data from the database
    apply_filter("all")  # Load all data initially

def add_to_cart():
    selected_item = menu_treeview.selection()
    if selected_item:  # Check if an item is selected
        food_id = menu_treeview.item(selected_item[0])["tags"][0]

        # Fetch the food details from the database
        cursor.execute("SELECT food_name, price FROM food WHERE food_id=?", (food_id,))
        food = cursor.fetchone()

        if food:
            food_name, price = food

            # Check if the item is already in the cart
            found_in_cart = False
            for index, item in enumerate(cart):
                if item[0] == food_id:
                    # Update quantity if item already in cart
                    cart[index] = (food_id, food_name, price, item[3] + 1)
                    found_in_cart = True
                    break

            if not found_in_cart:
                # Add new item to cart with quantity 1
                cart.append((food_id, food_name, price, 1))

            messagebox.showinfo("Success", f"{food_name} added to cart!")
            # For debugging: print the current contents of the cart
            print("Cart:", cart)
        else:
            messagebox.showerror("Error", "Failed to add food to cart")
    else:
        messagebox.showerror("Error", "Please select a food item")

def ViewCart():
    def update_total_price():
        total_price = sum(price * quantity for _, _, price, quantity in cart)
        lbl_total_price.config(text=f"Total Price: RM{total_price:.2f}")

    def delete_selected_item():
        selected_item = cart_treeview.selection()
        if selected_item:
            item_index = cart_treeview.index(selected_item[0])
            food_id, food_name, price, quantity = cart[item_index]
            if quantity > 1:
                cart[item_index] = (food_id, food_name, price, quantity - 1)
                cart_treeview.item(selected_item, values=(food_id, food_name, f"RM{price:.2f}", quantity - 1))
            else:
                deleted_item = cart.pop(item_index)
                cart_treeview.delete(selected_item[0])
            update_total_price()
            messagebox.showinfo("Success", f"Item '{food_name}' quantity has been updated in the cart.")
        else:
            messagebox.showerror("Error", "Please select an item to delete.")

    CartFrame = Toplevel()
    CartFrame.title("Shopping Cart")
    CartFrame.geometry("1920x1080+0+0")  # window size and position
    CartFrame.state("zoomed")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 16, 'bold'))  # Change heading font
    style.configure("Treeview", font=('times new roman', 14))  # Change body font

    # Define columns
    columns = ("Food ID", "Food Name", "Price", "Quantity")

    # Create Treeview widget
    cart_treeview = ttk.Treeview(CartFrame, columns=columns, show="headings")
    cart_treeview.heading("Food ID", text="Food ID")
    cart_treeview.heading("Food Name", text="Food Name")
    cart_treeview.heading("Price", text="Price")
    cart_treeview.heading("Quantity", text="Quantity")

    cart_treeview.pack(fill="both", expand=True)

    total_price = 0

    for item in cart:
        food_id, food_name, price, quantity = item
        cart_treeview.insert("", "end", values=(food_id, food_name, f"RM{price:.2f}", quantity))

    lbl_total_price = Label(CartFrame,
                            text=f"Total Price: RM{sum(price * quantity for _, _, price, quantity in cart):.2f}",
                            font=('times new roman', 16))
    lbl_total_price.pack(pady=10)

    # Create a frame for the buttons
    button_frame = Frame(CartFrame)
    button_frame.pack(side="bottom", pady=20)

    btn_delete = Button(button_frame, text="Delete Order", font=('times new roman', 16), command=delete_selected_item, bg='red', fg='white')
    btn_delete.bind("<Enter>", lambda e: btn_delete.config(bg="#FF8080"))
    btn_delete.bind("<Leave>", lambda e: btn_delete.config(bg="red"))
    btn_delete.pack(side="left", padx=10)

    btn_checkout = Button(button_frame, text="Place Order", font=('times new roman', 16), command=lambda: place_order(lbl_total_price.cget("text"), CartFrame), bg='#611BD1', fg='white')
    btn_checkout.bind("<Enter>", lambda e: btn_checkout.config(bg="#893FFF"))
    btn_checkout.bind("<Leave>", lambda e: btn_checkout.config(bg="#611BD1"))
    btn_checkout.pack(side="left", padx=10)

    btn_back = Button(button_frame, text="Back to Menu", font=('times new roman', 16), command=CartFrame.destroy, bg='#3580BB', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#48AFFF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#3580BB"))
    btn_back.pack(side="right", padx=10)

def place_order(total_price, cart_window):
    try:
        # Insert order details into the order table
        order_date = datetime.now().strftime("%Y-%m-%d")
        order_id = None
        for item in cart:
            food_id, _, price, quantity = item
            cursor.execute("INSERT INTO `order` (order_date, food_id, quantity, total_price) VALUES (?, ?, ?, ?)",
                           (order_date, food_id, quantity, price * quantity))
            order_id = cursor.lastrowid  # Get the last inserted order_id
        conn.commit()

        messagebox.showinfo("Success", "Order placed successfully!")
        cart_window.destroy()
        open_payment_window(total_price, order_id)  # Ensure this line is reached after the order is placed
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error placing order: {e}")

def open_payment_window(total_price, order_id):
    PaymentWindow = Toplevel()
    PaymentWindow.title("Payment")
    PaymentWindow.geometry("400x200")

    formatted_total_price = "RM{:.2f}".format(
        float(total_price.split("RM")[1]))  # Extract numerical part of total_price
    Label(PaymentWindow, text=f"Total Amount to Pay: {formatted_total_price}", font=('times new roman', 16)).pack(
        pady=10)

    pay_button = Button(PaymentWindow, text="Pay",command=lambda: process_payment(float(total_price.split("RM")[1]), PaymentWindow, order_id), bg='#0010A3', fg='white')
    pay_button.bind("<Enter>", lambda e: pay_button.config(bg="#0018F2"))
    pay_button.bind("<Leave>", lambda e: pay_button.config(bg="#0010A3"))
    pay_button.pack(pady=10)

def process_payment(total_price, payment_window, order_id):
    try:
        # Insert payment details into the payment table
        payment_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO payment (order_id, total_price, payment_date) VALUES (?, ?, ?)",
                       (order_id, total_price, payment_date))
        conn.commit()

        messagebox.showinfo("Success", "Payment processed successfully!")
        payment_window.destroy()
        open_review_window()

        # Clear the cart
        cart.clear()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error processing payment: {e}")

def open_review_window():
    review_window = Toplevel()
    review_window.title("Review and Rating")
    review_window.geometry("400x200")

    review_label = Label(review_window, text="Leave a review:")
    review_label.pack()

    review_text = Text(review_window, height=4, width=40)
    review_text.pack()

    rating_label = Label(review_window, text="Rating (1-5):")
    rating_label.pack()

    rating_entry = Entry(review_window)
    rating_entry.pack()

    submit_button = Button(review_window, text="Submit", command=lambda: submit_review_rating(review_text.get("1.0", END), rating_entry.get(), review_window), bg='#377E47', fg='white')
    submit_button.bind("<Enter>", lambda e: submit_button.config(bg="#5CD477"))
    submit_button.bind("<Leave>", lambda e: submit_button.config(bg="#377E47"))
    submit_button.pack()

def submit_review_rating(review, rating, review_window):
    try:
        rating_value = int(rating)
        if rating_value < 1 or rating_value > 5:
            messagebox.showerror("Error", "Rating must be between 1 and 5")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid rating. Please enter a number.")
        return

    customer_id = 1  # This should be dynamically fetched or passed
    review_date = datetime.now().strftime("%Y-%m-%d")

    try:
        cursor.execute("INSERT INTO review (customer_id, review, rating, review_date) VALUES (?, ?, ?, ?)",
                       (customer_id, review, rating_value, review_date))
        conn.commit()

        messagebox.showinfo("Success", "Thank you for your review and rating!")
        review_window.destroy()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error saving review: {e}")

def view_total_orders():
    try:
        # SQL query to calculate total orders and total cost per month
        query = """
            SELECT strftime('%Y-%m', order_date) AS month_year, COUNT(*) AS total_orders, SUM(total_price) AS total_cost
            FROM `order`
            GROUP BY strftime('%Y-%m', order_date)
            ORDER BY strftime('%Y-%m', order_date)
        """

        # Execute the query
        cursor.execute(query)
        result = cursor.fetchall()

        # Display the results
        display_total_orders(result)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching total orders: {e}")

# Function to display total orders and total cost per month
def display_total_orders(results):
    # Create a new window to display the results
    total_orders_window = Toplevel()
    total_orders_window.title("Total Orders and Total Cost Per Month")
    total_orders_window.geometry("1920x1080+0+0")  # window size and position
    total_orders_window.state("zoomed")

    # Create a treeview to display the results
    tree = ttk.Treeview(total_orders_window, columns=("Month", "Total Orders", "Total Cost"), show="headings")
    tree.heading("Month", text="Month")
    tree.heading("Total Orders", text="Total Orders")
    tree.heading("Total Cost", text="Total Cost")

    tree.column("Month", width=100, anchor="center")
    tree.column("Total Orders", width=100, anchor="center")
    tree.column("Total Cost", width=100, anchor="center")

    # Insert data into the treeview
    for row in results:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

    btn_back = Button(total_orders_window, text="Back to Admin Panel", font=('times new roman', 16), command=AdminPanel, bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='bottom', padx=10)

def view_review_rating():
    try:
        # SQL query to retrieve all customer reviews and ratings
        query = """
            SELECT review, rating
            FROM review
        """

        # Execute the query
        cursor.execute(query)
        result = cursor.fetchall()

        # Display the results
        display_view_review_rating(result)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching reviews and ratings: {e}")

# Function to display customer reviews and ratings
def display_view_review_rating(results):
    # Create a new window to display the results
    review_window = Toplevel()
    review_window.title("Customer Review and Rating")
    review_window.geometry("1920x1080+0+0")  # window size and position
    review_window.state("zoomed")

    # Create a treeview to display the results
    tree = ttk.Treeview(review_window, columns=("Review", "Rating"), show="headings")
    tree.heading("Review", text="Review")
    tree.heading("Rating", text="Rating")

    tree.column("Review", width=100, anchor="center")
    tree.column("Rating", width=100, anchor="center")

    # Insert data into the treeview
    for row in results:
        tree.insert("", "end", values=row)

    tree.pack(expand=True, fill="both")

    btn_back = Button(review_window, text="Back to Admin Panel", font=('times new roman', 16), command=AdminPanel, bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='bottom', padx=10)

def Logout():
    result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
    if result == 'yes':
        # Clear the cart
        cart.clear()
        # Close the current window
        root.deiconify()
        HomeFrame.withdraw()

def LogoutAdmin():
    root.deiconify()  # Show the main login window again
    AdminPanelFrame.destroy()  # Close the admin panel window

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root, bg='light blue')
    LoginFrame.pack(side='top', pady=80)

    lbl_title = Label(LoginFrame, text="Login:", font=('times new roman', 20, 'bold'), bd=18, bg='light blue')
    lbl_title.grid(row=0, columnspan=1)

    lbl_username = Label(LoginFrame, text="Username:", font=('times new roman', 16), bd=18, bg='light blue')
    lbl_username.grid(row=1, column=0)

    lbl_password = Label(LoginFrame, text="Password:", font=('times new roman', 16), bd=18, bg='light blue')
    lbl_password.grid(row=2, column=0)

    username = Entry(LoginFrame, font=('times new roman', 16), textvariable=USERNAME_LOGIN, width=15)
    username.grid(row=1, column=1)

    password = Entry(LoginFrame, font=('times new roman', 16), textvariable=PASSWORD_LOGIN, width=15, show="*")
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('times new roman', 16), width=20, command=Login, bg='blue', fg='white',relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="light green"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="blue"))
    btn_login.grid(row=4, columnspan=2, pady=30)

    lbl_text = Label(LoginFrame, text="Not a member?", font=('times new roman', 14), bg='light blue')
    lbl_text.grid(row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register Now", fg="green", font=('arial', 12), bg='light blue')
    lbl_register.bind('<Enter>', lambda event, label=lbl_register: label.config(font=('arial', 12, 'underline')))
    lbl_register.bind('<Leave>', lambda event, label=lbl_register: label.config(font=('arial', 12)))
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register.grid(row=6, columnspan=2)

def RegisterForm():
    global RegisterFrame, lbl_result2, confirm_password_entry
    RegisterFrame = Frame(root, bg='light blue')
    RegisterFrame.pack(side='top', pady=60)

    lbl_login = Label(RegisterFrame, text="Click to Login", fg="green", font=('arial', 12), bg='light blue')
    lbl_login.grid(row=11, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)

    lbl_result2 = Label(RegisterFrame, text="Registration Form:", font=('times new roman', 20, 'bold'), bd=18, bg='light blue')
    lbl_result2.grid(row=1, columnspan=2)

    lbl_username = Label(RegisterFrame, text="Username:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_username.grid(row=2)

    lbl_password = Label(RegisterFrame, text="Password:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_password.grid(row=3)

    lbl_confirm_password = Label(RegisterFrame, text="Confirm Password:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_confirm_password.grid(row=4)

    lbl_firstname = Label(RegisterFrame, text="First Name:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_firstname.grid(row=5)

    lbl_lastname = Label(RegisterFrame, text="Last Name:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_lastname.grid(row=6)

    lbl_date_of_birth = Label(RegisterFrame, text="Date of Birth:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_date_of_birth.grid(row=7)

    lbl_email_address = Label(RegisterFrame, text="Email Address:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_email_address.grid(row=8)

    lbl_phone_number = Label(RegisterFrame, text="Phone number:", font=('times new roman', 15), bd=18, bg='light blue')
    lbl_phone_number.grid(row=9)

    username = Entry(RegisterFrame, font=('times new roman', 15), textvariable=USERNAME_REGISTER, width=15)
    username.grid(row=2, column=1)

    password = Entry(RegisterFrame, font=('times new roman', 15), textvariable=PASSWORD_REGISTER, width=15, show="*")
    password.grid(row=3, column=1)

    confirm_password_entry = Entry(RegisterFrame, font=('times new roman', 15), width=15, show="*")
    confirm_password_entry.grid(row=4, column=1)

    firstname = Entry(RegisterFrame, font=('times new roman', 15), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=5, column=1)

    lastname = Entry(RegisterFrame, font=('times new roman', 15), textvariable=LASTNAME, width=15)
    lastname.grid(row=6, column=1)

    date_of_birth = Entry(RegisterFrame, font=('times new roman', 15), textvariable=DATE_OF_BIRTH, width=15)
    date_of_birth.grid(row=7, column=1)

    email_address = Entry(RegisterFrame, font=('times new roman', 15), textvariable=EMAIL_ADDRESS, width=15)
    email_address.grid(row=8, column=1)

    phone_number = Entry(RegisterFrame, font=('times new roman', 15), textvariable=PHONE_NUMBER, width=15)
    phone_number.grid(row=9, column=1)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 14), width=20, command=Register, bg='blue', fg='white', relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="light green"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="blue"))
    btn_login.grid(row=10, columnspan=2, pady=20)

def ToggleToLogin(event=None):  # switching from register to login page.
    if RegisterFrame is not None:
        RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):  # switching the interface from login to register after user click the register link
    if LoginFrame is not None:  # if login form is display, then need to deleted and switch to registration form
        LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    if (USERNAME_REGISTER.get() == "" or PASSWORD_REGISTER.get() == "" or
            FIRSTNAME.get() == "" or LASTNAME.get() == "" or
            confirm_password_entry.get() == "" or DATE_OF_BIRTH.get() == "" or
        EMAIL_ADDRESS.get() == "" or PHONE_NUMBER.get() == ""):
        messagebox.showerror("Error", "Please complete all the required fields!")
    elif PASSWORD_REGISTER.get() != confirm_password_entry.get():
        messagebox.showerror("Error", "Password and Confirm Password do not match!")
    else:
        try:
            cursor.execute("SELECT * FROM `customer` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
            else:
                cursor.execute(
                    "INSERT INTO `customer` (username, password, firstname, lastname, date_of_birth, email_address, phone_number) VALUES(?, ?, ?, ?, ?, ?, ?)",
                    (str(USERNAME_REGISTER.get()), str(PASSWORD_REGISTER.get()), str(FIRSTNAME.get()),
                     str(LASTNAME.get()), str(DATE_OF_BIRTH.get()), str(EMAIL_ADDRESS.get()), str(PHONE_NUMBER.get())))
                conn.commit()  # save current data to database
                USERNAME_REGISTER.set("")
                PASSWORD_REGISTER.set("")
                FIRSTNAME.set("")
                LASTNAME.set("")
                DATE_OF_BIRTH.set("")
                EMAIL_ADDRESS.set("")
                PHONE_NUMBER.set("")
                confirm_password_entry.delete(0, 'end')  # Clear confirm password field
                messagebox.showinfo("Success", "You Successfully Registered. Click to Login")
        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error occurred during registration: {}".format(e))

def Login():
    Database()
    if USERNAME_LOGIN.get() == "" or PASSWORD_LOGIN.get() == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `customer` WHERE `username` = ? and `password` = ?",
                       (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        if cursor.fetchone() is not None:
            messagebox.showinfo("Success", "You Successfully Login")
            Home()
        else:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? and `password` = ?",
                           (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
            if cursor.fetchone() is not None:
                messagebox.showinfo("Success", "You Successfully Login")
                AdminPanel()
            else:
                messagebox.showerror("Error", "Invalid username or password")


LoginForm()

if __name__ == '__main__':
    root.mainloop()

