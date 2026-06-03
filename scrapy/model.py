from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Article:
    title: str
    url: str
    description : str
    content : str
    source : str
    published_at : datetime
    sentiment : Optional[str] = None