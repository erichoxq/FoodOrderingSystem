import sqlite3
import tkinter.messagebox as messagebox
from tkinter import ttk, Radiobutton, Tk, StringVar, Toplevel, Frame, Label, Entry, Button, Text, Scrollbar, VERTICAL, filedialog, END, IntVar, Canvas, Menu,DISABLED,NORMAL
from datetime import datetime
from PIL import Image, ImageTk
from fpdf import FPDF
import os, webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Progressbar, Style

root = Tk()

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
        "CREATE TABLE IF NOT EXISTS `customer` (customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20) NOT NULL, "
        "password TEXT(20) NOT NULL, firstname TEXT(20) NOT NULL, lastname TEXT(20) NOT NULL, date_of_birth DATE NOT NULL, email_address TEXT(30) NOT NULL, phone_number TEXT(20) NOT NULL)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `food` (food_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, food_name TEXT(30) NOT NULL, "
        "description TEXT(50) NOT NULL, price FLOAT NOT NULL, food_category TEXT(20) NOT NULL,food_calories INTEGER NOT NULL, image_path TEXT NOT NULL, admin_id INTEGER NOT NULL, FOREIGN KEY(admin_id) REFERENCES admin(admin_id) )")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `review` (review_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, customer_id INTEGER NOT NULL,"
        "review TEXT(20) NOT NULL,rating INTEGER NOT NULL, review_date DATE NOT NULL, payment_id INTEGER NOT NULL, FOREIGN KEY (customer_id) REFERENCES customer(customer_id),FOREIGN KEY (payment_id) REFERENCES payment(payment_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `payment` (payment_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, payment_date DATE NOT NULL, "
        "order_id INTEGER NOT NULL, total_price FLOAT NOT NULL,total_amount FLOAT NOT NULL, FOREIGN KEY(order_id) REFERENCES orders (order_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `orders` (order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, order_date DATE NOT NULL, "
        "total_price FLOAT NOT NULL, total_food_calories INTEGER NOT NULL, customer_id INTEGER NOT NULL, FOREIGN KEY(customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `orderitem` (order_item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, order_id INTEGER NOT NULL, food_id INTEGER NOT NULL, "
        "quantity INTEGER NOT NULL, total_price FLOAT NOT NULL, total_food_calories INTEGER NOT NULL, customer_id INTEGER NOT NULL, FOREIGN KEY(order_id) REFERENCES orders (order_id), FOREIGN KEY(food_id) REFERENCES food(food_id), FOREIGN KEY(customer_id) REFERENCES customer(customer_id))")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `admin`(admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT(20) NOT NULL, "
        "password TEXT(20) NOT NULL, firstname TEXT(20) NOT NULL, lastname TEXT(20) NOT NULL, date_of_birth DATE NOT NULL, email_address TEXT(30) NOT NULL, phone_number TEXT(20) NOT NULL)")


#admin
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
            form_frame.deiconify()

    # Hide the main login window
    root.withdraw()
    form_frame.withdraw()

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

    btn_food_dashboard = Button(AdminPanelFrame, text="Food Dashboard", font=('times new roman', 16, 'bold'), width=20,
                                command=FoodDashboard, bg='#65D954', fg='white')
    btn_food_dashboard.bind("<Enter>", lambda e: btn_food_dashboard.config(bg="#77FF63"))
    btn_food_dashboard.bind("<Leave>", lambda e: btn_food_dashboard.config(bg="#65D954"))
    btn_food_dashboard.pack(pady=10)

    btn_view_review_rating = Button(AdminPanelFrame, text="View Review and Rating", font=('times new roman', 16, 'bold'),
                                    width=20, command=view_review_rating, bg='#E0B715', fg='white')
    btn_view_review_rating.bind("<Enter>", lambda e: btn_view_review_rating.config(bg="#FACC18"))
    btn_view_review_rating.bind("<Leave>", lambda e: btn_view_review_rating.config(bg="#E0B715"))
    btn_view_review_rating.pack(pady=10)

    btn_view_total_orders = Button(AdminPanelFrame, text="View Total Orders", font=('times new roman', 16, 'bold'), width=20,
                                   command=view_total_orders, bg='#840BC7', fg='white')
    btn_view_total_orders.bind("<Enter>", lambda e: btn_view_total_orders.config(bg="#AA0EFF"))
    btn_view_total_orders.bind("<Leave>", lambda e: btn_view_total_orders.config(bg="#840BC7"))
    btn_view_total_orders.pack(pady=10)

    btn_admin_register_form = Button(AdminPanelFrame, text="Register Admin", font=('times new roman', 16, 'bold'),
                                   width=20,
                                   command=AdminRegisterForm, bg='#EE8AF8', fg='white')
    btn_admin_register_form.bind("<Enter>", lambda e: btn_admin_register_form.config(bg="#F58EFF"))
    btn_admin_register_form.bind("<Leave>", lambda e: btn_admin_register_form.config(bg="#EE8AF8"))
    btn_admin_register_form.pack(pady=10)

    btn_logout_admin = Button(AdminPanelFrame, text="Logout", font=('times new roman', 16, 'bold'), width=20,
                              command=Logout, bg='#7E84F7', fg='white')
    btn_logout_admin.bind("<Enter>", lambda e: btn_logout_admin.config(bg="#B8BEED"))
    btn_logout_admin.bind("<Leave>", lambda e: btn_logout_admin.config(bg="#7E84F7"))
    btn_logout_admin.pack(pady=10)

    # Keep a reference to the image object to prevent garbage collection
    AdminPanelFrame.image = bg_image

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
                width, height = image.size

                # Determine the size to crop the image to a square
                if width > height:
                    left = (width - height) / 2
                    top = 0
                    right = (width + height) / 2
                    bottom = height
                else:
                    left = 0
                    top = (height - width) / 2
                    right = width
                    bottom = (height + width) / 2

                # Crop the image to the calculated coordinates
                image = image.crop((left, top, right, bottom))

                # Resize the image to fit the display area
                image.thumbnail((400, 400), Image.Resampling.LANCZOS)

                # Convert the image to a PhotoImage object
                photo = ImageTk.PhotoImage(image)

                # Update the image_label with the new image
                image_label.config(image=photo)
                image_label.image = photo

                # Update the food name label
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
            form_frame.deiconify()

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
    FoodFrame.configure(bg="#FFE1C6")

    # Create a frame for the "Food Dashboard" title
    title_frame = Frame(FoodFrame, bg="#FFE1C6")
    title_frame.pack(side="top", pady=10)

    # Add the "Food Dashboard" label
    title_label = Label(title_frame, text="Food Dashboard", font=('Bauhaus 93', 24), bg="#FFE1C6")
    title_label.pack()

    # Create a frame to contain the food options buttons
    food_options_frame = Frame(FoodFrame, bg="#FFE1C6")
    food_options_frame.pack(side="top", pady=20)

    # Create the food options buttons
    search_frame = Frame(FoodFrame, bg="#FFE1C6")
    search_frame.pack(side="top", pady=20)

    search_label = Label(search_frame, text="Search Food:", font=('times new roman', 16), bg="#FFE1C6")
    search_label.pack(side="left", padx=10)

    search_entry = Entry(search_frame, font=('times new roman', 16))
    search_entry.pack(side="left", padx=10)
    search_entry.insert(0, "Search Food Name")  # Placeholder for search
    search_entry.config(fg='grey')  # Set placeholder text color to grey
    search_entry.bind("<FocusIn>", lambda event: on_entry_click(search_entry, "Search Food Name"))
    search_entry.bind("<FocusOut>", lambda event: on_focus_out(search_entry, "Search Food Name"))

    search_button = Button(search_frame, text="Search", font=('times new roman', 16, 'bold'),
                           command=lambda: search_food(search_entry.get()), bg='#D1D1D1', fg='black')
    search_button.bind("<Enter>", lambda e: search_button.config(bg="#808080"))
    search_button.bind("<Leave>", lambda e: search_button.config(bg="#D1D1D1"))
    search_button.pack(side="left", padx=10)

    btn_add_food = Button(food_options_frame, text="Add Food", font=('times new roman', 16, 'bold'), width=15,
                          command=add_food_window, bg='#E69312', fg='white', relief='raised')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFA314"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.pack(side="left", padx=10)

    btn_delete_food = Button(food_options_frame, text="Delete Food", font=('times new roman', 16, 'bold'), width=15,
                             command=delete_food, bg='red', fg='white', relief='raised')
    btn_delete_food.bind("<Enter>", lambda e: btn_delete_food.config(bg="#FF8080"))
    btn_delete_food.bind("<Leave>", lambda e: btn_delete_food.config(bg="red"))
    btn_delete_food.pack(side="left", padx=10)

    btn_update_food = Button(food_options_frame, text="Update Food", font=('times new roman', 16, 'bold'), width=15,
                             command=update_food_window, bg='green', fg='white')
    btn_update_food.bind("<Enter>", lambda e: btn_update_food.config(bg="light green"))
    btn_update_food.bind("<Leave>", lambda e: btn_update_food.config(bg="green"))
    btn_update_food.pack(side="left", padx=10)

    btn_back = Button(food_options_frame, text="Back to Admin Panel", font=('times new roman', 16, 'bold'), command=back_to_admin_panel,
                      bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side="left", padx=10)

    btn_Logout = Button(food_options_frame, text="Logout", font=('times new roman', 16, 'bold'), width=15, command=Logout,
                        bg='#7E84F7', fg='white')
    btn_Logout.bind("<Enter>", lambda e: btn_Logout.config(bg="#B8BEED"))
    btn_Logout.bind("<Leave>", lambda e: btn_Logout.config(bg="#7E84F7"))
    btn_Logout.pack(side="left", padx=10)

    # Food type filter buttons
    food_category_frame = Frame(FoodFrame, bg="#FFE1C6")
    food_category_frame.pack(side="bottom", pady=20)

    selected_food_category = StringVar(value="all")  # Default to "all"

    btn_all = Radiobutton(food_category_frame, text="All", font=('times new roman', 16), variable=selected_food_category,
                          value="all", bg="#FFE1C6")
    btn_all.pack(side="left", padx=10)

    btn_breakfast = Radiobutton(food_category_frame, text="Breakfast", font=('times new roman', 16), variable=selected_food_category,
                            value="Breakfast", bg="#FFE1C6")
    btn_breakfast.pack(side="left", padx=10)

    btn_lunch = Radiobutton(food_category_frame, text="Lunch", font=('times new roman', 16), variable=selected_food_category,
                             value="Lunch", bg="#FFE1C6")
    btn_lunch.pack(side="left", padx=10)

    btn_dinner = Radiobutton(food_category_frame, text="Dinner", font=('times new roman', 16),
                                 variable=selected_food_category, value="Dinner", bg="#FFE1C6")
    btn_dinner.pack(side="left", padx=10)

    btn_drinks = Radiobutton(food_category_frame, text="Drinks", font=('times new roman', 16),
                             variable=selected_food_category, value="Drinks", bg="#FFE1C6")
    btn_drinks.pack(side="left", padx=10)

    btn_dessert = Radiobutton(food_category_frame, text="Dessert", font=('times new roman', 16),
                             variable=selected_food_category, value="Dessert", bg="#FFE1C6")
    btn_dessert.pack(side="left", padx=10)

    # Apply Filter button
    btn_filter = Button(food_category_frame, text="Apply Filter", font=('times new roman', 16),
                        command=lambda: apply_filter(selected_food_category.get()), bg='#D1D1D1', fg='black')
    btn_filter.bind("<Enter>", lambda e: btn_filter.config(bg="#808080"))
    btn_filter.bind("<Leave>", lambda e: btn_filter.config(bg="#D1D1D1"))
    btn_filter.pack(side="left", padx=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), foreground="#148699")

    # Define columns
    columns = ("Food ID", "Food Name", "Description", "Price", "Food Category", "Food Calories", "Image Path")

    # Create a Treeview widget to display food items
    food_treeview = ttk.Treeview(FoodFrame, columns=columns, show='headings', style="Treeview")
    food_treeview.heading("Food ID", text="Food ID")
    food_treeview.heading("Food Name", text="Food Name")
    food_treeview.heading("Description", text="Description")
    food_treeview.heading("Price", text="Price")
    food_treeview.heading("Food Category", text="Food Category")
    food_treeview.heading("Food Calories", text="Food Calories")
    food_treeview.heading("Image Path", text="Image Path")

    food_treeview.column("Food ID", width=100, anchor="center")
    food_treeview.column("Food Name", width=150, anchor="center")
    food_treeview.column("Description", width=200, anchor="center")
    food_treeview.column("Price", width=100, anchor="center")
    food_treeview.column("Food Category", width=150, anchor="center")
    food_treeview.column("Food Calories", width=150, anchor="center")
    food_treeview.column("Image Path", width=150, anchor="center")

    food_treeview.pack(side="left", fill="both",padx=(20, 0))

    # Bind the selection event to the treeview
    food_treeview.bind("<<TreeviewSelect>>", on_food_select)

    # Add vertical scrollbar to the treeview
    scrollbar = ttk.Scrollbar(FoodFrame, orient="vertical", command=food_treeview.yview)
    food_treeview.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="left", fill="y")

    # Frame to hold image and food name label
    display_frame = Frame(FoodFrame, bg="#FFE1C6")
    display_frame.pack(side="left", padx=20, pady=20, anchor="nw")

    # Label to display selected food item image
    image_label = Label(display_frame, bg="#FFE1C6")
    image_label.pack()

    # Label to display selected food item name
    food_name_label = Label(display_frame, font=('times new roman', 16), bg="#FFE1C6")
    food_name_label.pack()

    # Initially, populate the treeview with all food items
    apply_filter("all")

