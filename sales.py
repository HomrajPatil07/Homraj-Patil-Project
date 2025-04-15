from tkinter import *
from tkinter import ttk, messagebox
import os

sales_frame = None  # Define global variable


def sales_form(window):
    global back_image, bill_image, Sales_List, bill_area, invoice_entry, sales_Frame, bill_frame, sales_frame

    if sales_frame is not None:  # If the frame already exists, destroy it
        sales_frame.destroy()

    sales_frame = Frame(window, width=1330, height=800, bg='white')
    sales_frame.place(x=200, y=100)

    back_image = PhotoImage(file='back button.png')
    back_button = Button(sales_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=hide_sales)
    back_button.place(x=10, y=0)

    left_frame = Frame(sales_frame, bg='white')
    left_frame.place(x=100, y=100)

    invoice_label = Label(left_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white')
    invoice_label.grid(row=0, column=1, padx=10, sticky='w')

    invoice_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    invoice_entry.grid(row=0, column=2)

    search_button = Button(left_frame, text='Search', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                           bg='#0f4d7d', command=search)
    search_button.grid(row=0, column=3, padx=20, pady=10)

    clear_button = Button(left_frame, text='Clear', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                          bg='#0f4d7d', command=clear)
    clear_button.grid(row=0, column=4)

    # === Bill List ===
    sales_Frame = Frame(sales_frame, bd=3, relief=RIDGE)
    sales_Frame.place(x=70, y=180, width=230, height=460)

    scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
    Sales_List = Listbox(sales_Frame, font=("goudy old style", 15), bg="white", yscrollcommand=scrolly.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=Sales_List.yview)
    Sales_List.pack(fill=BOTH, expand=1)
    Sales_List.bind("<ButtonRelease-1>", get_data)

    # === Bill Area ===
    bill_frame = Frame(sales_frame, bd=3, relief=RIDGE)
    bill_frame.place(x=330, y=180, width=500, height=460)

    heading_label = Label(bill_frame, text='Customer Bill Area', font=('times new roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.pack(side=TOP, fill=X)

    scrolly2 = Scrollbar(bill_frame, orient=VERTICAL)
    bill_area = Text(bill_frame, font=("goudy old style", 15), bg="lightyellow", yscrollcommand=scrolly2.set)
    scrolly2.pack(side=RIGHT, fill=Y)
    scrolly2.config(command=bill_area.yview)
    bill_area.pack(fill=BOTH, expand=1)

    # === Image ===
    bill_image = PhotoImage(file='bill_logo.png')
    label = Label(sales_frame, image=bill_image, bg='white')
    label.place(x=910, y=260)

    show_sales(Sales_List)  # Load the sales list


# Function to hide the sales frame properly
def hide_sales():
    global sales_frame
    if sales_frame:
        sales_frame.destroy()  # Properly remove the frame
        sales_frame = None  # Reset to None


# Function to display all sales invoices
def show_sales(listbox):
    listbox.delete(0, END)  # Clear existing list
    if not os.path.exists('bill'):
        os.makedirs('bill')  # Create 'bill' folder if it doesn't exist
    files = os.listdir('bill')  # Get list of bill files
    for file in files:
        listbox.insert(END, file)  # Insert file names into the listbox


# Function to fetch and display selected bill data
def get_data(event):
    selected_index = Sales_List.curselection()
    if not selected_index:
        return  # No item selected

    file_name = Sales_List.get(selected_index[0])
    file_path = os.path.join('bill', file_name)

    try:
        with open(file_path, "r") as file:
            bill_content = file.read()
            bill_area.delete("1.0", END)
            bill_area.insert(END, bill_content)
    except Exception as e:
        print(f"Error loading file: {e}")


# Function to search for an invoice
def search():
    invoice_no = invoice_entry.get().strip()

    if not invoice_no:  # If field is empty
        messagebox.showwarning("Warning", "Invoice No. is required!")
        return

    Sales_List.delete(0, END)  # Clear existing list

    if not os.path.exists('bill'):
        messagebox.showerror("Error", "No invoices found!")  # Error if bill folder doesn't exist
        return

    files = os.listdir('bill')
    found = False
    for file in files:
        if invoice_no in file:  # Search for invoice number in filenames
            Sales_List.insert(END, file)
            found = True

    if not found:
        messagebox.showerror("Error", f"Invoice No. '{invoice_no}' not found!")  # Error if invoice doesn't exist


# Function to clear the search field and reload all invoices
def clear():
    invoice_entry.delete(0, END)  # Clear the invoice search field
    show_sales(Sales_List)  # Reload all invoices

