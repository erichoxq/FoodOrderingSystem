import sqlite3
import tkinter.messagebox as messagebox
from tkinter import ttk, Radiobutton, Tk, StringVar, Toplevel, Frame, Label, Entry, Button, Text, Scrollbar, VERTICAL, filedialog, END, IntVar, Canvas, Menu
from datetime import datetime
from PIL import Image, ImageTk
from fpdf import FPDF
import os, webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root = Tk()
root.title("Register and Login System")
root.geometry("1920x1080+0+0")  # window size and position
root.config()  # used to customize the window (bg colour, title)
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

conn = sqlite3.connect("db_food_ordering_system.db")  # connection to database
cursor = conn.cursor()  # use to execute the sql queries and fetch results from db

# Initialize Cart
cart = []

# Global variables to store the logged-in user's information
logged_in_user = {}


def Database():
    global conn, cursor
    conn = sqlite3.connect("db_food_ordering_system.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `customer` (customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20), "
        "password TEXT(20), firstname TEXT(20), lastname TEXT(20), date_of_birth DATE, email_address TEXT(30), phone_number TEXT(20))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `food` (food_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, food_name TEXT(30), "
        "description TEXT(50), price FLOAT, food_category TEXT(10),food_calories INTEGER, image_path TEXT, admin_id INTEGER, FOREIGN KEY(admin_id) REFERENCES admin(admin_id) )")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `review` (review_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customer_id INTEGER,"
        "review TEXT(20),rating INTEGER, review_date DATE, FOREIGN KEY (customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `payment` (payment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, payment_date DATE, "
        "order_id INTEGER, total_price FLOAT,total_amount FLOAT, FOREIGN KEY(order_id) REFERENCES orders(order_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `order` (order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, order_date DATE, "
        "total_price FLOAT, total_food_calories INTEGER, customer_id INTEGER, FOREIGN KEY(customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `orderitem` (order_item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,order_id INTEGER, food_id INTEGER, "
        "quantity INTEGER, total_price FLOAT, total_food_calories INTEGER, customer_id INTEGER, FOREIGN KEY(food_id) REFERENCES food(food_id), FOREIGN KEY(customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `admin`(admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20), "
        "password TEXT(20), firstname TEXT(20), lastname TEXT(20), date_of_birth DATE, email_address TEXT(30), phone_number TEXT(20))")

def Exit():
    result = messagebox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()

def Home():
    global HomeFrame

    def Logout():
        result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
        if result == 'yes':
            # Clear the cart
            cart.clear()
            # Close the current window
            HomeFrame.destroy()
            # Show the root window
            root.deiconify()

    # Hide the login window
    root.withdraw()

    # Create a Toplevel window for the home screen
    HomeFrame = Toplevel()
    HomeFrame.title("Home")
    HomeFrame.geometry("1920x1080+0+0")  # window size and position
    HomeFrame.state("zoomed")

    # Load the background image
    image = Image.open("homepage.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(HomeFrame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    lbl_home = Label(HomeFrame, text="WELCOME TO BOOGY RESTAURANT", font=('Algerian', 30, 'bold','italic'),fg='#3580BB',
                     highlightbackground="black", highlightcolor="black", highlightthickness=2)
    lbl_home.pack(pady=50)

    btn_view_menu = Button(HomeFrame, text="Food Menu", font=('times new roman', 16), width=20, command=ViewFoodMenu,
                           bg='green', fg='white', relief='raised')
    btn_view_menu.bind("<Enter>", lambda e: btn_view_menu.config(bg="light green"))
    btn_view_menu.bind("<Leave>", lambda e: btn_view_menu.config(bg="green"))
    btn_view_menu.pack(pady=20)

    btn_view_order_history = Button(HomeFrame, text="View Order History", font=('times new roman', 16), width=20,
                                    command=ViewOrderHistory, bg='blue', fg='white', relief='raised')
    btn_view_order_history.bind("<Enter>", lambda e: btn_view_order_history.config(bg="light blue"))
    btn_view_order_history.bind("<Leave>", lambda e: btn_view_order_history.config(bg="blue"))
    btn_view_order_history.pack(pady=20)

    btn_calculate_bmi = Button(HomeFrame, text="Calculate BMI", font=('times new roman', 16), width=20,command=bmi_window, bg='#EDCC4B', fg='white',relief='raised')
    btn_calculate_bmi.bind("<Enter>", lambda e: btn_calculate_bmi.config(bg="#FFDC51"))
    btn_calculate_bmi.bind("<Leave>", lambda e: btn_calculate_bmi.config(bg="#EDCC4B"))
    btn_calculate_bmi.pack(pady=20)

    btn_logout = Button(HomeFrame, text="Logout", font=('times new roman', 16), width=20, command=Logout, bg='#7E84F7',
                        fg='white', relief='raised')
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#B8BEED"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg="#7E84F7"))
    btn_logout.pack(pady=20)

    # Keep a reference to the image object to prevent garbage collection
    HomeFrame.image = bg_image

def AdminPanel():
    global AdminPanelFrame

    def Logout():
        result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
        if result == 'yes':
            # Clear the cart
            cart.clear()
            # Close the current window
            AdminPanelFrame.destroy()
            # Show the root window
            root.deiconify()

    # Hide the main login window
    root.withdraw()

    # Create a Toplevel window for the admin panel
    AdminPanelFrame = Toplevel()
    AdminPanelFrame.title("Admin Panel")
    AdminPanelFrame.geometry("1920x1080+0+0")  # window size and position
    AdminPanelFrame.state("zoomed")

    # Load the background image
    image = Image.open("adminpanel.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(AdminPanelFrame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    lbl_admin_panel = Label(AdminPanelFrame, text="WELCOME TO ADMIN PANEL", font=('Algerian', 30, 'bold','italic'), fg='#3580BB',
                            highlightbackground="black", highlightcolor="black", highlightthickness=2)
    lbl_admin_panel.pack(pady=20)

    btn_food_dashboard = Button(AdminPanelFrame, text="Food Dashboard", font=('times new roman', 16), width=20,
                                command=FoodDashboard, bg='#65D954', fg='white')
    btn_food_dashboard.bind("<Enter>", lambda e: btn_food_dashboard.config(bg="#77FF63"))
    btn_food_dashboard.bind("<Leave>", lambda e: btn_food_dashboard.config(bg="#65D954"))
    btn_food_dashboard.pack(pady=10)

    btn_view_review_rating = Button(AdminPanelFrame, text="View Review and Rating", font=('times new roman', 16),
                                    width=20, command=view_review_rating, bg='#E0B715', fg='white')
    btn_view_review_rating.bind("<Enter>", lambda e: btn_view_review_rating.config(bg="#FACC18"))
    btn_view_review_rating.bind("<Leave>", lambda e: btn_view_review_rating.config(bg="#E0B715"))
    btn_view_review_rating.pack(pady=10)

    btn_view_total_orders = Button(AdminPanelFrame, text="View Total Orders", font=('times new roman', 16), width=20,
                                   command=view_total_orders, bg='#840BC7', fg='white')
    btn_view_total_orders.bind("<Enter>", lambda e: btn_view_total_orders.config(bg="#AA0EFF"))
    btn_view_total_orders.bind("<Leave>", lambda e: btn_view_total_orders.config(bg="#840BC7"))
    btn_view_total_orders.pack(pady=10)

    btn_logout_admin = Button(AdminPanelFrame, text="Logout", font=('times new roman', 16), width=20,
                              command=Logout, bg='#7E84F7', fg='white')
    btn_logout_admin.bind("<Enter>", lambda e: btn_logout_admin.config(bg="#B8BEED"))
    btn_logout_admin.bind("<Leave>", lambda e: btn_logout_admin.config(bg="#7E84F7"))
    btn_logout_admin.pack(pady=10)

    # Keep a reference to the image object to prevent garbage collection
    AdminPanelFrame.image = bg_image

def add_food_window():
    # Create a new window for adding food
    add_food_window = Toplevel()
    add_food_window.title("Add Food")
    add_food_window.geometry("1920x1080+0+0")  # window size and position
    add_food_window.state("zoomed")
    add_food_window.configure(bg="#FFEC92")

    # Define the layout of the window
    frame = Frame(add_food_window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    frame.pack(side="top", anchor="center", padx=20, pady=20)

    label_food_name = Label(frame, text="Food Name:", font=('times new roman', 16))
    label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_food_name = Entry(frame, font=('times new roman', 16))
    entry_food_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    label_description = Label(frame, text="Food Description:", font=('times new roman', 16))
    label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    entry_description = Entry(frame, font=('times new roman', 16))
    entry_description.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    label_price = Label(frame, text="Price:", font=('times new roman', 16))
    label_price.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_price = Entry(frame, font=('times new roman', 16))
    entry_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    label_food_category = Label(frame, text="Food Category:", font=('times new roman', 16))
    label_food_category.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    # Use Combobox for food category
    food_categories = ["Breakfast", "Lunch", "Dinner", "Drinks", "Dessert"]
    combo_food_category = ttk.Combobox(frame, values=food_categories, font=('times new roman', 16))
    combo_food_category.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    label_food_calories = Label(frame, text="Food Calories:", font=('times new roman', 16))
    label_food_calories.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    entry_food_calories = Entry(frame, font=('times new roman', 16))
    entry_food_calories.grid(row=4, column=1, padx=10, pady=10, sticky="w")

    # Image upload section
    label_image_path = Label(frame, text="Image Path:", font=('times new roman', 16))
    label_image_path.grid(row=5, column=0, padx=10, pady=10, sticky="e")
    entry_image_path = Entry(frame, font=('times new roman', 16))
    entry_image_path.grid(row=5, column=1, padx=10, pady=10, sticky="w")

    image_label = Label(frame)
    image_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

    # Create a button to add the food
    btn_select_image = Button(frame, text="Select Image", font=('times new roman', 16),
                              command=lambda: select_image(entry_image_path, image_label), bg='#6DA397', fg='white')
    btn_select_image.bind("<Enter>", lambda e: btn_select_image.config(bg="#92DBCA"))
    btn_select_image.bind("<Leave>", lambda e: btn_select_image.config(bg="#6DA397"))
    btn_select_image.grid(row=6, columnspan=2, pady=20)

    btn_add_food = Button(frame, text="Add Food", font=('times new roman', 16), command=lambda: [add_food(entry_food_name, entry_description, entry_price, combo_food_category, entry_food_calories, entry_image_path),add_food_window.destroy()], bg='#E69312', fg='white')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFA314"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.grid(row=7, columnspan=2, pady=20)

    btn_back = Button(frame, text="Back to Dashboard", font=('times new roman', 16), command=lambda:[add_food_window.destroy(),FoodDashboard],
                      bg='#7E84F7', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B8BEED"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#7E84F7"))
    btn_back.grid(row=8, columnspan=2, pady=20)

