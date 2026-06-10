from datetime import datetime
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference

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


# createChart: reads the CSV at file_path, asks the user to choose between the
# original or converted data column, then writes the data to final.xlsx and
# embeds a bar or line chart with labelled axes and a title of
# "<student ID> <current date>".
# Arguments:
#   file_path (str): path to the CSV data file
#   chart_type (str): "bar" or "line"
# Returns: None
def createChart(file_path, chart_type):
    unit_map = {
        "temperature": ("Fahrenheit", "Celsius"),
        "weight": ("Pounds", "Kilograms"),
        "rainfall": ("Inches", "Centimeters"),
    }
    original_label, converted_label = unit_map.get(selected_spreadsheet, ("Original Value", "Converted Value"))

    print("Choose data source:")
    print(f"1. {original_label}")
    print(f"2. {converted_label}")
    source_choice = input("Selection: ")

    dates = []
    original_values = []
    converted_values = []
    try:
        with open(file_path, "r") as csv_file:
            for line in csv_file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    dates.append(parts[0])
                    original_values.append(float(parts[1]))
                    converted_values.append(float(parts[2]))
    except Exception as error:
        print(f"Error reading {file_path}: {error}")
        return

    if source_choice == "1":
        values = original_values
        y_label = original_label
    else:
        values = converted_values
        y_label = converted_label

    wb = Workbook()
    ws = wb.active
    ws.title = "Zoo Data"
    ws.append(["Date", y_label])
    for date, value in zip(dates, values):
        ws.append([date, value])

    if chart_type == "bar":
        chart = BarChart()
    else:
        chart = LineChart()

    chart.title = f"jamstr4441 {datetime.now().strftime('%m/%d/%Y')}"
    chart.x_axis.title = "Date"
    chart.y_axis.title = y_label

    data = Reference(ws, min_col=2, min_row=1, max_row=len(values) + 1)
    cats = Reference(ws, min_col=1, min_row=2, max_row=len(dates) + 1)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)

    ws.add_chart(chart, "E2")
    wb.save("final.xlsx")
    print("Chart saved to final.xlsx")


# generateReport: asks the user to choose between a line or bar chart, then
# calls createChart to generate the chart from the CSV data file.
# Arguments:
#   file_path (str): path to the CSV data file
# Returns: None
def generateReport(file_path):
    print("Choose graph type:")
    print("1. Line chart")
    print("2. Bar chart")
    chart_choice = input("Selection: ")
    if chart_choice == "1":
        createChart(file_path, "line")
    elif chart_choice == "2":
        createChart(file_path, "bar")
    else:
        print("Error: Invalid choice selected.")


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
        generateReport("ZooData.csv")
else:
    print("Error: Invalid choice selected.")