def select_image(entry_image_path, image_label):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
    if file_path:
        entry_image_path.delete(0, END)
        entry_image_path.insert(0, file_path)

        try:
            image = Image.open(file_path)
            width, height = image.size

            # Crop the image to a square
            if width > height:
                left = (width - height) / 2
                top = 0
                right = (width + height) / 2
                bottom = height
            else:
                left = 0
                top = (height - width) / 2
                right = width
                bottom = (height + width) / 2

            image = image.crop((left, top, right, bottom)).resize((400, 400), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

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

def add_food_window():
    # Create a new window for adding food
    add_food_window = Toplevel()
    add_food_window.title("Add Food")
    add_food_window.geometry("1920x1080+0+0")  # window size and position
    add_food_window.state("zoomed")
    add_food_window.configure(bg="#FFEC92")

    # Add a label for the title "Update Food"
    title_label = Label(add_food_window, text="Add Food", font=('Bauhaus 93', 24, 'bold'), bg="#FFEC92")
    title_label.pack(pady=15)

    # Define the layout of the window
    frame = Frame(add_food_window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    frame.pack(side="top", anchor="center", padx=20, pady=20)

    # Define functions for clearing the input fields
    def clear_fields():
        entry_food_name.delete(0, 'end')
        entry_description.delete(0, 'end')
        entry_price.delete(0, 'end')
        combo_food_category.set('')
        entry_food_calories.delete(0, 'end')
        entry_image_path.delete(0, 'end')
        image_label.destroy()

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
    btn_select_image.grid(row=6, columnspan=2, pady=10)

    btn_add_food = Button(frame, text="Add Food", font=('times new roman', 16), command=lambda: [add_food(entry_food_name, entry_description, entry_price, combo_food_category, entry_food_calories, entry_image_path),add_food_window.destroy()], bg='#E69312', fg='white')
    btn_add_food.bind("<Enter>", lambda e: btn_add_food.config(bg="#FFC84E"))
    btn_add_food.bind("<Leave>", lambda e: btn_add_food.config(bg="#E69312"))
    btn_add_food.grid(row=7, columnspan=2, pady=10)

    btn_clear_fields = Button(frame, text="Clear Fields", font=('times new roman', 16), command=clear_fields,
                              bg='#EB7F7F', fg='white')
    btn_clear_fields.bind("<Enter>", lambda e: btn_clear_fields.config(bg="#FF8A8A"))
    btn_clear_fields.bind("<Leave>", lambda e: btn_clear_fields.config(bg="#EB7F7F"))
    btn_clear_fields.grid(row=8, columnspan=2, pady=10)

    btn_back = Button(frame, text="Back to Dashboard", font=('times new roman', 16), command=lambda:[add_food_window.destroy(),FoodDashboard],
                      bg='#7E84F7', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B8BEED"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#7E84F7"))
    btn_back.grid(row=9, columnspan=2, pady=10)

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

                # Add a label for the title "Update Food"
                title_label = Label(update_food_window, text="Update Food", font=('Bauhaus 93', 24, 'bold'),
                                    bg="#9AF4F5")
                title_label.pack(pady=20)

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
                    try:
                        image = Image.open(food_details[5])
                        width, height = image.size

                        # Determine the size to crop the image to a square
                        if width > height:
                            left = (width - height) / 2
                            top = 0
                            right = (width + height) / 2
                            bottom = height
                        else:
                            left = 0
                            top = (height - width) / 2
                            right = width
                            bottom = (height + width) / 2

                        # Crop the image to the calculated coordinates
                        image = image.crop((left, top, right, bottom))

                        # Resize the image to fit the display area
                        image.thumbnail((400, 400), Image.Resampling.LANCZOS)

                        # Convert the image to a PhotoImage object
                        photo = ImageTk.PhotoImage(image)

                        # Update the image_label with the new image
                        image_label.config(image=photo)
                        image_label.image = photo
                    except Exception as e:
                        messagebox.showerror("Error", f"Error loading image: {e}")

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

                btn_back = Button(frame, text="Back to Dashboard", font=('times new roman', 16), command=lambda: update_food_window.destroy(),
                                  bg='#7E84F7', fg='white')
                btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B8BEED"))
                btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#7E84F7"))
                btn_back.grid(row=9, columnspan=2, pady=20)
            else:
                messagebox.showerror("Error", "Selected food details not found.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food details: {e}")

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

def view_total_orders():
    try:
        # SQL query to calculate total orders and total cost per month
        query = """
            SELECT strftime('%Y-%m', order_date) AS month_year, COUNT(*) AS total_orders, SUM(total_price) AS total_cost
            FROM `orders`
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

def fetch_food_order_details():
    Database()
    cursor.execute("""
        SELECT 
            f.food_id,
            f.food_name,
            SUM(oi.quantity) AS total_orders,
            f.price AS price_per_item,
            SUM(oi.quantity * f.price) AS total_price
        FROM 
            orderitem oi
        JOIN 
            food f ON oi.food_id = f.food_id
        GROUP BY 
            f.food_id, f.food_name, f.price
    """)
    return cursor.fetchall()

def display_total_orders(results):
    def back_to_admin_panel():
        result = messagebox.askquestion('System', 'Are you sure you want to return to the admin panel?', icon="warning")
        if result == 'yes':
            total_orders_window.destroy()

    def display_food_order_details():
        food_order_details = fetch_food_order_details()

        # Clear existing data
        tree.delete(*tree.get_children())

        # Display food order details columns
        tree["columns"] = ("Food ID", "Food", "Total Orders", "Price per Item", "Total Price")
        tree.heading("Food ID", text="Food ID")
        tree.heading("Food", text="Food")
        tree.heading("Total Orders", text="Total Orders")
        tree.heading("Price per Item", text="Price per Item")
        tree.heading("Total Price", text="Total Price")

        # Adjust column widths and alignment
        tree.column("Food ID", width=100, anchor="center")
        tree.column("Food", width=200, anchor="center")
        tree.column("Total Orders", width=150, anchor="center")
        tree.column("Price per Item", width=150, anchor="center")
        tree.column("Total Price", width=150, anchor="center")

        for row in food_order_details:
            tree.insert("", "end", values=row)

    def show_total_orders_view():
        # Clear existing data
        tree.delete(*tree.get_children())

        # Display total orders columns
        tree["columns"] = ("Month", "Total Orders", "Total Cost")
        tree.heading("Month", text="Month")
        tree.heading("Total Orders", text="Total Orders")
        tree.heading("Total Cost", text="Total Cost")

        # Adjust column widths and alignment
        tree.column("Month", width=200, anchor="center")
        tree.column("Total Orders", width=150, anchor="center")
        tree.column("Total Cost", width=150, anchor="center")

        for row in results:
            tree.insert("", "end", values=row)

    total_orders_window = Toplevel()
    total_orders_window.title("Total Orders and Food Order Details")
    total_orders_window.geometry("1920x1080+0+0")  # window size and position
    total_orders_window.state("zoomed")
    total_orders_window.configure(bg="#F4D5FF")

    title_label = Label(total_orders_window, text="Total Orders and Food Order Details:", font=('Bauhaus 93', 18), fg='#4D8DAD', highlightbackground="black", highlightcolor="black", highlightthickness=2)
    title_label.pack(side="top", pady=10)

    tree_frame = Frame(total_orders_window)
    tree_frame.pack(expand=True, padx=20, fill="both")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14, 'bold'), foreground="blue")

    # Initialize Treeview with all possible columns
    tree = ttk.Treeview(tree_frame, columns=("Month", "Total Orders", "Total Cost", "Food", "Price per Item", "Total Price"), show="headings")
    tree.heading("Month", text="Month")
    tree.heading("Total Orders", text="Total Orders")
    tree.heading("Total Cost", text="Total Cost")
    tree.heading("Food", text="Food")
    tree.heading("Price per Item", text="Price per Item")
    tree.heading("Total Price", text="Total Price")

    # Configure column widths and alignment
    tree.column("Month", width=200, anchor="center")
    tree.column("Total Orders", width=150, anchor="center")
    tree.column("Total Cost", width=150, anchor="center")
    tree.column("Food", width=200, anchor="center")
    tree.column("Price per Item", width=150, anchor="center")
    tree.column("Total Price", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both")

    btn_food_details = Button(total_orders_window, text="Food Order Details", font=('times new roman', 16),
                              command=display_food_order_details, bg='#45AD29', fg='white')
    btn_food_details.bind("<Enter>", lambda e: btn_food_details.config(bg="#61F239"))
    btn_food_details.bind("<Leave>", lambda e: btn_food_details.config(bg="#45AD29"))
    btn_food_details.pack(side='left', padx=10, pady=10)

    btn_summary_view = Button(total_orders_window, text="Summary View", font=('times new roman', 16),
                              command=show_total_orders_view, bg='#4D8DAD', fg='white')
    btn_summary_view.bind("<Enter>", lambda e: btn_summary_view.config(bg="#60A3D9"))
    btn_summary_view.bind("<Leave>", lambda e: btn_summary_view.config(bg="#4D8DAD"))
    btn_summary_view.pack(side='left', padx=10, pady=10)

    btn_back = Button(total_orders_window, text="Back to Admin Panel", font=('times new roman', 16),
                      command=back_to_admin_panel, bg='#E061ED', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#F168FF"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#E061ED"))
    btn_back.pack(side='right', padx=10, pady=10)

    # Initially show the total orders view
    show_total_orders_view()

    total_orders_window.mainloop()

def view_review_rating():
    try:
        # SQL query to retrieve customer username, review, rating, and dates
        query = """
            SELECT c.username, r.review, r.rating, r.review_date
            FROM review r
            JOIN customer c ON r.customer_id = c.customer_id
        """

        # Execute the query
        cursor.execute(query)
        result = cursor.fetchall()

        # Display the results
        display_view_review_rating(result)
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching reviews and ratings: {e}")

def filter_reviews(results, filter_type):
    filtered_results = []
    for review, rating, review_date in results:
        if filter_type == 'All':
            filtered_results.append((review, rating, review_date))
        elif filter_type == 'Good' and rating >= 4:
            filtered_results.append((review, rating, review_date))
        elif filter_type == 'Bad' and rating <= 2:
            filtered_results.append((review, rating, review_date))
    return filtered_results

def sort_reviews(results, sort_type):
    if sort_type == 'None':
        return results
    elif sort_type == 'New_to_Old':
        return sorted(results, key=lambda x: x[2], reverse=True)  # Sort by review_date descending
    elif sort_type == 'Old_to_New':
        return sorted(results, key=lambda x: x[2])  # Sort by review_date ascending

def display_view_review_rating(results):
    def back_to_admin_panel():
        result = messagebox.askquestion('System', 'Are you sure you want to return to the admin panel?', icon="warning")
        if result == 'yes':
            review_window.destroy()

    def display_reviews_chart():
        ratings = [1, 2, 3, 4, 5]
        rating_counts = {rating: 0 for rating in ratings}
        total_reviews = len(results)

        for _, _, rating, _ in results:
            if rating in rating_counts:
                rating_counts[rating] += 1

        percentages = [rating_counts[rating] / total_reviews * 100 if total_reviews > 0 else 0 for rating in ratings]

        fig, ax = plt.subplots(figsize=(8, 6))

        bars = ax.bar(ratings, percentages, color='royalblue', alpha=0.85)

        ax.set_xlabel('Rating', fontsize=12, fontweight='bold')
        ax.set_ylabel('Percentage of Reviews (%)', fontsize=12, fontweight='bold')
        ax.set_title(f'Customer Review Ratings (Total Reviews: {total_reviews})', fontsize=14, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=10)

        for bar, percentage in zip(bars, percentages):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, f'{percentage:.1f}%', ha='center', va='bottom', fontsize=8, fontweight='bold')

        fig.tight_layout(pad=3)

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    def apply_filter(filter_type):
        nonlocal results_display
        results_display = filter_reviews(results, filter_type)
        refresh_treeview(results_display)

    def apply_sort(sort_type):
        nonlocal results_display
        results_display = sort_reviews(results_display, sort_type)
        refresh_treeview(results_display)

    def refresh_treeview(results_to_display):
        tree.delete(*tree.get_children())
        for username, review, rating, review_date in results_to_display:
            tree.insert("", "end", values=(username, review, rating, review_date))

    def filter_reviews(results, filter_type):
        if filter_type == 'Good':
            return [result for result in results if result[2] >= 4]
        elif filter_type == 'Bad':
            return [result for result in results if result[2] <= 2]
        else:
            return results

    def sort_reviews(results, sort_type):
        if sort_type == 'New_to_Old':
            return sorted(results, key=lambda x: x[3], reverse=True)
        elif sort_type == 'Old_to_New':
            return sorted(results, key=lambda x: x[3])
        else:
            return results

    review_window = Toplevel()
    review_window.title("Customer Review and Rating")
    review_window.geometry("1920x1080+0+0")  # window size and position
    review_window.state("zoomed")
    review_window.configure(bg="#E6E6FA")

    title_label = Label(review_window, text="Customer Review Ratings", font=('Bauhaus 93', 24), fg='#4D8DAD',
                        bg='#E6E6FA', highlightbackground="black", highlightcolor="black", highlightthickness=2)
    title_label.pack(side='top', pady=10)

    # Filter and Sort Options
    filter_frame = Frame(review_window, bg="#E6E6FA")
    filter_frame.pack(side='top', anchor='ne', padx=20, pady=10)

    filter_label = Label(filter_frame, text="Filter:", font=('times new roman', 12), bg="#E6E6FA")
    filter_label.grid(row=0, column=0, padx=5)

    filter_options = ttk.Combobox(filter_frame, values=['All', 'Good', 'Bad'], state='readonly', width=10)
    filter_options.current(0)
    filter_options.grid(row=0, column=1, padx=5)

    filter_button = Button(filter_frame, text="Apply Filter", command=lambda: apply_filter(filter_options.get()),
                           bg='#E061ED', fg='white', activebackground='#F168FF', activeforeground='white')
    filter_button.grid(row=0, column=2, padx=5)

    sort_label = Label(filter_frame, text="Sort:", font=('times new roman', 12), bg="#E6E6FA")
    sort_label.grid(row=0, column=3, padx=5)

    sort_options = ttk.Combobox(filter_frame, values=['None', 'New to Old', 'Old to New'], state='readonly', width=12)
    sort_options.current(0)
    sort_options.grid(row=0, column=4, padx=5)

    sort_button = Button(filter_frame, text="Apply Sort",
                         command=lambda: apply_sort(sort_options.get().replace(' ', '_')), bg='#E061ED', fg='white',
                         activebackground='#F168FF', activeforeground='white')
    sort_button.grid(row=0, column=5, padx=5)

    # Frames for chart and treeview
    main_frame = Frame(review_window, bg="#E6E6FA")
    main_frame.pack(side='top', fill='both', expand=True, padx=20, pady=10)

    chart_frame = Frame(main_frame, bg="#E6E6FA")
    chart_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)

    tree_frame = Frame(main_frame)
    tree_frame.pack(side='right', fill='both', expand=True, padx=10, pady=5)

    display_reviews_chart()

    style = ttk.Style()
    style.configure("Treeview", font=('times new roman', 12), rowheight=25)
    style.configure("Treeview.Heading", font=('times new roman', 14, 'bold'), foreground="blue")
    style.map("Treeview", background=[("selected", "#6A5ACD")], foreground=[("selected", "white")])

    tree = ttk.Treeview(tree_frame, columns=("Username", "Review", "Rating", "Date"), show="headings")
    tree.heading("Username", text="Username")
    tree.heading("Review", text="Review")
    tree.heading("Rating", text="Rating")
    tree.heading("Date", text="Date")

    tree.column("Username", width=100, anchor="center")
    tree.column("Review", width=300, anchor="center")
    tree.column("Rating", width=100, anchor="center")
    tree.column("Date", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    results_display = results
    refresh_treeview(results_display)

    tree.pack(expand=True, fill="both")

    # Back to Admin Panel Button
    btn_back = Button(review_window, text="Back to Admin Panel", font=('times new roman', 16), command=back_to_admin_panel,
                      bg='#E061ED', fg='white', activebackground='#F168FF', activeforeground='white')
    btn_back.pack(side='bottom', pady=5)

    review_window.mainloop()



#customer
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
            width, height = image.size

            # Determine the size to crop the image to a square
            if width > height:
                left = (width - height) / 2
                top = 0
                right = (width + height) / 2
                bottom = height
            else:
                left = 0
                top = (height - width) / 2
                right = width
                bottom = (height + width) / 2

            # Crop the image to the calculated coordinates
            image = image.crop((left, top, right, bottom))

            # Resize the image to fit the display area
            image.thumbnail((250, 250), Image.Resampling.LANCZOS)

            # Convert the image to a PhotoImage object
            photo = ImageTk.PhotoImage(image)

            # Update the image_label with the new image
            image_label = Label(detail_window, image=photo, bg="white")
            image_label.image = photo
            image_label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

        info_frame = Frame(detail_window, bg="white")
        info_frame.pack(fill='both', expand=True, padx=20, pady=10)

        description_label = Label(info_frame, text=f"Description: {description}", font=('Arial', 12), bg="white",
                                  wraplength=450)
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

def ViewFoodMenu():
    def fetch_food_by_category(category):
        if category == "Best Selling":
            query = """
            SELECT food.food_id, food.food_name, food.description, food.price, food.food_category, food.food_calories, food.image_path, SUM(orderitem.quantity) as total_sold
            FROM orderitem
            JOIN food ON orderitem.food_id = food.food_id
            GROUP BY food.food_id
            ORDER BY total_sold DESC
            LIMIT 8
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

            add_to_cart_btn = Button(button_frame, text="Add to Cart", font=('Arial', 10),command=lambda f_id=food_id, f_name=food_name, f_price=price, f_calories=food_calories, f_image_path=image_path: add_to_cart(f_id, f_name, f_price, f_calories,f_image_path),bg="#FFFE91")
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

    def search_food(query, current_category):
        try:
            if query.strip() == "":
                if current_category == "Best Selling":
                    # Fetch and display best-selling items
                    items = fetch_food_by_category("Best Selling")
                    if items:
                        display_food_items(items)
                    else:
                        messagebox.showinfo("No Results", "No best-selling items found.")
                else:
                    # Fetch and display items from the selected category
                    sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_name LIKE ? AND food_category = ?"
                    cursor.execute(sql_query, ('%' + query + '%', current_category))
                    rows = cursor.fetchall()
                    if rows:
                        display_food_items(rows)
                    else:
                        messagebox.showinfo("No Results", f"No items found in the {current_category} category.")
            else:
                if current_category == "Best Selling":
                    # Search among best-selling items
                    sql_query = """
                    SELECT food.food_id, food.food_name, food.description, food.price, food.food_category, food.food_calories, food.image_path, SUM(orderitem.quantity) as total_sold
                    FROM orderitem
                    JOIN food ON orderitem.food_id = food.food_id
                    WHERE food.food_name LIKE ?
                    GROUP BY food.food_id
                    ORDER BY total_sold DESC
                    """
                    cursor.execute(sql_query, ('%' + query + '%',))
                    rows = cursor.fetchall()
                    if rows:
                        display_food_items(rows[:5])  # Display top 5 results
                    else:
                        messagebox.showinfo("No Results", "No best-selling items match your search.")
                else:
                    # Search for items based on the query in the selected category
                    sql_query = "SELECT food_id, food_name, description, price, food_category, food_calories, image_path FROM food WHERE food_name LIKE ? AND food_category = ?"
                    cursor.execute(sql_query, ('%' + query + '%', current_category))
                    rows = cursor.fetchall()
                    if rows:
                        display_food_items(rows)
                    else:
                        messagebox.showinfo("No Results",
                                            f"No items match your search in the {current_category} category.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching food data: {e}")

    def logout():
        result = messagebox.askquestion('System', 'Are you sure you want to logout?', icon="warning")
        if result == 'yes':
            cart.clear()
            MenuFrame.destroy()
            form_frame.deiconify()

    root.withdraw()
    form_frame.withdraw()

    MenuFrame = Toplevel()
    MenuFrame.title("Food Menu")
    MenuFrame.geometry("1920x1080+0+0")  # window size and position
    MenuFrame.state("zoomed")
    MenuFrame.configure(bg="#f8f8f8")

    top_frame = Frame(MenuFrame, bg="#BACFFA", height=100)
    top_frame.pack(fill='x')

    title_label = Label(top_frame, text="Food Menu", font=('Edwardian Script ITC', 45, 'bold'), bg="#BACFFA")
    title_label.pack(pady=20)

    selected_category = StringVar(value="Best Selling")

    search_frame = Frame(top_frame, bg="#BACFFA")
    search_frame.pack(side='bottom', pady=10)

    # Display selected category name above the search entry
    selected_category_label = Label(search_frame, text=selected_category.get(), font=('Bauhaus 93', 20, 'bold','underline'), bg="#BACFFA",fg='#796796')
    selected_category_label.pack(side='top', pady=5)

    search_entry = Entry(search_frame, font=('Arial', 12), width=30)
    search_entry.pack(side='left', padx=10)
    search_entry.insert(0, "Search Food Name")  # Placeholder for search
    search_entry.config(fg='grey')  # Set placeholder text color to grey
    search_entry.bind("<FocusIn>", lambda event: on_entry_click(search_entry, "Search Food Name"))
    search_entry.bind("<FocusOut>", lambda event: on_focus_out(search_entry, "Search Food Name"))

    search_btn = Button(search_frame, text="Search", font=('Arial', 12),bg="#D1D1D1", command=lambda: search_food(search_entry.get(), selected_category.get()))
    search_btn.bind("<Enter>", lambda e: search_btn.config(bg="#808080"))
    search_btn.bind("<Leave>", lambda e: search_btn.config(bg="#D1D1D1"))
    search_btn.pack(side='left')

    category_frame = Frame(MenuFrame, bg="#9CA8F7", height=50, highlightbackground="black", highlightcolor="black",
                           highlightthickness=2)
    category_frame.pack(side='left', fill='y')

    category_label = Label(category_frame, text="Category", font=('Bauhaus 93', 14, 'bold'), bg="#9CA8F7")
    category_label.pack(pady=10)

    categories = ["Best Selling", "Breakfast", "Lunch", "Dinner", "Drinks", "Dessert"]

    def update_selected_category(category):
        selected_category.set(category)
        selected_category_label.config(text=selected_category.get())
        display_food_items(fetch_food_by_category(category))

    for category in categories:
        category_btn = Radiobutton(category_frame, text=category, variable=selected_category, value=category,
                                   indicatoron=0,
                                   font=('Arial', 14), bg="#C6B0D6",
                                   command=lambda c=category: update_selected_category(c), width=9)  # Adjust the width value as needed
        category_btn.pack(fill='y', padx=5, pady=3)

    # Frame for food items with scrollbar
    food_frame = Frame(MenuFrame, bg="#f8f8f8")
    food_frame.pack(fill='both', expand=True, pady=10)

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

    logout_btn = Button(bottom_frame, text="Logout", font=('Arial', 14, 'bold'), command=logout, bg='#5DC2AB',
                        fg='black')
    logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#72EDD1"))
    logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#5DC2AB"))
    logout_btn.pack(side='right', padx=10, pady=10)

def add_to_cart(food_id, food_name, price, food_calories, image_path):
    # Check if the item is already in the cart
    found_in_cart = False
    for index, item in enumerate(cart):
        if item[0] == food_id:
            # Update quantity if item already in cart
            cart[index] = (food_id, food_name, price, food_calories, item[4] + 1, image_path)
            found_in_cart = True
            break

    if not found_in_cart:
        # Add new item to cart with quantity 1
        cart.append((food_id, food_name, price, food_calories, 1, image_path))

    messagebox.showinfo("Success", f"{food_name} added to cart!")
    # For debugging: print the current contents of the cart
    print("Cart:", cart)

def ViewCart():
    def update_cart_table(filtered_cart=None):
        for widget in items_frame.winfo_children():
            widget.destroy()

        display_cart = filtered_cart if filtered_cart is not None else cart

        # Create table headers
        headers = ["No.", "Food ID", "Food", "Details", "Quantity", "Total Price", ""]
        for col_num, header in enumerate(headers):
            header_label = Label(items_frame, text=header, font=('Arial', 16, 'bold'), bg="white")
            header_label.grid(row=0, column=col_num, padx=20, pady=10)

        for row_num, item in enumerate(display_cart, start=1):
            food_id, food_name, price, food_calories, quantity, image_path = item

            # Row Number
            row_label = Label(items_frame, text=str(row_num), font=('Arial', 12), bg="white")
            row_label.grid(row=row_num * 2 - 1, column=0, padx=20, pady=10, sticky="nsew")

            # Food ID
            food_id_label = Label(items_frame, text=str(food_id), font=('Arial', 12), bg="white")
            food_id_label.grid(row=row_num * 2 - 1, column=1, padx=20, pady=10, sticky="nsew")

            # Description with image
            desc_frame = Frame(items_frame, bg="white")
            desc_frame.grid(row=row_num * 2 - 1, column=2, padx=20, pady=10, sticky="nsew")
            try:
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)  # Resize image as needed
                img = ImageTk.PhotoImage(img)
                img_label = Label(desc_frame, image=img)
                img_label.image = img
                img_label.pack(side='left', padx=10, pady=10)
            except Exception as e:
                print(f"Error loading image: {e}")
                img_label = Label(desc_frame, text="No Image", width=10, height=5)
                img_label.pack(side='left', padx=10, pady=10)

            # Name Label with Details
            name_label_text = f"{food_name}\nCost: RM{price:.2f}\nCalories: {food_calories}"
            name_label = Label(desc_frame, text=name_label_text, font=('Arial', 12), bg="white", justify="left")
            name_label.pack(side='left', padx=10, pady=10)

            # Details Button (in Details Column)
            details_button = Button(items_frame, text="Details", font=('Arial', 12), bg="lightblue", fg="black",
                                    command=lambda i=food_id: show_food_detail(i))
            details_button.grid(row=row_num * 2 - 1, column=3, padx=40, pady=45, sticky="nsew")

            # Quantity Control
            qty_frame = Frame(items_frame, bg="white")
            qty_frame.grid(row=row_num * 2 - 1, column=4, padx=20, pady=10, sticky="nsew")
            Button(qty_frame, text="-", font=('Arial', 14),
                   command=lambda i=cart.index(item): decrease_quantity(i)).pack(side="left", padx=10, pady=10)
            qty_label = Label(qty_frame, text=str(quantity), font=('Arial', 14))
            qty_label.pack(side="left", padx=10, pady=10)
            Button(qty_frame, text="+", font=('Arial', 14),
                   command=lambda i=cart.index(item): increase_quantity(i)).pack(side="left", padx=10, pady=10)

            # Price
            price_label = Label(items_frame, text=f"RM{price * quantity:.2f}", font=('Arial', 18), fg="blue",
                                bg="white")
            price_label.grid(row=row_num * 2 - 1, column=5, padx=20, pady=10, sticky="nsew")

            # Delete Button
            if show_delete_buttons:
                delete_button = Button(items_frame, text="X", font=('Arial', 18), bg="red", fg="white",
                                       command=lambda i=cart.index(item): delete_item(i))
                delete_button.grid(row=row_num * 2 - 1, column=6, padx=40, pady=45, sticky="nsew")
            else:
                remove_placeholder = Label(items_frame, text="", font=('Arial', 18), bg="white")
                remove_placeholder.grid(row=row_num * 2 - 1, column=6, padx=20, pady=10, sticky="nsew")

            # Add separator
            separator = ttk.Separator(items_frame, orient='horizontal')
            separator.grid(row=row_num * 2, column=0, columnspan=7, sticky='ew', pady=10)

        total_price = sum(item[2] * item[4] for item in display_cart)
        total_calories = sum(item[3] * item[4] for item in display_cart)
        lbl_total_price.config(text=f"Total Amount: RM{total_price:.2f}")
        lbl_total_food_calories.config(text=f"Total Calories: {total_calories}")

    def decrease_quantity(index):
        if cart[index][4] > 1:
            cart[index] = (
                cart[index][0], cart[index][1], cart[index][2], cart[index][3], cart[index][4] - 1, cart[index][5])
            update_cart_table()

    def increase_quantity(index):
        cart[index] = (
            cart[index][0], cart[index][1], cart[index][2], cart[index][3], cart[index][4] + 1, cart[index][5])
        update_cart_table()

    def delete_item(index):
        del cart[index]
        update_cart_table()

    def place_order(total_price_str, total_calories_str, cart_data, cart_window):
        try:
            if not cart_data:  # Check if cart is empty
                messagebox.showerror("Error", "Cannot place order. Cart is empty.")
                return

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
            total_price = float(total_price_str.split(": ")[1].replace("RM", ""))
            total_food_calories = int(total_calories_str.split(": ")[1])

            # Insert a new order in the Orders table
            order_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO `orders` (order_date, total_price, total_food_calories, customer_id) VALUES (?, ?, ?, ?)",
                (order_date, total_price, total_food_calories, customer_id)
            )
            order_id = cursor.lastrowid  # Get the last inserted order_id

            # Insert each item in the cart into the OrderItems table
            for item in cart_data:
                food_id, _, price, food_calories, quantity = item[:5]  # Ensure only first 5 elements are unpacked
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

    def toggle_delete_buttons():
        nonlocal show_delete_buttons
        show_delete_buttons = not show_delete_buttons
        update_cart_table()
        if show_delete_buttons:
            toggle_button.config(text="Done")
        else:
            toggle_button.config(text="🗑️")

    def search_food():
        query = search_entry.get().lower()
        filtered_cart = [item for item in cart if query in item[1].lower()]
        update_cart_table(filtered_cart)

    # Function to fetch customer ID based on username and password
    def fetch_customer_id(username, password):
        conn = sqlite3.connect("db_food_ordering_system.db")
        cursor = conn.cursor()

        try:
            # Fetch the customer ID based on the stored username and password
            query = """
                    SELECT customer_id
                    FROM customer
                    WHERE username = ? AND password = ?
                    """
            cursor.execute(query, (username, password))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise sqlite3.Error("Customer not found")

            customer_id = customer_data[0]  # Extract customer_id from the fetched data

            # Return the customer_id for further processing
            return customer_id

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return None

    # Function to fetch customer data from the database
    def fetch_customer_data(customer_id):
        conn = sqlite3.connect("db_food_ordering_system.db")
        cursor = conn.cursor()

        # Example query to fetch customer data
        cursor.execute("SELECT username, firstname, lastname, email_address, password FROM customer WHERE customer_id = ?",
                       (customer_id,))
        customer_data = cursor.fetchone()

        return customer_data

    # Function to update customer data in the database
    def update_customer_data(customer_id, new_username, firstname, lastname, email, new_password):
        conn = sqlite3.connect("db_food_ordering_system.db")
        cursor = conn.cursor()

        try:
            # Check if the new username is already in use by another customer
            cursor.execute("SELECT customer_id FROM customer WHERE username = ? AND customer_id != ?",
                           (new_username, customer_id))
            existing_customer = cursor.fetchone()

            if existing_customer:
                messagebox.showerror("Username Error", "Username already exists. Please choose a different username.")
                return False  # Return False to indicate failure

            # Update the customer data
            cursor.execute(
                "UPDATE customer SET username = ?, firstname = ?, lastname = ?, email_address = ?, password = ? WHERE customer_id = ?",
                (new_username, firstname, lastname, email, new_password, customer_id)
            )
            conn.commit()

            # Update logged_in_user if the update was successful
            logged_in_user['username'] = new_username
            logged_in_user['password'] = new_password

            return True  # Return True to indicate success

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

            return False

    # Function to load customer data into labels and allow editing
    def load_customer_data_view(customer_id):
        customer_data = fetch_customer_data(customer_id)
        if customer_data:
            username_var.set(customer_data[0])
            firstname_var.set(customer_data[1])
            lastname_var.set(customer_data[2])
            email_var.set(customer_data[3])
            password_var.set(customer_data[4])

    def save_customer_data(customer_id):
        username = username_var.get()
        firstname = firstname_var.get()
        lastname = lastname_var.get()
        email = email_var.get()
        password = password_var.get()

        if update_customer_data(customer_id, username, firstname, lastname, email, password):
            # Update was successful, reload customer data using new username and password
            load_customer_data_view(customer_id)
            messagebox.showinfo("Success", "Customer information updated successfully!")
        else:
            # Update failed, reload customer data using old username and password
            load_customer_data_view(customer_id)

    def toggle_edit_save():
        nonlocal is_edit_mode
        if is_edit_mode:
            # Save mode: Save the data and disable entries
            save_customer_data(customer_id)
            toggle_entry_state(DISABLED)
            edit_save_button.config(text="Edit")
        else:
            # Edit mode: Enable the entries for editing
            toggle_entry_state(NORMAL)
            edit_save_button.config(text="Save")

        # Toggle the edit mode
        is_edit_mode = not is_edit_mode

    def toggle_entry_state(state):
        # Toggle the state of the entry fields
        username_entry.config(state=state)
        firstname_entry.config(state=state)
        lastname_entry.config(state=state)
        email_entry.config(state=state)
        password_entry.config(state=state)

    cart_window = Toplevel()
    cart_window.title("Shopping Cart")
    cart_window.geometry("1920x1080+0+0")
    cart_window.state("zoomed")
    cart_window.configure(bg="#F7F6AF")

    top_frame = Frame(cart_window, bg="#F7F6AF")
    top_frame.pack(fill='x')

    # Add Cart Label at the top
    cart_label = Label(top_frame, text="Shopping Cart", font=('Edwardian Script ITC', 30, 'bold'), bg="#F7F6AF")
    cart_label.pack(side="top", padx=10, pady=5)

    search_frame = Frame(top_frame, bg="#F7F6AF")
    search_frame.pack(pady=5)

    search_label = Label(search_frame, text="Search Food:", font=('Arial', 14), bg="#F7F6AF")
    search_label.pack(side='left')

    search_entry = Entry(search_frame, font=('Arial', 14), width=20)  # Adjust width as needed
    search_entry.pack(side='left', padx=5)
    search_entry.insert(0, "Search Food Name")  # Placeholder for search
    search_entry.config(fg='grey')  # Set placeholder text color to grey
    search_entry.bind("<FocusIn>", lambda event: on_entry_click(search_entry, "Search Food Name"))
    search_entry.bind("<FocusOut>", lambda event: on_focus_out(search_entry, "Search Food Name"))

    search_button = Button(search_frame, text="Search", font=('Arial', 14),bg="#D1D1D1", command=search_food)
    search_button.bind("<Enter>", lambda e: search_button.config(bg="#808080"))
    search_button.bind("<Leave>", lambda e: search_button.config(bg="#D1D1D1"))
    search_button.pack(side='left', padx=5)

    # Toggle Button with emoji
    toggle_button = Button(search_frame, text="🗑️", font=('Arial', 14),bg="#ED746E", command=toggle_delete_buttons)
    toggle_button.bind("<Enter>", lambda e: toggle_button.config(bg="#FF7C76"))
    toggle_button.bind("<Leave>", lambda e: toggle_button.config(bg="#ED746E"))
    toggle_button.pack(side='left', pady=10, padx=5)

    # Fetch customer_id from logged_in_user
    customer_id = fetch_customer_id(logged_in_user['username'], logged_in_user['password'])

    # Create the left side frame (for customer information and action buttons)
    left_frame = Frame(cart_window, bg="#F7F6AF", width=300)
    left_frame.pack(side="left", fill="y", padx=10, pady=10, anchor="n")

    # Create a frame for the customer information section with light blue background
    customer_section_frame = Frame(left_frame, bg="#d9edf7", padx=20, pady=10,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    customer_section_frame.pack(anchor="n", pady=10, fill="both", expand=True)

    # Customer Information Section at the top of left_frame
    customer_info_frame = Frame(customer_section_frame, bg="#d9edf7")
    customer_info_frame.pack(anchor="n", pady=10)

    # Label for "Customer Information"
    customer_info_label = Label(customer_info_frame, text="Customer Information", font=('Arial', 18, 'bold','underline'),
                                bg="#d9edf7")
    customer_info_label.grid(row=0, columnspan=2, padx=20, pady=10)

    username_var = StringVar()
    firstname_var = StringVar()
    lastname_var = StringVar()
    email_var = StringVar()
    password_var = StringVar()

    # Load customer data into the variables
    load_customer_data_view(customer_id)

    username_label = Label(customer_info_frame, text="Username:", font=('Arial', 12), bg="#d9edf7")
    username_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
    username_entry = Entry(customer_info_frame, textvariable=username_var, font=('Arial', 12))
    username_entry.grid(row=1, column=1, padx=20, pady=5)

    # First Name Entry
    firstname_label = Label(customer_info_frame, text="First Name:", font=('Arial', 12), bg="#d9edf7")
    firstname_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
    firstname_entry = Entry(customer_info_frame, textvariable=firstname_var, font=('Arial', 12))
    firstname_entry.grid(row=2, column=1, padx=20, pady=5)

    # Last Name Entry
    lastname_label = Label(customer_info_frame, text="Last Name:", font=('Arial', 12), bg="#d9edf7")
    lastname_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
    lastname_entry = Entry(customer_info_frame, textvariable=lastname_var, font=('Arial', 12))
    lastname_entry.grid(row=3, column=1, padx=20, pady=5)

    # Email Entry
    email_label = Label(customer_info_frame, text="Email:", font=('Arial', 12), bg="#d9edf7")
    email_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
    email_entry = Entry(customer_info_frame, textvariable=email_var, font=('Arial', 12))
    email_entry.grid(row=4, column=1, padx=20, pady=5)

    password_label = Label(customer_info_frame, text="Password:", font=('Arial', 12), bg="#d9edf7")
    password_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
    password_entry = Entry(customer_info_frame, textvariable=password_var, font=('Arial', 12))
    password_entry.grid(row=5, column=1, padx=20, pady=5)

    # Save Button for Customer Information
    # Edit/Save Button for Customer Information
    is_edit_mode = False
    edit_save_button = Button(customer_info_frame, text="Edit", font=('Arial', 14),bg="#ED746E", command=toggle_edit_save)
    edit_save_button.bind("<Enter>", lambda e: edit_save_button.config(bg="#FF7C76"))
    edit_save_button.bind("<Leave>", lambda e: edit_save_button.config(bg="#ED746E"))
    edit_save_button.grid(row=6, columnspan=2, pady=10)

    # Initially set all entries to be disabled
    toggle_entry_state(DISABLED)

    # Action Buttons Section below the customer information
    actions_frame = Frame(customer_section_frame, bg="#d9edf7")
    actions_frame.pack(anchor="n", pady=20)

    btn_view_order_history = Button(actions_frame, text="View Order History", font=('Arial', 14,'bold'),bg="#8AB7F7", width=25,
                                    command=ViewOrderHistory)
    btn_view_order_history.bind("<Enter>", lambda e: btn_view_order_history.config(bg="#B1D3F7"))
    btn_view_order_history.bind("<Leave>", lambda e: btn_view_order_history.config(bg="#8AB7F7"))
    btn_view_order_history.pack(pady=10, padx=20, anchor="w")

    btn_view_reviews = Button(actions_frame, text="View Reviews & Ratings", font=('Arial', 14,'bold'),bg="#9886C9", width=25,
                              command=view_reviews_window)
    btn_view_reviews.bind("<Enter>", lambda e: btn_view_reviews.config(bg="#BBA5F7"))
    btn_view_reviews.bind("<Leave>", lambda e: btn_view_reviews.config(bg="#9886C9"))
    btn_view_reviews.pack(pady=10, padx=20, anchor="w")

    btn_calculate_bmi = Button(actions_frame, text="Calculate BMI", font=('Arial', 14, 'bold'), width=25,
                               command=bmi_window, bg='#EDCC4B')
    btn_calculate_bmi.bind("<Enter>", lambda e: btn_calculate_bmi.config(bg="#FFDC51"))
    btn_calculate_bmi.bind("<Leave>", lambda e: btn_calculate_bmi.config(bg="#EDCC4B"))
    btn_calculate_bmi.pack(pady=10, padx=20, anchor="w")

    btn_back_to_menu = Button(actions_frame, text="Back to Menu", font=('Arial', 14,'bold'),bg="#D698B8", width=25,
                              command=cart_window.destroy)
    btn_back_to_menu.bind("<Enter>", lambda e: btn_back_to_menu.config(bg="#F7B0D4"))
    btn_back_to_menu.bind("<Leave>", lambda e: btn_back_to_menu.config(bg="#D698B8"))
    btn_back_to_menu.pack(pady=10, padx=20, anchor="w")

    # Main Frame for the table and bottom frame
    main_frame = Frame(cart_window, bg="#D7DAEB",highlightbackground="black", highlightcolor="black", highlightthickness=2)
    main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Scrollable Frame for the food table
    table_frame = Frame(main_frame, bg="white", bd=1, relief="solid")
    table_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    canvas = Canvas(table_frame, bg="white")
    scrollbar = Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    items_frame = scrollable_frame

    # Bottom Frame for total price and order button
    bottom_frame = Frame(main_frame, bg="#EAEDFF")
    bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    total_price = sum(item[2] * item[4] for item in cart)
    total_calories = sum(item[3] * item[4] for item in cart)

    lbl_total_price = Label(bottom_frame, text=f"Total Amount: RM{total_price:.2f}", font=('Arial', 14, 'bold'),
                            fg="#7E6EA8", bg="#EAEDFF")
    lbl_total_price.pack(side='top', pady=5)

    lbl_total_food_calories = Label(bottom_frame, text=f"Total Calories: {total_calories}", font=('Arial', 14, 'bold'),
                                    fg="#7E6EA8", bg="#EAEDFF")
    lbl_total_food_calories.pack(side='top', pady=5)

    payment_button = Button(bottom_frame, text="Place Order", font=('Arial', 14, 'bold'), bg="orange", fg="#EAEDFF",
                            command=lambda: place_order(lbl_total_price.cget("text"),
                                                        lbl_total_food_calories.cget("text"), cart, cart_window))
    payment_button.bind("<Enter>", lambda e: payment_button.config(bg="#FFC06E"))
    payment_button.bind("<Leave>", lambda e: payment_button.config(bg="orange"))
    payment_button.pack(side='top', pady=5)

    show_delete_buttons = False
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

    # Create a gray frame at the top center
    top_frame = Frame(PaymentWindow, width=600, height=100,highlightbackground="black", highlightcolor="black", highlightthickness=2)
    top_frame.place(relx=0.5, y=10, anchor='n')

    # Add content to the gray frame
    Label(top_frame, text="Payment", font=('Script MT Bold', 26,'underline'), fg='blue').pack(pady=10)

    Label(top_frame, text=f"Total Price: {formatted_total_price}", font=('times new roman', 16, 'bold')).pack(pady=10)
    Label(top_frame, text=f"Tax (6%): {formatted_tax_amount}", font=('times new roman', 16, 'bold')).pack(pady=10)
    Label(top_frame, text=f"Total Amount (including tax): {formatted_total_amount}",font=('times new roman', 16, 'bold')).pack(pady=10)

    pay_button = Button(top_frame, text="Pay", font=('times new roman', 16, 'bold'),
                        command=lambda: complete_payment(total_price, tax_amount, total_amount, PaymentWindow, order_id),
                        bg='#0010A3', fg='white')
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

    # Create a frame for the label and buttons
    frame = Frame(review_choice_window, bd=2, relief="solid")
    frame.pack(pady=50)

    Label(frame, text="Review and Rating", font=('times new roman', 24, 'bold','underline')).pack(pady=20)

    Label(frame, text="Would you like to leave a review and rating?", font=('times new roman', 20, 'bold')).pack(pady=20)

    yes_button = Button(frame, text="Yes", font=('times new roman', 16, 'bold'),
                        command=lambda: [review_choice_window.destroy(), open_review_window(order_id, total_price, tax_amount, total_amount)], bg='#377E47', fg='white')
    yes_button.pack(pady=10)

    no_button = Button(frame, text="No", font=('times new roman', 16, 'bold'),
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

    review_frame = Frame(review_window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    review_frame.pack(side='top', anchor="center", pady=10)

    Label(review_frame, text="Review and Rating", font=('Edwardian Script ITC', 30, 'bold','underline')).pack(pady=5)

    review_label = Label(review_frame, text="Leave a review:", font=('Vivaldi', 18), fg='blue')
    review_label.pack()

    review_text = Text(review_frame, height=4, width=50, font=('times new roman', 12))
    review_text.pack(padx=10,pady=10)

    rating_label = Label(review_frame, text="Rating:", font=('Vivaldi', 18), fg='blue')
    rating_label.pack()

    stars_frame = Frame(review_frame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    stars_frame.pack(pady=10)

    rating = IntVar()
    rating.set(0)  # Initialize rating to 0

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

    submit_button = Button(review_frame, text="Submit", command=lambda: submit_review_rating(
        review_text.get("1.0", "end-1c"), rating.get(), review_window, order_id, total_price, tax_amount, total_amount
    ), bg='#377E47', fg='white', font=('times new roman', 14, 'bold'))
    submit_button.bind("<Enter>", lambda e: submit_button.config(bg="#63E380"))
    submit_button.bind("<Leave>", lambda e: submit_button.config(bg="#377E47"))
    submit_button.pack(pady=5)

    # Display the reviews chart
    display_reviews_chart(review_window)

    # Keep a reference to the image object to prevent garbage collection
    review_window.image = bg_image

def submit_review_rating(review, rating, review_window, order_id, total_price, tax_amount, total_amount):
    if rating == 0:  # Check if no star is selected
        messagebox.showerror("Error", "Please select a rating.")
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

        query_payment = """
                                SELECT payment_id
                                FROM payment
                                WHERE order_id = ?
                                """
        cursor.execute(query_payment, (order_id,))
        payment_data = cursor.fetchone()

        if not payment_data:
            raise sqlite3.Error("Payment information not found")

        payment_id = payment_data[0]

        # Insert the review into the review table
        cursor.execute("INSERT INTO review (customer_id, review, rating, review_date,payment_id) VALUES (?, ?, ?, ?, ?)",
                       (customer_id, review, rating, review_date, payment_id))
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

    fig, ax = plt.subplots(figsize=(6,4))  # Increased figure size

    colors = ['#ffd700' for r in ratings]

    bars = ax.barh([f'{r} star' for r in ratings], percentages, color=colors, edgecolor='black')

    for bar, percentage in zip(bars, percentages):
        width = bar.get_width()
        label_x_pos = width + 1
        ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{percentage:.1f}%',
                va='center', ha='left', fontsize=8, color='black', weight='bold')

    ax.set_title(f'Customer Reviews from {sum(counts):,} reviews', fontsize=9, weight='bold', pad=20)
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
    canvas.get_tk_widget().pack(pady=5)

def rating_to_stars(text_widget, rating):
    filled_star = '★'
    empty_star = '☆'
    stars = ''
    filled_stars_count = int(rating)

    # Create stars string
    stars += filled_star * filled_stars_count
    stars += empty_star * (5 - filled_stars_count)

    # Insert stars into the text widget with appropriate tags
    for i, star in enumerate(stars):
        if star == filled_star:
            text_widget.insert(END, star, 'filled_star')
        else:
            text_widget.insert(END, star, 'empty_star')

def fetch_reviews(sort_order="new_to_old", review_filter=None):
    conn = sqlite3.connect('db_food_ordering_system.db')  # Replace with your database file
    cursor = conn.cursor()

    query = "SELECT review, rating, review_date, customer_id FROM review"

    if review_filter:
        if review_filter == "good":
            query += " WHERE rating >= 4"
        elif review_filter == "bad":
            query += " WHERE rating <= 2"

    query += " ORDER BY review_date DESC" if sort_order == "new_to_old" else " ORDER BY review_date ASC"

    cursor.execute(query)
    reviews = cursor.fetchall()
    return reviews

def view_reviews_window():
    def update_reviews():
        sort_order = sort_var.get()
        review_filter = filter_var.get()
        reviews = fetch_reviews(sort_order, review_filter)
        review_text.config(state=NORMAL)
        review_text.delete('1.0', END)
        for review, rating, review_date, customer_id in reviews:
            cursor.execute("SELECT username FROM customer WHERE customer_id = ?", (customer_id,))
            customer_name = cursor.fetchone()[0]
            review_text.insert(END, f"Review by {customer_name} on {review_date}:\n", 'bold')
            review_text.insert(END, review + "\n")
            rating_to_stars(review_text, rating)
            review_text.insert(END, "\n")
            review_text.insert(END, '-' * 138 + '\n', 'separator')
        review_text.config(state=DISABLED)

    review_window = Toplevel()
    review_window.title("View Reviews")
    review_window.geometry("1920x1080+0+0")
    review_window.state("zoomed")

    main_frame = Frame(review_window, bg="lightgray")
    main_frame.pack(fill='both', expand=True)

    title_label = Label(main_frame, text="Customer Reviews", font=('Bauhaus 93', 24, 'bold'), bg="lightgray",fg="#796796")
    title_label.pack(side='top', pady=20)

    filter_frame = Frame(main_frame, bg="lightgray")
    filter_frame.pack(fill='y',anchor="center", padx=20)

    sort_var = StringVar(value="new_to_old")
    filter_var = StringVar(value="all")

    # Sort by Date
    sort_label = Label(filter_frame, text="Date:", font=('times new roman', 16, 'bold'), bg="lightgray")
    sort_label.pack(side='left', padx=10)
    sort_new_to_old = Radiobutton(filter_frame, text="New to Old", variable=sort_var, value="new_to_old",
                                  bg="lightgray", font=('times new roman', 12, 'bold'), command=update_reviews)
    sort_old_to_new = Radiobutton(filter_frame, text="Old to New", variable=sort_var, value="old_to_new",
                                  bg="lightgray", font=('times new roman', 12, 'bold'), command=update_reviews)
    sort_new_to_old.pack(side='left')
    sort_old_to_new.pack(side='left')

    # Filter
    filter_label = Label(filter_frame, text="Filter:", font=('times new roman', 16, 'bold'), bg="lightgray")
    filter_label.pack(side='left', padx=10, anchor='center')
    filter_all = Radiobutton(filter_frame, text="All", variable=filter_var, value="all", bg="lightgray", font=('times new roman', 12, 'bold'),
                             command=update_reviews)
    filter_good = Radiobutton(filter_frame, text="Good", variable=filter_var, value="good", bg="lightgray",font=('times new roman', 12, 'bold'),
                              command=update_reviews)
    filter_bad = Radiobutton(filter_frame, text="Bad", variable=filter_var, value="bad", bg="lightgray",font=('times new roman', 12, 'bold'),
                             command=update_reviews)
    filter_all.pack(side='left')
    filter_good.pack(side='left')
    filter_bad.pack(side='left')

    content_frame = Frame(main_frame, bg="lightgray")
    content_frame.pack(fill='both', expand=True, padx=20, pady=20)

    chart_frame = ttk.Frame(content_frame, width=400, height=800, relief='solid', borderwidth=1)
    chart_frame.pack(side='left', fill='y', expand=False, padx=10, pady=10)
    display_reviews_chart(chart_frame)

    review_frame = ttk.Frame(content_frame, relief='solid', borderwidth=1)
    review_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

    scrollbar = Scrollbar(review_frame)
    scrollbar.pack(side='right', fill='y')

    review_text = Text(review_frame, font=('times new roman', 14), bg='white', yscrollcommand=scrollbar.set,
                       wrap='word')
    review_text.pack(side='right', fill='both', expand=True)
    scrollbar.config(command=review_text.yview)

    review_text.tag_configure('filled_star', foreground='gold')
    review_text.tag_configure('empty_star', foreground='gray')
    review_text.tag_configure('bold', font=('times new roman', 14, 'bold'))
    review_text.tag_configure('separator', font=('times new roman', 14))

    conn = sqlite3.connect('db_food_ordering_system.db')  # Replace with your database file
    cursor = conn.cursor()

    update_reviews()  # Initial population of reviews

    close_button = Button(review_window, text="Close", font=('times new roman', 16, 'bold'), command=review_window.destroy, bg="#3580BB")
    close_button.bind("<Enter>", lambda e: close_button.config(bg="#48AFFF"))
    close_button.bind("<Leave>", lambda e: close_button.config(bg="#3580BB"))
    close_button.pack(side='bottom', pady=20)

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

    # Add header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "BOOGY RESTAURANT", ln=True, align="C")
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "9870 St Vincent Place, Glasgow", ln=True, align="C")
    pdf.cell(0, 10, txt="Receipt", ln=True, align="C")
    pdf.cell(0, 10, txt=f"Order ID: {order_id}", ln=True, align="C")
    pdf.ln(10)

    # Add separator
    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(5)

    # Add column headers
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(35, 10, "Food ID", align="C")
    pdf.cell(40, 10, "Food Name", align="C")
    pdf.cell(35, 10, "Price", align="C")
    pdf.cell(35, 10, "Quantity", align="C")
    pdf.cell(40, 10, "Total Price", align="C")
    pdf.ln()

    # Add separator
    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(5)

    # Add item rows
    pdf.set_font("Arial", size=12)
    for row in rows:
        food_id, food_name, food_price, quantity = row
        total_price_item = food_price * quantity
        pdf.cell(35, 10, txt=str(food_id), align="C")
        pdf.cell(40, 10, food_name, align="C")
        pdf.cell(35, 10, f"RM{food_price:.2f}", align="C")
        pdf.cell(35, 10, str(quantity), align="C")
        pdf.cell(40, 10, f"RM{total_price_item:.2f}", align="C")
        pdf.ln()

    # Add separator
    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(5)

    # Add totals
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(120, 10, "", align="C")
    pdf.cell(55, 10, f"Subtotal: RM{total_price:.2f}", ln=True, align="R")
    pdf.cell(120, 10, "", align="C")
    pdf.cell(55, 10, f"Tax Amount (6%): RM{tax_amount:.2f}", ln=True, align="R")
    pdf.cell(120, 10, "", align="C")
    pdf.cell(55, 10, f"Total Amount: RM{total_amount:.2f}", ln=True, align="R")
    pdf.ln(5)

    # Add separator
    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(5)

    # Add date/time
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Date/Time: {datetime.now().strftime('%d.%m.%Y / %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Add footer
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Thank you for ordering!", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Tel: 0113456789", ln=True, align="C")
    pdf.cell(0, 10, "Fax: 0163435871", ln=True, align="C")
    pdf.cell(0, 10, "E-mail: boogyrestaurant@gmail.com", ln=True, align="C")

    # Construct the file path
    receipt_filename = f"receipt_{order_id}.pdf"
    receipt_filepath = os.path.join(os.getcwd(), receipt_filename)

    # Save the PDF
    pdf.output(receipt_filepath)

    messagebox.showinfo("Receipt", f"Receipt saved as {receipt_filepath}")
    webbrowser.open_new(receipt_filepath)

def ViewOrderHistory():
    global logged_in_user

    OrderHistoryFrame = Toplevel()
    OrderHistoryFrame.title("Order History")
    OrderHistoryFrame.geometry("1920x1080+0+0")  # window size and position
    OrderHistoryFrame.state("zoomed")
    OrderHistoryFrame.configure(bg="#FFC06E")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 16, 'bold'))  # Change heading font
    style.configure("Treeview", font=('times new roman', 14))  # Change body font

    def show_detailed_order_history():
        # Clear current Treeview
        for item in order_history_treeview.get_children():
            order_history_treeview.delete(item)

        # Define columns for detailed view
        order_history_treeview["columns"] = (
            "Order ID", "Order Date", "Food ID", "Quantity", "Total Price", "Total Food Calories")

        for col in order_history_treeview["columns"]:
            order_history_treeview.heading(col, text=col)
            order_history_treeview.column(col, width=200, anchor='center')

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_id
                FROM customer
                WHERE username = ? AND password = ?
            """, (logged_in_user['username'], logged_in_user['password']))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise sqlite3.Error("Customer not found")

            customer_id = customer_data[0]

            cursor.execute("""
                SELECT o.order_id, o.order_date, oi.food_id, oi.quantity, oi.total_price, oi.total_food_calories
                FROM `orders` o
                JOIN `orderitem` oi ON o.order_id = oi.order_id
                WHERE oi.customer_id = ?
                ORDER BY o.order_id DESC
            """, (customer_id,))
            order_history = cursor.fetchall()

            for row in order_history:
                order_history_treeview.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching order history: {e}")

    def show_summary_order_history():
        # Clear current Treeview
        for item in order_history_treeview.get_children():
            order_history_treeview.delete(item)

        # Define columns for summary view
        order_history_treeview["columns"] = ("Food ID", "Food Name", "Total Quantity Ordered")

        for col in order_history_treeview["columns"]:
            order_history_treeview.heading(col, text=col)
            order_history_treeview.column(col, width=200, anchor='center')

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_id
                FROM customer
                WHERE username = ? AND password = ?
            """, (logged_in_user['username'], logged_in_user['password']))
            customer_data = cursor.fetchone()

            if not customer_data:
                raise sqlite3.Error("Customer not found")

            customer_id = customer_data[0]

            cursor.execute("""
                SELECT oi.food_id, f.food_name, SUM(oi.quantity) as total_quantity
                FROM `orders` o
                JOIN `orderitem` oi ON o.order_id = oi.order_id
                JOIN `food` f ON oi.food_id = f.food_id
                WHERE oi.customer_id = ?
                GROUP BY oi.food_id, f.food_name
            """, (customer_id,))
            order_history = cursor.fetchall()

            for row in order_history:
                order_history_treeview.insert("", "end", values=row)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching order history: {e}")

    lbl_order_history = Label(OrderHistoryFrame, text="Order History", font=('Bauhaus 93', 24),bg='#FFC06E')
    lbl_order_history.pack(side="top", pady=10)

    # Create a frame for the Treeview and scrollbar
    tree_frame = Frame(OrderHistoryFrame)
    tree_frame.pack(fill="both",padx=20, expand=True)

    # Create Treeview widget
    order_history_treeview = ttk.Treeview(tree_frame, show="headings")
    order_history_treeview.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=order_history_treeview.yview)
    scrollbar.pack(side="right", fill="y")

    order_history_treeview.configure(yscrollcommand=scrollbar.set)

    # Create a frame for the buttons
    button_frame = Frame(OrderHistoryFrame,bg='#FFC06E')
    button_frame.pack(side="bottom", pady=20)

    btn_detailed_view = Button(button_frame, text="Detailed View", font=('times new roman', 16),
                               command=show_detailed_order_history, bg='#3580BB', fg='white')
    btn_detailed_view.bind("<Enter>", lambda e: btn_detailed_view.config(bg="#48AFFF"))
    btn_detailed_view.bind("<Leave>", lambda e: btn_detailed_view.config(bg="#3580BB"))
    btn_detailed_view.pack(side="left", padx=10, pady=10)

    btn_summary_view = Button(button_frame, text="Summary View", font=('times new roman', 16),
                              command=show_summary_order_history, bg='#4CBD2C', fg='white')
    btn_summary_view.bind("<Enter>", lambda e: btn_summary_view.config(bg="#61F239"))
    btn_summary_view.bind("<Leave>", lambda e: btn_summary_view.config(bg="#4CBD2C"))
    btn_summary_view.pack(side="left", padx=10, pady=10)

    btn_back = Button(button_frame, text="Back", font=('times new roman', 16),
                      command=OrderHistoryFrame.destroy, bg='#8C73BD', fg='white')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#B293F0"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#8C73BD"))
    btn_back.pack(side="left", padx=10, pady=10)

    # Initially show the summary order history
    show_summary_order_history()

