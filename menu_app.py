from datetime import datetime

selected_spreadsheet = None


# convertData: applies the conversion formula appropriate for the currently
# selected spreadsheet (temperature, weight, or rainfall) to the given value
# and returns the converted result.
def convertData(data):
    if selected_spreadsheet == "temperature":
        return (data - 32) * 5 / 9
    elif selected_spreadsheet == "weight":
        return data / 2.205
    elif selected_spreadsheet == "rainfall":
        return data * 2.54


# insertData: appends a comma-separated row to the CSV file at the given path,
# creating the file if it does not already exist. Errors during the write are
# caught, reported, and re-raised so the caller can react.
def insertData(file_path, csv_row):
    try:
        with open(file_path, "a") as csv_file:
            csv_file.write(csv_row + "\n")
    except Exception as error:
        print(f"Error writing to {file_path}: {error}")
        raise


# viewData: prints the path of the file being read followed by its contents,
# using read-only permissions and handling any errors during the read.
def viewData(file_path):
    print(f"Reading file: {file_path}")
    try:
        with open(file_path, "r") as csv_file:
            print(csv_file.read())
    except Exception as error:
        print(f"Error reading {file_path}: {error}")


# getInput: prompts the user for a spreadsheet type and a number of entries,
# converts each entry, saves it to ZooData.csv via insertData, and prints a
# confirmation message for every successful write.
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
        try:
            entry_date = input("Enter date: ")
            value = float(input("Enter value: "))
            # convertData: takes the numerical value as its argument and returns the converted value (float) based on the selected spreadsheet type.
            converted = convertData(value)
            data = f"{entry_date},{value},{converted}"
            insertData("ZooData.csv", data)
            print(f"The following data was saved at {datetime.now()}: {data}.")
        except Exception as error:
            print(f"Error processing entry: {error}")


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
    elif option == "2":
        viewData("ZooData.csv")
    else:
        print("Error: The chosen functionality is not implemented yet")
else:
    print("Error: Invalid choice selected.")
