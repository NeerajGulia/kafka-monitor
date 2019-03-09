import datetime

t1 = datetime.datetime(2019, 3, 9, 10, 55, 30, 991882)
t2 = datetime.datetime(2019, 3, 10, 10, 55, 30, 991882)

print((t2-t1).total_seconds())