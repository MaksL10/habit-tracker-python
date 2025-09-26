class Habit:

    """
    Represents a habit to be tracked in the application.

    A Habit consists of name, periodicity (how often should it be done) and short user description (Optional).
    Attributes:
        name(str) - Name of the habit
        periodicity(str): How often should habit be repeated. Must be "daily", "weekly" or "monthly".
        description(str): short description of the habit.

    """

    def __init__(self, name: str, periodicity: str, description: str = None):
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

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if name is not None:
            name = name.strip()
        if not name:
            raise ValueError ("Habit name cannot be empty")
        elif  1 == len(name) or len(name) > 20:
            if 1 == len(name):
                raise ValueError ("Habit name is too short")
            else:
                raise ValueError ("Habit name is too long")
        elif name.isdigit():
            raise ValueError ("Habit name cannot be a digit")
        elif name in ["daily", "weekly", "monthly"]:
            raise ValueError ("Wrong habit name")
        else:
            self._name = name

    def __str__(self):
        return f'{self.name} ({self.periodicity}: {self.description})'