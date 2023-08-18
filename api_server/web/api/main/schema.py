from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    """Simple item model."""

    models_name_list: List[str]
    file_path: str
