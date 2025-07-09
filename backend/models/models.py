from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)


class Fiis(Model):
    id = fields.IntField(primary_key=True)
    code = fields.CharField(max_length=7, unique=True)
    price = fields.FloatField()
    dividend = fields.FloatField()


class UserFiis(Model):
    id = fields.IntField(primary_key=True)
    fii = fields.ForeignKeyField("models.Fiis", related_name="user_fiis")
    user = fields.ForeignKeyField("models.Users", related_name="user_fiis", on_delete=fields.CASCADE)
    quantity = fields.IntField()

    class Meta:
        table = "user_fiis"
        unique_together = ("user", "fii") 