def select_image(entry_image_path, image_label):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        entry_image_path.delete(0, END)
        entry_image_path.insert(0, file_path)

        image = Image.open(file_path)
        image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

def FoodDashboard():
    global food_treeview

    def apply_filter(food_category):
        # Clear previous search results
        food_treeview.delete(*food_treeview.get_children())

        try:
            # Construct the SQL query based on the selected food type
            sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food"
            if food_category and food_category != "all":
                sql_query += f" WHERE food_category = '{food_category}'"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Populate the treeview with fetched data
            for row in rows:
                food_id, food_name, description, price, food_category, food_calories, image_path = row
                food_treeview.insert("", "end", values=(
                food_id, food_name, description, price, food_category, food_calories, image_path), tags=(food_id,))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    def search_food(query):
        # Clear previous search results
        food_treeview.delete(*food_treeview.get_children())

        try:
            # Construct the SQL query based on the search query
            sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_name LIKE ?"
            cursor.execute(sql_query, ('%' + query + '%',))
            rows = cursor.fetchall()

            # Populate the treeview with fetched data
            for row in rows:
                food_id, food_name, description, price, food_category, food_calories, image_path = row
                food_treeview.insert("", "end", values=(
                food_id, food_name, description, price, food_category, food_calories, image_path), tags=(food_id,))
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    def on_food_select(event):
        selected_item = food_treeview.selection()
        if selected_item:
            item = food_treeview.item(selected_item)
            image_path = item['values'][6]  # The image_path is in the 7th column (index 6)
            food_name = item['values'][1]  # The food_name is in the 2nd column (index 1)
            try:
                image = Image.open(image_path)
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                image_label.config(image=photo)
                image_label.image = photo
                food_name_label.config(text=food_name)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {e}")

    def Logout():
        result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
        if result == 'yes':
            # Clear the cart
            cart.clear()
            # Close the current window
            FoodFrame.destroy()
            # Show the root window
            root.deiconify()

    def back_to_admin_panel():
        result = messagebox.askquestion('System', 'Are you sure you want to return to the admin panel?', icon="warning")
        if result == 'yes':
            # Close the current window
            FoodFrame.destroy()
            # Show the Admin Panel
            AdminPanel()

    AdminPanelFrame.withdraw()  # Hide the AdminPanelFrame

    FoodFrame = Toplevel()
    FoodFrame.title("Food Dashboard")
    FoodFrame.geometry("1920x1080+0+0")  # window size and position
    FoodFrame.state("zoomed")
    FoodFrame.configure(bg="#C4FF7E")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), foreground="#148699")

    # Create a frame to contain the food options buttons
    food_options_frame = Frame(FoodFrame, bg="#C4FF7E")
    food_options_frame.pack(side="top", pady=20)

    # Create the food options buttons
    search_frame = Frame(FoodFrame, bg="#C4FF7E")
    search_frame.pack(side="top", pady=20)

    search_label = Label(search_frame, text="Search Food:", font=('times new roman', 16), bg="#C4FF7E")
    search_label.pack(side="left", padx=10)

    search_entry = Entry(search_frame, font=('times new roman', 16))
    search_entry.pack(side="left", padx=10)

    search_button = Button(search_frame, text="Search", font=('times new roman', 16),
                           command=lambda: search_food(search_entry.get()), bg='#D1D1D1', fg='black')
    search_button.bind("<Enter>", lambda e: search_button.config(bg="#808080"))
    search_button.bind("<Leave>", lambda e: search_button.config(bg="#D1D1D1"))
    search_button.pack(side="left", padx=10)

    btn_add_food = Button(food_options_frame, text="Add Food", font=('times new roman', 16), width=15,
                          command=add_food_window, bg='#E69312', fg='white', relief='raised')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFA314"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.pack(side="left", padx=10)

    btn_delete_food = Button(food_options_frame, text="Delete Food", font=('times new roman', 16), width=15,
                             command=delete_food, bg='red', fg='white', relief='raised')
    btn_delete_food.bind("<Enter>", lambda e: btn_delete_food.config(bg="#FF8080"))
    btn_delete_food.bind("<Leave>", lambda e: btn_delete_food.config(bg="red"))
    btn_delete_food.pack(side="left", padx=10)

    btn_update_food = Button(food_options_frame, text="Update Food", font=('times new roman', 16), width=15,
                             command=update_food_window, bg='green', fg='white')
    btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="light green"))
    btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="green"))
    btn_update_food.pack(side="left", padx=10)

    btn_back = Button(food_options_frame, text="Back to Admin Panel", font=('times new roman', 16), command=back_to_admin_panel,
                      bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side="left", padx=10)

    btn_Logout = Button(food_options_frame, text="Logout", font=('times new roman', 16), width=15, command=Logout,
                        bg='#7E84F7', fg='white')
    btn_Logout.bind("<Enter>", lambda e: btn_Logout.config(bg="#B8BEED"))
    btn_Logout.bind("<Leave>", lambda e: btn_Logout.config(bg="#7E84F7"))
    btn_Logout.pack(side="left", padx=10)

    # Food type filter buttons
    food_category_frame = Frame(FoodFrame, bg="#C4FF7E")
    food_category_frame.pack(side="bottom", pady=20)

    selected_food_category = StringVar(value="all")  # Default to "all"

    btn_all = Radiobutton(food_category_frame, text="All", font=('times new roman', 16), variable=selected_food_category,
                          value="all", bg="#C4FF7E")
    btn_all.pack(side="left", padx=10)

    btn_breakfast = Radiobutton(food_category_frame, text="Breakfast", font=('times new roman', 16), variable=selected_food_category,
                            value="Breakfast", bg="#C4FF7E")
    btn_breakfast.pack(side="left", padx=10)

    btn_lunch = Radiobutton(food_category_frame, text="Lunch", font=('times new roman', 16), variable=selected_food_category,
                             value="Lunch", bg="#C4FF7E")
    btn_lunch.pack(side="left", padx=10)

    btn_dinner = Radiobutton(food_category_frame, text="Dinner", font=('times new roman', 16),
                                 variable=selected_food_category, value="Dinner", bg="#C4FF7E")
    btn_dinner.pack(side="left", padx=10)

    btn_drinks = Radiobutton(food_category_frame, text="Drinks", font=('times new roman', 16),
                             variable=selected_food_category, value="Drinks", bg="#C4FF7E")
    btn_drinks.pack(side="left", padx=10)

    btn_dessert = Radiobutton(food_category_frame, text="Dessert", font=('times new roman', 16),
                             variable=selected_food_category, value="Dessert", bg="#C4FF7E")
    btn_dessert.pack(side="left", padx=10)

    # Apply Filter button
    btn_filter = Button(food_category_frame, text="Apply Filter", font=('times new roman', 16),
                        command=lambda: apply_filter(selected_food_category.get()), bg='#D1D1D1', fg='black')
    btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#808080"))
    btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#D1D1D1"))
    btn_filter.pack(side="left", padx=10)

    # Define columns
    columns = ("Food ID", "Food Name", "Description", "Price", "Food Categories", "Food Calories", "Image Path")

    # Create a Treeview widget to display food items
    food_treeview = ttk.Treeview(FoodFrame, columns=columns, show='headings', style="Treeview")
    food_treeview.heading("Food ID", text="Food ID")
    food_treeview.heading("Food Name", text="Food Name")
    food_treeview.heading("Description", text="Description")
    food_treeview.heading("Price", text="Price")
    food_treeview.heading("Food Categories", text="Food Categories")
    food_treeview.heading("Food Calories", text="Food Calories")
    food_treeview.heading("Image Path", text="Image Path")

    food_treeview.column("Food ID", width=100, anchor="center")
    food_treeview.column("Food Name", width=150, anchor="center")
    food_treeview.column("Description", width=300, anchor="center")
    food_treeview.column("Price", width=100, anchor="center")
    food_treeview.column("Food Categories", width=150, anchor="center")
    food_treeview.column("Food Calories", width=150, anchor="center")
    food_treeview.column("Image Path", width=150, anchor="center")

    food_treeview.pack(side="left", padx=20, pady=20, fill="y")

    # Add vertical scrollbar to the treeview
    sb = Scrollbar(FoodFrame, orient=VERTICAL, command=food_treeview.yview)
    food_treeview.config(yscrollcommand=sb.set)
    food_treeview.pack(side="left", fill="both")
    sb.pack(side="left", fill="y")

    # Bind the selection event to the treeview
    food_treeview.bind("<<TreeviewSelect>>", on_food_select)

    # Frame to hold image and food name label
    display_frame = Frame(FoodFrame, bg="#C4FF7E")
    display_frame.pack(side="left", padx=20, pady=20, anchor="nw")

    # Label to display selected food item image
    image_label = Label(display_frame, bg="#C4FF7E")
    image_label.pack(pady=20)

    # Label to display selected food item name
    food_name_label = Label(display_frame, font=('times new roman', 16), bg="#C4FF7E")
    food_name_label.pack(pady=10)

    # Initially, populate the treeview with all food items
    apply_filter("all")

