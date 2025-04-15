from tkinter import *
from employees import employee_form
from suppliers import supplier_form
from category import category_form
from products import product_form
from sales import sales_form
from employees import connect_database
from tkinter import ttk, messagebox
import time
import os
import subprocess

def update():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * from employee_data')
        emp_records = cursor.fetchall()
        total_emp_count_Label.config(text=len(emp_records))

        cursor.execute('SELECT * from supplier_data')
        sup_records = cursor.fetchall()
        total_supp_count_Label.config(text=len(sup_records))

        cursor.execute('SELECT * from category_data')
        cat_records = cursor.fetchall()
        total_cat_count_Label.config(text=len(cat_records))

        cursor.execute('SELECT * from product_data')
        prod_records = cursor.fetchall()
        total_prod_count_Label.config(text=len(prod_records))

        bill = len(os.listdir('bill'))
        total_sales_count_Label.config(text=str(bill))  # Correct way to update the label text

        date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
        subtitleLabel.config(text=f'Welcome Admin\t\t\t\t\t\t\t {date_time}')
    finally:
        cursor.close()
        connection.close()
    subtitleLabel.after(1000, update)


def logout(window):
    window.destroy()
    subprocess.run(["python", "login page.py"])

current_frame = None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame = form_function(window)

# GUI part
window = Tk()
window.title('Dashboard | Developed By Homraj Patil')
window.geometry('1530x800+0+0')
window.resizable(0, 0)
window.config(bg='white')

titleLabel = Label(window, text=' Medical Store Management system', font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w')
titleLabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window, text='Logout', command=lambda: logout(window), font=('times new roman', 20, 'bold'), fg='#010c48')
logoutButton.place(x=1360, y=7)

subtitleLabel = Label(window, text='Welcome Admin\t\t Date: 02-01-2025\t\t Time: 12:36:17 pm', font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=66, relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0, y=98, width=200, height=700)

try:
    machin_image = PhotoImage(file='dashboard logo.png')
    imageLabel = Label(leftFrame, image=machin_image)
    imageLabel.pack()
except Exception as e:
    imageLabel = Label(leftFrame, text='Machine Image Missing', bg='white', fg='red', font=('times new roman', 10))
    imageLabel.pack()

manuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
manuLabel.pack(fill=X)

try:
    employee_icon = PhotoImage(file='employees.png')
    supplier_icon = PhotoImage(file='supplier.png')
    category_icon = PhotoImage(file='category.png')
    product_icon = PhotoImage(file='product.png')
    sales_icon = PhotoImage(file='sales.png')
    exit_icon = PhotoImage(file='exit.png')
except Exception as e:
    employee_icon = supplier_icon = category_icon = product_icon = sales_icon = exit_icon = None

employee_button = Button(leftFrame, image=employee_icon, compound=LEFT, text=' Employees', font=('times new roman', 15, 'bold'),
                         anchor='w', pady=13, command=lambda: show_form(employee_form))
employee_button.pack(fill=X)

supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT, text=' Suppliers', font=('times new roman', 15, 'bold'),
                         anchor='w', pady=13, command=lambda: supplier_form(window))
supplier_button.pack(fill=X)

category_button = Button(leftFrame, image=category_icon, compound=LEFT, text=' Categories', font=('times new roman', 15, 'bold'),
                         anchor='w', pady=13, command=lambda: category_form(window))
category_button.pack(fill=X)

product_button = Button(leftFrame, image=product_icon, compound=LEFT, text=' Products', font=('times new roman', 15, 'bold'),
                        anchor='w', pady=14, command=lambda: product_form(window))
product_button.pack(fill=X)

sales_button = Button(leftFrame, image=sales_icon, compound=LEFT, text=' Sales', font=('times new roman', 15, 'bold'),
                      anchor='w', pady=14, command=lambda: sales_form(window))
sales_button.pack(fill=X)


