from datetime import datetime

class Task():
    def __init__(self, name, description, duration, urgency, impact, date_is, date_for):
        self.name: str = name
        self.description: str = description
        self.duration: int = duration
        self.completed: bool = False
        self.date_is: datetime | None = date_is
        self.date_for: str | None = date_for
        self.deferred: bool = False
        self.impact: int = impact
        self.urgency: int = urgency
        self.priority: int = self.impact * self.urgency

    # This will make it easy to identify duplicate tasks, even if they aren't completely identical
    def __eq__(self, other):
        return (self.name == other.name) and (self.date_is == other.date_is)

    # These are implemented so that I can easily sort a list of tasks by priority
    def __gt__(self, other):
        return self.priority > other.priority
    def __gte__(self, other):
        return self.priority >= other.priority
    def __lt__(self, other):
        return self.priority < other.priority
    def __lte__(self, other):
        return self.priority <= other.priority

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.date_is:
            return (f"{self.name}\n{self.description}\n{self.duration}\n{self.completed}\n{self.date_is}"
                    f"\n{self.date_for}\n{self.deferred}\n{self.impact}\n{self.urgency}\n{self.priority}")
        else:
            return (f"{self.name}\n{self.description}\n{self.duration}\n{self.completed}"
                    f"\n{self.deferred}\n{self.impact}\n{self.urgency}\n{self.priority}")
