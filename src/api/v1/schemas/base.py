from pydantic import BaseModel, constr


class BaseSchema(BaseModel):
    """ Базовая схема для запросов """
    title: constr(min_length=2, max_length=30)
    description: constr(min_length=2, max_length=150)
