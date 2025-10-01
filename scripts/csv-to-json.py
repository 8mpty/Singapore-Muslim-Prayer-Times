import pandas as pd
import json
from datetime import datetime

def csv_to_json(csv_file, json_file):
    """
    Convert CSV prayer times to JSON format with month-wise organization
    """
    df = pd.read_csv(csv_file, dtype=str)
    
    # Extract year from the first date
    first_date = df.iloc[0]['Date']
    year = datetime.strptime(first_date, '%d-%m-%Y').year
    
    json_data = {
        "year": year,
        "prayer_times": {}
    }
    
    # Month names mapping
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }
    
    def add_colon_to_time(time_str):
        """
        Simply add colon to time string: '0543' -> '05:43'
        """
        time_str = str(time_str).strip()
        
        # Pad with leading zero if needed (for 3-digit times)
        if len(time_str) == 3:
            time_str = '0' + time_str
        
        if len(time_str) == 4:
            return f"{time_str[:2]}:{time_str[2:]}"
        return time_str
    
    def convert_date_format(date_str):
        """
        Convert date from 'dd-mm-yyyy' to 'yyyy-mm-dd' format
        """
        try:
            date_obj = datetime.strptime(date_str, '%d-%m-%Y')
            return date_obj.strftime('%Y-%m-%d')
        except:
            return date_str
    
    for index, row in df.iterrows():
        original_date = row['Date']
        formatted_date = convert_date_format(original_date)
        
        # Extract month from the date
        date_obj = datetime.strptime(original_date, '%d-%m-%Y')
        month_num = date_obj.month
        month_name = month_names[month_num]
        
        # Create the day entry
        day_entry = {
            "date": formatted_date,
            "day": row['Day'],
            "prayers": {
                "subuh": add_colon_to_time(row['Subuh']),
                "syuruk": add_colon_to_time(row['Syuruk']),
                "zohor": add_colon_to_time(row['Zohor']),
                "asar": add_colon_to_time(row['Asar']),
                "maghrib": add_colon_to_time(row['Maghrib']),
                "isyak": add_colon_to_time(row['Isyak'])
            }
        }
        
        # Initialize the month array if it doesn't exist
        if month_name not in json_data['prayer_times']:
            json_data['prayer_times'][month_name] = []
        
        # Add the day entry to the appropriate month
        json_data['prayer_times'][month_name].append(day_entry)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON file saved as: {json_file}")
    
    # Display summary
    print(f"\nConversion Summary:")
    print(f"Year: {year}")
    print(f"Months processed: {list(json_data['prayer_times'].keys())}")
    for month, days in json_data['prayer_times'].items():
        print(f"  {month}: {len(days)} days")
    
    return json_data

def validate_json_structure(json_data):
    """
    Validate the JSON structure and display a sample
    """
    print("\nSample of JSON structure:")
    first_month = list(json_data['prayer_times'].keys())[0]
    first_entry = json_data['prayer_times'][first_month][0]
    
    print(json.dumps({
        "year": json_data['year'],
        "prayer_times": {
            first_month: [first_entry]
        }
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    input_csv = "../2024/csv/prayer_times_2024.csv"
    output_json = "Expected.json"
    
    try:
        # Convert CSV to JSON
        result_json = csv_to_json(input_csv, output_json)
        
        # Validate and show sample structure
        validate_json_structure(result_json)
        
        print(f"\nSuccessfully converted {input_csv} to {output_json}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_csv}' not found. Please make sure it exists.")
    except Exception as e:
        print(f"An error occurred: {e}")