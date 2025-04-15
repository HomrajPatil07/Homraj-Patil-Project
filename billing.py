#billing.py
from tkinter import *
from tkinter import ttk, messagebox
from products import search_product, show_all, treeview_data
from datetime import datetime
import time
import pymysql
import os
import tempfile
import subprocess

# Create main window
window = Tk()
window.title('Dashboard')
window.geometry('1530x800+0+0')
window.resizable(0, 0)
window.config(bg='white')


window.chk_print = 0  # Default: No bill generated yet


# === Title Label ===
titleLabel = Label(window, text='   Electronics Shop Management System', font=('times new roman', 40, 'bold'),
                   bg='#010c48', fg='white', anchor='w')
titleLabel.place(x=0, y=0, relwidth=1)

# === Logout Button ===
logoutButton = Button(window, text='Logout', command=lambda: logout(window), font=('times new roman', 20, 'bold'), fg='#010c48', cursor='hand2')
logoutButton.place(x=1360, y=7)

# === Display Current Date & Time ===
def update_datetime():
    current_time = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')  # Format: 02-01-2025 12:36:17 PM
    subtitleLabel.config(text=f'Welcome Admin\t\t Date: {current_time}')
    subtitleLabel.after(1000, update_datetime)  # Update time every second

subtitleLabel = Label(window, text='', font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=66, relwidth=1)
update_datetime()  # Start updating time

# === Product Frame ===
product_frame1 = Frame(window, bd=4, relief=RIDGE, bg='white')
product_frame1.place(x=21, y=110, width=410, height=650)

title = Label(product_frame1, text='All Products', font=('times new roman', 15, 'bold'), bg='#0f4d7d', fg='white')
title.pack(side=TOP, fill=X)

product_frame2 = Frame(product_frame1, bd=4, relief=RIDGE, bg='white')
product_frame2.place(x=2, y=32, width=400, height=120)

# === Search Section ===
name_search_label = Label(product_frame2, text='Search Name', font=('times new roman', 14, 'bold'), bg='white')
name_search_label.grid(row=0, column=0, pady=20, sticky='w')

name_search_entry = Entry(product_frame2, font=('times new roman', 14, 'bold'), bg='lightyellow')
name_search_entry.grid(row=0, column=1, pady=20, sticky='w')

# Add a search combobox for search criteria
search_combobox = ttk.Combobox(product_frame2, values=('Name'), state='readonly', width=15, font=('times new roman', 12))
search_combobox.grid(row=0, column=2, padx=10, pady=20)
search_combobox.set('Name')  # Default search criteria

# Arrange buttons in the same row
search_button = Button(product_frame2, text='Search', font=('times new roman', 12), width=15, cursor='hand2', fg='white',
                       bg='#0f4d7d', command=lambda: search_product( search_combobox, name_search_entry, treeview))
search_button.grid(row=1, column=0, padx=15, sticky='e')

show_button = Button(product_frame2, text='Show All', font=('times new roman', 12), width=15, cursor='hand2', fg='white',
                     bg='#0f4d7d', command=lambda: show_all(treeview, search_combobox, name_search_entry,))
show_button.grid(row=1, column=1, padx=15, sticky='e')

# === Treeview for displaying product data ===
product_frame3 = Frame(window, bd=3, relief=RIDGE)
product_frame3.place(x=20, y=290, width=410, height=470)

scrolly = Scrollbar(product_frame3, orient=VERTICAL)
scrollx = Scrollbar(product_frame3, orient=HORIZONTAL)

