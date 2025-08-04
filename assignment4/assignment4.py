import pandas as pd
import json
#task1

# Step 1: Create the original DataFrame
data = {
   'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
task1_data_frame = pd.DataFrame(data)
print("Original DataFrame:")
print(task1_data_frame)

# Step 2: Add a Salary column
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print("\nDataFrame with Salary column:")
print(task1_with_salary)

# Step 3: Modify Age column
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print("\nDataFrame with incremented Age:")
print(task1_older)

# Step 4: Save to CSV
task1_older.to_csv('employees.csv', index=False)
print("\nDataFrame saved to 'employees.csv'")

# Task 2 Step 1: Read data from a csv file 
task2_employees = pd.read_csv('employees.csv')
print("\nLoaded DataFrame from CSV (task2_employees):")
print(task2_employees)

# Task 2 Step 2: Create the JSON file 

additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as json_file:
    json.dump(additional_employees, json_file, indent=4)

# Load JSON file into DataFrame
json_employees = pd.read_json('additional_employees.json')
print("\nLoaded DataFrame from JSON (json_employees):")
print(json_employees)

# Task 2 Step 3: Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print("\nCombined DataFrame (more_employees):")
print(more_employees)
#------

# Task 3 Step 1: Use the head() method:
first_three = more_employees.head(3)
print("\nFirst three rows (first_three):")
print(first_three)

# Task 3 Step 2: Use the tail()method 
last_two = more_employees.tail(2)
print("\nLast two rows (last_two):")
print(last_two)

# Task 3 Step 3: Get the shape of a DataFrame
employee_shape = more_employees.shape
print("\nShape of the DataFrame (employee_shape):")
print(employee_shape)

# Task 3 Step 4: Use the info()method:
print("\nDataFrame info:")
more_employees.info()

#Task 4

# Load the dirty data CSV into dirty_data DataFrame
dirty_data = pd.read_csv('assignment4/dirty_data.csv')
print("\nDirty Data:")
print(dirty_data)

# Create a copy for cleaning
clean_data = dirty_data.copy()

# 1. Remove duplicates 
clean_data.drop_duplicates(inplace=True)
print("\nAfter removing duplicates:")
print(clean_data)

# 2. Convert Age to numeric 
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print("\nAfter converting Age to numeric:")
print(clean_data)

# 3. Replace 'unknown' and 'n/a' in Salary with NaN, then convert to numeric
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], pd.NA)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
print("\nAfter cleaning and converting Salary:")
print(clean_data)

# 4. Fill missing numeric values
clean_data['Age'].fillna(clean_data['Age'].mean(), inplace=True)
clean_data['Salary'].fillna(clean_data['Salary'].median(), inplace=True)
print("\nAfter filling missing Age and Salary:")
print(clean_data)

# Convert Hire Date to datetime (keep NaT)
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], errors='coerce')
# Fill missing Hire Date with placeholder date so no NaT remain
clean_data['Hire Date'] = clean_data['Hire Date'].fillna(pd.Timestamp('1900-01-01'))
print("\nAfter converting and filling Hire Date:")
print(clean_data)

# 6. Strip whitespace and standardize Name and Department to uppercase
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print("\nAfter cleaning Name and Department:")
print(clean_data)















