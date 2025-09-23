class Habit:

    """
    Represents a habit to be tracked in the application.

    A Habit consists of name, periodicity (how often should it be done) and short user description (Optional).
    Attributes:
        name(str) - Name of the habit
        periodicity(str): How often should habit be repeated. Must be "daily", "weekly" or "monthly".
        description(str): short description of the habit.

    """

    def __init__(self, name: str, periodicity: str, description: str):
        self.name = name
        self.periodicity = periodicity
        self.description = description

    @property
    def periodicity(self):
        return self._periodicity
    
    @periodicity.setter
    def periodicity(self, periodicity):
        if periodicity not in ["daily", "weekly", "monthly"]:
            raise ValueError ("Invalid periodicity")
        self._periodicity = periodicity

    def __str__(self):
        return f'{self.name} ({self.periodicity}: {self.description})'

    

habit = Habit("laufen", "weekly", "2 Mal laufen wöchentlich")
habit.increment()
print(habit)
habit.reset()
print(habit)