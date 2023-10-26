import openpyxl
import re

os.chdir('C:/Users/lucco/Desktop/emulator project')


# Load the excel file
wb = openpyxl.load_workbook('instructions.xlsx')
sheet = wb.active

# Load the C++ source code file
with open('cpu.cpp', 'r') as f:
    cpp_source = f.readlines()

# Create two lists to store the hex numbers
excel_hex = []
cpp_hex = []

# Get all the hex numbers from the excel file and add them to the 'excel_hex' list
for row in sheet.iter_rows(values_only=True):
    if row[1] != None:
        excel_hex.append(str(row[1]).upper())

# Get all the hex numbers from the C++ source code file and add them to the 'cpp_hex' list
for line in cpp_source:
    line = line.strip()
    if line.startswith("case "):
        line = line[5:].split("//")[0]
        line = line.strip(":")
        cpp_hex.append(line[:-2].upper())

# Compare the two lists and print the hex numbers that aren't matched in the other list
for excel_num in excel_hex:
    if excel_num not in cpp_hex:
        print("Excel hex number not in C++ source code:", excel_num)

for cpp_num in cpp_hex:
    if cpp_num not in excel_hex:
        print("C++ hex number not in Excel file:", cpp_num)
