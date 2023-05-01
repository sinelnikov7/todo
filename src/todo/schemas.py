from datetime import date
from typing import Optional, Union, List

from pydantic import BaseModel, Field, EmailStr



class Shedule_Schema(BaseModel):
    id: Optional[int] = Field()
    date: date


