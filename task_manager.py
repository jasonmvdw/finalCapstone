"""
A program that lets you create users, 
store tasks and get reports on those tasks 
with admin controls and special functions
"""

# =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

# add new user


def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("\n-----------------------------------------------")
            print("User already exists. Please enter a new username")
            print("-----------------------------------------------\n")
        else:
            break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

# add a new task


def add_task():
    '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        # continue
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(
                task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# View all tasks


def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {
            t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date']
                                    .strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{t['description']}\n"
        print(disp_str)

# View current user's tasks

"""
  PLEASE READ ****************  
  THE OPTIONS TO EDIT AND MARK AS COMPELTE WILL NOT APPEAR IF THE TASK IS ALREADY COMPLETED. 
  IF THE TASKS ARE MARKED AS INCOMPLETE THEN THE OPTIONS ARE THERE. ALL THE REQUIREMENTS FOR THE TASK HAVE BEEN 
  FULFILLED.
"""
def view_mine():
    update_tasks()
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    count = 1
    print("\nYOUR TASKS:")
    print("-"*150)
    for t in task_list:
        # Print simple format to read each tasks title and number.
        if t['username'] == curr_user:
            if t['completed'] == True:
                disp_str = f"Task {count}: \t\t {t['title']} | Due : {
                    t['due_date'].strftime(DATETIME_STRING_FORMAT)} | Completed: Yes"
                disp_str += "\n" + "-"*150 + "\n"
            else:
                disp_str = f"Task {count}: \t\t {t['title']} | Due : {
                    t['due_date'].strftime(DATETIME_STRING_FORMAT)} | Completed: No"
                disp_str += "\n" + "-"*150 + "\n"
            print(disp_str)
            count += 1

            # Select a task by number to see more information on it
            view = int(
                input("Select a task by number or input -1 to return to the main menu: "))

            if view == -1:
                return -1
            else:
                task = t
                print(task)
                disp_str = f"-------------------------------------------------------\nTask info:\n|{
                    t['title']}\n"
                disp_str += f"\n|Assigned to: \t \t{t['username']}\n"
                disp_str += "---------------\n"
                disp_str += f"|Date Assigned: \t{
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += "---------------\n"
                disp_str += f"|Due Date: \t \t{
                    t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += "---------------\n"
                disp_str += f"|Task Description: \n {t['description']}\n"
                disp_str += f"-------------------------------------------------------\n"
                print(disp_str)

# Will only print options to edit and mark as complete IF its not already completed
            if task['completed'] != True:
                option = input("""Select option:
e - edit task
c - mark a task as complete
m - return to main menu: \n""").lower()

                if option == 'm':
                    return -1

                elif option == 'c':
                    task['completed'] = True
                    print(
                        "\n-------------------------------------------------------------")
                    print(f"{task['title']} has been marked as Completed")
                    print(
                        "-------------------------------------------------------------")
                    view_mine()

                elif option == 'e':
                    edit = input("""\nWhat would you like to edit: 
u - username
d - Due Date
c - cancel: \n""").lower()

                    # Nested If's for checking the users choice
                    if edit == "c":
                        view_mine()

                    elif edit == "d":
                        while True:
                            try:
                                new_due = input(
                                    "New due date of task (YYYY-MM-DD): ")
                                new_due_date = datetime.strptime(
                                    new_due, DATETIME_STRING_FORMAT)
                                task['due_date'] = new_due_date
                                view_mine()
                                break
                            except ValueError:
                                print(
                                    "Invalid datetime format. Please use the format specified")

                    elif edit == "u":
                        new_user = input("New user assigned to task: ")

                        if new_user in username_password.keys():
                            task['username'] = new_user
                            view_mine()

                        else:
                            print("\nUser does not exist")
                            view_mine()
                    else:
                        print("Invalid Choice")
                        view_mine()

                else:
                    print("\nInvalid choice. Returning to main menu\n")
                    return -1
            else:
                if input("Return to tasks y/n: ").lower() == "y":
                    view_mine()
                else:
                    return -1

# Function to write updated data to txt files


def update_tasks():
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Generate report files of statistics


def reports():
    with open("task_overview.txt", "w") as task_overview:
        tasks_num = len(task_list)
        completed_count = 0
        uncomplete_count = 0
        overdue_count = 0
        for task in task_list:
            if task['completed'] == True:
                completed_count += 1
            else:
                uncomplete_count += 1
                if task['due_date'].date() <= date.today():
                    overdue_count += 1

        to_write = f"Number of tasks : {tasks_num}\n"
        to_write += f"Completed : {completed_count}\n"
        to_write += f"Uncomplete : {uncomplete_count}\n"
        to_write += f"Overdue & Uncomplete : {overdue_count}\n"
        to_write += f"Incomplete : {round(uncomplete_count /
                                          tasks_num*100, 2)}%\n"
        to_write += f"Overdue : {round(overdue_count/tasks_num*100, 2)}%\n"
        task_overview.write(to_write)

    with open("user_overview.txt", "w") as user_overview:
        user_num = len(username_password.keys())
        tasks_num = len(task_list)

        to_write = f"User count: {user_num}\n"
        to_write += f"Task count: {tasks_num}\n"

        for user in username_password.keys():
            to_write += f"\nUser info for {user}: \n"
            user_task_count = 0
            user_complete_count = 0
            user_incomplete_count = 0
            user_overdue = 0
            for task in task_list:
                if task['username'] == user:
                    user_task_count += 1
                    if task['completed'] == True:
                        user_complete_count += 1
                    else:
                        user_incomplete_count += 1
                        if task['due_date'].date() <= date.today():
                            user_overdue += 1
            if user_task_count == 0:
                continue
            else:
                to_write += f"Tasks: {user_task_count}\n"
                to_write += f"% of Tasks: {
                    round(user_task_count/tasks_num*100, 2)}\n"
                to_write += f"Complete: {round(user_complete_count /
                                               user_task_count*100, 2)}\n"
                to_write += f"Incomplete: {
                    round(user_incomplete_count/user_task_count*100, 2)}\n"
                to_write += f"Overdue: {round(user_overdue /
                                              user_task_count*100, 2)}\n"

        user_overview.write(to_write)

# Read statistic report files and print them


def display_stats():
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        reports()
    line = ''
    with open("task_overview.txt", "r") as task_overview:
        task_stats = task_overview.readlines()
        for task in task_stats:
            line += task
        print("\n-"*150)
        print("Tasks statistics:")
        print("-"*150)
        print(line)
        print("-"*150)

    line = ''
    with open("user_overview.txt", "r") as user_overview:
        user_stats = user_overview.readlines()
        for user in user_stats:
            line += user
        print("User statistics:")
        print("-"*150)
        print(line)
        print("-"*150)


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    print(curr_user)
    if curr_user == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
e - Exit
    : ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'ds' and curr_user == 'admin':
        display_stats()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    elif menu == 'gr':
        reports()

    else:
        print("You have made a wrong choice, Please Try again")
