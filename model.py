import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Column, Integer, VARCHAR, Date

engine = sqlalchemy.create_engine('mysql://damian:123456@localhost/application')

Base = declarative_base()
Session = sessionmaker(bind=engine)


class DataSet(Base):
    __tablename__ = 'data_sets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    creation_date = Column(Date, default=datetime.utcnow())

    dynamic_model = relationship('DynamicModel', back_populates='data_sets')

    def get_table_name(self):
        return f'data_sets_{DataSet.id}'


class DynamicModel(Base):
    __tablename__ = DataSet().get_table_name()
    id = Column(Integer, primary_key=True, autoincrement=True)

    data_sets = relationship('DataSet', back_populates='dynamic_model')

    @classmethod
    def create_metadata_for_dynamic_model(cls):
        data_schema = {'col1': Integer, 'col2': VARCHAR}
        for col_name, col_type in data_schema.items():
            setattr(DynamicModel, col_name, col_type)


Base.metadata.create_all(bind=engine)
