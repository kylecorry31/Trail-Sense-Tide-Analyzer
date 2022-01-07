import datetime

date = datetime.datetime(2021, 1, 1)
frequency = datetime.timedelta(14.77)

print("SPRING")
while date.year == 2021:
    print(date)
    date += frequency

print()

date = datetime.datetime(2021, 1, 8)
print("NEAP")
while date.year == 2021:
    print(date)
    date += frequency