def add_food(entry_food_name, entry_description, entry_price, combo_food_category, entry_food_calories, entry_image_path):
    # Get the values entered by the user
    food_name = entry_food_name.get()
    description = entry_description.get()
    price = entry_price.get()
    food_category = combo_food_category.get()
    food_calories = entry_food_calories.get()
    image_path = entry_image_path.get()

    # Check if all fields are filled
    if food_name and description and price and food_category and food_calories and image_path:
        try:
            # Fetch the admin ID based on the logged-in user information
            query = """
                        SELECT admin_id
                        FROM admin
                        WHERE username = ? AND password = ?
                    """
            cursor.execute(query, (logged_in_user['username'], logged_in_user['password']))
            admin_data = cursor.fetchone()

            if not admin_data:
                raise sqlite3.Error("Admin not found")

            admin_id = admin_data[0]
            # Insert the food details into the database
            cursor.execute(
                "INSERT INTO food (food_name, description, price, food_category, food_calories, image_path, admin_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (food_name, description, price, food_category, food_calories, image_path, admin_id))
            conn.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Food successfully added!")

            # Fetch data from the database and update the food_treeview
            update_food_treeview()


        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error adding food: {e}")
    else:
        messagebox.showerror("Error", "Please fill in all fields!")

def update_food_window():
    # Get the selected food_id
    food_id = get_selected_food_id()

    if food_id:
        try:
            cursor.execute(
                "SELECT food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_id=?",
                (food_id,))
            food_details = cursor.fetchone()
            if food_details:
                update_food_window = Toplevel()
                update_food_window.title("Update Food")
                update_food_window.geometry("1920x1080+0+0")  # window size and position
                update_food_window.state("zoomed")
                update_food_window.configure(bg="#9AF4F5")

                frame = Frame(update_food_window, highlightbackground="black", highlightcolor="black",
                                           highlightthickness=2)
                frame.pack(side="top", anchor="center", padx=20, pady=20)

                label_food_name = Label(frame, text="Food Name:", font=('times new roman', 16))
                label_food_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
                entry_food_name = Entry(frame, font=('times new roman', 16))
                entry_food_name.grid(row=0, column=1, padx=10, pady=10, sticky="w")
                entry_food_name.insert(0, food_details[0])

                label_description = Label(frame, text="Food Description:", font=('times new roman', 16))
                label_description.grid(row=1, column=0, padx=10, pady=10, sticky="e")
                entry_description = Entry(frame, font=('times new roman', 16))
                entry_description.grid(row=1, column=1, padx=10, pady=10, sticky="w")
                entry_description.insert(0, food_details[1])

                label_price = Label(frame, text="Price:", font=('times new roman', 16))
                label_price.grid(row=2, column=0, padx=10, pady=10, sticky="e")
                entry_price = Entry(frame, font=('times new roman', 16))
                entry_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")
                entry_price.insert(0, food_details[2])

                label_food_category = Label(frame, text="Food Category:", font=('times new roman', 16))
                label_food_category.grid(row=3, column=0, padx=10, pady=10, sticky="e")

                # Use Combobox for food category
                food_categories = ["Breakfast", "Lunch", "Dinner", "Drinks", "Dessert"]
                combo_food_category = ttk.Combobox(frame, values=food_categories, font=('times new roman', 16))
                combo_food_category.grid(row=3, column=1, padx=10, pady=10, sticky="w")
                combo_food_category.set(food_details[3])  # Set the current category

                label_food_calories = Label(frame, text="Food Calories:", font=('times new roman', 16))
                label_food_calories.grid(row=4, column=0, padx=10, pady=10, sticky="e")
                entry_food_calories = Entry(frame, font=('times new roman', 16))
                entry_food_calories.grid(row=4, column=1, padx=10, pady=10, sticky="w")
                entry_food_calories.insert(0, food_details[4])

                label_image_path = Label(frame, text="Image Path:", font=('times new roman', 16))
                label_image_path.grid(row=5, column=0, padx=10, pady=10, sticky="e")
                entry_image_path = Entry(frame, font=('times new roman', 16))
                entry_image_path.grid(row=5, column=1, padx=10, pady=10, sticky="w")
                entry_image_path.insert(0, food_details[5])

                image_label = Label(frame)
                image_label.grid(row=0, column=2, rowspan=6, padx=10, pady=10)
                if food_details[5]:
                    image = Image.open(food_details[5])
                    image.thumbnail((400, 400))
                    photo = ImageTk.PhotoImage(image)
                    image_label.config(image=photo)
                    image_label.image = photo

                btn_select_image = Button(frame, text="Select Image", font=('times new roman', 16),
                                          command=lambda: select_image(entry_image_path, image_label), bg='#6DA397', fg='white')
                btn_select_image.bind("<Enter>", lambda e: btn_select_image.config(bg="#92DBCA"))
                btn_select_image.bind("<Leave>", lambda e: btn_select_image.config(bg="#6DA397"))
                btn_select_image.grid(row=7, columnspan=2, padx=10, pady=10)

                btn_update_food = Button(frame, text="Update Food", font=('times new roman', 16),
                                         command=lambda: [update_food(food_id, entry_food_name.get(),
                                                                     entry_description.get(), entry_price.get(),
                                                                     combo_food_category.get(), entry_food_calories.get(),
                                                                     entry_image_path.get()), update_food_window.destroy()], bg='#E69312', fg='white')
                btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="#FFA314"))
                btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="#E69312"))
                btn_update_food.grid(row=8, columnspan=2, pady=20)

                btn_back = Button(frame, text="Back to Dashboard", font=('times new roman', 16), command=lambda: [update_food_window.destroy(),FoodDashboard()],
                                  bg='#7E84F7', fg='white')
                btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B8BEED"))
                btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#7E84F7"))
                btn_back.grid(row=9, columnspan=2, pady=20)
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

def update_food(food_id, food_name, description, price, food_category, food_calories, image_path):
    try:
        cursor.execute(
            "UPDATE food SET food_name=?, description=?, price=?, food_category=?, food_calories=?, image_path=? WHERE food_id=?",
            (food_name, description, price, food_category, food_calories, image_path, food_id))
        conn.commit()  # Commit the transaction
        messagebox.showinfo("Success", "Food details updated successfully!")

        # Fetch the updated data from the database and update the food treeview
        update_food_treeview()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating food details: {e}")

def update_food_treeview():
    # Clear existing data in the treeview
    for item in food_treeview.get_children():
        food_treeview.delete(item)

    try:
        # Fetch data from the database
        cursor.execute("SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food")
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
    food_id = item_values[0]

    # Prompt the user for confirmation
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{food_id}'?")

    if confirm:
        try:
            # Delete the selected item from the database table
            cursor.execute("DELETE FROM food WHERE food_id=?", (food_id,))
            conn.commit()  # Commit the transaction

            # Delete the selected item from the Treeview
            food_treeview.delete(selected_item)
            messagebox.showinfo("Success", f"'{food_id}' deleted successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting food: {e}")