def bmi_window():
    global weight_entry, height_entry, gender_var, result_label, canvas

    bmi_root = Toplevel()
    bmi_root.title("BMI Calculator")
    bmi_root.geometry("1920x1080+0+0")  # window size and position
    bmi_root.state("zoomed")

    # Load the background image
    image = Image.open("bmi.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(bmi_root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

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
    back_button = Button(bmi_root, text="Back", font=('times new roman', 16, 'bold'), command=bmi_root.destroy, bg='#00129A', fg='white')
    back_button.bind("<Enter>", lambda e: back_button.config(bg="#001EFF"))
    back_button.bind("<Leave>", lambda e: back_button.config(bg="#00129A"))
    back_button.pack(side="bottom", pady=20)

    canvas = None

    # Keep a reference to the image object to prevent garbage collection
    bmi_window.image = bg_image

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


#login & register
def LoginForm():
    global LoginFrame, lbl_result1, form_frame

    root.withdraw()

    form_frame = Toplevel()
    form_frame.title("Register and Login System")
    form_frame.geometry("1920x1080+0+0")  # window size and position
    form_frame.config()  # used to customize the window (bg colour, title)
    form_frame.state("zoomed")  # maximize the root window to fill the entire screen

    # Load the background image
    image = Image.open("background.png")  # Replace with your image file path
    resized_image = image.resize((1920, 1080), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = Label(form_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    LoginFrame = Frame(form_frame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
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

    root.withdraw()

    RegisterFrame = Frame(form_frame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
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

def AdminRegisterForm():
    global lbl_result2, confirm_password_entry

    AdminFrame = Toplevel()
    AdminFrame.title("Admin Register")
    AdminFrame.geometry("1920x1080+0+0")  # window size and position
    AdminFrame.state("zoomed")
    AdminFrame.configure(bg="#FFC06E")

    AdminRegisterFrame = Frame(AdminFrame, highlightbackground="black", highlightcolor="black", highlightthickness=2)
    AdminRegisterFrame.pack(side='top', pady=50)

    lbl_result2 = Label(AdminRegisterFrame, text="Admin Registration Form:", font=('Script MT Bold', 24, 'bold'), fg='#0016BA', bd=18)
    lbl_result2.grid(row=1, columnspan=2)

    lbl_username = Label(AdminRegisterFrame, text="Username:", font=('times new roman', 15), bd=18)
    lbl_username.grid(row=2)

    lbl_password = Label(AdminRegisterFrame, text="Password:", font=('times new roman', 15), bd=18)
    lbl_password.grid(row=3)

    lbl_confirm_password = Label(AdminRegisterFrame, text="Confirm Password:", font=('times new roman', 15), bd=18)
    lbl_confirm_password.grid(row=4)

    lbl_firstname = Label(AdminRegisterFrame, text="First Name:", font=('times new roman', 15), bd=18)
    lbl_firstname.grid(row=5)

    lbl_lastname = Label(AdminRegisterFrame, text="Last Name:", font=('times new roman', 15), bd=18)
    lbl_lastname.grid(row=6)

    lbl_date_of_birth = Label(AdminRegisterFrame, text="Date of Birth:", font=('times new roman', 15), bd=18)
    lbl_date_of_birth.grid(row=7)

    lbl_email_address = Label(AdminRegisterFrame, text="Email Address:", font=('times new roman', 15), bd=18)
    lbl_email_address.grid(row=8)

    lbl_phone_number = Label(AdminRegisterFrame, text="Phone number:", font=('times new roman', 15), bd=18)
    lbl_phone_number.grid(row=9)

    # Clear existing text in the entry fields
    USERNAME_REGISTER.set("")
    PASSWORD_REGISTER.set("")
    FIRSTNAME.set("")
    LASTNAME.set("")
    DATE_OF_BIRTH.set("")
    EMAIL_ADDRESS.set("")
    PHONE_NUMBER.set("")

    username = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=USERNAME_REGISTER, width=20)
    username.grid(row=2, column=1,padx=10)
    username.insert(0, "Enter your username")  # Placeholder for username
    username.config(fg='grey')  # Set placeholder text color to grey
    username.bind("<FocusIn>", lambda event: on_entry_click(username, "Enter your username"))
    username.bind("<FocusOut>", lambda event: on_focus_out(username, "Enter your username"))

    password = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=PASSWORD_REGISTER, width=20)
    password.grid(row=3, column=1,padx=10)
    password.insert(0, "Enter your password")  # Placeholder for password
    password.config(fg='grey')  # Set placeholder text color to grey
    password.bind("<FocusIn>", lambda event: password_on_focus_in(password, "Enter your password"))
    password.bind("<FocusOut>", lambda event: password_on_focus_out(password, "Enter your password"))

    confirm_password_entry = Entry(AdminRegisterFrame, font=('times new roman', 15), width=20)
    confirm_password_entry.grid(row=4, column=1,padx=10)
    confirm_password_entry.insert(0, "Confirm your password")  # Placeholder for confirm password
    confirm_password_entry.config(fg='grey')  # Set placeholder text color to grey
    confirm_password_entry.bind("<FocusIn>",
                                lambda event: password_on_focus_in(confirm_password_entry, "Confirm your password"))
    confirm_password_entry.bind("<FocusOut>",
                                lambda event: password_on_focus_out(confirm_password_entry, "Confirm your password"))

    firstname = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=FIRSTNAME, width=20)
    firstname.grid(row=5, column=1,padx=10)
    firstname.insert(0, "Enter your first name")  # Placeholder for first name
    firstname.config(fg='grey')  # Set placeholder text color to grey
    firstname.bind("<FocusIn>", lambda event: on_entry_click(firstname, "Enter your first name"))
    firstname.bind("<FocusOut>", lambda event: on_focus_out(firstname, "Enter your first name"))

    lastname = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=LASTNAME, width=20)
    lastname.grid(row=6, column=1,padx=10)
    lastname.insert(0, "Enter your last name")  # Placeholder for last name
    lastname.config(fg='grey')  # Set placeholder text color to grey
    lastname.bind("<FocusIn>", lambda event: on_entry_click(lastname, "Enter your last name"))
    lastname.bind("<FocusOut>", lambda event: on_focus_out(lastname, "Enter your last name"))

    date_of_birth = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=DATE_OF_BIRTH, width=20)
    date_of_birth.grid(row=7, column=1,padx=10)
    date_of_birth.insert(0, "Enter day-month-year")  # Placeholder for date of birth
    date_of_birth.config(fg='grey')  # Set placeholder text color to grey
    date_of_birth.bind("<FocusIn>", lambda event: on_entry_click(date_of_birth, "Enter day-month-year"))
    date_of_birth.bind("<FocusOut>", lambda event: on_focus_out(date_of_birth, "Enter day-month-year"))

    email_address = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=EMAIL_ADDRESS, width=20)
    email_address.grid(row=8, column=1,padx=10)
    email_address.insert(0, "Enter your email address")  # Placeholder for email address
    email_address.config(fg='grey')  # Set placeholder text color to grey
    email_address.bind("<FocusIn>", lambda event: on_entry_click(email_address, "Enter your email address"))
    email_address.bind("<FocusOut>", lambda event: on_focus_out(email_address, "Enter your email address"))

    phone_number = Entry(AdminRegisterFrame, font=('times new roman', 15), textvariable=PHONE_NUMBER, width=20)
    phone_number.grid(row=9, column=1,padx=10)
    phone_number.insert(0, "Enter your phone number")  # Placeholder for phone number
    phone_number.config(fg='grey')  # Set placeholder text color to grey
    phone_number.bind("<FocusIn>", lambda event: on_entry_click(phone_number, "Enter your phone number"))
    phone_number.bind("<FocusOut>", lambda event: on_focus_out(phone_number, "Enter your phone number"))

    btn_register = Button(AdminRegisterFrame, text="Register", font=('arial', 14,'bold'), width=20, command=AdminRegister, bg='#A5AAF7',
                          fg='white', relief='raised')
    btn_register.bind("<Enter>", lambda e: btn_register.config(bg="#B9BFFF"))
    btn_register.bind("<Leave>", lambda e: btn_register.config(bg="#A5AAF7"))
    btn_register.grid(row=10, columnspan=2, pady=20)

    btn_back = Button(AdminRegisterFrame, text="Back to Admin Panel", font=('arial', 14, 'bold'), width=20,
                          command=AdminFrame.destroy, bg='#D92525',
                          fg='white', relief='raised')
    btn_back.bind("<Enter>", lambda e: btn_back.config(bg="#FF2B2B"))
    btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#D92525"))
    btn_back.grid(row=11, columnspan=2, pady=10)

