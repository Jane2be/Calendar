from datetime import datetime, date, timedelta
import csv

today = datetime.now()
today_key = today.strftime("%d-%m-%Y")

def read_file():
    reminders = {}
    try:
        with open("reminders.csv") as my_file:
            for line in csv.reader(my_file, delimiter=";"):
                reminders[line[0]] = line[1:]
    except FileNotFoundError:
        with open("reminders.csv", "w") as my_file:
            pass
    return reminders
reminders = read_file()

try:
    entries = reminders[today_key]
except KeyError:
    entries = []
if len(entries) == 1:
    print(f"Hello! You have {len(entries)} reminder today.")
else:
    print(f"Hello! You have {len(entries)} reminders today.")
if len(entries) > 0:
    print("1 - read")
print("2 - continue")
print("0 - exit")

def check_command():
    if int(command) == 1:
        print_today()

    elif int(command) == 2:
        help()

    elif int(command) == 3:
        print_month()

    elif int(command) == 4:
        print_week()

    elif int(command) == 5:
        add_reminder()

    elif int(command) == 6:
        find_date()

    elif int(command) == 7:
        find_reminder()

    else:
        print("Unknown command. Try again.")

def print_today():
    print(f"Your reminders for {today.strftime('%A, %d %B %Y')}:")
    if len(entries) == 0:
        print("You have no reminders for today.")
    else:
        for entry in entries:
            print(f"  • {entry}")

def help():
        print("Commands:")
        print("1 - read today's reminders")
        print("2 - list of commands")
        print("3 - print month")
        print("4 - print week")
        print("5 - add a reminder")
        print("6 - find by date")
        print("7 - find by keyword")
        print("0 - exit")

def print_month():
    month, year = 13, "a"
    while month > 12 or month < 0:
        try:
            month = int(input("Inuput month in a number format. For this month input 0: "))
            if month > 12 or month < 0:
                print("Sorry, wrong format. Try again.")
        except ValueError:
            print("Sorry, wrong format. Try again.")
    while year == "a" and month != 0:
        try:
            year = int(input("Inuput year in a number format: "))
        except ValueError:
            print("Sorry, wrong format. Try again.")
    if month == 0:
        month, year = int(today.strftime("%m")), int(today.strftime("%Y"))

    i = date(year, month, 1).weekday() #Mon = 0
    next_month = 0
    next_year = 0
    if month == 12:
        next_month = 1
        next_year = year+1
    else:
        next_month = month+1
        next_year = year
    last_day = date(next_year, next_month, 1) - timedelta(days=1)
    length = int(last_day.day)
    
    month_print = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]

    row = 0
    for day in range(1, length+1):
        if len(str(day)) == 1:
            day = f"0{day}" 
        check = f"{day}-{month}-{year}"
        if check_date(check):
            month_print[row][i] = f"{day}*"
        else:
            month_print[row][i] = day
        i += 1
        if i == 7:
            i = 0
            row += 1
      
    dt = datetime(2000, month, 1)
    month_name = dt.strftime('%B')
    print()
    print(month_name, year)
    print("Mon  Tue  Wed  Thu  Fri  Sat  Sun")
    for week in month_print:
        for day in week:
            if day == 0:
                day = " "
            if len(str(day)) == 1:
                day = " " + str(day)
            print(f"{day:<3}  ", end="")
        print()
    print("* - reminders")

def print_week():
    week, year = 60, "a"
    while week > 52 or week < 0:
        try:
            week = int(input("Inuput week in a number format. For this week input 0: "))
            if week > 52 or week < 0:
                print("Sorry, wrong format. Try again.")
        except ValueError:
            print("Sorry, wrong format. Try again.")
    while year == "a" and week != 0:
        try:
            year = int(input("Inuput year in a number format: "))
        except ValueError:
            print("Sorry, wrong format. Try again.")
    if week == 0:
        week, year = today.strftime("%U"), today.strftime("%Y")

    start_of_week = datetime.strptime(f"{year}-W{week}-1", "%Y-W%W-%w")
    print()
    print(f"Week {week}:")
    for i in range(7):
        current_day = start_of_week + timedelta(days=i)
        check = current_day.strftime("%d-%m-%Y")
        if check_date(check):
            print(f"{current_day.strftime('%a %d %b, %Y')}*")
        else:
            print(current_day.strftime('%a %d %b, %Y'))
    print("* - reminders")

def add_reminder():
    while True:
        entry_date = input("Input the date in 'dd-mm-yyyy' format:")
        try:
            datetime.strptime(entry_date, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date format. Please try again.")
    entry = str(input("Input the reminder:"))

    global reminders
    if entry_date not in reminders:
        reminders[entry_date] = []
    reminders[entry_date].append(entry)
    
    with open("reminders.csv", "w") as my_file:
        for key, values in reminders.items():
            values_str = ";".join(values)
            my_file.write(f"{key};{values_str}\n")

    print("The reminder added.")

def check_date(entry_date):
    global reminders
    parts = entry_date.split("-")
    day = parts[0]
    month = parts[1]
    year = parts[2]
    if len(str(day)) == 1:
        day = f"0{day}" 
    if len(str(month)) == 1:
        month = f"0{month}"
    entry_date = f"{day}-{month}-{year}"
    return entry_date in reminders

def find_date():
    while True:
        entry_date = input("Input the date in 'dd-mm-yyyy' format:")
        try:
            datetime.strptime(entry_date, "%d-%m-%Y")
            break
        except ValueError:
            print("Invalid date format. Please try again.")
    print_date = datetime.strptime(entry_date, '%d-%m-%Y')
    if check_date(entry_date):
        print(f"Your reminders for {print_date.strftime('%A, %d %B %Y')}:")
        for reminder in reminders[entry_date]:
            print(reminder)
        if print_date > today:
            days_until = (print_date - today).days + 1
            if days_until == 1:
                print("It's 1 day until this date.")
            elif days_until > 1:
                print(f"It's {days_until} days until this date.")
        elif print_date < today:
            days_until = (today - print_date).days
            if days_until == 1:
                print("It was 1 day ago.")
            elif days_until > 1:
                print(f"It was {days_until} days ago.")
    else:
        print(f"You have 0 reminders for {print_date.strftime('%A, %d %B %Y')}.")

def find_reminder():
    global reminders
    entry = input("Input a key word:")
    found = [(key, value) for key, values in reminders.items() for value in values if entry in value]
    if found:
        for key, value in found:
            print_key = datetime.strptime(key, '%d-%m-%Y')
            print(f"{print_key.strftime('%A, %d %B %Y')}: {value}")
    else:
        print(f"No match found for {entry}")

while True:
    try:
        print()
        command = int(input("command: "))
        if command == 0:
            print("Shutting down...")
            break
        check_command()
    except ValueError:
        print("Unknown command. Try again.")
