# product.py
from tkinter import *
from tkinter import ttk, messagebox
from category import clear_fields
from employees import connect_database

def select_data(event, treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox):
    index = treeview.selection()
    if not index:
        return
    content = treeview.item(index, 'values')
    if content:
        name_entry.delete(0, END)
        price_entry.delete(0, END)
        quantity_entry.delete(0, END)
        discount_spinbox.delete(0, END)
        category_combobox.set(content[1])
        supplier_combobox.set(content[2])
        name_entry.insert(0, content[3])
        price_entry.insert(0, content[4])
        discount_spinbox.insert(0, content[5])  # Corrected usage for Spinbox
        quantity_entry.insert(0, content[7])  # Quantity is now at index 7
        status_combobox.set(content[8])  # Status is now at index 8

def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT id, category, supplier, name, price, discount, discounted_price, quantity, status FROM product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())  # Clear treeview
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def add_product(category, supplier, name, price, discount, quantity, status, treeview):
    if category in ['Empty', 'Select'] or supplier in ['Empty', 'Select'] or not name or not price or not quantity or status == 'Select status':
        messagebox.showerror('Error', 'All fields are required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('''CREATE TABLE IF NOT EXISTS product_data (
                          id INT AUTO_INCREMENT PRIMARY KEY,
                          category VARCHAR(100),
                          supplier VARCHAR(100),
                          name VARCHAR(100),
                          price DECIMAL(10,2),
                          discount DECIMAL(5,2),
                          discounted_price DECIMAL(10,2),
                          quantity INT,
                          status VARCHAR(50)
                      )''')

        # Calculate discounted price
        discounted_price = round(float(price) * (1 - float(discount) / 100), 2)

        cursor.execute('''INSERT INTO product_data (category, supplier, name, price, discount, discounted_price, quantity, status)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                       (category, supplier, name, price, discount, discounted_price, quantity, status))
        connection.commit()
        messagebox.showinfo('Success', 'Product added successfully')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def update_product(category, supplier, name, price, discount, quantity, status, treeview):
    index = treeview.selection()

    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return

    selected_item = treeview.item(index)
    content = selected_item['values']
    product_id = content[0]  # Fetching ID

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')

        # Calculate discounted price
        discounted_price = round(float(price) * (1 - float(discount) / 100), 2)

        cursor.execute('''
            UPDATE product_data 
            SET category = %s, supplier = %s, name = %s, price = %s, discount = %s, discounted_price = %s, quantity = %s, status = %s
            WHERE id = %s
        ''', (category, supplier, name, price, discount, discounted_price, quantity, status, product_id))

        connection.commit()
        messagebox.showinfo('Success', 'Product updated successfully')

        # Refresh Treeview Data
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror('Error', f'Error updating product: {str(e)}')

    finally:
        cursor.close()
        connection.close()

def delete_product(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return

    ans = messagebox.askyesno('Confirm', 'Do you really want to delete?')
    if ans:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')

            # Fetch the selected item's ID
            dict_data = treeview.item(index)
            content = dict_data['values']
            if not content:
                messagebox.showerror('Error', 'Could not retrieve record ID')
                return
            product_id = content[0]  # Assuming the ID is in the first column

            # Delete the product
            cursor.execute('DELETE FROM product_data WHERE id=%s', (product_id,))
            connection.commit()

            # Reset AUTO_INCREMENT to reuse the deleted ID
            cursor.execute('ALTER TABLE product_data AUTO_INCREMENT = 1')
            connection.commit()

            # Refresh the Treeview after deletion
            treeview_data(treeview)
            messagebox.showinfo('Info', 'Record is deleted')
            clear_fields(category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox, treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
def clear_fields(category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox, treeview):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set('Select Status')
    discount_spinbox.delete(0, END)
    discount_spinbox.insert(0, 0)

def search_product(search_combobox, search_entry, treeview):
    if search_combobox.get() == 'Search By':
        messagebox.showwarning('Warning', 'Please select an option')
    elif search_entry.get() == '':
        messagebox.showwarning('Warning', 'Please enter the value to search')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute(f'SELECT id, name, price, quantity, status FROM product_data WHERE {search_combobox.get()}=%s', (search_entry.get(),))
            records = cursor.fetchall()
            if len(records) == 0:
                messagebox.showerror('Error', 'No records found')
                return
            treeview.delete(*treeview.get_children())  # Clear the treeview
            for record in records:
                treeview.insert('', END, values=record)  # Insert found records into the treeview
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def show_all(treeview, search_combobox, search_entry):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT id, name, price, quantity, status FROM product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())  # Clear the treeview
        for record in records:
            treeview.insert('', END, values=record)  # Insert all records into the treeview
        search_combobox.set('Search By')  # Reset search combobox
        search_entry.delete(0, END)  # Clear search entry
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox, supplier_combobox):
    category_option = []
    supplier_option = []
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT name FROM category_data')
        category_option = [name[0] for name in cursor.fetchall()]
        category_combobox['values'] = category_option or ['Empty']
        category_combobox.set('Select')

        cursor.execute('SELECT name FROM supplier_data')
        supplier_option = [name[0] for name in cursor.fetchall()]
        supplier_combobox['values'] = supplier_option or ['Empty']
        supplier_combobox.set('Select')
    except Exception as e:
        messagebox.showerror('Error', f'Error fetching data: {e}')
    finally:
        cursor.close()
        connection.close()