# Configure treeview to display id, name, price, quantity, and status
treeview = ttk.Treeview(product_frame3, columns=('id', 'name', 'price', 'quantity', 'status'), show='headings',
                        yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

scrolly.pack(side=RIGHT, fill=Y)
scrollx.pack(side=BOTTOM, fill=X)
scrollx.config(command=treeview.xview)
scrolly.config(command=treeview.yview)
treeview.pack(fill=BOTH, expand=1)

# Set headings for the treeview
treeview.heading('id', text='ID')
treeview.heading('name', text='Name')
treeview.heading('price', text='Price')
treeview.heading('quantity', text='Quantity')
treeview.heading('status', text='Status')

# Set column widths
treeview.column('id', width=50)
treeview.column('name', width=160)
treeview.column('price', width=100)
treeview.column('quantity', width=80)
treeview.column('status', width=90)


# === Customer Frame ===
customer_frame = Frame(window, bd=4, relief=RIDGE)
customer_frame.place(x=435, y=110, width=530, height=70)

ctitle = Label(customer_frame, text='Customer Details', font=('times new roman', 15, 'bold'), bg='#0f4d7d', fg='white')
ctitle.pack(side=TOP, fill=X)

name_label = Label(customer_frame, text='Name', font=('times new roman', 15, 'bold')).place(x=13, y=32)
txt_name = Entry(customer_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
txt_name.place(x=75, y=34, width=180)

contact_label = Label(customer_frame, text='Contact No.', font=('times new roman', 15, 'bold')).place(x=260, y=32)
txt_contact = Entry(customer_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
txt_contact.place(x=375, y=34, width=140)

# === Calculator and Cart Frame ===
cal_cart_frame = Frame(window, bd=2, relief=RIDGE, bg='white')
cal_cart_frame.place(x=435, y=188, width=530, height=445)

# === Calculator Frame ===
cal_frame = Frame(cal_cart_frame, bd=2, relief=RIDGE, bg='white')
cal_frame.place(x=5, y=10, width=268, height=420)

cal_title = Label(cal_frame, text='Calculator', font=('goudy old style', 15, 'bold'))
cal_title.grid(row=0, column=0, columnspan=4, pady=2, sticky="nsew")

txt_cal_input = Entry(cal_frame, font=('arial', 15, 'bold'), width=22, bd=9, relief=GROOVE)
txt_cal_input.grid(row=1, column=0, columnspan=4, pady=5)

# Function to handle button clicks
def button_click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = str(eval(txt_cal_input.get()))
            txt_cal_input.delete(0, END)
            txt_cal_input.insert(0, result)
        except Exception as e:
            txt_cal_input.delete(0, END)
            txt_cal_input.insert(0, "Error")
    elif text == "C":
        txt_cal_input.delete(0, END)
    else:
        txt_cal_input.insert(END, text)

# Use grid for buttons
buttons = [
    '7', '8', '9', '+',
    '4', '5', '6', '-',
    '1', '2', '3', '*',
    '0', 'C', '=', '/'
]

row_val = 2
col_val = 0

for button in buttons:
    button_obj = Button(cal_frame, text=button, font=('arial', 15, 'bold'), bd=5, width=4, pady=17, cursor='hand2')
    button_obj.grid(row=row_val, column=col_val)
    button_obj.bind("<Button-1>", button_click)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# === Cart Frame ===
cart_frame = Frame(cal_cart_frame, bd=3, relief=RIDGE)
cart_frame.place(x=280, y=8, width=245, height=420)
cart_title = Label(cart_frame, text='My Cart \t Total Product: [0]', font=('goudy old style', 15, 'bold'))
cart_title.pack(side=TOP, fill=X)

scrolly = Scrollbar(cart_frame, orient=VERTICAL)
scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)

treeview_cart = ttk.Treeview(cart_frame, columns=('id', 'name', 'price', 'quantity', 'total'), show='headings',
                             yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

scrolly.pack(side=RIGHT, fill=Y)
scrollx.pack(side=BOTTOM, fill=X)
scrollx.config(command=treeview_cart.xview)
scrolly.config(command=treeview_cart.yview)
treeview_cart.pack(fill=BOTH, expand=1)

treeview_cart.heading('id', text='ID')
treeview_cart.heading('name', text='Name')
treeview_cart.heading('price', text='Price')
treeview_cart.heading('quantity', text='quantity')
treeview_cart.heading('total', text='Total')

treeview_cart.column('id', width=40)
treeview_cart.column('name', width=100)
treeview_cart.column('price', width=80)
treeview_cart.column('quantity', width=50)
treeview_cart.column('total', width=90)

# === ADD Cart Widgets Frame ===
add_cart_widgets_frame = Frame(window, bd=2, relief=RIDGE, bg='white')
add_cart_widgets_frame.place(x=435, y=640, width=530, height=120)

label_p_name = Label(add_cart_widgets_frame, text='Product Name', font=('times new roman', 15, 'bold'), bg='white')
label_p_name.place(x=5, y=5)
txt_p_name = Entry(add_cart_widgets_frame, font=('times new roman', 15, 'bold'), bg='lightyellow', state='readonly')
txt_p_name.place(x=5, y=35, width=190, height=22)

label_p_price = Label(add_cart_widgets_frame, text='Price Per quantity', font=('times new roman', 15, 'bold'), bg='white')
label_p_price.place(x=230, y=5)
txt_p_price = Entry(add_cart_widgets_frame, font=('times new roman', 15, 'bold'), bg='lightyellow', state='readonly')
txt_p_price.place(x=230, y=35, width=150, height=22)

label_p_quantity = Label(add_cart_widgets_frame, text='Quantity', font=('times new roman', 15, 'bold'), bg='white')
label_p_quantity.place(x=390, y=5)
txt_p_quantity = Entry(add_cart_widgets_frame, font=('times new roman', 15, 'bold'), bg='lightyellow')
txt_p_quantity.place(x=390, y=35, width=120, height=22)

label_inStock = Label(add_cart_widgets_frame, text='In Stock [9999]', font=('times new roman', 15, 'bold'), bg='white')
label_inStock.place(x=5, y=70)

clear_button = Button(add_cart_widgets_frame, text='Clear', font=('times new roman', 12), width=8, cursor='hand2', fg='white', bg='#0f4d7d')
clear_button.place(x=180, y=70, width=150, height=30)

add_button = Button(add_cart_widgets_frame, text='Add | Update Cart', font=('times new roman', 12), width=8, cursor='hand2', fg='white', bg='#0f4d7d')
add_button.place(x=340, y=70, width=180, height=30)

# Global variable to store the available stock
available_stock = 0

def on_product_select(event):
    global available_stock
    selected_item = treeview.selection()  # Get the selected item
    if selected_item:  # If an item is selected
        item = treeview.item(selected_item)  # Get the item's data
        product_data = item['values']  # Extract the values (id, name, price, quantity, status)

        # Debug: Print the product data to inspect its contents
        print("Selected Product Data:", product_data)

        # Update the ADD CART WIDGETS FRAME entries
        txt_p_name.config(state='normal')  # Enable the entry to update
        txt_p_name.delete(0, END)  # Clear the entry
        txt_p_name.insert(0, product_data[1])  # Insert the product name
        txt_p_name.config(state='readonly')  # Set it back to readonly

        txt_p_price.config(state='normal')  # Enable the entry to update
        txt_p_price.delete(0, END)  # Clear the entry
        txt_p_price.insert(0, product_data[2])  # Insert the product price
        txt_p_price.config(state='readonly')  # Set it back to readonly

        # Update the in-stock label and store the available stock
        try:
            # Ensure the quantity is a valid integer
            available_stock = int(product_data[3])  # Store the available stock
            label_inStock.config(text=f'In Stock [{available_stock}]')  # Update the in-stock value
        except (ValueError, IndexError) as e:
            # Handle invalid quantity data
            print(f"Error parsing quantity: {e}")
            available_stock = 0  # Default to 0 if quantity is invalid
            label_inStock.config(text='In Stock [0]')  # Update the in-stock value

        # Clear the quantity entry
        txt_p_quantity.delete(0, END)

# Function to add/update cart
def add_to_cart():
    global available_stock
    try:
        # Check if all required fields are filled
        if not treeview.selection():
            messagebox.showerror("Error", "Please select a product from the list.")
            return
        if not txt_p_quantity.get():
            messagebox.showerror("Error", "Please enter the quantity.")
            return

        # Get the entered quantity
        product_quantity = int(txt_p_quantity.get())

        # Validate the quantity against the available stock
        if product_quantity > available_stock:
            messagebox.showerror("Error", f"Cannot add more than {available_stock} items. Insufficient stock.")
            return

        # Get the product details
        product_id = treeview.item(treeview.selection(), 'values')[0]  # Get the ID from the selected item
        product_name = txt_p_name.get()
        product_price = float(txt_p_price.get())

        # Calculate total price
        total_price = product_price * product_quantity

        # Check if the product is already in the cart
        cart_items = treeview_cart.get_children()
        found = False
        for item in cart_items:
            if treeview_cart.item(item, 'values')[0] == product_id:
                # Update the existing item
                treeview_cart.item(item, values=(product_id, product_name, product_price, product_quantity, total_price))
                found = True
                messagebox.showinfo("Updated", f"Quantity updated for {product_name}.")
                break

        if not found:
            # Add new item to the cart
            treeview_cart.insert('', 'end', values=(product_id, product_name, product_price, product_quantity, total_price))
            messagebox.showinfo("Added", f"{product_name} added to cart.")

        # Update the total product count in the cart title
        cart_title.config(text=f'My Cart \t Total Product: [{len(cart_items) + 1}]')

        # Clear the quantity entry
        txt_p_quantity.delete(0, END)

        # Update the bill amount, discount, and net pay
        update_bill()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Bind the product selection event to the Product Frame treeview
treeview.bind('<<TreeviewSelect>>', on_product_select)

# Bind the add/update cart button
add_button.config(command=add_to_cart)

def clear_cart():
    # Clear the selected item from the cart
    selected_item = treeview_cart.selection()  # Get the selected item in the cart
    if selected_item:  # If an item is selected
        # Remove the selected item from the cart
        treeview_cart.delete(selected_item)

        # Update the total product count in the cart title
        cart_items = treeview_cart.get_children()
        cart_title.config(text=f'My Cart \t Total Product: [{len(cart_items)}]')

        # Update the bill amount, discount, and net pay
        update_bill()

    # Clear the Add Cart Widgets Frame fields
    txt_p_name.config(state='normal')  # Enable the entry to update
    txt_p_name.delete(0, END)  # Clear the product name field
    txt_p_name.config(state='readonly')  # Set it back to readonly

    txt_p_price.config(state='normal')  # Enable the entry to update
    txt_p_price.delete(0, END)  # Clear the price field
    txt_p_price.config(state='readonly')  # Set it back to readonly

    txt_p_quantity.delete(0, END)  # Clear the quantity field

    # Reset the in-stock label to its default value
    label_inStock.config(text='In Stock [9999]')


# === Clear All Function ===
def clear_all_data():
    # Clear Product Frame Data
    name_search_entry.delete(0, END)  # Clear the search entry
    search_combobox.set('Name')  # Reset the search combobox
    treeview.delete(*treeview.get_children())  # Clear the product treeview

    # Clear Customer Frame Data
    txt_name.delete(0, END)  # Clear the customer name entry
    txt_contact.delete(0, END)  # Clear the customer contact entry

    # Clear Cart Frame Data
    treeview_cart.delete(*treeview_cart.get_children())  # Clear the cart treeview
    cart_title.config(text='My Cart \t Total Product: [0]')  # Reset the cart title

    # Clear Add Cart Widgets Frame Data
    txt_p_name.config(state='normal')  # Enable the entry to update
    txt_p_name.delete(0, END)  # Clear the product name field
    txt_p_name.config(state='readonly')  # Set it back to readonly

    txt_p_price.config(state='normal')  # Enable the entry to update
    txt_p_price.delete(0, END)  # Clear the price field
    txt_p_price.config(state='readonly')  # Set it back to readonly

    txt_p_quantity.delete(0, END)  # Clear the quantity field
    label_inStock.config(text='In Stock [9999]')  # Reset the in-stock label

    # Clear Billing Area Data
    txt_bill_area.delete(1.0, END)  # Clear the bill area

    # Clear Bill Menu Frame Data
    label_amnt.config(text='Bill Amount\n0')  # Reset the bill amount label
    label_discount.config(text='Discount \n%')  # Reset the discount label
    label_net_pay.config(text='Net Pay\n0')  # Reset the net pay label

    # Clear Calculator Data
    txt_cal_input.delete(0, END)  # Clear the calculator input field


# Function to update the bill amount, discount, and net pay
def update_bill():
    cart_items = treeview_cart.get_children()
    total_amount = 0

    for item in cart_items:
        total_amount += float(treeview_cart.item(item, 'values')[4])  # Sum up the total prices

    # Calculate discount (assuming a fixed discount percentage for simplicity)
    discount_percentage = 10  # 10% discount
    discount = (total_amount * discount_percentage) / 100
    net_pay = total_amount - discount

    # Update the labels
    label_amnt.config(text=f'Bill Amount\n{total_amount:.2f}')
    label_discount.config(text=f'Discount \n{discount_percentage}%')
    label_net_pay.config(text=f'Net Pay\n{net_pay:.2f}')

# Bind the "Clear" button to the clear_cart function
clear_button.config(command=clear_cart)

# Function to handle cart item selection from the Cart Frame
def on_cart_item_select(event):
    selected_item = treeview_cart.selection()  # Get the selected item
    if selected_item:  # If an item is selected
        item = treeview_cart.item(selected_item)  # Get the item's data
        cart_item_data = item['values']  # Extract the values (id, name, price, quantity, total)

        # Update the ADD CART WIDGETS FRAME entries
        txt_p_name.config(state='normal')  # Enable the entry to update
        txt_p_name.delete(0, END)  # Clear the entry
        txt_p_name.insert(0, cart_item_data[1])  # Insert the product name
        txt_p_name.config(state='readonly')  # Set it back to readonly

        txt_p_price.config(state='normal')  # Enable the entry to update
        txt_p_price.delete(0, END)  # Clear the entry
        txt_p_price.insert(0, cart_item_data[2])  # Insert the product price
        txt_p_price.config(state='readonly')  # Set it back to readonly

        txt_p_quantity.delete(0, END)  # Clear the quantity entry
        txt_p_quantity.insert(0, cart_item_data[3])  # Insert the product quantity

        # Update the in-stock label (assuming the in-stock value is available)
        # You may need to fetch the in-stock value from the product list or database
        label_inStock.config(text=f'In Stock [{cart_item_data[3]}]')  # Update the in-stock value

# Bind the cart item selection event to the Cart Frame treeview
treeview_cart.bind('<<TreeviewSelect>>', on_cart_item_select)

# === Billing Area ===
bill_frame = Frame(window, bd=2, relief=RIDGE, bg='white')
bill_frame.place(x=990, y=110, width=512, height=522)

btitle = Label(bill_frame, text='Customer Billing Area', font=('Helvetica', 15, 'bold'), bg='#0f4d7d', fg='white')
btitle.pack(side=TOP, fill=X)

scrolly = Scrollbar(bill_frame, orient=VERTICAL)
scrolly.pack(side=RIGHT, fill=Y)

txt_bill_area = Text(bill_frame, yscrollcommand=scrolly.set, wrap=WORD)
txt_bill_area.pack(fill=BOTH, expand=1)

scrolly.config(command=txt_bill_area.yview)

billMenuFrame = Frame(window, bd=2, relief=RIDGE, bg='white')
billMenuFrame.place(x=990, y=640, width=512, height=120)

label_amnt = Label(billMenuFrame, text='Bill Amount\n0', font=("goudy old style", 15, "bold"), bg="#4d636d", fg="white")
label_amnt.place(x=6, y=5, width=150, height=70)

label_discount = Label(billMenuFrame, text='Discount \n%', font=("goudy old style", 15, "bold"), bg="#4d636d", fg="white")
label_discount.place(x=163, y=5, width=150, height=70)

label_net_pay = Label(billMenuFrame, text='Net Pay\n0', font=("goudy old style", 15, "bold"), bg="#4d636d", fg="white")
label_net_pay.place(x=320, y=5, width=180, height=70)

generate_bill_button = Button(billMenuFrame, text='Generate Bill', command=lambda: generate_bill(window), font=("goudy old style", 15, "bold"),cursor='hand2', bg="#0f4d7d", fg="white")
generate_bill_button.place(x=6, y=80, width=150, height=30)

print_button = Button(billMenuFrame, text='Print',command=lambda: print_bill(window), font=("goudy old style", 15, "bold"),cursor='hand2', bg="#0f4d7d", fg="white")
print_button.place(x=163, y=80, width=150, height=30)

clear_all = Button(billMenuFrame, text='Clear All', font=("goudy old style", 15, "bold"),cursor='hand2', bg="#0f4d7d", fg="white", command=clear_all_data)
clear_all.place(x=320, y=80, width=180, height=30)


def generate_bill(window):
    # Check if customer details are provided
    if txt_name.get() == '' or txt_contact.get() == '':
        messagebox.showerror("Error", "Customer Details are required", parent=window)
        return  # Stop execution if customer details are missing

    # Check if the cart is empty
    cart_items = treeview_cart.get_children()  # Get all items in the cart
    if not cart_items:  # If the cart is empty
        messagebox.showerror("Error", "Cart is empty. Add products to generate a bill.", parent=window)
        return  # Stop execution if the cart is empty

    # Clear the bill area before generating a new bill
    txt_bill_area.delete(1.0, END)

    # Generate the bill top, middle, and bottom sections
    bill_top(window)
    bill_middle(window)
    bill_bottom(window)

    window.chk_print = 1  # This enables the print functionality

    # Generate a unique invoice number
    invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))

    # Save the bill to a file
    try:
        # Ensure the 'bill' directory exists
        import os
        if not os.path.exists('bill'):
            os.makedirs('bill')

        # Write the bill content to a file
        file_path = f'bill/{str(invoice)}.txt'
        with open(file_path, 'w') as fp:
            fp.write(txt_bill_area.get('1.0', END))

        messagebox.showinfo('Saved', f"Bill has been saved as {file_path}", parent=window)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the bill: {e}", parent=window)

def bill_top(window):
    invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))  # Unique invoice number
    bill_top_temp = f'''
\t\tXYZ-Inventory 
\t Phone No. 98725*****, Delhi-125001 
{str("="*47)} 
Customer Name: {txt_name.get()}
Ph no.: {txt_contact.get()} 
Bill No. {str(invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))} 
{str("="*47)} 
Product Name\t\t\tquantity\tPrice 
{str("="*47)} 
    '''
    txt_bill_area.delete(1.0, END)  # Clear the bill area
    txt_bill_area.insert('1.0', bill_top_temp)


