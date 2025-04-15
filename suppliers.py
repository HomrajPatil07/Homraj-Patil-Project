# supplier.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database


# Function to add supplier
def add_supplier(invoice, name, contact, description):
    if invoice == '' or name == '' or contact == '' or description.strip() == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            # Creating table if it does not exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS supplier_data (
                                invoice INT PRIMARY KEY, 
                                name VARCHAR(100), 
                                contact VARCHAR(15),
                                description TEXT
                             )''')

            # Check if the invoice already exists
            cursor.execute('SELECT invoice FROM supplier_data WHERE invoice = %s', (invoice,))
            existing_invoice = cursor.fetchone()

            if existing_invoice:
                messagebox.showerror('Error', 'Invoice number already exists')
            else:
                # Inserting supplier data into the table
                cursor.execute('''INSERT INTO supplier_data (invoice, name, contact, description) 
                                 VALUES (%s, %s, %s, %s)''', (invoice, name, contact, description))
                connection.commit()
                messagebox.showinfo('Success', 'Supplier added successfully!')
                show_suppliers()  # Refresh the Treeview after adding supplier
        except Exception as e:
            messagebox.showerror('Error', f'Error: {str(e)}')
        finally:
            connection.close()


# Function to update supplier
def update_supplier(invoice, name, contact, description):
    if invoice == '' or name == '' or contact == '' or description.strip() == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            # Updating supplier data in the database
            cursor.execute('''UPDATE supplier_data 
                              SET name = %s, contact = %s, description = %s 
                              WHERE invoice = %s''', (name, contact, description, invoice))
            if cursor.rowcount == 0:
                messagebox.showerror('Error', 'Invoice number not found')
            else:
                connection.commit()
                messagebox.showinfo('Success', 'Supplier updated successfully!')
                show_suppliers()  # Refresh the Treeview after updating supplier
        except Exception as e:
            messagebox.showerror('Error', f'Error: {str(e)}')
        finally:
            connection.close()


# Function to delete supplier
def delete_supplier(invoice):
    if invoice == '':
        messagebox.showerror('Error', 'Invoice number is required to delete')
        return

    # Confirm deletion
    confirmation = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete invoice number {invoice}?')
    if confirmation:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            # Deleting supplier data from the database
            cursor.execute('''DELETE FROM supplier_data WHERE invoice = %s''', (invoice,))
            if cursor.rowcount == 0:
                messagebox.showerror('Error', 'Invoice number not found')
            else:
                connection.commit()
                messagebox.showinfo('Success', 'Supplier deleted successfully!')
                show_suppliers()  # Refresh the Treeview after deletion
        except Exception as e:
            messagebox.showerror('Error', f'Error: {str(e)}')
        finally:
            connection.close()


# Function to clear the form fields
def clear_form():
    invoice_entry.delete(0, END)
    supplier_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)


# Function to fetch and display data in Treeview
def show_suppliers(search_term=""):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        # Fetch data from the database with optional search term
        if search_term:
            cursor.execute(f"SELECT * FROM supplier_data WHERE name LIKE %s OR invoice LIKE %s",
                           ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute('SELECT * FROM supplier_data')

        rows = cursor.fetchall()

        # Clear existing rows in Treeview before inserting new data
        for row in treeview.get_children():
            treeview.delete(row)

        # Insert fetched data into Treeview
        if rows:
            for row in rows:
                treeview.insert('', 'end', values=row)
        else:
            messagebox.showerror('Error', 'Record not found')

    except Exception as e:
        messagebox.showerror('Error', f'Error: {str(e)}')
    finally:
        connection.close()


# Function to search suppliers
def search_suppliers():
    search_term = search_entry.get()
    show_suppliers(search_term)


# Function to handle Treeview selection event
def on_treeview_select(event):
    selected_item = treeview.selection()
    if selected_item:
        # Get the selected row's values
        values = treeview.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        invoice_entry.delete(0, END)
        invoice_entry.insert(0, values[0])  # Invoice No.

        supplier_entry.delete(0, END)
        supplier_entry.insert(0, values[1])  # Supplier Name

        contact_entry.delete(0, END)
        contact_entry.insert(0, values[2])  # Contact

        description_text.delete(1.0, END)
        description_text.insert(1.0, values[3])  # Description


# Global variable to track the employee frame
supplier_frame = None


# Function to remove only the existing employee frame
def remove_supplier_frame():
    global supplier_frame
    if supplier_frame is not None:
        supplier_frame.destroy()
        supplier_frame = None  # Reset reference after destroying


# Supplier Form function
def supplier_form(window):
    global back_image, supplier_frame, treeview, invoice_entry, supplier_entry, contact_entry, description_text, search_entry

    remove_supplier_frame()

    supplier_frame = Frame(window, width=1330, height=700, bg='white')
    supplier_frame.place(x=200, y=100)

    heading_label = Label(supplier_frame, text='Manage Supplier Details', font=('times new roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back button.png')  # Ensure the file exists
    back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)

    left_frame = Frame(supplier_frame, bg='white')
    left_frame.place(x=10, y=100)

    # Form fields
    invoice_label = Label(left_frame, text='Invoice No.', font=('times new roman', 14, 'bold'), bg='white')
    invoice_label.grid(row=0, column=0, padx=(20, 40), sticky='w')
    invoice_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    invoice_entry.grid(row=0, column=1)

    supplier_label = Label(left_frame, text='Supplier Name', font=('times new roman', 14, 'bold'), bg='white')
    supplier_label.grid(row=1, column=0, padx=(20, 40), pady=15, sticky='w')
    supplier_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    supplier_entry.grid(row=1, column=1)

    contact_label = Label(left_frame, text='Contact', font=('times new roman', 14, 'bold'), bg='white')
    contact_label.grid(row=2, column=0, padx=(20, 40), sticky='w')
    contact_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    contact_entry.grid(row=2, column=1)

    description_label = Label(left_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=3, column=0, padx=(20, 40), pady=15, sticky='nw')
    description_text = Text(left_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=3, column=1, pady=25)

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=4, columnspan=2, pady=20)

    # Button to add supplier
    add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: add_supplier(invoice_entry.get(), supplier_entry.get(),
                                                                   contact_entry.get(),
                                                                   description_text.get(1.0, END).strip()))
    add_button.grid(row=0, column=0, padx=20)

    # Update and Delete buttons
    update_button = Button(button_frame, text='Update', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white',
                           bg='#0f4d7d', command=lambda: update_supplier(invoice_entry.get(), supplier_entry.get(),
                                                                         contact_entry.get(),
                                                                         description_text.get(1.0, END).strip()))
    update_button.grid(row=0, column=1)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white',
                           bg='#0f4d7d', command=lambda: delete_supplier(invoice_entry.get()))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='white',
                          bg='#0f4d7d', command=clear_form)
    clear_button.grid(row=0, column=3)

    # Right frame for treeview and search
    right_frame = Frame(supplier_frame, bg='white')
    right_frame.place(x=520, y=97, width=700, height=400)

    search_frame = Frame(right_frame, bg='white')
    search_frame.pack(pady=(0, 20))

    # Search fields
    num_label = Label(search_frame, text='Search', font=('times new roman', 14, 'bold'), bg='white')
    num_label.grid(row=0, column=0, padx=(0, 15), sticky='w')
    search_entry = Entry(search_frame, font=('times new roman', 14, 'bold'), bg='lightyellow', width=20)
    search_entry.grid(row=0, column=1)

    search_button = Button(search_frame, text='Search', font=('times new roman', 12), width=8, cursor='hand2',
                           fg='white',
                           bg='#0f4d7d', command=search_suppliers)
    search_button.grid(row=0, column=2, padx=15)

    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), width=8, cursor='hand2',
                         fg='white',
                         bg='#0f4d7d', command=lambda: show_suppliers())
    show_button.grid(row=0, column=3)

    # Treeview for displaying supplier data
    scrolly = Scrollbar(right_frame, orient=VERTICAL)
    scrollx = Scrollbar(right_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(right_frame, columns=('invoice', 'name', 'contact', 'description'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('invoice', text='Invoice Id')
    treeview.heading('name', text='Supplier Name')
    treeview.heading('contact', text='Supplier Contact')
    treeview.heading('description', text='Description')

    treeview.column('invoice', width=80)
    treeview.column('name', width=160)
    treeview.column('contact', width=120)
    treeview.column('description', width=200)

    # Bind the Treeview selection event to the on_treeview_select function
    treeview.bind('<<TreeviewSelect>>', on_treeview_select)

    show_suppliers()  # Automatically show all suppliers when the form is loaded

    return supplier_frame