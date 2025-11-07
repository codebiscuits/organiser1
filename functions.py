from datetime import datetime, timedelta
import json
from pathlib import Path
from pprint import pprint
from models import Task

# def collate_recurring(now: datetime) -> list[str]:
#     """
#     days: which days of the week does the task show up, empty list means every day
#     duration: expected time to complete in minutes
#     impact: how important it is. 1 = low importance, 3 = high importance
#     urgency: how soon it needs to be done. same scale as impact, tasks with a time become high urgency at that time
#
#     :param now:
#     :return : list of today's regular tasks
#     """
#
#     recurring_tasks = load_json('regular')
#
#     todays_recurring = []
#     for task in recurring_tasks:
#         if isinstance(recurring_tasks[task]['urgency'], str):
#             h, m = recurring_tasks[task]['urgency'].split(' ')
#             recurring_tasks[task]['urgency'] = time(int(h), int(m))
#         if (not recurring_tasks[task]['days']) or (now.weekday() in recurring_tasks[task]['days']):
#             todays_recurring.append(task)
#
#     return todays_recurring
#
# def save_recurring():
#     recurring_path = LIST_PATHS['recurring']
#     if not recurring_path.exists():
#         recurring_path.parent.mkdir(parents=True, exist_ok=True)
#         recurring_path.touch(exist_ok=True)
#
# def increment_workout():
#     """There needs to be a function that cycles through the workouts list, but i don't want it to increment on days that
#     i don't open the app, and i also don't want it to increment more than once on days that i open the app more than
#     once, so i need a counter that prevents both of those possibilities.
#     To prevent multiple incerements per day, this function calculates the number of days since 0/0/00 and keeps a record
#     of the last day number that the app was opened, and only increments if the day number has changed.
#     To prevent incrementing on days that the app isn't used, there is another count thast it uses to choose the workout
#     which is only incremented when the app is opened and the day number has changed since last time."""
#
#     # TODO i also need to be able to defer the workout if it is not marked complete, this would require not incrementing
#     #  the count. Perhaps i could start by checking if there is a workout in the list of tasks carried over from
#     #  yesterday, and if there is, don't increment, just return yesterday's number
#
#     count_path = "workout_count.json"
#
#     with open(count_path, 'r') as f:
#         count_dict = json.load(f)
#
#     # get counter
#     number = count_dict['count']
#
#     # create a number that counts up days
#     today = (2025 * 365) + now.timetuple().tm_yday
#     # compare day number to make sure this is a new day
#     if today > count_dict['day']:
#         count_dict['count'] += 1
#         count_dict['day'] = today
#
#     with open(count_path, 'w') as f:
#         json.dump(count_dict, f)
#
#     return number
#
# def load_workouts():
#     workouts = load_json('workouts')
#     wo_list = list(workouts.keys())
#
#     # pprint(workouts)
#
#     counter = increment_workout()
#     return wo_list[counter % len(wo_list)]

#####################################################################

# function to load lists
def load_json(list_path: Path) -> list:
    # load regular tasks list from file, create file if it doesn't exist
    if list_path.exists():
        with open(list_path, 'r') as f:
            task_list = json.load(f)
    else:
        task_list = []

    # pprint(regular_tasks)
    return task_list

# function to serialise tasks
def serialise_task(task: Task) -> dict:
    """Takes a Task object and turns it into a dictionary for saving as JSON.
    Translates datetime object into ISO format"""

    if task.date_is:
        date_is = task.date_is.isoformat()
    else:
        date_is = None

    return {
        "name": task.name,
        "description": task.description,
        "mandatory": task.mandatory,
        "duration": task.duration,
        "completed": task.completed,
        "date_is": date_is,
        "date_for": task.date_for,
        "deferred": task.deferred,
        "impact": task.impact,
        "urgency": task.urgency,
        "priority": task.priority,
    }