# Global variable to track the employee frame
product_frame = None

def remove_product_frame():
    global product_frame
    if product_frame is not None:
        product_frame.destroy()
        product_frame = None  # Reset reference after destroying

def product_form(window):
    global back_image, product_frame

    remove_product_frame()

    product_frame = Frame(window, width=1330, height=800, bg='white')
    product_frame.place(x=200, y=100)

    back_image = PhotoImage(file='back button.png')  # Ensure the file exists
    back_button = Button(product_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=0)

    left_frame = Frame(product_frame, bg='white', bd=2, relief=RIDGE)
    left_frame.place(x=30, y=40, height=640)

    heading_label = Label(left_frame, text='Manage Product Details', font=('times new roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.grid(row=0, columnspan=2, sticky='we')

    category_label = Label(left_frame, text='Category', font=('times new roman', 14, 'bold'), bg='white')
    category_label.grid(row=1, column=0, padx=20, sticky='w')
    category_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
    category_combobox.grid(row=1, column=1, pady=45)
    category_combobox.set('Empty')

    supplier_label = Label(left_frame, text='Supplier', font=('times new roman', 14, 'bold'), bg='white')
    supplier_label.grid(row=2, column=0, padx=20, sticky='w')
    supplier_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
    supplier_combobox.grid(row=2, column=1)
    supplier_combobox.set('Empty')

    name_label = Label(left_frame, text='Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=3, column=0, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    name_entry.grid(row=3, column=1, pady=45)

    price_label = Label(left_frame, text='Price', font=('times new roman', 14, 'bold'), bg='white')
    price_label.grid(row=4, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    price_entry.grid(row=4, column=1)

    discount_label = Label(left_frame, text='Discount(%)', font=('times new roman', 14, 'bold'), bg='white')
    discount_label.grid(row=5, column=0, padx=20, sticky='w')
    discount_spinbox = Spinbox(left_frame, from_=0, to=100, font=('times new roman', 14, 'bold'), bg='white')
    discount_spinbox.grid(row=5, column=1, pady=45)

    quantity_label = Label(left_frame, text='Quantity', font=('times new roman', 14, 'bold'), bg='white')
    quantity_label.grid(row=6, column=0, padx=20, sticky='w')
    quantity_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    quantity_entry.grid(row=6, column=1)

    status_label = Label(left_frame, text='Status', font=('times new roman', 14, 'bold'), bg='white')
    status_label.grid(row=7, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=('times new roman', 14, 'bold'), width=18, state='readonly')
    status_combobox.grid(row=7, column=1, pady=45)
    status_combobox.set('Select status')

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=8, columnspan=2)

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: add_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), discount_spinbox.get(), quantity_entry.get(), status_combobox.get(), treeview))
    add_button.grid(row=0, column=0, padx=10, pady=0)

    update_button = Button(button_frame, text='Update', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: update_product(category_combobox.get(), supplier_combobox.get(), name_entry.get(), price_entry.get(), discount_spinbox.get(), quantity_entry.get(), status_combobox.get(), treeview))
    update_button.grid(row=0, column=1, padx=10, pady=0)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: delete_product(treeview, category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox))
    delete_button.grid(row=0, column=2, padx=10, pady=0)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: clear_fields(category_combobox, supplier_combobox, name_entry, price_entry, discount_spinbox, quantity_entry, status_combobox, treeview))
    clear_button.grid(row=0, column=3, padx=10, pady=0)

    search_frame = LabelFrame(product_frame, text='Search Product', font=('times new roman', 14, 'bold'), bg='white')
    search_frame.place(x=500, y=25, width=680)

    search_combobox = ttk.Combobox(search_frame, values=('Category', 'Supplier', 'Name', 'Status'), state='readonly', width=20, font=('times new roman', 14))
    search_combobox.grid(row=0, column=1, padx=20, pady=10)
    search_combobox.set('Search By')

    search_entry = Entry(search_frame, font=('times new roman', 14, 'bold'), bg='lightyellow', width=20)
    search_entry.grid(row=0, column=2)

    search_button = Button(search_frame, text='Search', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: search_product(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=3, padx=20, pady=10)

    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: show_all(treeview, search_combobox, search_entry))
    show_button.grid(row=0, column=4, padx=(0, 20), pady=10)

    treeview_frame = Frame(product_frame)
    treeview_frame.place(x=500, y=120, width=680, height=557)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(treeview_frame, columns=('id', 'category', 'supplier', 'name', 'price', 'discount', 'discounted_price', 'quantity', 'status'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='Id')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Name')
    treeview.heading('price', text='Price')
    treeview.heading('discount', text='Discount(%)')
    treeview.heading('discounted_price', text='Discounted Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')

    treeview.column('id', width=70)
    treeview.column('price', width=100)
    treeview.column('discount', width=100)
    treeview.column('discounted_price', width=100)
    treeview.column('quantity', width=100)
    treeview.column('status', width=90)
    fetch_supplier_category(category_combobox, supplier_combobox)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                  lambda event: select_data(event, treeview, category_combobox, supplier_combobox, name_entry,
                                            price_entry, discount_spinbox, quantity_entry, status_combobox))

    return product_frame