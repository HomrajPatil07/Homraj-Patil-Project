# employee.py
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pymysql
from datetime import datetime

# Database connection
def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='homraj07',
            database='inventory_system'
        )
        cursor = connection.cursor()

        # Create database if it does not exist
        cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
        cursor.execute('USE inventory_system')

        # Create table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS employee_data (
                           empid INT PRIMARY KEY,
                           name VARCHAR(100),
                           email VARCHAR(100),
                           gender VARCHAR(50),
                           dob VARCHAR(30),
                           contact VARCHAR(30),
                           employment_type VARCHAR(50),
                           education VARCHAR(50),
                           work_shift VARCHAR(50),
                           address TEXT,
                           doj VARCHAR(30),
                           salary VARCHAR(50),
                           usertype VARCHAR(50),
                           password VARCHAR(50)
                       )''')

        return cursor, connection
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f'Database connectivity issue: {e}')
        return None, None

# Fetch data for the Treeview
def treeview_data(tree):
    cursor, connection = connect_database()
    if not (cursor and connection):
        return
    cursor.execute('SELECT * FROM employee_data')
    employee_records = cursor.fetchall()
    tree.delete(*tree.get_children())  # Clear treeview
    for record in employee_records:
        tree.insert('', END, values=record)
    connection.close()

# Search Employee
def search_employee(tree, search_field, search_value):
    if search_field == 'Search By' or not search_value.strip():
        messagebox.showerror('Error', 'Please select a search field and enter a value.')
        return

    field_map = {
        'Id': 'empid',
        'Name': 'name',
        'Email': 'email'
    }
    search_column = field_map.get(search_field)

    cursor, connection = connect_database()
    if cursor and connection:
        try:
            query = f"SELECT * FROM employee_data WHERE {search_column} LIKE %s"
            cursor.execute(query, ('%' + search_value + '%',))
            search_results = cursor.fetchall()
            tree.delete(*tree.get_children())  # Clear the Treeview
            for record in search_results:
                tree.insert('', END, values=record)
            if not search_results:
                messagebox.showinfo('Info', 'No matching records found.')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Search failed: {e}')
        finally:
            connection.close()

# Clear form fields
def clear_employee_form(entries):
    for entry in entries.values():
        if isinstance(entry, ttk.Combobox):
            entry.set('Select')
        elif isinstance(entry, DateEntry):
            entry.set_date(datetime.today())  # Set to today's date
        else:
            entry.delete(0, END)

# Add employee
def save_employee(tree, *fields):
    if any(field == '' or field == 'Select' for field in fields):
        messagebox.showerror('Error', 'All fields are required')
        return

    cursor, connection = connect_database()
    if cursor and connection:
        try:
            cursor.execute('INSERT INTO employee_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           fields)
            connection.commit()
            treeview_data(tree)
            messagebox.showinfo('Success', 'Employee added successfully!')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Failed to add employee: {e}')
        finally:
            connection.close()

# Update employee
def update_employee(tree, *fields):
    if any(field == '' or field == 'Select' for field in fields):
        messagebox.showerror('Error', 'All fields are required')
        return

    empid = fields[0]
    if not empid.isdigit():  # Validate empid is numeric
        messagebox.showerror('Error', 'Invalid Employee ID')
        return

    cursor, connection = connect_database()
    if cursor and connection:
        try:
            cursor.execute('''UPDATE employee_data SET
                             name=%s, email=%s, gender=%s, dob=%s, contact=%s,
                             employment_type=%s, education=%s, work_shift=%s, address=%s,
                             doj=%s, salary=%s, usertype=%s, password=%s
                             WHERE empid=%s''',
                           (*fields[1:], fields[0]))  # Pass fields[0] (empid) at the end
            connection.commit()
            treeview_data(tree)  # Refresh the Treeview
            messagebox.showinfo('Success', 'Employee updated successfully!')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Failed to update employee: {e}')
        finally:
            connection.close()

# Delete employee
def delete_employee(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Error', 'No employee selected')
        return

    empid = tree.item(selected_item, 'values')[0]
    cursor, connection = connect_database()
    if cursor and connection:
        try:
            cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))
            connection.commit()
            treeview_data(tree)
            messagebox.showinfo('Success', 'Employee deleted successfully!')
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f'Failed to delete employee: {e}')
        finally:
            connection.close()

# Global variable to track the employee frame
employee_frame = None

# Function to remove only the existing employee frame
def remove_employee_frame():
    global employee_frame
    if employee_frame is not None:
        employee_frame.destroy()
        employee_frame = None  # Reset reference after destroying

# Employee form
def employee_form(window):
    global back_image, employee_frame  # Track employee frame globally

    # Remove only the employee frame before creating a new one
    remove_employee_frame()

    employee_frame = Frame(window, width=1330, height=700, bg='white')
    employee_frame.place(x=200, y=100)

    heading_label = Label(employee_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'),
                          bg='#0f4d7d', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    back_image = PhotoImage(file='back button.png')
    back_button = Button(employee_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=30)

    tree_frame = Frame(employee_frame, bg='white')
    tree_frame.place(x=0, y=50, width=1330, height=235)

    search_frame = Frame(tree_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'), font=('times new roman', 12),
                                   state='readonly', justify=CENTER)
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: search_employee(tree, search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d', command=lambda: treeview_data(tree))
    show_button.grid(row=0, column=3)

    columns = ('empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type', 'education', 'work_shift',
               'address', 'doj', 'salary', 'usertype', 'password')
    tree = ttk.Treeview(tree_frame, columns=columns, show='headings')

    # Scrollbars
    vertical_scrollbar = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    vertical_scrollbar.pack(side=RIGHT, fill=Y)
    horizontal_scrollbar = Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)

    tree.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    tree.pack(fill=BOTH, expand=True)

    # Column Widths
    column_widths = {
        'empid': 50,
        'name': 150,
        'email': 200,
        'gender': 80,
        'dob': 100,
        'contact': 110,
        'employment_type': 120,
        'education': 120,
        'work_shift': 100,
        'address': 200,
        'doj': 100,
        'salary': 100,
        'usertype': 110,
        'password': 100
    }
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=column_widths.get(col, 100))

    treeview_data(tree)

    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=200, y=330, width=1200, height=400)

    # Employee form labels and entries
    labels = ['EmpId', 'Name', 'Email', 'Gender', 'DOB', 'Contact', 'Employment Type', 'Education', 'Work Shift',
              'Address', 'DOJ', 'Salary', 'User Type', 'Password']
    entries = {}
    row, col = 0, 0

    for label in labels:
        lbl = Label(detail_frame, text=label, font=('times new roman', 12), bg='white')
        lbl.grid(row=row, column=col, padx=10, pady=10, sticky=W)
        if label == 'Gender':
            entry = ttk.Combobox(detail_frame, values=['Select', 'Male', 'Female'], state='readonly')
            entry.set('Select')
        elif label in ['Employment Type', 'Education', 'Work Shift', 'User Type']:
            values = {
                'Employment Type': ['Select', 'Full Time', 'Part Time'],
                'Education': ['Select', 'BCA', 'MCA','B.Com','BA','MBA','BSC','B.Tech','M.Tech'],
                'Work Shift': ['Select', 'Morning', 'Evening', 'Night'],
                'User Type': ['Select', 'Employee', 'Admin']
            }
            entry = ttk.Combobox(detail_frame, values=values[label], state='readonly')
            entry.set('Select')
        elif label in ['DOB', 'DOJ']:
            entry = DateEntry(detail_frame, date_pattern='dd/mm/yyyy')
        else:
            entry = Entry(detail_frame, font=('times new roman', 12))
        entry.grid(row=row, column=col + 1, padx=10, pady=10)
        entries[label] = entry
        col += 2
        if col == 6:
            row += 1
            col = 0

    # Function to fill form fields when a row is selected
    def fill_form_fields(event):
        selected_item = tree.selection()
        if not selected_item:
            return

        # Get the selected row's data
        row_data = tree.item(selected_item, 'values')

        # Map the row data to the form fields
        for i, label in enumerate(labels):
            if label in ['DOB', 'DOJ']:
                # For DateEntry fields, set the date
                entries[label].set_date(datetime.strptime(row_data[i], '%d/%m/%Y'))
            else:
                # For other fields, insert the value
                if isinstance(entries[label], ttk.Combobox):
                    entries[label].set(row_data[i])
                else:
                    entries[label].delete(0, END)
                    entries[label].insert(0, row_data[i])

    # Bind the Treeview selection event to the fill_form_fields function
    tree.bind('<<TreeviewSelect>>', fill_form_fields)

    # Buttons
    def get_field_values():
        return [entries[label].get() for label in labels]

    button_frame = Frame(detail_frame, bg='white')
    button_frame.grid(row=row + 1, column=0, columnspan=6, pady=20)

    Button(button_frame, text='Save', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d',
           command=lambda: save_employee(tree, *get_field_values())).grid(row=0, column=0, padx=30)

    Button(button_frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2', fg='white',
           bg='#0f4d7d',
           command=lambda: update_employee(tree, *get_field_values())).grid(row=0, column=1)

    Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2', fg='white',
           bg='#0f4d7d',
           command=lambda: delete_employee(tree)).grid(row=0, column=2, padx=30)

    Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2', fg='white',
           bg='#0f4d7d', command=lambda: clear_employee_form(entries)).grid(row=0, column=3)

    return employee_frame