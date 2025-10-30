from datetime import datetime, time
import json
from pathlib import Path
from pprint import pprint

# TODO i could have an 'optional' property for certain recurring tasks, so that the initial dialogue can ask me 'do you
#  need to do X today?' and give me the option to defer or skip

now = datetime.now()
LISTS = {
    'regular': Path("data/regular1.json"),
    'workouts': Path("data/workouts.json"),
    'workout_count': Path("data/workout_count.json")
}

def load_json(list_name: str) -> dict:
    # load regular tasks list from file, create file if it doesn't exist
    list_path = LISTS[list_name]
    if list_path.exists():
        with open(list_path, 'r') as f:
            task_list = json.load(f)
    else:
        task_list = {}

    # pprint(regular_tasks)
    return task_list

def collate_regular(now: datetime) -> list[str]:
    """
    days: which days of the week does the task show up, empty list means every day
    duration: expected time to complete in minutes
    impact: how important it is. 1 = low importance, 3 = high importance
    urgency: how soon it needs to be done. same scale as impact, tasks with a time become high urgency at that time

    :param now:
    :return : list of today's regular tasks
    """

    regular_tasks = load_json('regular')

    todays_regular = []
    for task in regular_tasks:
        if isinstance(regular_tasks[task]['urgency'], str):
            h, m = regular_tasks[task]['urgency'].split(' ')
            regular_tasks[task]['urgency'] = time(int(h), int(m))
        if (not regular_tasks[task]['days']) or (now.weekday() in regular_tasks[task]['days']):
            todays_regular.append(task)

    return todays_regular

def save_regular():
    regular_path = LISTS['regular_path']
    if not regular_path.exists():
        regular_path.parent.mkdir(parents=True, exist_ok=True)
        regular_path.touch(exist_ok=True)

def increment_workout():
    with open(LISTS['workout_count'], 'r') as f:
        count_dict = json.load(f)

    # get counter
    number = count_dict['count']

    # create a number that counts up days
    today = (2025 * 365) + now.timetuple().tm_yday

    # compare day number to make sure this is a new day
    if today > count_dict['day']:
        count_dict['count'] += 1
        count_dict['day'] = today

    with open(LISTS['workout_count'], 'w') as f:
        json.dump(count_dict, f)

    return number

def load_workouts():
    workouts = load_json('workouts')
    wo_list = list(workouts.keys())

    # pprint(workouts)

    counter = increment_workout()
    return wo_list[counter % len(wo_list)]

# import data
workout = load_workouts()
regular = collate_regular(now)

count = 0
while True:
    count += 1
    response = input("\nReady for the day?")
    if response == 'n':
        break
    print(f"\n{now.date()} Today's List")

    for task in regular:
        print(f"- {task}")

    print(f"- workout")
    print("  Essentials")
    print(f"  {workout}")

