# Task 2
import csv
import traceback

def read_employees():
    data = {}
    rows = []

    try:
        with open("../csv/employees.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(row)
            data["rows"] = rows
        return data

    except Exception as e:
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        exit(1)
# Required global variable
employees = read_employees()
print(employees) 

# Task 3
def column_index(fieldname):
    return employees["fields"].index(fieldname)
employee_id_column = column_index("employee_id")

# Task 4
def first_name(row_num):
    col = column_index("first_name")
    return employees["rows"][row_num][col]

# Task 5 
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches

# Task 6 
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

# Task 7
def sort_by_last_name():
    last_name_col = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_name_col])
    return employees["rows"]
sort_by_last_name()
print(employees)

# Task 8
def employee_dict(row):
    return {
        key: value
        for key, value in zip(employees["fields"], row)
        if key != "employee_id"
    }
print(employee_dict(employees["rows"][0]))

# Task 9
def all_employees_dict():
    all_emps = {}
    for row in employees["rows"]:
        emp_id = row[employee_id_column]
        all_emps[emp_id] = employee_dict(row)
    return all_emps
print(all_employees_dict())

# Task 10
import os
def get_this_value():
    return os.getenv("THISVALUE")
print(get_this_value()) 

# Task 11
import custom_module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
set_that_secret("new_secret_value")
print(custom_module.secret)  

# Task 12
import csv

def read_csv_to_dict(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        fields = next(reader)
        rows = [tuple(row) for row in reader]
        return {"fields": fields, "rows": rows}
    
def read_minutes():
    m1 = read_csv_to_dict("../csv/minutes1.csv")
    m2 = read_csv_to_dict("../csv/minutes2.csv")
    return m1, m2

minutes1, minutes2 = read_minutes()
print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

#Task 13
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    combined_set = set1.union(set2)
    return combined_set

minutes_set = create_minutes_set()
print("Combined minutes set:", minutes_set)

# Task 14
from datetime import datetime

def create_minutes_list():
    return list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), list(minutes_set)))

minutes_list = create_minutes_list()
print("Minutes List:", minutes_list)

# Task 15
import csv
from datetime import datetime

def write_sorted_list():
    sorted_minutes = sorted(minutes_list, key=lambda x: x[1])
    converted = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), sorted_minutes))
    
    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted)

    return converted

converted_minutes = write_sorted_list()
print("Sorted and converted minutes written to file:")
print(converted_minutes)

