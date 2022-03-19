from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

# pour le post create 

class Life(models.Model):

     id = fields.IntField(pk=[True])
     todo = fields.CharField(max_length=250)
     due_date = fields.CharField(max_length=250)

class LifeInput(models.Model):

    todo = fields.CharField(max_length=250)
    due_date = fields.CharField(max_length=250)

class PydanticMeta:
    pass



Life_Pydantic = pydantic_model_creator(Life, name='Life')
LifeIn_Pydantic = pydantic_model_creator(Life, name='LifeIn', exclude_readonly=True)
LifeInput_Pydantic = pydantic_model_creator(LifeInput, name='LifeInput')

