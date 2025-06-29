from tkinter import *
from tkinter import messagebox
import csv
import re
import mysql.connector
from employee_db import EmployeeDB
from config import APP_CREDENTIALS, DB_CONFIG

def validate_input(emp_id, name, dept):
    if not emp_id.isdigit():
        messagebox.showwarning("Invalid Input", "Employee ID must be a number!")
        return False
    if not re.match(r'^[A-Za-z\s]+$', name):
        messagebox.showwarning("Invalid Input", "Name must contain only letters and spaces!")
        return False
    if not re.match(r'^[A-Za-z\s]+$', dept):
        messagebox.showwarning("Invalid Input", "Department must contain only letters and spaces!")
        return False
    return True

class EmployeeApp:
    def __init__(self, master):
        self.master = master
        master.geometry("700x350")
        master.title("Employee CRUD App")
        self.db = EmployeeDB()

        # GUI elements
        Label(master, text="Employee ID", font=("Serif",12)).place(x=40,y=40)
        Label(master, text="Employee Name", font=("Serif",12)).place(x=40,y=90)
        Label(master, text="Employee Dept", font=("Serif",12)).place(x=40,y=140)
        Label(master, text="Search", font=("Serif",12)).place(x=40, y=300)

        self.enterID = Entry(master)
        self.enterID.place(x=180,y=40)
        self.enterName = Entry(master)
        self.enterName.place(x=180,y=90)
        self.enterDept = Entry(master)
        self.enterDept.place(x=180,y=140)
        self.searchEntry = Entry(master)
        self.searchEntry.place(x=180, y=300)

        # Buttons
        Button(master, text="Insert", command=self.insertData).place(x=40,y=200)
        Button(master, text="Update", command=self.updateData).place(x=130,y=200)
        Button(master, text="Fetch", command=self.getData).place(x=220,y=200)
        Button(master, text="Delete", command=self.deleteData).place(x=310,y=200)
        Button(master, text="Reset", command=self.resetFields).place(x=450,y=300)
        Button(master, text="Search", command=self.searchData).place(x=340,y=300)
        Button(master, text="Export CSV", command=self.exportCSV).place(x=540,y=300)

        # Listbox
        self.showData = Listbox(master, width=40, height=15)
        self.showData.place(x=400,y=30)
        self.show()

    def insertData(self):
        emp_id = self.enterID.get()
        name = self.enterName.get()
        dept = self.enterDept.get()
        if not all([emp_id, name, dept]):
            messagebox.showwarning("Error", "All fields are required!")
            return
        if not validate_input(emp_id, name, dept):
            return
        try:
            self.db.insert_employee(emp_id, name, dept)
            messagebox.showinfo("Success", "Data Inserted")
            self.show()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            self.resetFields()

    def updateData(self):
        emp_id = self.enterID.get()
        name = self.enterName.get()
        dept = self.enterDept.get()
        if not all([emp_id, name, dept]):
            messagebox.showwarning("Error", "All fields are required!")
            return
        if not validate_input(emp_id, name, dept):
            return
        try:
            self.db.update_employee(emp_id, name, dept)
            messagebox.showinfo("Success", "Data Updated")
            self.show()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            self.resetFields()

    def getData(self):
        emp_id = self.enterID.get()
        if not emp_id:
            messagebox.showwarning("Error", "Employee ID is required!")
            return
        try:
            result = self.db.get_employee(emp_id)
            if result:
                emp = result[0]
                self.enterName.delete(0, END)
                self.enterName.insert(0, emp[1])
                self.enterDept.delete(0, END)
                self.enterDept.insert(0, emp[2])
                self.showData.delete(0, END)
                self.showData.insert(END, f"{emp[0]} {emp[1]} {emp[2]}")
            else:
                messagebox.showinfo("Not Found", "Employee not found")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def deleteData(self):
        emp_id = self.enterID.get()
        if not emp_id:
            messagebox.showwarning("Error", "Employee ID is required!")
            return
        try:
            self.db.delete_employee(emp_id)
            messagebox.showinfo("Success", "Data Deleted")
            self.show()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            self.resetFields()

    def searchData(self):
        search_term = self.searchEntry.get()
        if not search_term:
            self.show()
            return
        try:
            results = self.db.search_employees(search_term)
            self.showData.delete(0, END)
            for emp in results:
                self.showData.insert(END, f"{emp[0]} {emp[1]} {emp[2]}")
            if not results:
                self.showData.insert(END, "No results found")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def exportCSV(self):
        try:
            with open('employees.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['ID', 'Name', 'Department'])
                employees = self.db.get_all_employees()
                for emp in employees:
                    writer.writerow([emp[0], emp[1], emp[2]])
            messagebox.showinfo("Success", "Data exported to employees.csv")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def show(self):
        try:
            employees = self.db.get_all_employees()
            self.showData.delete(0, END)
            for emp in employees:
                self.showData.insert(END, f"{emp[0]} {emp[1]} {emp[2]}")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def resetFields(self):
        self.enterID.delete(0, END)
        self.enterName.delete(0, END)
        self.enterDept.delete(0, END)
        self.searchEntry.delete(0, END)
        self.show()

def main_window():
    root = Tk()
    EmployeeApp(root)
    root.mainloop()

def login():
    def check_login():
        if (userEntry.get() == APP_CREDENTIALS['username'] and 
            pwdEntry.get() == APP_CREDENTIALS['password']):
            loginWindow.destroy()
            main_window()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    loginWindow = Tk()
    loginWindow.title("Login")
    loginWindow.geometry("300x150")
    Label(loginWindow, text="Username:").place(x=20, y=30)
    Label(loginWindow, text="Password:").place(x=20, y=60)
    userEntry = Entry(loginWindow)
    userEntry.place(x=100, y=30)
    pwdEntry = Entry(loginWindow, show='*')
    pwdEntry.place(x=100, y=60)
    Button(loginWindow, text="Login", command=check_login, width=10).place(x=120, y=100)
    loginWindow.mainloop()

if __name__ == "__main__":
    login()