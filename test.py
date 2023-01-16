from datetime import datetime, date 

dt = datetime(2023, 1, 16)

print(dt.strftime('%A'))
today = date.today()
todays_date = today.strftime("%B %d, %Y")
print(todays_date)