exit_button = Button(leftFrame, image=exit_icon, compound=LEFT, text=' Exit', font=('times new roman', 15, 'bold'),
                     anchor='w', pady=14, command=window.quit)
exit_button.pack(fill=X)

#===Employee Frame===
emp_frame = Frame(window, bg='#ff8c00', bd=3, relief=RIDGE)
emp_frame.place(x=400, y=120, height=200, width=400)

total_emp_icon = PhotoImage(file='total_emp.png')
total_emp_icon_Label = Label(emp_frame, image=total_emp_icon, bg='#ff8c00')
total_emp_icon_Label.pack(pady=15)

total_emp_icon_Label = Label(emp_frame, text='Total Employees', bg='#ff8c00', fg='white', font=('times new roman', 15, 'bold'))
total_emp_icon_Label.pack()

total_emp_count_Label = Label(emp_frame, text='0', bg='#ff8c00', fg='white', font=('times new roman', 15, 'bold'))
total_emp_count_Label.pack()

#===Supplier Frame===
supp_frame = Frame(window, bg='#008b8b', bd=3, relief=RIDGE)
supp_frame.place(x=900, y=120, height=200, width=400)

total_supp_icon = PhotoImage(file='total_supp.png')
total_supp_icon_Label = Label(supp_frame, image=total_supp_icon, bg='#008b8b')
total_supp_icon_Label.pack(pady=15)

total_supp_icon_Label = Label(supp_frame, text='Total Supplier', bg='#008b8b', fg='white', font=('times new roman', 15, 'bold'))
total_supp_icon_Label.pack()

total_supp_count_Label = Label(supp_frame, text='0', bg='#008b8b', fg='white', font=('times new roman', 15, 'bold'))
total_supp_count_Label.pack()

#===Category Frame===
cat_frame = Frame(window, bg='#2c3e50', bd=3, relief=RIDGE)
cat_frame.place(x=400, y=350, height=200, width=400)

total_cat_icon = PhotoImage(file='total_cat.png')
total_cat_icon_Label = Label(cat_frame, image=total_cat_icon, bg='#2c3e50')
total_cat_icon_Label.pack(pady=10)

total_cat_Label = Label(cat_frame, text='Total Category', bg='#2c3e50', fg='white', font=('times new roman', 15, 'bold'))
total_cat_Label.pack()

total_cat_count_Label = Label(cat_frame, text='0', bg='#2c3e50', fg='white', font=('times new roman', 15, 'bold'))
total_cat_count_Label.pack()

#===Product Frame===
prod_frame = Frame(window, bg='#8e44ad', bd=3, relief=RIDGE)
prod_frame.place(x=900, y=350, height=200, width=400)

total_prod_icon = PhotoImage(file='total_prod.png')
total_prod_icon_Label = Label(prod_frame, image=total_prod_icon, bg='#8e44ad')
total_prod_icon_Label.pack(pady=10)

total_prod_Label = Label(prod_frame, text='Total Products', bg='#8e44ad', fg='white', font=('times new roman', 15, 'bold'))
total_prod_Label.pack()

total_prod_count_Label = Label(prod_frame, text='0', bg='#8e44ad', fg='white', font=('times new roman', 15, 'bold'))
total_prod_count_Label.pack()

#===Sales Frame===
sales_frame = Frame(window, bg='#ff0000', bd=3, relief=RIDGE)
sales_frame.place(x=650, y=570, height=200, width=400)

total_sales_icon = PhotoImage(file='total_sales.png')
total_sales_icon_Label = Label(sales_frame, image=total_sales_icon, bg='#ff0000')
total_sales_icon_Label.pack(pady=10)

total_sales_Label = Label(sales_frame, text='Total Sales', bg='#ff0000', fg='white', font=('times new roman', 15, 'bold'))
total_sales_Label.pack()

total_sales_count_Label = Label(sales_frame, text='0', bg='#ff0000', fg='white', font=('times new roman', 15, 'bold'))
total_sales_count_Label.pack()

update()

window.mainloop()