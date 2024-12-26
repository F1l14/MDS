# Helper Functions

# Function to convert a date string to a number
def date_to_number(date_str):
    # Mapping of month names to their numeric values
    month_mapping = {
        "January": "01", "February": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "September": "09", "October": "10", "November": "11", "December": "12"
    }
    
    # Split the input into the month and year parts
    month_name, year = date_str.split()
    
    # Get the numeric month from the mapping
    numeric_month = month_mapping.get(month_name)
    
    # Return the formatted four-digit number
    return int(year + numeric_month)

# Function to get a valid numeric input within the specified range
def get_valid_input(prompt, min_val, max_val):
    while True:
        value = input(prompt)
        if value.replace('.', '', 1).isdigit():
            value = float(value)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Value out of bounds. Please enter a value between {min_val} and {max_val}.")
        else:
            print("Invalid input. Please enter a numeric value.")