# function to deserialise tasks
def deserialise_task(task: dict) -> Task:
    """Takes a serialised task dictionary, recalculates urgency if required, then instantiates
    a new Task object with the appropriate attributes, and updates completed, deferred and priority
    to ensure their values are preserved"""

    if task["date_is"]:
        new_date = datetime.fromisoformat(task["date_is"])
        urgency = calculate_urgency(new_date, task["duration"])
    else:
        new_date = None
        urgency = task["urgency"]

    new_task = Task(
        name=task["name"],
        description=task["description"],
        mandatory=task['mandatory'],
        duration=task["duration"],
        date_is=new_date,
        date_for=task["date_for"],
        impact=task["impact"],
        urgency=urgency
    )

    new_task.completed = task["completed"]
    new_task.deferred = task["deferred"]
    new_task.priority = task["impact"] * urgency

    return new_task

# function to serialise whole list
def serialise_list(task_list: list[Task]) -> list[dict]:
    return [serialise_task(t) for t in task_list]

# function to deserialise whole list
def deserialise_list(task_list: list[dict]) -> list[Task]:
    return [deserialise_task(t) for t in task_list]

# function to save lists
def save_json(list_name: str, serialised_list: list, lists: dict) -> None:
    list_path = lists[list_name]['path']
    with open(list_path, 'w') as f:
        json.dump(serialised_list, f)
    print(f"{list_name} saved successfuly")

# function to create a new task
def calculate_urgency(date_is, duration) -> int:
    now = datetime.now()
    free_hours_per_day = 3 # very rough estimate of how much time i have for working through tasks
    days_until_deadline = (date_is - now).days
    free_hours = days_until_deadline * free_hours_per_day
    duration_multiple = free_hours / (duration / 60)

    if duration_multiple <5:
        return 3
    elif duration_multiple < 10:
        return 2
    else:
        return 1

def add_task(list_name: str) -> Task|None:
    if list_name not in lists.keys():
        print(f"Invalid task list, must be one of: {[lists.keys()]}")
        return

    name: str = input("Enter task name: ")
    description: str = input("Enter task description: ")
    mandatory: bool = True if (input("Is this task mandatory? (Y/n): ").lower() == 'y') else False
    duration: int = int(input("Enter task duration in minutes: "))
    impact: int = int(input("Enter task impact (1-3): "))
    date_is = input("Enter task time as 'yy/mm/dd hh:mm' (optional): ") or None
    if date_is:
        date_is = datetime.strptime(date_is, "%y/%m/%d %H:%M")
        date_for = input("For deadline, enter 'd', for appointment, enter 'a' (optional): ")
        urgency: int = calculate_urgency(date_is, duration)
    else:
        date_for = None
        urgency: int = int(input("Enter task urgency (1-3): "))

    lists[list_name]['list'].append(Task(name, description, mandatory, duration, urgency, impact, date_is, date_for))

# function to create a new list
def create_list(list_name: str) -> list:
    global lists
    list_path = Path(f"data/{list_name}.json")

    if list_path.exists():
        print("List already exists")
    else:
        lists[list_name]["path"] = list_path
        lists[list_name]["list"] = []

    # TODO function to manage loading and preparing all lists

def load_all_lists(list_names) -> dict[str: dict]:
    all_lists = {}

    for list_name in list_names:
        all_lists[list_name] = {}
        all_lists[list_name]['path'] = Path(f"data/{list_name}.json")
        this_list = load_json(all_lists[list_name]['path'])
        all_lists[list_name]['list'] = deserialise_list(this_list)

    return all_lists

    # TODO function to back up all lists to json before a risky operation

def save_list(list_name: str, lists: dict) -> None:
    serialised_list = serialise_list(lists[list_name]['list'])
    save_json(list_name, serialised_list, lists)

def save_all_lists() -> None:
    for list in lists:
        save_list(list)

# TODO function to set task as complete

# TODO function to set task as deferred
# remember to check for 'mandatory' before allowing deferral

# TODO function to compile 'today' list from other lists

# TODO i need the option to skip recurring tasks, so that the initial dialogue can ask me 'do you
#  need to do X today?' and give me the option to defer or skip

if __name__ == "__main__":

    list_names = [
        "today",
        "defer",
        "workouts",
        "recurring",
        "housework",
        "appointments",
        "deadlines",
        "one_offs",
        "completed",
    ]

    lists = load_all_lists(list_names)

    for list_name in lists.keys():
        if lists[list_name]['list']:
            print(list_name)
            print([str(l) for l in lists[list_name]['list']])

            print([l for l in lists[list_name]['list']])