def AdminRegister():
    Database()
    # Placeholder values to check against
    placeholders = {
        "USERNAME_REGISTER": "Enter your username",
        "PASSWORD_REGISTER": "Enter your password",
        "FIRSTNAME": "Enter your first name",
        "LASTNAME": "Enter your last name",
        "DATE_OF_BIRTH": "Enter day-month-year",
        "EMAIL_ADDRESS": "Enter your email address",
        "PHONE_NUMBER": "Enter your phone number"
    }

    # Check if any field is empty or contains placeholder text
    if (USERNAME_REGISTER.get() in ("", placeholders["USERNAME_REGISTER"]) or
            PASSWORD_REGISTER.get() in ("", placeholders["PASSWORD_REGISTER"]) or
            FIRSTNAME.get() in ("", placeholders["FIRSTNAME"]) or
            LASTNAME.get() in ("", placeholders["LASTNAME"]) or
            confirm_password_entry.get() in ("", placeholders["PASSWORD_REGISTER"]) or
            DATE_OF_BIRTH.get() in ("", placeholders["DATE_OF_BIRTH"]) or
            EMAIL_ADDRESS.get() in ("", placeholders["EMAIL_ADDRESS"]) or
            PHONE_NUMBER.get() in ("", placeholders["PHONE_NUMBER"])):
        messagebox.showerror("Error", "Please complete all the required fields!")

    elif PASSWORD_REGISTER.get() != confirm_password_entry.get():
        messagebox.showerror("Error", "Password and Confirm Password do not match!")
    else:
        try:
            # Check if username already exists in the admin table
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
                return

            # Check if username already exists in the customer table
            cursor.execute("SELECT * FROM `customer` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username is already taken!")
                return

            # Insert the new user into the admin table
            cursor.execute(
                "INSERT INTO `admin` (username, password, firstname, lastname, date_of_birth, email_address, phone_number) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (USERNAME_REGISTER.get(), PASSWORD_REGISTER.get(), FIRSTNAME.get(),
                 LASTNAME.get(), DATE_OF_BIRTH.get(), EMAIL_ADDRESS.get(), PHONE_NUMBER.get()))
            conn.commit()  # save current data to database

            # Clear the input fields after successful registration
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
            messagebox.showerror("Error", f"Error occurred during registration: {e}")

