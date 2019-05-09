import datetime
import pandas as pd

# holidays = pd.read_csv('../additional_data/feiertage.csv')
# holidays.set_index(holidays.Datum)

def day_of_year_to_date(day, year):
    current_date = datetime.datetime(year, 1, 1) + datetime.timedelta(int(day))
    return current_date
