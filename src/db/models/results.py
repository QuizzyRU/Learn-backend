from tortoise import Model, fields
from .tasks import Tasks

# Модель для результатов теста
class Results(Model):
    id = fields.UUIDField(pk=True)
    task = fields.ForeignKeyField("models.Tasks", related_name="results")
    user_id = fields.UUIDField() # Просто заглушка