#less message for the search when no have this food or this food is at what category
def ViewFoodMenu():
    def fetch_food_by_category(category):
        if category == "Best Selling":
            query = """
            SELECT food.food_id, food.food_name, food.description, food.price, food.food_category, food.food_calories, food.image_path, SUM(orderitem.quantity) as total_sold
            FROM orderitem
            JOIN food ON orderitem.food_id = food.food_id
            GROUP BY food.food_id
            ORDER BY total_sold DESC
            LIMIT 5
            """
        else:
            query = """
            SELECT food_id, food_name, description, price, food_category, food_calories, image_path
            FROM food
            WHERE food_category = ?
            """
            cursor.execute(query, (category,))
            return cursor.fetchall()
        cursor.execute(query)
        return cursor.fetchall()

    def display_food_items(food_items):
        # Clear existing items
        for widget in food_canvas_frame.winfo_children():
            widget.destroy()

        fixed_width = 300  # Fixed width for food frames
        fixed_height = 200  # Fixed height for food frames
        image_size = (150, 150)  # Size for the images

        # Add padding for grid layout
        row, col = 0, 0
        for row_data in food_items:
            food_id, food_name, description, price, food_category, food_calories, image_path = row_data[:7]

            food_frame_inner = Frame(food_canvas_frame, bg="white", bd=2, relief='ridge', width=fixed_width, height=fixed_height)
            food_frame_inner.grid(row=row, column=col, padx=10, pady=10)

            try:
                image = Image.open(image_path)
                # Crop or resize the image to fit the fixed size
                width, height = image.size
                if width > height:
                    left = (width - height) / 2
                    right = (width + height) / 2
                    top = 0
                    bottom = height
                else:
                    left = 0
                    right = width
                    top = (height - width) / 2
                    bottom = (height + width) / 2
                image = image.crop((left, top, right, bottom)).resize(image_size, Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                image_label = Label(food_frame_inner, image=photo, bg="white")
                image_label.image = photo
                image_label.grid(row=0, column=0, rowspan=2, padx=5, pady=5)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading image: {e}")

            name_label = Label(food_frame_inner, text=food_name, font=('Arial', 12, 'bold'), bg="white")
            name_label.grid(row=0, column=1, sticky='w', padx=5)

            price_label = Label(food_frame_inner, text=f"RM{price:.2f}", font=('Arial', 10), bg="white")
            price_label.grid(row=1, column=1, sticky='w', padx=5)

            button_frame = Frame(food_frame_inner, bg="white")
            button_frame.grid(row=2, column=1, sticky='w', padx=5, pady=5)

            add_to_cart_btn = Button(button_frame, text="Add to Cart", font=('Arial', 10),command=lambda f_id=food_id, f_name=food_name, f_price=price, f_calories=food_calories: add_to_cart(f_id, f_name, f_price, f_calories),bg="#FFFE91")
            add_to_cart_btn.pack(side='left', padx=5)

            detail_btn = Button(button_frame, text="Detail", font=('Arial', 10), command=lambda f_id=food_id: show_food_detail(f_id),bg="#AEFFA7")
            detail_btn.pack(side='left', padx=5)

            # Move to the next column or row
            col += 1
            if col >= 4:  # Assuming you want 4 items per row
                col = 0
                row += 1

        # Update the scroll region of the canvas
        food_canvas.update_idletasks()
        food_canvas.config(scrollregion=food_canvas.bbox("all"))

    def show_food_detail(food_id):
        def close_detail():
            detail_window.destroy()

        cursor.execute("SELECT * FROM food WHERE food_id = ?", (food_id,))
        food_item = cursor.fetchone()
        if not food_item:
            messagebox.showerror("Error", "Food item not found.")
            return

        food_id, food_name, description, price, food_category, food_calories, image_path, admin_id = food_item

        detail_window = Toplevel()
        detail_window.title(f"Detail of {food_name}")
        detail_window.geometry("1920x1080+0+0")  # window size and position
        detail_window.state("zoomed")
        detail_window.configure(bg="white")

        top_frame = Frame(detail_window, bg="#BACFFA", height=50)
        top_frame.pack(fill='x')

        title_label = Label(top_frame, text=f"{food_name}", font=('Arial', 18, 'bold'), bg="#BACFFA")
        title_label.pack(pady=10)

        try:
            image = Image.open(image_path)
            image.thumbnail((250, 250))
            photo = ImageTk.PhotoImage(image)
            image_label = Label(detail_window, image=photo, bg="white")
            image_label.image = photo
            image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

        info_frame = Frame(detail_window, bg="white")
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)

        description_label = Label(info_frame, text=f"Description: {description}", font=('Arial', 12), bg="white", wraplength=450)
        description_label.pack(anchor="center", pady=5)

        price_label = Label(info_frame, text=f"Price: RM{price:.2f}", font=('Arial', 12), bg="white")
        price_label.pack(anchor="center", pady=5)

        category_label = Label(info_frame, text=f"Category: {food_category}", font=('Arial', 12), bg="white")
        category_label.pack(anchor="center", pady=5)

        calories_label = Label(info_frame, text=f"Calories: {food_calories} kcal", font=('Arial', 12), bg="white")
        calories_label.pack(anchor="center", pady=5)

        bottom_frame = Frame(detail_window, bg="#BDD3FF", height=50)
        bottom_frame.pack(fill='x', side='bottom')

        close_btn = Button(bottom_frame, text="Close", font=('Arial', 12, 'bold'), command=close_detail)
        close_btn.pack(side='bottom', pady=10)

    def search_food(query, current_category):
        try:
            if query.strip() == "":
                if current_category == "Best Selling":
                    # Fetch and display best-selling items
                    display_food_items(fetch_food_by_category("Best Selling"))
                else:
                    # Fetch and display items from the selected category
                    sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_name LIKE ? AND food_category = ?"
                    cursor.execute(sql_query, ('%' + query + '%', current_category))
                    rows = cursor.fetchall()
                    display_food_items(rows)
            else:
                if current_category == "Best Selling":
                    # Search among best-selling items
                    sql_query = """
                    SELECT food.food_id, food.food_name, food.description, food.price, food.food_category, food.food_calories, food.image_path, SUM(orderitem.quantity) as total_sold
                    FROM orderitem
                    JOIN food ON orderitem.food_id = food.food_id
                    WHERE food_name LIKE ?
                    GROUP BY food.food_id
                    ORDER BY total_sold DESC
                    """
                    cursor.execute(sql_query, ('%' + query + '%',))
                    rows = cursor.fetchall()
                    display_food_items(rows[:5])  # Display top 5 results
                else:
                    # Search for items based on the query in the selected category
                    sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_name LIKE ? AND food_category = ?"
                    cursor.execute(sql_query, ('%' + query + '%', current_category))
                    rows = cursor.fetchall()
                    display_food_items(rows)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    def back_home():
        result = messagebox.askquestion('System', 'Are you sure you want to return to Home?', icon="warning")
        if result == 'yes':
            MenuFrame.destroy()
            Home()

    def logout():
        result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
        if result == 'yes':
            cart.clear()
            MenuFrame.destroy()
            root.deiconify()

    HomeFrame.withdraw()

    MenuFrame = Toplevel()
    MenuFrame.title("Food Menu")
    MenuFrame.geometry("1920x1080+0+0")  # window size and position
    MenuFrame.state("zoomed")
    MenuFrame.configure(bg="#f8f8f8")

    top_frame = Frame(MenuFrame, bg="#BACFFA", height=100)
    top_frame.pack(fill='x')

    title_label = Label(top_frame, text="Food Menu", font=('Edwardian Script ITC', 40, 'bold'), bg="#BACFFA")
    title_label.pack(pady=20)

    selected_category = StringVar(value="Best Selling")

    search_frame = Frame(top_frame, bg="#BACFFA")
    search_frame.pack(side='bottom', pady=10)

    # Display selected category name above the search entry
    selected_category_label = Label(search_frame, text=selected_category.get(), font=('Arial', 18, 'bold'),
                                    bg="#BACFFA")
    selected_category_label.pack(side='top', pady=5)

    search_entry = Entry(search_frame, font=('Arial', 12), width=30)
    search_entry.pack(side='left', padx=10)

    search_btn = Button(search_frame, text="Search", font=('Arial', 12),
                        command=lambda: search_food(search_entry.get(), selected_category.get()))
    search_btn.pack(side='left')

    category_frame = Frame(MenuFrame, bg="#9CA8F7", height=50, highlightbackground="black", highlightcolor="black",
                           highlightthickness=2)
    category_frame.pack(side='left', fill='y')

    category_label = Label(category_frame, text="Category", font=('Arial', 14, 'bold'), bg="#9CA8F7")
    category_label.pack(pady=10)

    categories = ["Best Selling", "Breakfast", "Lunch", "Dinner", "Drinks", "Dessert"]

    def update_selected_category(category):
        selected_category.set(category)
        selected_category_label.config(text=selected_category.get())
        display_food_items(fetch_food_by_category(category))

    for category in categories:
        category_btn = Radiobutton(category_frame, text=category, variable=selected_category, value=category,
                                   indicatoron=0,
                                   font=('Arial', 14), bg="#9893BF",
                                   command=lambda c=category: update_selected_category(c), width=9)  # Adjust the width value as needed
        category_btn.pack(fill='y', padx=5, pady=3)

    # Frame for food items with scrollbar
    food_frame = Frame(MenuFrame, bg="#f8f8f8")
    food_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Adding a canvas to allow scrolling
    food_canvas = Canvas(food_frame, bg="#f8f8f8")
    food_canvas.pack(side='left', fill='both', expand=True)

    # Adding a scrollbar
    scrollbar = Scrollbar(food_frame, orient="vertical", command=food_canvas.yview)
    scrollbar.pack(side='right', fill='y')

    food_canvas.config(yscrollcommand=scrollbar.set)
    food_canvas.bind('<Configure>', lambda e: food_canvas.config(scrollregion=food_canvas.bbox("all")))

    # Frame inside the canvas to hold the food items
    food_canvas_frame = Frame(food_canvas, bg="#f8f8f8")
    food_canvas.create_window((0, 0), window=food_canvas_frame, anchor="nw")

    # Display initial food items
    display_food_items(fetch_food_by_category(selected_category.get()))

    bottom_frame = Frame(MenuFrame, bg="#BDD3FF", height=60)
    bottom_frame.pack(fill='x', side='bottom')

    cart_btn = Button(bottom_frame, text="View Cart", font=('Arial', 14, 'bold'), command=ViewCart, bg='#22B14C',
                      fg='black')
    cart_btn.bind("<Enter>", lambda e: cart_btn.config(bg="light green"))
    cart_btn.bind("<Leave>", lambda e: cart_btn.config(bg="#22B14C"))
    cart_btn.pack(side='left', padx=10, pady=10)

    logout_btn = Button(bottom_frame, text="Logout", font=('Arial', 14, 'bold'), command=logout, bg='#7E84F7',
                        fg='black')
    logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#B8BEED"))
    logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#7E84F7"))
    logout_btn.pack(side='right', padx=10, pady=10)

    back_home_btn = Button(bottom_frame, text="Back to Home", font=('Arial', 14, 'bold'), command=back_home,
                           bg='#E061ED', fg='black')
    back_home_btn.bind("<Enter>", lambda e: back_home_btn.config(bg="#F168FF"))
    back_home_btn.bind("<Leave>", lambda e: back_home_btn.config(bg="#E061ED"))
    back_home_btn.pack(side='right', padx=10, pady=10)

def add_to_cart(food_id, food_name, price, food_calories):
    # Fetch the food details from the database
    cursor.execute("SELECT price, food_calories FROM food WHERE food_id=?", (food_id,))
    result = cursor.fetchone()
    if result:

        # Check if the item is already in the cart
        found_in_cart = False
        for index, item in enumerate(cart):
            if item[0] == food_id:
                # Update quantity if item already in cart
                cart[index] = (food_id, food_name, price, food_calories, item[4] + 1)
                found_in_cart = True
                break

        if not found_in_cart:
            # Add new item to cart with quantity 1
            cart.append((food_id, food_name, price, food_calories, 1))

        messagebox.showinfo("Success", f"{food_name} added to cart!")
        # For debugging: print the current contents of the cart
        print("Cart:", cart)
    else:
        messagebox.showerror("Error", "Failed to add food to cart")

