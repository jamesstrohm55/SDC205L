from datetime import datetime

print("jamstr4441 Spreadsheet Automation Menu.")
print("1. Input Data")
print("2. View Current Data")
print("3. Generate Report")

# The next line retrieves the inputted option and stores into the variable called option.
option = input("Select an option: ")

print("You selected option", option)
print("the time and date is", str(datetime.now()))
