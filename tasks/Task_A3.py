from datetime import datetime

# Mapping of day names to their weekday numbers.
DAY_MAPPING = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
    "mondays": 0,
    "tuesdays": 1,
    "wednesdays": 2,
    "thursdays": 3,
    "fridays": 4,
    "saturdays": 5,
    "sundays": 6,
}

def count_wednesdays(input_file: str, output_file: str, target_day: str = "wednesday"):
    """
    Count the number of occurrences of a specified weekday in a list of dates and write the result.
    
    Parameters:
      - input_file: File with dates (one per line in "YYYY-MM-DD" format).
      - output_file: File where the count will be written.
      - target_day: The day to count (e.g., "tuesday", "thursday", etc.).
    """
    target_day = target_day.lower()
    if target_day not in DAY_MAPPING:
        raise ValueError(f"Invalid target_day: {target_day}. Must be one of {list(DAY_MAPPING.keys())}.")

    target_index = DAY_MAPPING[target_day]

    with open(input_file, "r", encoding="utf-8") as f:
        dates = f.readlines()

    count = 0
    for date in dates:
        try:
            parsed_date = datetime.strptime(date.strip(), "%Y-%m-%d")
            if parsed_date.weekday() == target_index:
                count += 1
        except ValueError:
            continue  # Skip invalid lines

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(count))