#less enter the table code
def ViewCart():
    def update_cart_table():
        # Clear the current contents of the table
        for item in cart_treeview.get_children():
            cart_treeview.delete(item)

        # Insert cart items into the table
        for item in cart:
            food_id, food_name, price, food_calories, quantity = item
            cart_treeview.insert("", "end", values=(food_id, food_name, f"RM{price:.2f}", food_calories, quantity))

        # Update total price and calories
        total_price = sum(item[2] * item[4] for item in cart)
        total_calories = sum(item[3] * item[4] for item in cart)
        lbl_total_price.config(text=f"Total Price: RM{total_price:.2f}")
        lbl_total_food_calories.config(text=f"Total Food Calories: {total_calories}")

    def delete_selected_item():
        selected_item = cart_treeview.selection()
        if selected_item:
            item_index = int(cart_treeview.index(selected_item[0]))
            food_id, food_name, price, food_calories, quantity = cart[item_index]
            if quantity > 1:
                cart[item_index] = (food_id, food_name, price, food_calories, quantity - 1)
                update_cart_table()
                messagebox.showinfo("Success", f"Item '{food_name}' quantity has been updated in the cart.")
            else:
                del cart[item_index]
                update_cart_table()
                messagebox.showinfo("Success", f"Item '{food_name}' has been removed from the cart.")
        else:
            messagebox.showerror("Error", "Please select an item to delete.")

    def place_order(total_price, total_food_calories, cart_data, cart_window):
        try:
            cursor = conn.cursor()

            # Fetch the customer ID based on the stored username and password
            query = """
                    SELECT customer_id
                    FROM customer
                    WHERE username = ? AND password = ?
                    """
            cursor.execute(query, (logged_in_user['username'], logged_in_user['password']))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise sqlite3.Error("Customer not found")

            customer_id = customer_data[0]

            # Extract float values from the total price and total food calories strings
            total_price = float(total_price.replace("Total Price: RM", ""))
            total_food_calories = int(total_food_calories.replace("Total Food Calories: ", ""))

            # Insert a new order in the Orders table
            order_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO `order` (order_date, total_price, total_food_calories, customer_id) VALUES (?, ?, ?, ?)",
                (order_date, total_price, total_food_calories, customer_id)
            )
            order_id = cursor.lastrowid  # Get the last inserted order_id

            # Insert each item in the cart into the OrderItems table
            for item in cart_data:
                food_id, _, price, food_calories, quantity = item
                cursor.execute(
                    "INSERT INTO 'orderitem' (order_id, food_id, quantity, total_price, total_food_calories, customer_id) VALUES (?, ?, ?, ?, ?, ?)",
                    (order_id, food_id, quantity, price * quantity, food_calories * quantity, customer_id)
                )

            conn.commit()

            messagebox.showinfo("Success", "Order placed successfully!")

            # Clear the cart and update the cart table before closing the window
            cart.clear()
            update_cart_table()

            cart_window.destroy()
            open_payment_window(total_price, order_id)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error placing order: {e}")

    cart_window = Toplevel()
    cart_window.title("Shopping Cart")
    cart_window.geometry("1920x1080+0+0")  # window size and position
    cart_window.state("zoomed")
    cart_window.configure(bg="lavender")

    # Top frame with title
    top_frame = Frame(cart_window, bg="#BACFFA", height=50)
    top_frame.pack(fill='x')

    title_label = Label(top_frame, text="Shopping Cart", font=('Edwardian Script ITC', 40, 'bold'), bg="#BACFFA")
    title_label.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), foreground="#148699")

    # Treeview table for cart items
    columns = ("food_id", "food_name", "price", "food_calories", "quantity")
    cart_treeview = ttk.Treeview(cart_window, columns=columns, show='headings')
    cart_treeview.heading("food_id", text="Food ID")
    cart_treeview.heading("food_name", text="Food Name")
    cart_treeview.heading("price", text="Price")
    cart_treeview.heading("food_calories", text="Food Calories")
    cart_treeview.heading("quantity", text="Quantity")

    cart_treeview.column("food_id", anchor="center")
    cart_treeview.column("food_name", anchor="center")
    cart_treeview.column("price", anchor="center")
    cart_treeview.column("food_calories", anchor="center")
    cart_treeview.column("quantity", anchor="center")

    cart_treeview.pack(fill='both', expand=True, padx=10, pady=10)

    # Frame for total price and calories
    bottom_frame = Frame(cart_window, bg="lavender", height=50)
    bottom_frame.pack(anchor="center", padx=10, pady=10)

    for item in cart:
        food_id, food_name, price, food_calories, quantity = item
        cart_treeview.insert("", "end", values=(food_id, food_name, f"RM{price:.2f}", food_calories, quantity))

    lbl_total_price = Label(bottom_frame,
                            text=f"Total Price: RM{sum(price * quantity for _, _, price, _, quantity in cart):.2f}",
                            font=('times new roman', 16), bg="lavender")
    lbl_total_price.grid(padx=10,pady=10)

    lbl_total_food_calories = Label(bottom_frame,
                                    text=f"Total Food Calories: {sum(food_calories * quantity for _, _, _, food_calories, quantity in cart)}",
                                    font=('times new roman', 16), bg="lavender")
    lbl_total_food_calories.grid(row=1, column=0,padx=20,pady=10)


    # Buttons for cart actions
    action_frame = Frame(cart_window, bg="lavender", height=50)
    action_frame.pack(anchor="center", padx=10, pady=10)

    delete_order_btn = Button(action_frame, text="Delete Order", font=('Arial', 14, 'bold'), bg="red", fg="white", command=delete_selected_item)
    delete_order_btn.grid(row=0, column=0, padx=10, pady=10)

    place_order_btn = Button(action_frame, text="Place Order", font=('Arial', 14, 'bold'), bg="blue", fg="white",
                             command=lambda: place_order(lbl_total_price.cget("text"),
                                                         lbl_total_food_calories.cget("text"), cart, cart_window))
    place_order_btn.grid(row=0, column=1, padx=10, pady=10)

    back_to_menu_btn = Button(action_frame, text="Back to Menu", font=('Arial', 14, 'bold'), bg="gray", fg="white", command=cart_window.destroy)
    back_to_menu_btn.grid(row=0, column=2, padx=10, pady=10)

    update_cart_table()


def open_payment_window(total_price, order_id):
    PaymentWindow = Toplevel()
    PaymentWindow.title("Payment")
    PaymentWindow.geometry("1920x1080+0+0")  # window size and position
    PaymentWindow.state("zoomed")
    PaymentWindow.grid_columnconfigure(0, weight=1)
    PaymentWindow.grid_columnconfigure(1, weight=1)

    # Load the background image
    image = Image.open("paymentwindow.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(PaymentWindow, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tax_rate = 0.06  # Assuming 6% tax rate

    tax_amount = total_price * tax_rate
    total_amount = total_price + tax_amount

    formatted_total_price = "RM{:.2f}".format(total_price)
    formatted_tax_amount = "RM{:.2f}".format(tax_amount)
    formatted_total_amount = "RM{:.2f}".format(total_amount)

    Label(PaymentWindow, text="Payment",font=('Script MT Bold', 26),fg='blue', highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=10)
    Label(PaymentWindow, text=f"Total Amount to Pay: {formatted_total_price}", font=('times new roman', 16,'bold'),highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=10)
    Label(PaymentWindow, text=f"Tax (6%): {formatted_tax_amount}", font=('times new roman', 16,'bold'),highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=10)
    Label(PaymentWindow, text=f"Total Amount (including tax): {formatted_total_amount}",font=('times new roman', 16,'bold'),highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=10)

    pay_button = Button(PaymentWindow, text="Pay", font=('times new roman', 16,'bold'),command=lambda: complete_payment(total_price, tax_amount, total_amount, PaymentWindow,order_id), bg='#0010A3', fg='white')
    pay_button.bind("<Enter>", lambda e: pay_button.config(bg="#0018F2"))
    pay_button.bind("<Leave>", lambda e: pay_button.config(bg="#0010A3"))
    pay_button.pack(pady=10)

    # Keep a reference to the image object to prevent garbage collection
    PaymentWindow.image = bg_image

def complete_payment(total_price, tax_amount, total_amount, payment_window, order_id):
    try:
        # Convert prices to float
        total_price_float = float(total_price)
        tax_amount_float = float(tax_amount)
        total_amount_float = float(total_amount)

        # Insert payment details into the payment table
        payment_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO payment (order_id, total_price, total_amount, payment_date) VALUES (?, ?, ?, ?)",
            (order_id, total_price_float, total_amount_float, payment_date)
        )
        conn.commit()

        # Show thank you message
        messagebox.showinfo("Payment Successful", "Thank you for your payment!")

        # Close payment window
        payment_window.destroy()

        # Prompt user for review and rating
        review_rating_choice(order_id, total_price_float, tax_amount_float, total_amount_float)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error processing payment: {e}")