def bill_middle(window):
    connection = None
    cursor = None
    try:
        # Establish a connection to the MySQL database
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='homraj07',
            database='inventory_system'
        )
        cursor = connection.cursor()

        # Get all items in the cart
        cart_items = treeview_cart.get_children()
        for item in cart_items:
            # Get the values of the item from the cart Treeview
            row = treeview_cart.item(item, 'values')
            print(f"Row Data: {row}")  # Debugging: Print row data

            id = int(row[0])  # Product ID
            name = row[1]  # Product name
            price_per_unit = float(row[2])  # Price per unit
            sold_quantity = int(float(row[3]))  # Quantity sold

            # **Fetch the actual available quantity from the database**
            cursor.execute("SELECT quantity FROM product_data WHERE id=%s", (id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", f"Product with ID {id} not found!", parent=window)
                return

            available_quantity = int(result[0])  # Available quantity in stock

            # **Check if stock is enough**
            if sold_quantity > available_quantity:
                messagebox.showerror("Error", f"Insufficient stock for {name}! Only {available_quantity} left.",
                                     parent=window)
                return  # Stop execution if stock is insufficient

            # **Correct subtraction**
            remaining_quantity = available_quantity - sold_quantity

            print(
                f"Product ID: {id} | Available: {available_quantity} | Sold: {sold_quantity} | Remaining: {remaining_quantity}")  # Debugging

            # Determine status
            status = 'Active' if remaining_quantity > 0 else 'InActive'

            # Calculate total price
            total_price = price_per_unit * sold_quantity

            # Insert the bill details into the text area
            txt_bill_area.insert(END, f"\n{name}\t\t\t{sold_quantity}\tRs.{total_price:.2f}")

            # **Update the database with the correct remaining quantity**
            update_query = 'UPDATE product_data SET quantity=%s, status=%s WHERE id=%s'
            cursor.execute(update_query, (remaining_quantity, status, id))
            connection.commit()

            # Debugging: Print the update query
            print(f"Updated: ID {id} | New Quantity: {remaining_quantity} | Status: {status}")

        # **Refresh the product frame to reflect changes**
        update_product_frame()

        # Notify user of successful update
        messagebox.showinfo("Success", "Bill generated and database updated successfully!", parent=window)

    except Exception as ex:
        # Show error message if something goes wrong
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=window)
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def update_product_frame():
    """Fetch updated product data and refresh the treeview"""
    try:
        # Reconnect to the database
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='homraj07',
            database='inventory_system'
        )
        cursor = connection.cursor()

        # Clear the existing product frame
        for item in treeview.get_children():
            treeview.delete(item)

        # Fetch updated product data, only Active products
        cursor.execute("SELECT id, name, price, quantity, status FROM product_data WHERE status='Active'")
        products = cursor.fetchall()

        # Insert updated product data into treeview
        for product in products:
            treeview.insert("", "end", values=product)

        connection.close()
    except Exception as ex:
        messagebox.showerror("Error", f"Error updating product frame: {str(ex)}")


