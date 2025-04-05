from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


class PyObjectId(str):
    """Class used to convert mongodb _id to string"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, **kwargs):
        try:
            ObjectId(v)
        except ValueError:
            raise ValueError("Not a valid ObjectId")
        return str(v)


class LogSchema(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    user_id: int
    date: str
    message: str
    data: dict

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }