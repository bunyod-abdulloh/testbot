import time
from datetime import datetime

first_time = datetime.now()
time.sleep(2)
later_time = datetime.now()

difference = later_time - first_time
print(first_time)
# minutes, seconds = divmod(difference.total_seconds(), 60)

# print(f"Time difference: {minutes} minutes, {seconds} seconds")
# time.sleep(5)
# first_times = datetime.datetime.now()
# time.sleep(6)
# later_times = datetime.datetime.now()
#
# differences = later_times - first_times
#
# minutess, secondss = divmod(differences.total_seconds(), 60)
#
# print(f"Time difference: {minutess} minutes, {secondss} seconds")
#
# print(difference)
#
# if difference < differences:
#     print("natija")
