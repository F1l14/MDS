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
    
    # Return the formatted number
    return int(year + numeric_month)
