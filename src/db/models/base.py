from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.ext.declarative import as_declarative


metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    """Abstract model with declarative base functionality."""

    id = Column(Integer, autoincrement=True, primary_key=True)


    
