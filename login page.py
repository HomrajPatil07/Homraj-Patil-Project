from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pymysql
import os
import email_pass
import smtplib
import time
import socket

class Login_System:
    def __init__(self, window):
        self.window = window
        self.window.title("Login System | Developed By Homraj | Webcode")
        self.window.geometry("1530x800+0+0")
        self.window.config(bg="#fafafa")

        self.otp = ''

        # =====images=====
        self.phone_image = ImageTk.PhotoImage(file="phone.png")
        self.label_Phone_image = Label(self.window, image=self.phone_image, bd=0).place(x=250, y=80)

        # ====Login Frame====
        self.employee_id = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.window, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=700, y=110, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white").place(x=0, y=30, relwidth=1)

        label_user = Label(login_frame, text="Employee ID", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=100)

        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=140, width=250)

        label_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC").place(x=50, y=240, width=250)

        button_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15), bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white", cursor="hand2").place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold")).place(x=150, y=355)

        button_forget = Button(login_frame, text="Forget Password?", command=self.forget_window, font=("times new roman", 13), bg="white", fg="#00759E", bd=0, activebackground="white", activeforeground="#00759E").place(x=100, y=390)

        # =====Frame2====
        register_frame = Frame(self.window, bd=2, relief=RIDGE, bg="white")
        register_frame.place(x=700, y=585, width=350, height=60)

        label_register = Label(register_frame, text="HP 07", font=("times new roman", 13), bg="white").place(x=0, y=17, relwidth=1)

        # ====Animation Images===
        self.im1 = ImageTk.PhotoImage(file="im1.png")
        self.im2 = ImageTk.PhotoImage(file="im2.png")
        self.im3 = ImageTk.PhotoImage(file="im3.png")

        self.label_change_image = Label(self.window, bg="white")
        self.label_change_image.place(x=417, y=183, width=240, height=428)

        self.animate()

    # =======All Functions========
    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.label_change_image.config(image=self.im)
        self.label_change_image.after(2000, self.animate)  # Pass the function reference, not the function call

    def login(self):
        try:
            # Connect to MySQL database
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="homraj07",
                database="inventory_system"
            )
            cur = conn.cursor()

            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.window)
            else:
                # Use parameterized query to avoid SQL injection
                cur.execute('SELECT usertype FROM employee_data WHERE empid=%s AND password=%s',
                            (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror('Error', "Invalid USERNAME/PASSWORD", parent=self.window)
                else:
                    print(user)
                    if user[0] == "Admin":
                        self.window.destroy()
                        os.system("python Dashboard.py")
                    else:
                        self.window.destroy()
                        os.system("python billing.py")

        except pymysql.Error as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.window)
        finally:
            if conn:
                conn.close()

    def forget_window(self):
        try:
            # Connect to MySQL database
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="homraj07",
                database="inventory_system"
            )
            cur = conn.cursor()
            if self.employee_id.get() == "":
                messagebox.showerror('Error', "Employee ID must be required", parent=self.window)
            else:
                # Use parameterized query to avoid SQL injection
                cur.execute('SELECT email FROM employee_data WHERE empid=%s', (self.employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror('Error', "Invalid Employee ID, try again", parent=self.window)
                else:
                    # ====Forget Window====
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # call send_email_function()
                    chk = self.send_email(email[0])
                    if chk != 's':
                        messagebox.showerror("Error", "Connection Error, try again", parent=self.window)
                    else:
                        self.forget_win = Toplevel(self.window)
                        self.forget_win.title('RESET PASSWORD')
                        self.forget_win.geometry('400x350+500+100')
                        self.forget_win.focus_force()

                        title = Label(self.forget_win, text='Reset Password', font=('goudy old style', 15, 'bold'), bg="#3f51b5", fg="white").pack(side=TOP, fill=X)
                        label_reset = Label(self.forget_win, text='Enter OTP Sent on Registered Email', font=('times new roman', 15, 'bold')).place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=('times new roman', 15, 'bold'), bg='lightyellow').place(x=20, y=100, width=250, height=30)

                        self.button_reset = Button(self.forget_win, text="SUBMIT",command=self.validate_otp, font=('times new roman', 15, 'bold'), bg='lightblue')
                        self.button_reset.place(x=280, y=100, width=100, height=30)

                        label_new_pass = Label(self.forget_win, text='New Password', font=('times new roman', 15, 'bold')).place(x=20, y=160)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=('times new roman', 15, 'bold'), bg='lightyellow').place(x=20, y=190, width=250, height=30)

                        label_conf_pass = Label(self.forget_win, text='Confirm Password', font=('times new roman', 15, 'bold')).place(x=20, y=225)
                        txt_conf_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=('times new roman', 15, 'bold'), bg='lightyellow').place(x=20, y=255, width=250, height=30)

                        self.button_update = Button(self.forget_win, text="Update",command=self.update_password, state=DISABLED, font=('times new roman', 15, 'bold'), bg='lightblue')
                        self.button_update.place(x=150, y=300, width=100, height=30)

        except pymysql.Error as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.window)

    def update_password(self):
        if self.var_new_pass.get()=="" or self.var_conf_pass.get()=="":
            messagebox.showerror("Error","Password is required",parent=self.forget_win)
        elif self.var_new_pass.get()!=self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password & confirm password should be same", parent=self.forget_win)
        else:
            try:
                # Connect to MySQL database
                conn = pymysql.connect(
                    host="localhost",
                    user="root",
                    password="homraj07",
                    database="inventory_system"
                )
                cur = conn.cursor()
                cur.execute("Update employee_data SET password=%s where empid=%s",(self.var_new_pass.get(),self.employee_id.get()))
                conn.commit()
                messagebox.showinfo("Success","Password updated sucessfully",parent=self.forget_win)
                self.forget_win.destroy()

            except pymysql.Error as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.window)

    def validate_otp(self):
        if int(self.otp)==int(self.var_otp.get()):
            self.button_update.config(state=NORMAL)
            self.button_reset.config(state=DISABLED)
        else:
            messagebox.showerror("Error","Invalid OTP, Try again", parent=self.forget_win)

    def send_email(self, to_):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            email_ = email_pass.email_
            pass_ = email_pass.pass_

            s.login(email_, pass_)

            self.otp = int(time.strftime("%H%M%S")) + int(time.strftime("%S"))

            subj = 'IMS-Reset Password'
            msg = f'Dear Sir/Madam,\n\nYour Reset OTP is {str(self.otp)}.\nwith Regards,\nHP07 Team'
            msg = "Subject:{}\n\n{}".format(subj, msg)
            s.sendmail(email_, to_, msg)
            chk = s.ehlo()
            if chk[0] == 250:
                return 's'
            else:
                return 'f'
        except smtplib.SMTPException as e:
            messagebox.showerror("SMTP Error", f"SMTP error occurred: {str(e)}", parent=self.window)
            return 'f'
        except socket.gaierror as e:
            messagebox.showerror("Connection Error", f"Failed to connect to the server, Please connect with internet: {str(e)}", parent=self.window)
            return 'f'
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.window)
            return 'f'
        finally:
            if 's' in locals():
                s.quit()

window = Tk()
obj = Login_System(window)
window.mainloop()