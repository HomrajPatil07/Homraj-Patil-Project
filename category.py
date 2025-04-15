# category.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database


# Function to add category
def add_category(id, name, description):
    if id == '' or name == '' or description == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')

            # Ensure the table exists
            cursor.execute('''CREATE TABLE IF NOT EXISTS category_data (
                                id INT PRIMARY KEY, 
                                name VARCHAR(100), 
                                description TEXT
                             )''')

            # Check if the ID already exists
            cursor.execute('SELECT * FROM category_data WHERE id = %s', (id,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
                return

            # Insert data into the table
            cursor.execute('INSERT INTO category_data (id, name, description) VALUES (%s, %s, %s)',
                           (id, name, description))
            connection.commit()
            messagebox.showinfo('Success', 'Category added successfully')
        except Exception as e:
            messagebox.showerror('Error', f"Error due to: {str(e)}")
        finally:
            cursor.close()
            connection.close()


# Function to delete category
def delete_category(treeview):
    selected_item = treeview.focus()
    if not selected_item:
        messagebox.showerror('Error', 'No item selected')
        return

    values = treeview.item(selected_item, 'values')
    category_id = values[0]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM category_data WHERE id = %s', (category_id,))
        connection.commit()
        treeview.delete(selected_item)
        messagebox.showinfo('Success', 'Category deleted successfully')
    except Exception as e:
        messagebox.showerror('Error', f"Error due to: {str(e)}")
    finally:
        cursor.close()
        connection.close()


# Function to clear fields
def clear_fields(id_entry, category_name_entry, description_text):
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)


# Function to load categories
def load_categories(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('''CREATE TABLE IF NOT EXISTS category_data (
                            id INT PRIMARY KEY, 
                            name VARCHAR(100), 
                            description TEXT
                         )''')

        cursor.execute('SELECT * FROM category_data')
        rows = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in rows:
            treeview.insert('', 'end', values=row)
    except Exception as e:
        messagebox.showerror('Error', f"Error due to: {str(e)}")
    finally:
        cursor.close()
        connection.close()


# Function to handle Treeview selection event
def on_treeview_select(event, id_entry, category_name_entry, description_text):
    selected_item = treeview.focus()
    if selected_item:
        # Get the selected row's values
        values = treeview.item(selected_item, 'values')

        # Populate the form fields with the selected row's data
        id_entry.delete(0, END)
        id_entry.insert(0, values[0])  # Id

        category_name_entry.delete(0, END)
        category_name_entry.insert(0, values[1])  # Category Name

        description_text.delete(1.0, END)
        description_text.insert(1.0, values[2])  # Description


# Global variable to track the employee frame
category_frame = None


# Function to remove only the existing employee frame
def remove_category_frame():
    global category_frame
    if category_frame is not None:
        category_frame.destroy()
        category_frame = None  # Reset reference after destroying


# Category form function
def category_form(window):
    global back_image, logo, category_frame, treeview

    remove_category_frame()

    category_frame = Frame(window, width=1330, height=700, bg='white')
    category_frame.place(x=200, y=100)

    heading_label = Label(category_frame, text='Manage Category Details', font=('times new roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back button.png')  # Ensure the file exists
    back_button = Button(category_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: category_frame.place_forget())
    back_button.place(x=10, y=30)

    logo = PhotoImage(file='product_category.png')
    label = Label(category_frame, image=logo, bg='white')
    label.place(x=30, y=100)

    details_frame = Frame(category_frame, bg='white')
    details_frame.place(x=500, y=60)

    id_label = Label(details_frame, text='Id', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=(20, 40), sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    id_entry.grid(row=0, column=1)

    category_name_label = Label(details_frame, text='Category Name', font=('times new roman', 14, 'bold'), bg='white')
    category_name_label.grid(row=1, column=0, padx=(20, 40), sticky='w')
    category_name_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    category_name_entry.grid(row=1, column=1, pady=20)

    description_label = Label(details_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=2, column=0, padx=(20, 40), sticky='w')
    description_text = Text(details_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=2, column=1)

    button_frame = Frame(category_frame, bg='white')
    button_frame.place(x=650, y=280)

    treeview_frame = Frame(category_frame, bg='white')
    treeview_frame.place(x=530, y=340, height=300, width=600)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    treeview = ttk.Treeview(treeview_frame, columns=('id', 'name', 'description'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='Id')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')

    treeview.column('id', width=80)
    treeview.column('name', width=140)
    treeview.column('description', width=300)

    # Bind the Treeview selection event to the on_treeview_select function
    treeview.bind('<<TreeviewSelect>>',
                  lambda event: on_treeview_select(event, id_entry, category_name_entry, description_text))

    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                        bg='#0f4d7d', command=lambda: [
            add_category(id_entry.get(), category_name_entry.get(),
                         description_text.get(1.0, END).strip()),
            load_categories(treeview)])
    add_button.grid(row=0, column=0, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=8, cursor='hand2',
                           fg='white',
                           bg='#0f4d7d', command=lambda: delete_category(treeview))
    delete_button.grid(row=0, column=1, padx=10)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=8, cursor='hand2', fg='white',
                          bg='#0f4d7d', command=lambda: clear_fields(id_entry, category_name_entry, description_text))
    clear_button.grid(row=0, column=2, padx=20)

    load_categories(treeview)

    return category_frame