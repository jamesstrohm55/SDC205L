from datetime import datetime

print("jamstr4441 Spreadsheet Automation Menu.")

menu_options = ["Input Data", "View Current Data", "Generate Report"]

for number, label in enumerate(menu_options, start=1):
    print(f"{number}. {label}")

# The next line retrieves the inputted option and stores into the variable called option.
option = input("Select an option: ")

if option.isdigit() and 1 <= int(option) <= len(menu_options):
    print("You selected option", option)
    print("the time and date is", str(datetime.now()))
else:
    print("Error: Invalid choice selected.")