def review_rating_choice(order_id, total_price, tax_amount, total_amount):
    review_choice_window = Toplevel()
    review_choice_window.title("Review and Rating")
    review_choice_window.geometry("1920x1080+0+0")  # window size and position
    review_choice_window.state("zoomed")

    # Load the background image
    image = Image.open("reviewchoice.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(review_choice_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(review_choice_window, text="Would you like to leave a review and rating?", font=('times new roman', 20,'bold'),highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=10)

    yes_button = Button(review_choice_window, text="Yes", font=('times new roman', 20,'bold'),
                        command=lambda: [review_choice_window.destroy(), open_review_window(order_id, total_price, tax_amount, total_amount)], bg='#377E47', fg='white')
    yes_button.pack(pady=10)

    no_button = Button(review_choice_window, text="No", font=('times new roman', 20,'bold'),
                       command=lambda: [review_choice_window.destroy(), receipt(order_id, total_price, tax_amount, total_amount)], bg='#E74C3C', fg='white')
    no_button.pack(pady=10)

    # Keep a reference to the image object to prevent garbage collection
    review_choice_window.image = bg_image

def open_review_window(order_id, total_price, tax_amount, total_amount):
    review_window = Toplevel()
    review_window.title("Review and Rating")
    review_window.geometry("1920x1080+0+0")  # window size and position
    review_window.state("zoomed")

    # Load the background image
    image = Image.open("reviewwindow.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(review_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(review_window, text="Review and Rating",font=('Edwardian Script ITC', 30, 'bold'),highlightbackground="black", highlightcolor="black", highlightthickness=2).pack(pady=5)

    review_label = Label(review_window, text="Leave a review:", font=('Vivaldi', 18), fg='blue',highlightbackground="black", highlightcolor="black", highlightthickness=2)
    review_label.pack()

    review_text = Text(review_window, height=4, width=50, font=('times new roman', 12),highlightbackground="black", highlightcolor="black", highlightthickness=2)
    review_text.pack(pady=10)

    rating_label = Label(review_window, text="Rating:", font=('Vivaldi', 18), fg='blue',highlightbackground="black", highlightcolor="black", highlightthickness=2)
    rating_label.pack()

    stars_frame = Frame(review_window,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    stars_frame.pack(pady=10)

    rating = IntVar()
    rating.set(1)

    star_canvases = []

    def create_star(canvas, fill_type='empty'):
        canvas.delete("all")
        if fill_type == 'full':
            canvas.create_polygon([25, 2, 31, 18, 47, 18, 34, 28, 39, 44, 25, 34, 11, 44, 16, 28, 3, 18, 19, 18], fill='gold', outline='black')
        else:
            canvas.create_polygon([25, 2, 31, 18, 47, 18, 34, 28, 39, 44, 25, 34, 11, 44, 16, 28, 3, 18, 19, 18], fill='grey', outline='black')

    def select_star(star_number):
        rating.set(star_number)
        for i in range(5):
            if i < star_number:
                create_star(star_canvases[i], 'full')
            else:
                create_star(star_canvases[i], 'empty')

    def create_star_canvas(index):
        canvas = Canvas(stars_frame, width=50, height=50, bg='white', highlightthickness=0)
        canvas.pack(side='left')
        canvas.bind("<Button-1>", lambda e, idx=index: select_star(idx + 1))
        star_canvases.append(canvas)
        create_star(canvas)

    for i in range(5):
        create_star_canvas(i)

    submit_button = Button(review_window, text="Submit", command=lambda: submit_review_rating(
        review_text.get("1.0", END), rating.get(), review_window, order_id, total_price, tax_amount, total_amount
    ), bg='#377E47', fg='white', font=('times new roman', 14, 'bold'))
    submit_button.pack(pady=10)

    # Display the reviews chart
    display_reviews_chart(review_window)

    # Keep a reference to the image object to prevent garbage collection
    review_window.image = bg_image

def submit_review_rating(review, rating, review_window, order_id, total_price, tax_amount, total_amount):
    try:
        rating_value = float(rating)
        if rating_value < 0.5 or rating_value > 5.0:
            messagebox.showerror("Error", "Rating must be between 0.5 and 5.0")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid rating. Please enter a number.")
        return

    review_date = datetime.now().strftime("%Y-%m-%d")

    try:
        # Fetch the customer ID based on the stored username and password
        query = """
                        SELECT customer_id
                        FROM customer
                        WHERE username = ? AND password = ?
                        """
        cursor.execute(query, (logged_in_user['username'], logged_in_user['password']))
        customer_data = cursor.fetchone()

        if not customer_data:
            raise sqlite3.Error("Customer not found")

        customer_id = customer_data[0]

        # Insert the review into the review table
        cursor.execute("INSERT INTO review (customer_id, review, rating, review_date) VALUES (?, ?, ?, ?)",
                       (customer_id, review, rating_value, review_date))
        conn.commit()

        messagebox.showinfo("Success", "Thank you for your review and rating!")
        review_window.destroy()

        # Display the receipt
        receipt(order_id, total_price, tax_amount, total_amount)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error saving review: {e}")

def display_reviews_chart(parent):
    cursor.execute("SELECT rating, COUNT(*) FROM review GROUP BY rating")
    review_data = cursor.fetchall()

    ratings = [5, 4, 3, 2, 1]
    counts = [0] * len(ratings)

    for rating, count in review_data:
        index = ratings.index(int(rating))
        counts[index] = count

    percentages = [count / sum(counts) * 100 for count in counts]

    fig, ax = plt.subplots(figsize=(8, 6))  # Increased figure size

    colors = ['#ffd700' for r in ratings]

    bars = ax.barh([f'{r} star' for r in ratings], percentages, color=colors, edgecolor='black')

    for bar, percentage in zip(bars, percentages):
        width = bar.get_width()
        label_x_pos = width + 1
        ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{percentage:.1f}%',
                va='center', ha='left', fontsize=8, color='black', weight='bold')

    ax.set_title(f'Customer Reviews from {sum(counts):,} reviews', fontsize=10, weight='bold', pad=20)
    ax.set_xlabel('Percentage (%)', fontsize=8)
    ax.set_ylabel('Ratings', fontsize=8)
    ax.invert_yaxis()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)


#add more information, table smaller it
def receipt(order_id, total_price, tax_amount, total_amount):
    # Execute a SQL query to fetch rows from the database
    cursor.execute("""
        SELECT food.food_id, food.food_name, food.price, "orderitem".quantity
        FROM "orderitem"
        JOIN food ON "orderitem".food_id = food.food_id
        WHERE "orderitem".order_id = ?
    """, (order_id,))
    rows = cursor.fetchall()  # Fetch all rows returned by the query

    # Your existing code for generating the PDF receipt
    pdf = FPDF("P", "mm", "A4")
    w = 210
    h = 297

    # Add a page
    pdf.add_page()

    # Set title
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Receipt", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Order ID: {order_id}", ln=True, align="C")

    # Add table header
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(130, 136, 255)  # background
    pdf.cell(30, 10, txt="Food ID", border=1, ln=0, fill=True, align="C")
    pdf.cell(60, 10, txt="Name", border=1, ln=0, fill=True, align="C")
    pdf.cell(40, 10, txt="Price (RM)", border=1, ln=0, fill=True, align="C")
    pdf.cell(30, 10, txt="Quantity", border=1, ln=0, fill=True, align="C")
    pdf.cell(40, 10, txt="Total Price (RM)", border=1, ln=0, fill=True, align="C")
    pdf.ln()

    # Add food details
    pdf.set_font("Arial", size=12)

    total_quantity = 0
    for row in rows:
        food_id, food_name, food_price, quantity = row
        total_price_item = food_price * quantity
        total_quantity += quantity
        pdf.cell(30, 10, txt=str(food_id), border=1, align="C")
        pdf.cell(60, 10, txt=food_name, border=1, align="C")
        pdf.cell(40, 10, txt=f"RM{food_price:.2f}", border=1, align="C")
        pdf.cell(30, 10, txt=str(quantity), border=1, align="C")
        pdf.cell(40, 10, txt=f"RM{total_price_item:.2f}", border=1, align="C")
        pdf.ln()

    # Add totals
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(160, 254, 255)  # background
    pdf.cell(160, 10, txt="Total Quantity:", border=1, align="R")
    pdf.cell(40, 10, txt=str(total_quantity), border=1, align="C")
    pdf.ln()
    pdf.cell(160, 10, txt="Subtotal (RM):", border=1, align="R")
    pdf.cell(40, 10, txt=f"RM{total_price:.2f}", border=1, align="C")
    pdf.ln()
    pdf.cell(160, 10, txt="Tax Amount (RM):", border=1, align="R")
    pdf.cell(40, 10, txt=f"RM{tax_amount:.2f}", border=1, align="C")
    pdf.ln()
    pdf.cell(160, 10, txt="Total Amount (RM):", border=1, align="R")
    pdf.cell(40, 10, txt=f"RM{total_amount:.2f}", border=1, align="C")
    pdf.ln()

    # Construct the file path
    receipt_filename = f"receipt_{order_id}.pdf"
    receipt_filepath = os.path.join(os.getcwd(), receipt_filename)

    # Save the PDF
    pdf.output(receipt_filepath)

    messagebox.showinfo("Receipt", f"Receipt saved as {receipt_filepath}")
    webbrowser.open_new(receipt_filepath)

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
    def back_to_admin_panel():
        result = messagebox.askquestion('System', 'Are you sure you want to return to the admin panel?', icon="warning")
        if result == 'yes':
            # Close the current window
            total_orders_window.destroy()

    # Create a new window to display the results
    total_orders_window = Toplevel()
    total_orders_window.title("Total Orders and Total Cost Per Month")
    total_orders_window.geometry("1920x1080+0+0")  # window size and position
    total_orders_window.state("zoomed")
    total_orders_window.configure(bg="#F4D5FF")

    # Create and place the title label at the top center
    title_label = Label(total_orders_window, text="Total Order:", font=('Bauhaus 93', 18), fg='#4D8DAD', highlightbackground="black", highlightcolor="black", highlightthickness=2)
    title_label.pack(side="top", pady=10)

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

    btn_back = Button(total_orders_window, text="Back to Admin Panel", font=('times new roman', 16), command=back_to_admin_panel,
                      bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='bottom', padx=10,pady=10)

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
    def back_to_admin_panel():
        result = messagebox.askquestion('System', 'Are you sure you want to return to the admin panel?', icon="warning")
        if result == 'yes':
            # Close the current window
            review_window.destroy()

    # Create a new window to display the results
    review_window = Toplevel()
    review_window.title("Customer Review and Rating")
    review_window.geometry("1920x1080+0+0")  # window size and position
    review_window.state("zoomed")
    review_window.configure(bg="#C8C1FF")

    # Create and place the title label at the top center
    title_label = Label(review_window, text="Customer review rating:", font=('Bauhaus 93', 18), fg='#4D8DAD',
                        highlightbackground="black", highlightcolor="black", highlightthickness=2)
    title_label.pack(side="top", pady=10)

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

    btn_back = Button(review_window, text="Back to Admin Panel", font=('times new roman', 16), command= back_to_admin_panel,
                      bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='bottom', padx=10, pady=10)

