import datetime


class Task:
    def __init__(self, name: str, description: str, trigger_time: datetime.datetime):
        self.name = name
        self.description = description
        self.trigger_time = trigger_time


    @staticmethod
    def from_dict(json_data: dict):
        return Task(
            json_data["name"],
            json_data["description"],
            datetime.datetime.fromtimestamp(float(json_data["trigger_timestamp"]))
        )
