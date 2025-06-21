from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    fiis: fields.ReverseRelation["Fii"]  # user.fiis.all() access all Fiis linked in the user


class Fii(Model):
    id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=7)
    price = fields.FloatField()
    dividend = fields.FloatField()
    user = fields.ForeignKeyField("models.Users", related_name="fiis", on_delete=fields.CASCADE)
    
