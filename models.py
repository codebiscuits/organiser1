from datetime import datetime

class Task():
    def __init__(self, name, description, duration, completed, urgency, impact, deadline):
        self.name = name
        self.description = description
        self.duration = duration
        self.completed = completed
        self.urgency = urgency
        self.impact = impact
        self.deadline = deadline


class Live_List():
    def __init__(self):
        self.live_list = []

    def add_task(self):
        name = input("Enter task name: ")
        description = input("Enter task description: ")
        duration = input("Enter task duration: ")
        urgency = input("Enter task urgency: ")
        impact = input("Enter task impact: ")
        deadline = input("Enter task deadline (optional): ")

        self.live_list.append(Task(name, description, duration, False, urgency, impact, deadline))