#add how many times u order that food
def ViewOrderHistory():
    global logged_in_user

    OrderHistoryFrame = Toplevel()
    OrderHistoryFrame.title("Order History")
    OrderHistoryFrame.geometry("1920x1080+0+0")  # window size and position
    OrderHistoryFrame.state("zoomed")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 16, 'bold'))  # Change heading font
    style.configure("Treeview", font=('times new roman', 14))  # Change body font

    # Define columns
    columns = ("Order ID", "Order Date", "Food ID", "Quantity", "Total Price", "Total Food Calories")

    lbl_order_history = Label(OrderHistoryFrame, text="Order History", font=('Bauhaus 93', 18))
    lbl_order_history.pack(side="top", pady=10)

    # Create Treeview widget
    order_history_treeview = ttk.Treeview(OrderHistoryFrame, columns=columns, show="headings")
    order_history_treeview.heading("Order ID", text="Order ID")
    order_history_treeview.heading("Order Date", text="Order Date")
    order_history_treeview.heading("Food ID", text="Food ID")
    order_history_treeview.heading("Quantity", text="Quantity")
    order_history_treeview.heading("Total Price", text="Total Price")
    order_history_treeview.heading("Total Food Calories", text="Total Food Calories")

    order_history_treeview.pack(fill="both", expand=True)

    # Fetch order history for the customer
    try:
        cursor = conn.cursor()
        query = """
            SELECT customer_id
            FROM customer
            WHERE username = ? AND password = ?
        """
        cursor.execute(query, (logged_in_user['username'], logged_in_user['password']))
        customer_data = cursor.fetchone()

        if not customer_data:
            raise sqlite3.Error("Customer not found")

        customer_id = customer_data[0]

        cursor.execute("""
            SELECT o.order_id, o.order_date, oi.food_id, oi.quantity, oi.total_price, oi.total_food_calories
            FROM `order` o
            JOIN `orderitem` oi ON o.order_id = oi.order_id
            WHERE oi.customer_id = ?
        """, (customer_id,))
        order_history = cursor.fetchall()

        for row in order_history:
            order_history_treeview.insert("", "end", values=row)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching order history: {e}")

    # Create a frame for the buttons
    button_frame = Frame(OrderHistoryFrame)
    button_frame.pack(side="bottom", pady=20)

    btn_back = Button(button_frame, text="Back to Admin Panel", font=('times new roman', 16), command=OrderHistoryFrame.destroy, bg='#3580BB', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#48AFFF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#3580BB"))
    btn_back.pack(side="bottom", padx=10,pady=10)

def bmi_window():
    global weight_entry, height_entry, gender_var, result_label, canvas

    bmi_root = Toplevel()
    bmi_root.title("BMI Calculator")
    bmi_root.geometry("1920x1080+0+0")  # window size and position
    bmi_root.state("zoomed")
    bmi_root.configure(bg="#BFBEFF")

    # Define a larger font for the labels and buttons
    font_large = ("Arial", 13, "bold")  # Font family, size, and style

    # Create and place the title label at the top center
    title_label = Label(bmi_root, text="BMI Calculator", font=('Bauhaus 93', 18), fg='#4D8DAD',highlightbackground="black", highlightcolor="black", highlightthickness=2)
    title_label.pack(side="top")

    # Create and place a frame for the input fields using grid
    input_frame = Frame(bmi_root,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    input_frame.pack(side="top", anchor="center", padx=20, pady=20)

    # Create and place the height label and entry in the input frame
    Label(input_frame, text="Height (cm):", font=font_large).grid(row=0, column=0, padx=10, pady=10)
    height_entry = Entry(input_frame, font=font_large)
    height_entry.grid(row=0, column=1, padx=10, pady=10)

    # Create and place the weight label and entry in the input frame
    Label(input_frame, text="Weight (kg):", font=font_large).grid(row=1, column=0, padx=10, pady=10)
    weight_entry = Entry(input_frame, font=font_large)
    weight_entry.grid(row=1, column=1, padx=10, pady=10)

    # Create and place the gender label and radio buttons in the input frame
    Label(input_frame, text="Gender:", font=font_large).grid(row=2, column=0, padx=10, pady=10)
    gender_var = StringVar(value="Male")
    Radiobutton(input_frame, text="Male", variable=gender_var, value="Male", font=font_large).grid(row=2, column=1, padx=10, pady=10, sticky="w")
    Radiobutton(input_frame, text="Female", variable=gender_var, value="Female", font=font_large).grid(row=2, column=1, padx=10, pady=10, sticky="e")

    # Create and place the calculate button in the input frame
    calculate_button = Button(input_frame, text="Calculate BMI", font=font_large, command=lambda: calculate_bmi(weight_entry.get(), height_entry.get(), gender_var.get(), result_label, bmi_root), bg='#367E7F', fg='white')
    calculate_button.bind("<Enter>", lambda e: calculate_button.config(bg="#59CFD1"))
    calculate_button.bind("<Leave>", lambda e: calculate_button.config(bg="#367E7F"))
    calculate_button.grid(row=3, columnspan=2, pady=10)

    # Create and place the result label at the top center
    result_label = Label(bmi_root, text="BMI: ", font=font_large,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    result_label.pack(side="top", pady=20)

    # Create and place the Back to Home button
    back_button = Button(bmi_root, text="Back to Home", font=font_large, command=bmi_root.destroy, bg='#6BE681', fg='white')
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#77FF90"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg="#6BE681"))
    back_button.pack(side="bottom", pady=20)

    canvas = None

def calculate_bmi(weight, height, gender, result_label, bmi_root):
    try:
        weight = float(weight)
        height = float(height) / 100  # convert height to meters
        bmi = weight / (height * height)
        bmi = round(bmi, 1)

        if gender == "Male" or gender == "Female":
            if bmi < 18.5:
                category = "Underweight"
            elif 18.5 <= bmi < 24.9:
                category = "Normal weight"
            elif 25 <= bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obese"

        result_label.config(text=f"BMI: {bmi} ({category})")
        plot_bmi_chart(bmi, bmi_root)
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers for height and weight.")

def plot_bmi_chart(bmi, bmi_root):
    global canvas

    # Remove previous canvas if it exists
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()
        canvas = None

    # Enlarge the figure size for better visibility
    fig, ax = plt.subplots(figsize=(14, 4))  # Adjust the figure size here

    # Define the BMI ranges and their corresponding colors
    categories = ['Underweight', 'Normal weight', 'Overweight', 'Obese']
    colors = ['#87CEEB', '#32CD32', '#FFA500', '#FF4500']
    bmi_ranges = [0, 18.5, 24.9, 29.9, 50]

    # Create the bar for the BMI categories
    for i in range(len(bmi_ranges) - 1):
        ax.barh(0, bmi_ranges[i + 1] - bmi_ranges[i], left=bmi_ranges[i], color=colors[i])

    # Plot the user's BMI
    ax.plot(bmi, 0, 'D', color='white', markersize=12)

    # Add text and formatting
    ax.text(bmi, 0.1, f'{bmi}', color='black', ha='center', va='bottom', fontsize=14)
    ax.set_yticks([])
    ax.set_xlim(0, 50)
    ax.set_xlabel('BMI', fontsize=6)
    ax.set_title('Your BMI', fontsize=11)

    # Add category labels
    for i in range(len(categories)):
        x = (bmi_ranges[i] + bmi_ranges[i + 1]) / 2
        ax.text(x, -0.2, categories[i], ha='center', va='bottom', fontsize=12)

    # Embed the chart in the BMI window
    canvas = FigureCanvasTkAgg(fig, master=bmi_root)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", pady=20)

    plt.close(fig)  # Close the figure to prevent duplicate plots

def LoginForm():
    global LoginFrame, lbl_result1

    # Load the background image
    image = Image.open("background.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    LoginFrame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    LoginFrame.pack(side='top', pady=80)

    lbl_title = Label(LoginFrame, text="Login:", font=('Script MT Bold', 24, 'bold'), fg='#0016BA', bd=18)
    lbl_title.grid(row=0, columnspan=2)

    lbl_username = Label(LoginFrame, text="Username:", font=('times new roman', 16), bd=18)
    lbl_username.grid(row=1, column=0)

    lbl_password = Label(LoginFrame, text="Password:", font=('times new roman', 16), bd=18)
    lbl_password.grid(row=2, column=0)

    # Clear existing text in the entry fields
    USERNAME_LOGIN.set("")
    PASSWORD_LOGIN.set("")

    username = Entry(LoginFrame, font=('times new roman', 14), textvariable=USERNAME_LOGIN, width=20)
    username.grid(row=1, column=1,padx=10)
    username.insert(0, "Enter your username")  # Placeholder for username
    username.config(fg='grey')  # Set placeholder text color to grey
    username.bind("<FocusIn>", lambda event: on_entry_click(username, "Enter your username"))
    username.bind("<FocusOut>", lambda event: on_focus_out(username, "Enter your username"))

    password = Entry(LoginFrame, font=('times new roman', 14), textvariable=PASSWORD_LOGIN, width=20)
    password.grid(row=2, column=1,padx=10)
    password.insert(0, "Enter your password")  # Placeholder for password
    password.config(fg='grey')  # Set placeholder text color to grey
    password.bind("<FocusIn>", lambda event: password_on_focus_in(password, "Enter your password"))
    password.bind("<FocusOut>", lambda event: password_on_focus_out(password, "Enter your password"))

    btn_login = Button(LoginFrame, text="Login", font=('times new roman', 16,'bold'), width=20, command=Login, bg='#A5AAF7',
                       fg='white', relief='raised')
    btn_login.bind("<Enter>", lambda e: btn_login.config(bg="#B9BFFF"))
    btn_login.bind("<Leave>", lambda e: btn_login.config(bg="#A5AAF7"))
    btn_login.grid(row=4, columnspan=2, pady=30)

    lbl_text = Label(LoginFrame, text="Not a member?", font=('times new roman', 14))
    lbl_text.grid(row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register Now", fg="#00A4FF", font=('arial', 12))
    lbl_register.bind('<Enter>', lambda event, label=lbl_register: label.config(font=('arial', 12, 'underline')))
    lbl_register.bind('<Leave>', lambda event, label=lbl_register: label.config(font=('arial', 12)))
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_register.grid(row=6, columnspan=2)

    # Keep a reference to the image object to prevent garbage collection
    LoginFrame.image = bg_image

def on_entry_click(entry, placeholder):
    """function that gets called whenever entry is clicked"""
    if entry.get() == placeholder:
        entry.delete(0, "end")  # delete all the text in the entry
        entry.insert(0, '')  # Insert blank for user input
        entry.config(fg='black')

def on_focus_out(entry, placeholder):
    """function that gets called whenever entry is clicked out"""
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def password_on_focus_in(entry, placeholder):
    """Function that gets called when password entry gets focus"""
    if entry.get() == placeholder:
        entry.delete(0, "end")  # Delete placeholder text
        entry.config(fg='black', show='*')  # Change text color to black and show asterisks

def password_on_focus_out(entry, placeholder):
    """Function that gets called when password entry loses focus"""
    if not entry.get():
        entry.insert(0, placeholder)  # Restore placeholder text
        entry.config(fg='grey', show='')  # Change text color to grey and show placeholder text

def RegisterForm():
    global RegisterFrame, lbl_result2, confirm_password_entry
    RegisterFrame = Frame(root, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    RegisterFrame.pack(side='top', pady=50)

    lbl_login = Label(RegisterFrame, text="Click to Login", fg="#00A4FF", font=('arial', 12))
    lbl_login.bind('<Enter>', lambda event, label=lbl_login: label.config(font=('arial', 12, 'underline')))
    lbl_login.bind('<Leave>', lambda event, label=lbl_login: label.config(font=('arial', 12)))
    lbl_login.grid(row=11, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)

    lbl_result2 = Label(RegisterFrame, text="Registration Form:", font=('Script MT Bold', 24, 'bold'), fg='#0016BA', bd=18)
    lbl_result2.grid(row=1, columnspan=2)

    lbl_username = Label(RegisterFrame, text="Username:", font=('times new roman', 15), bd=18)
    lbl_username.grid(row=2)

    lbl_password = Label(RegisterFrame, text="Password:", font=('times new roman', 15), bd=18)
    lbl_password.grid(row=3)

    lbl_confirm_password = Label(RegisterFrame, text="Confirm Password:", font=('times new roman', 15), bd=18)
    lbl_confirm_password.grid(row=4)

    lbl_firstname = Label(RegisterFrame, text="First Name:", font=('times new roman', 15), bd=18)
    lbl_firstname.grid(row=5)

    lbl_lastname = Label(RegisterFrame, text="Last Name:", font=('times new roman', 15), bd=18)
    lbl_lastname.grid(row=6)

    lbl_date_of_birth = Label(RegisterFrame, text="Date of Birth:", font=('times new roman', 15), bd=18)
    lbl_date_of_birth.grid(row=7)

    lbl_email_address = Label(RegisterFrame, text="Email Address:", font=('times new roman', 15), bd=18)
    lbl_email_address.grid(row=8)

    lbl_phone_number = Label(RegisterFrame, text="Phone number:", font=('times new roman', 15), bd=18)
    lbl_phone_number.grid(row=9)

    # Clear existing text in the entry fields
    USERNAME_REGISTER.set("")
    PASSWORD_REGISTER.set("")
    FIRSTNAME.set("")
    LASTNAME.set("")
    DATE_OF_BIRTH.set("")
    EMAIL_ADDRESS.set("")
    PHONE_NUMBER.set("")

    username = Entry(RegisterFrame, font=('times new roman', 15), textvariable=USERNAME_REGISTER, width=20)
    username.grid(row=2, column=1,padx=10)
    username.insert(0, "Enter your username")  # Placeholder for username
    username.config(fg='grey')  # Set placeholder text color to grey
    username.bind("<FocusIn>", lambda event: on_entry_click(username, "Enter your username"))
    username.bind("<FocusOut>", lambda event: on_focus_out(username, "Enter your username"))

    password = Entry(RegisterFrame, font=('times new roman', 15), textvariable=PASSWORD_REGISTER, width=20)
    password.grid(row=3, column=1,padx=10)
    password.insert(0, "Enter your password")  # Placeholder for password
    password.config(fg='grey')  # Set placeholder text color to grey
    password.bind("<FocusIn>", lambda event: password_on_focus_in(password, "Enter your password"))
    password.bind("<FocusOut>", lambda event: password_on_focus_out(password, "Enter your password"))

    confirm_password_entry = Entry(RegisterFrame, font=('times new roman', 15), width=20)
    confirm_password_entry.grid(row=4, column=1,padx=10)
    confirm_password_entry.insert(0, "Confirm your password")  # Placeholder for confirm password
    confirm_password_entry.config(fg='grey')  # Set placeholder text color to grey
    confirm_password_entry.bind("<FocusIn>",
                                lambda event: password_on_focus_in(confirm_password_entry, "Confirm your password"))
    confirm_password_entry.bind("<FocusOut>",
                                lambda event: password_on_focus_out(confirm_password_entry, "Confirm your password"))

    firstname = Entry(RegisterFrame, font=('times new roman', 15), textvariable=FIRSTNAME, width=20)
    firstname.grid(row=5, column=1,padx=10)
    firstname.insert(0, "Enter your first name")  # Placeholder for first name
    firstname.config(fg='grey')  # Set placeholder text color to grey
    firstname.bind("<FocusIn>", lambda event: on_entry_click(firstname, "Enter your first name"))
    firstname.bind("<FocusOut>", lambda event: on_focus_out(firstname, "Enter your first name"))

    lastname = Entry(RegisterFrame, font=('times new roman', 15), textvariable=LASTNAME, width=20)
    lastname.grid(row=6, column=1,padx=10)
    lastname.insert(0, "Enter your last name")  # Placeholder for last name
    lastname.config(fg='grey')  # Set placeholder text color to grey
    lastname.bind("<FocusIn>", lambda event: on_entry_click(lastname, "Enter your last name"))
    lastname.bind("<FocusOut>", lambda event: on_focus_out(lastname, "Enter your last name"))

    date_of_birth = Entry(RegisterFrame, font=('times new roman', 15), textvariable=DATE_OF_BIRTH, width=20)
    date_of_birth.grid(row=7, column=1,padx=10)
    date_of_birth.insert(0, "Enter day-month-year")  # Placeholder for date of birth
    date_of_birth.config(fg='grey')  # Set placeholder text color to grey
    date_of_birth.bind("<FocusIn>", lambda event: on_entry_click(date_of_birth, "Enter day-month-year"))
    date_of_birth.bind("<FocusOut>", lambda event: on_focus_out(date_of_birth, "Enter day-month-year"))

    email_address = Entry(RegisterFrame, font=('times new roman', 15), textvariable=EMAIL_ADDRESS, width=20)
    email_address.grid(row=8, column=1,padx=10)
    email_address.insert(0, "Enter your email address")  # Placeholder for email address
    email_address.config(fg='grey')  # Set placeholder text color to grey
    email_address.bind("<FocusIn>", lambda event: on_entry_click(email_address, "Enter your email address"))
    email_address.bind("<FocusOut>", lambda event: on_focus_out(email_address, "Enter your email address"))

    phone_number = Entry(RegisterFrame, font=('times new roman', 15), textvariable=PHONE_NUMBER, width=20)
    phone_number.grid(row=9, column=1,padx=10)
    phone_number.insert(0, "Enter your phone number")  # Placeholder for phone number
    phone_number.config(fg='grey')  # Set placeholder text color to grey
    phone_number.bind("<FocusIn>", lambda event: on_entry_click(phone_number, "Enter your phone number"))
    phone_number.bind("<FocusOut>", lambda event: on_focus_out(phone_number, "Enter your phone number"))

    btn_register = Button(RegisterFrame, text="Register", font=('arial', 14,'bold'), width=20, command=Register, bg='#A5AAF7',
                          fg='white', relief='raised')
    btn_register.bind("<Enter>", lambda e: btn_register.config(bg="#B9BFFF"))
    btn_register.bind("<Leave>", lambda e: btn_register.config(bg="#A5AAF7"))
    btn_register.grid(row=10, columnspan=2, pady=20)

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
    global logged_in_user
    Database()
    if USERNAME_LOGIN.get() == "" or PASSWORD_LOGIN.get() == "":
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        cursor.execute("SELECT * FROM `customer` WHERE `username` = ? and `password` = ?",
                       (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        customer = cursor.fetchone()
        if customer is not None:
            logged_in_user['username'] = USERNAME_LOGIN.get()
            logged_in_user['password'] = PASSWORD_LOGIN.get()
            messagebox.showinfo("Success", "You Successfully Login")
            Home()
        else:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? and `password` = ?",
                           (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
            if cursor.fetchone() is not None:
                logged_in_user['username'] = USERNAME_LOGIN.get()
                logged_in_user['password'] = PASSWORD_LOGIN.get()
                messagebox.showinfo("Success", "You Successfully Login")
                AdminPanel()
            else:
                messagebox.showerror("Error", "Invalid username or password")


LoginForm()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

if __name__ == '__main__':
    root.mainloop()

