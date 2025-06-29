import mysql.connector as sql
from config import DB_CONFIG

class EmployeeDB:
    def __init__(self):
        self.config = DB_CONFIG
    
    def connect(self):
        return sql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            auth_plugin=self.config['auth_plugin']
        )
    
    def insert_employee(self, emp_id, name, dept):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO empDetails VALUES (%s, %s, %s)', (emp_id, name, dept))
        conn.commit()
        conn.close()
    
    def update_employee(self, emp_id, name, dept):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE empDetails SET empName=%s, empDept=%s WHERE empID=%s', (name, dept, emp_id))
        conn.commit()
        conn.close()
    
    def delete_employee(self, emp_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM empDetails WHERE empID=%s', (emp_id,))
        conn.commit()
        conn.close()
    
    def get_employee(self, emp_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empDetails WHERE empID=%s", (emp_id,))
        result = cursor.fetchall()
        conn.close()
        return result
    
    def get_all_employees(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM empDetails")
        result = cursor.fetchall()
        conn.close()
        return result
    
    def search_employees(self, search_term):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM empDetails WHERE empName LIKE %s OR empDept LIKE %s",
            (f'%{search_term}%', f'%{search_term}%')
        )
        result = cursor.fetchall()
        conn.close()
        return result