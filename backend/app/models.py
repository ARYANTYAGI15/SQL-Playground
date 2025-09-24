from sqlalchemy import Column , Integer ,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SampleTable(Base):
    __tablename__ = "sample_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Integer)



