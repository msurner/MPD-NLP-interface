from locust import HttpLocust, TaskSet, task
from random import randint

instructions = [
"Play.",
"Stop.",
"Pause.",
"Play David Bowie.",
"Play Heroes from David Bowie.",
"Play not David Bowie.",
"Play David Bowie, Iron Maiden or Five Finger Death Punch.",
"Play not David Bowie, but Iron Maiden.",
"Don't play David Bowie.",
"Playing David Bowie would be nice.",
"My grandmother wants me to play David Bowie.",
"Don't stop.",
"Don't pause.",
"Resume.",
"Don't resume.",
"Play rock music or electro house.",
"Continue.",
"Stop playing."
]

#define simulated behavior
class UserBehavior(TaskSet):

    @task(5)
    def index(self):
        # Make a HTTP-GET request, encode spaces (' ') with '%20'
        # select instructions randomly
        self.client.get("/" + instructions[randint(0, len(instructions)-1)].replace(" ", "%20"))


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
