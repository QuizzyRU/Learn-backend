from tortoise import Model, fields
from tasks import Tasks

class Results(Model):
    id = fields.UUIDField(pk=True)
    task = fields.ForeignKeyField("models.Tasks", related_name="results")
    user_id = fields.UUIDField()