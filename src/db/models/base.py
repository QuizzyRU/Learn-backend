from enum import Enum

class Level(Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"
    MASTER = "Master"

class Status(Enum):
    START = "started"
    SOLVE = "solve"
    FINISH = "finish"