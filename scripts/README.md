# Prayer Times CSV Formatter and JSON Converter

This repository contains two Python scripts for processing prayer times data:

- [```csv-formatter.py```](#csv-formatterpy) - Formats raw prayer times CSV data into a standardized format

- [```csv-to-json.py```](#csv-to-jsonpy) - Converts formatted CSV data into organized JSON structure

# Prerequisites

- Python 3.6+

- Required packages: ```pandas```

# Install dependencies:

```py
pip install pandas
```
or 

```py
pip install -r req
```

# Scripts Overview

## ```csv-formatter.py```

This script takes raw prayer times data and formats it with consistent date formatting and 24-hour time format.
    
Input **CSV Format** (Raw Data)

Your input CSV should have the following structure (if gotten directly from [data.gov.sg](https://data.gov.sg/)):

```
Date,Day,Subuh,Syuruk,Zohor,Asar,Maghrib,Isyak
2024-01-01,Mon,5 44,07 07,1 10,4 34,7 10,8 25
2024-01-02,Tues,5 44,07 08,1 10,4 34,7 11,8 26
2024-01-03,Wed,5 45,07 08,1 11,4 35,7 11,8 26
```

**Accepted Input Formats:**

- **Dates**: ```yyyy-mm-dd```, ```d-m-yyyy```, or ```dd-m-yyyy```

- **Times**:

    - **Space-separated**: ```"5 44"```, ```"07 07"```

    - **Concatenated**: ```"544"```, ```"0707"```

- **Afternoon prayers** (Zohor, Asar, Maghrib, Isyak) should be in 12-hour format

**Output CSV Format**

The script converts the data to:

```
Date,Day,Subuh,Syuruk,Zohor,Asar,Maghrib,Isyak
01-01-2024,Mon,0544,0707,1310,1634,1910,2025
02-01-2024,Tues,0544,0708,1310,1634,1911,2026
03-01-2024,Wed,0545,0708,1311,1635,1911,2026
```

**Output Features:**

- **Dates**: Always ```dd-mm-yyyy``` format

- **Times**: 4-digit 24-hour format with leading zeros

- **Morning prayers (Subuh, Syuruk)**: Kept as ```AM``` times

- **Afternoon prayers**: Converted from ```12-hour``` to ```24-hour``` format by adding 12 hours

**Usage**

1. Update the file paths in the script:

```py
input_filename = "../2025/csv/prayer_times_2025.csv"  # The input file or file path
output_filename = "Expected.csv"  # The desired output file
```

2. Run the script:

```py
python csv-formatter.py
```

## ```csv-to-json.py```

This script converts the formatted CSV data into a structured JSON file organized by months.

**Input CSV Format** (Must use **formatted CSV** from csv-formatter.py)

Your input CSV should be in this exact format:

```
Date,Day,Subuh,Syuruk,Zohor,Asar,Maghrib,Isyak
01-01-2025,Wed,0543,0707,1309,1633,1910,2025
02-01-2025,Thurs,0544,0707,1310,1634,1910,2025
03-01-2025,Fri,0544,0708,1310,1634,1911,2025
```

**Requirements:**

- **Dates**: Must be in ```dd-mm-yyyy``` format

- **Times**: Must be 4-digit 24-hour format (e.g., ```0543```, ```1309```)

**Output JSON Format**

The script generates JSON with this structure:

```json
{
  "year": 2025,
  "prayer_times": {
    "January": [
      {
        "date": "2025-01-01",
        "day": "Wed",
        "prayers": {
          "subuh": "05:43",
          "syuruk": "07:07",
          "zohor": "13:09",
          "asar": "16:33",
          "maghrib": "19:10",
          "isyak": "20:25"
        }
      }
    ]
  }
}
```

**Output Features:**

- **Year**: Extracted automatically from the first date

- **Organization**: Prayer times grouped by month names

- **Date format**: Converted to ```yyyy-mm-dd```

- **Time format**: ```HH:MM``` with colon separator

**Usage**

1. Update the file paths in the script:

```py
input_csv = "../2025/csv/prayer_times_2025.csv"  # The formatted CSV file or file path
output_json = "Expected.json"  # The desired JSON output file
```

2. Run the script:

```py
python csv-to-json.py
```

# Support

If you encounter issues:

1. Ensure your ```input data``` matches the ```required``` formats

2. Check that all ```required``` columns are ```present```

3. Verify ```file paths``` are correct

4. Check ```Python``` and ```pandas``` are properly installed