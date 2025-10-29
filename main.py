from datetime import datetime, time

workouts = [
    'Kb snatch',
    'Heavy kb swings + pistol squats superset',
    'Neutral-grip archer pullups + dips',
    'Light swings + split-squats superset',
    'Light pull + burpees superset',
    'Kb snatch',
    'Heavy kb swings + stair climbs superset',
    'Weighted pullups + heavy kb oh press',
    'Light swings + burpees superset',
    'Light pull + light kb oh press superset',
]

# days: which days of the week does the task show up, empty list means every day
# duration: expected time to complete in minutes
# impact: how important it is. 1 = low importance, 3 = high importance
# urgency: how soon it needs to be done. same scale as impact, tasks with a time become high urgency at that time
regular_tasks = {
    'get ready for work': {'days': [0, 1, 2, 6], 'duration': 60, 'impact': 3, 'urgency': time(12)},
    'Check emails': {'days': [], 'duration': 10, 'impact': 2, 'urgency': 2},
}

# TODO I should use the data from the tasks dictionary to create task objects that have other properties like 'completed'
#  and 'deferred' etc

# TODO i could have an 'optional' property for certain recurring tasks, so that the initial dialogue can ask me 'do you
#  need to do X today?' and give me the option to defer or skip

count = 0
while True:
    now = datetime.now()
    count += 1
    response = input("\nReady for the day?")
    if response == 'n':
        break
    print(f"\n{now.date()} Today's List")
    for task in regular_tasks:
        if (not regular_tasks[task]['days']) or (now.weekday() in regular_tasks[task]['days']):
            print(f"- {task}")

    todays_workout = workouts[count % len(workouts)]
    print(f"- {todays_workout}")

