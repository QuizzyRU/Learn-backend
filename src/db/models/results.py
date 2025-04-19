from tortoise import Model, fields
from .tasks import Tasks
from .user import User

# Модель для результатов теста
class Results(Model):
    id = fields.UUIDField(pk=True)
    task = fields.ForeignKeyField("models.Tasks", related_name="results")
    user = fields.ForeignKeyField("models.User", related_name="results")
    points_earned = fields.IntField()  # Количество заработанных очков