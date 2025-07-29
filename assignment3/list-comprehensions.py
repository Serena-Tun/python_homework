# Task 3: List Comprehensions Practice

import csv

# Read CSV into a list of lists
with open("../csv/employees.csv", "r") as file:
    reader = csv.reader(file)
    data = list(reader)

# Skip header and join first + last names
full_names = [row[0] + " " + row[1] for row in data[1:]]
print("All full names:", full_names)

# Filter names that contain 'e'
names_with_e = [name for name in full_names if 'e' in name.lower()]
print("Names with 'e':", names_with_e)