def ToggleToLogin(event=None):  # switching from register to login page.
    if RegisterFrame is not None:
        form_frame.withdraw()
        RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):  # switching the interface from login to register after user click the register link
    if LoginFrame is not None:  # if login form is display, then need to deleted and switch to registration form
        LoginFrame.destroy()
    RegisterForm()

def Register():
    Database()
    try:
        # Placeholder values to check against
        placeholders = {
            "USERNAME_REGISTER": "Enter your username",
            "PASSWORD_REGISTER": "Enter your password",
            "FIRSTNAME": "Enter your first name",
            "LASTNAME": "Enter your last name",
            "DATE_OF_BIRTH": "Enter day-month-year",
            "EMAIL_ADDRESS": "Enter your email address",
            "PHONE_NUMBER": "Enter your phone number"
        }

        # Check if any field is empty or contains placeholder text
        if (USERNAME_REGISTER.get() in ("", placeholders["USERNAME_REGISTER"]) or
                PASSWORD_REGISTER.get() in ("", placeholders["PASSWORD_REGISTER"]) or
                FIRSTNAME.get() in ("", placeholders["FIRSTNAME"]) or
                LASTNAME.get() in ("", placeholders["LASTNAME"]) or
                confirm_password_entry.get() in ("", placeholders["PASSWORD_REGISTER"]) or
                DATE_OF_BIRTH.get() in ("", placeholders["DATE_OF_BIRTH"]) or
                EMAIL_ADDRESS.get() in ("", placeholders["EMAIL_ADDRESS"]) or
                PHONE_NUMBER.get() in ("", placeholders["PHONE_NUMBER"])):
            messagebox.showerror("Error", "Please complete all the required fields!")
            return

        # Check if passwords match
        if PASSWORD_REGISTER.get() != confirm_password_entry.get():
            messagebox.showerror("Error", "Password and Confirm Password do not match!")
            return

        # Check if the username already exists in customer or admin tables
        cursor.execute("SELECT username FROM `customer` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
        if cursor.fetchone() is not None:
            messagebox.showerror("Error", "Username is already taken!")
            return

        cursor.execute("SELECT username FROM `admin` WHERE `username` = ?", (USERNAME_REGISTER.get(),))
        if cursor.fetchone() is not None:
            messagebox.showerror("Error", "Username is already taken!")
            return

        # Insert the new user into the customer table
        cursor.execute(
            "INSERT INTO `customer` (username, password, firstname, lastname, date_of_birth, email_address, phone_number) VALUES(?, ?, ?, ?, ?, ?, ?)",
            (USERNAME_REGISTER.get(), PASSWORD_REGISTER.get(), FIRSTNAME.get(),
             LASTNAME.get(), DATE_OF_BIRTH.get(), EMAIL_ADDRESS.get(), PHONE_NUMBER.get())
        )
        conn.commit()  # Save changes to database

        # Clear the input fields after successful registration
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
        messagebox.showerror("Error", f"Error occurred during registration: {e}")

def Login():
    global logged_in_user
    Database()
    try:
        # Check if the fields are empty
        if USERNAME_LOGIN.get() == "" or PASSWORD_LOGIN.get() == "":
            messagebox.showerror("Error", "Please complete the required field!")
            return

        # Check in the customer table
        cursor.execute("SELECT * FROM `customer` WHERE `username` = ? AND `password` = ?",
                       (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        customer = cursor.fetchone()

        if customer is not None:
            logged_in_user['username'] = USERNAME_LOGIN.get()
            logged_in_user['password'] = PASSWORD_LOGIN.get()
            messagebox.showinfo("Success", "You Successfully Logged In")
            ViewFoodMenu()
            return

        # Check in the admin table
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?",
                       (USERNAME_LOGIN.get(), PASSWORD_LOGIN.get()))
        admin = cursor.fetchone()

        if admin is not None:
            logged_in_user['username'] = USERNAME_LOGIN.get()
            logged_in_user['password'] = PASSWORD_LOGIN.get()
            messagebox.showinfo("Success", "You Successfully Logged In")
            AdminPanel()
            return

        # If no match found in both tables
        messagebox.showerror("Error", "Invalid username or password")

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error occurred during login: {e}")

def load_window():
    try:
        # Try to load the image
        image = Image.open('name.png')

        # Resize the image
        resized_image = image.resize((500, 500), Image.Resampling.LANCZOS)

        # Convert the image to a format suitable for Tkinter
        bg_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        # Show an error message and exit if the image could not be loaded
        messagebox.showerror("Image Error", f"Could not load image: {e}")
        root.destroy()  # Close the application
        return  # Exit the function

    # Create a label with the background image and place it on the window
    bg_label = Label(root, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Update the window's geometry to fit the image
    width, height = resized_image.size
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    root.overrideredirect(True)  # Remove window decorations
    root.resizable(False, False)  # Make the window non-resizable

    # Set the background color to match the yellow border
    root.config(background="#f1c40f")

    # Add a welcome label
    welcome_label = Label(root, text="WELCOME TO BOOGY!", bg="#f1c40f", font=("Trebuchet Ms", 15, "bold"), fg="#FFFFFF")
    welcome_label.place(x=(width - 230) // 2, y=10)  # Center the label horizontally

    # Add a progress label
    progress_label = Label(root, text="Loading...", font=("Trebuchet Ms", 13, "bold"), fg="#FFFFFF", bg="#f1c40f")
    progress_label.place(x=(width - 100) // 2, y=height - 70)  # Place near the bottom

    # Configure the progress bar style
    style = Style()
    style.theme_use('clam')
    style.configure("red.Horizontal.TProgressbar", background="#108cff")

    # Add the progress bar
    progress = Progressbar(root, orient='horizontal', length=400, mode='determinate',
                           style="red.Horizontal.TProgressbar")
    progress.place(x=(width - 400) // 2, y=height - 40)  # Place near the bottom

    def top():
        # Close the current window and open the LandingPage
        root.withdraw()

        root.destroy()

    def load():
        # Simulate a loading process
        global i
        if i <= 100:
            txt = 'Loading...' + (str(i) + '%')
            progress_label.config(text=txt)
            progress['value'] = i
            i += 1
            progress_label.after(60, load)  # Call this function again after 60 milliseconds
        else:
            LoginForm()

    # Start the loading process
    load()

    # Keep a reference to the image object to prevent garbage collection
    load_window.image = bg_image


# Initialize the global variable
i = 0

# Call the function to load the window
load_window()



if __name__ == '__main__':
    root.mainloop()

