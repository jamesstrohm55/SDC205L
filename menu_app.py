from datetime import datetime

selected_spreadsheet = None


def convertData(data):
    if selected_spreadsheet == "temperature":
        return (data - 32) * 5 / 9
    elif selected_spreadsheet == "weight":
        return data / 2.205
    elif selected_spreadsheet == "rainfall":
        return data * 2.54


def getInput():
    global selected_spreadsheet
    print("Select spreadsheet type:")
    print("1. Temperature (F to C)")
    print("2. Weight (lbs to Kg)")
    print("3. Rainfall (in to cm)")
    sheet_choice = input("Selection: ")
    spreadsheet_map = {"1": "temperature", "2": "weight", "3": "rainfall"}
    selected_spreadsheet = spreadsheet_map.get(sheet_choice)

    entry_count = int(input("How many entries are being entered? "))
    for _ in range(entry_count):
        entry_date = input("Enter date: ")
        value = float(input("Enter value: "))
        # convertData: takes the numerical value as its argument and returns the converted value (float) based on the selected spreadsheet type.
        converted = convertData(value)
        print(f"The following was saved at {datetime.now()}:")
        print(entry_date, value, converted)


print("jamstr4441 Spreadsheet Automation Menu.")

menu_options = ["Input Data", "View Current Data", "Generate Report"]

for number, label in enumerate(menu_options, start=1):
    print(f"{number}. {label}")

# The next line retrieves the inputted option and stores into the variable called option.
option = input("Select an option: ")

if option.isdigit() and 1 <= int(option) <= len(menu_options):
    print("You selected option", option)
    print("the time and date is", str(datetime.now()))
    if option == "1":
        getInput()
    else:
        print("Error: The chosen functionality is not implemented yet")
else:
    print("Error: Invalid choice selected.")
