from tortoise import Model, fields
from .base import Level


# Модель для задач
class Tasks(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128)
    description = fields.TextField()
    level = fields.CharEnumField(Level)
    db_path = fields.CharField(max_length=128, default="")
    answer = fields.CharField(max_length=128)
    price = fields.IntField(default=0)