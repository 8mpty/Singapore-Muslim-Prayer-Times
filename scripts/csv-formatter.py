import pandas as pd
from datetime import datetime

def format_prayer_times(input_file, output_file):
    """
    Format CSV prayer times data with proper date format and 24hr time formatting
    """
    df = pd.read_csv(input_file)
    
    def format_time(time_str, prayer_name):
        """
        Convert time string to proper 24hr format with leading zeros
        For morning prayers (Subuh, Syuruk): keep as is
        For afternoon prayers (Zohor, Asar, Maghrib, Isyak): add 12 hours for PM times
        Handles both "5 43" and "543" formats
        """
        if pd.isna(time_str):
            return ""
        
        time_str = str(time_str).strip()
        
        # Handle different input formats
        if ' ' in time_str:
            # Format: "5 43" or "07 07"
            parts = time_str.split()
            if len(parts) != 2:
                return time_str
            hour, minute = parts
        else:
            # Format: "543" or "707"
            if len(time_str) == 3:
                # Format: "543" -> hour="5", minute="43"
                hour = time_str[0]
                minute = time_str[1:3]
            elif len(time_str) == 4:
                # Format: "0707" -> hour="07", minute="07"
                hour = time_str[0:2]
                minute = time_str[2:4]
            else:
                return time_str
        
        try:
            hour_int = int(hour)
            minute_int = int(minute)
        except ValueError:
            return time_str
        
        # For afternoon prayers, add 12 hours to convert to 24hr format
        if prayer_name in ['Zohor', 'Asar', 'Maghrib', 'Isyak']:
            # Only add 12 hours if it's PM time (typically 1-12)
            if hour_int < 12:
                hour_int += 12
        
        # Format hour and minute with leading zeros (eg. 534 to 0534, 746 to 0746)
        hour_str = str(hour_int).zfill(2)
        minute_str = str(minute_int).zfill(2)
        
        return f"{hour_str}{minute_str}"
    
    def format_date(date_str):
        """
        Convert date to dd-mm-yyyy format
        Handles both "2024-01-01" and "1-1-2025" formats
        """
        try:
            # Try parsing as yyyy-mm-dd first
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            try:
                # Try parsing as d-m-yyyy or dd-m-yyyy
                if '-' in date_str:
                    parts = date_str.split('-')
                    if len(parts) == 3:
                        day, month, year = parts
                        # Pad single digit day and month with zeros
                        day = day.zfill(2)
                        month = month.zfill(2)
                        date_str = f"{day}-{month}-{year}"
                        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                    else:
                        return date_str
                else:
                    return date_str
            except:
                return date_str
        
        return date_obj.strftime('%d-%m-%Y')

    df['Date'] = df['Date'].apply(format_date)
    df['Subuh'] = df['Subuh'].apply(lambda x: format_time(x, 'Subuh'))
    df['Syuruk'] = df['Syuruk'].apply(lambda x: format_time(x, 'Syuruk'))
    df['Zohor'] = df['Zohor'].apply(lambda x: format_time(x, 'Zohor'))
    df['Asar'] = df['Asar'].apply(lambda x: format_time(x, 'Asar'))
    df['Maghrib'] = df['Maghrib'].apply(lambda x: format_time(x, 'Maghrib'))
    df['Isyak'] = df['Isyak'].apply(lambda x: format_time(x, 'Isyak'))
    
    df.to_csv(output_file, index=False)
    print(f"Formatted CSV saved as: {output_file}")
    
    print("\nFirst 5 rows of formatted data:")
    print(df.head().to_string(index=False))
    
    return df

if __name__ == "__main__":
    input_filename = "../2024/csv/prayer_times_2024.csv"
    output_filename = "Expected.csv"
    
    try:
        result_df = format_prayer_times(input_filename, output_filename)
        print(f"\nSuccessfully converted {input_filename} to {output_filename}")
        
        print("\nSample conversions:")
        sample_data = result_df.head(3)
        for col in ['Subuh', 'Syuruk', 'Zohor', 'Asar', 'Maghrib', 'Isyak']:
            if col in sample_data.columns:
                print(f"{col}: {list(sample_data[col])}")
                
    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found. Please make sure it exists.")
    except Exception as e:
        print(f"An error occurred: {e}")