def bill_bottom(window):
    cart_items = treeview_cart.get_children()  # Get all items in the cart
    total_amount = 0

    # Calculate the total bill amount
    for item in cart_items:
        row = treeview_cart.item(item, 'values')
        total_amount += float(row[4])  # Sum up the total prices

    # Calculate discount (assuming a fixed discount percentage for simplicity)
    discount_percentage = 10  # 10% discount
    discount = (total_amount * discount_percentage) / 100
    net_pay = total_amount - discount

    # Update the bill area with the total amount, discount, and net pay
    bill_bottom_temp = f'''
{str("=" * 47)}
 Bill Amount\t\t\t\tRs.{total_amount:.2f}
 Discount\t\t\t\tRs.{discount:.2f}
 Net Pay\t\t\t\tRs.{net_pay:.2f}
{str("=" * 47)}\n
    '''
    txt_bill_area.insert(END, bill_bottom_temp)


import tempfile
import os
from tkinter import messagebox, END


def print_bill(window):
    try:
        # Check if a bill has been generated
        if hasattr(window, 'chk_print') and window.chk_print == 1:
            messagebox.showinfo('Print', "Please wait while printing...", parent=window)

            # Create a temporary file for printing
            new_file = tempfile.mktemp('.txt')
            with open(new_file, 'w') as file:
                file.write(txt_bill_area.get('1.0', END))  # Get bill content

            # Print the file
            os.startfile(new_file, 'print')

        else:
            messagebox.showerror('Print', "Please generate a bill before printing.", parent=window)

    except Exception as ex:
        messagebox.showerror('Error', f"Printing failed due to: {str(ex)}", parent=window)


def logout(window):
    window.destroy()
    subprocess.run(["python", "login page.py"])


# Run the application
window.mainloop()