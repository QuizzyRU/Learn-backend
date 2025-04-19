from tortoise import Model, fields
from .base import Level


class User(Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=128)
    username = fields.CharField(max_length=32)
    avatar = fields.CharField(max_length=256)
    description = fields.TextField()
    points = fields.IntField()
    is_admin = fields.BooleanField(default=False)
    level = fields.CharEnumField(Level)
    password = fields.TextField()