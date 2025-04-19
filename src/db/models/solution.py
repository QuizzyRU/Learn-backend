from tortoise import Model, fields
from .base import Status
from .tasks import Tasks

class Solution(Model):
    id = fields.UUIDField(pk=True)
    task = fields.ForeignKeyField("models.Tasks", related_name="solution")
    status = fields.CharEnumField(Status)