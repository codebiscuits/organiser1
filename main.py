from datetime import datetime, timedelta
import json
from pathlib import Path
import click
from pprint import pprint
from models import Task
from functions import *

@click.group()
def cli():
    pass

# create a new task
dt_formats = ["%y/%m/%d %H:%M", "%Y/%m/%d %H:%M"]
@click.command()
@click.argument("name")
def new_task(name) -> None:
    click.clear()
    description = click.prompt("Enter a description")
    mandatory = click.prompt("Is it mandatory?", type=click.BOOL)
    duration = click.prompt("How many minutes will it take?", type=click.INT)
    impact = click.prompt("How important? (1-3)", type=click.IntRange(1, 3, clamp=True))
    date_is = click.prompt("Enter a date (optional)", default="")
    if date_is.strip():
        date_is = datetime.strptime(date_is, "%y/%m/%d %H:%M")
        date_for = click.prompt("Appointment or deadline?", type=click.Choice(["a", "d"], case_sensitive=False))
        urgency: int = calculate_urgency(date_is, duration)
    else:
        date_is = None
        date_for = None
        urgency = click.prompt("How urgent? (1-3)", type=click.INT)
    list_name = click.prompt("Which list?", type=str)

    lists[list_name]['list'].append(Task(name, description, mandatory, duration, urgency, impact, date_is, date_for))
    save_list(list_name, lists)
cli.add_command(new_task)

@click.command()
def show_lists() -> None:
    click.clear()
    for list in lists:
        if lists[list]['list']:
            click.echo(list)
            for task in lists[list]['list']:
                click.echo(f"- {task.name} ({task.duration}mins)")
cli.add_command(show_lists)

########################################################################################################################

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

# for list_name in lists.keys():
#     if lists[list_name]['list']:
#         print(list_name)
#         print([str(l) for l in lists[list_name]['list']])
#
#         print([l for l in lists[list_name]['list']])

if __name__ == "__main__":
    cli()
