
# Python3 code to demonstrate working of
# Validate String date format
# Using strptime()
from datetime import datetime,date
test_str = '28-10-2021'
print("The original string is : " + str(test_str))
format = "%d-%m-%Y"
res = True
try:
    res = bool(datetime.strptime(test_str, format))
except ValueError:
    res = False
print("Does date match format? : " + str(res))

today = date.today()
today = today.strftime("%d-%m-%Y")
d1= datetime.strptime(test_str, format)
d2= datetime.strptime(today, format)
print(today, test_str)
print(d1>=d2)