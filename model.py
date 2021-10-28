import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker, mapper
from sqlalchemy import Column, Integer, VARCHAR, Date, MetaData, Table, Float

Base = declarative_base()

MAPPING_FOR_TYPE = {
    'STR': VARCHAR(255),
    'INT': Integer,
    'FLOAT': Float
}

'''
Is it good option for setting sqlite ? I see some disadvantages about it.
'''
def get_engine(debug: bool):
    if debug is True:
        return sqlalchemy.create_engine('sqlite:///:memory:')
    return sqlalchemy.create_engine('mysql://damian:123456@localhost/application')


def create_session(engine):
    Session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine)
    return Session()


class DataSet(Base):
    __tablename__ = 'data_sets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    creation_date = Column(Date, default=datetime.utcnow())

    def get_table_name(self):
        return f'data_sets_{DataSet.id}'
    
'''
I want to create dynamic table which will be in relationship with DatSet
fields in dynamic table will be create base on xls file which we try to import
so input for dynami catble will be d = {'filed_name': filed_type, }

class DynamicTable(object):
    pass


def create_dynamic_table(data):
    metadata = MetaData(bind=engine)
    table_name = 'table1'
    t = Table(table_name, metadata,
              *(Column(k, v) for k, v in data.items()))
    metadata.create_all()
    mapper(DynamicTable, t)
'''
