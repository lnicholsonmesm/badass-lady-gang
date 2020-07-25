#db.py

#________*_________*_________*_________*_________*_________*_________*_________*
from sqlalchemy.engine.url import URL

sqlite_db = {'drivername': 'sqlite', 'database': 'db.sqlite'}
print(URL(**sqlite_db))

#________*_________*_________*_________*_________*_________*_________*_________*
from sqlalchemy import create_engine

#database uniform resource identifyer
db_uri = "sqlite:///db.sqlite" 
engine = create_engine(db_uri)

# DBAPI - PEP249
# create table
engine.execute('CREATE TABLE "EX1" ('
               'id INTEGER NOT NULL,'
               'name VARCHAR, '
               'PRIMARY KEY (id));')
# insert a raw
engine.execute('INSERT INTO "EX1" '
               '(id, name) '
               'VALUES (1,"raw1")')

# select *
result = engine.execute('SELECT * FROM '
                        '"EX1"')
for _r in result:
   print(_r)

# delete *
engine.execute('DELETE from "EX1" where id=1;')
result = engine.execute('SELECT * FROM "EX1"')
print(result.fetchall())

#________*_________*_________*_________*_________*_________*_________*_________*
db_uri = "sqlite:///db.sqlite" 
engine = create_engine(db_uri)
# Create connection
conn = engine.connect()
# Begin transaction
trans = conn.begin()
conn.execute('INSERT INTO "EX1" (name) '
             'VALUES ("Hello")')
trans.commit()
# Close connection
conn.close()

#________*_________*_________*_________*_________*_________*_________*_________*
#from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)

# Create a metadata instance
metadata = MetaData(engine)
# Declare a table
table = Table('Example',metadata,
              Column('id',Integer, primary_key=True),
              Column('name',String))
# Create all tables
metadata.create_all()
for _t in metadata.tables:
   print("Table: ", _t)

   from sqlalchemy import create_engine
from sqlalchemy import inspect

#________*_________*_________*_________*_________*_________*_________*_________*
#db_uri = 'sqlite:///db.sqlite'
#engine = create_engine(db_uri)

inspector = inspect(engine)

# Get table information
print(inspector.get_table_names())

# Get column information
print(inspector.get_columns('EX1'))


#________*_________*_________*_________*_________*_________*_________*_________*
#from sqlalchemy import create_engine
#from sqlalchemy import MetaData
#from sqlalchemy import Table

#db_uri = 'sqlite:///db.sqlite'
#engine = create_engine(db_uri)

# Create a MetaData instance
metadata = MetaData()
print(metadata.tables)

# reflect db schema to MetaData
metadata.reflect(bind=engine)
print(metadata.tables)

#________*_________*_________*_________*_________*_________*_________*_________*
#________ SQL DDL:(CREATE, DROP, ALTER, TRUNCATE) _________*_________*_________*

#from sqlalchemy import create_engine
#from sqlalchemy import MetaData
#from sqlalchemy import Table
#from sqlalchemy import Column
#from sqlalchemy import Integer
#from sqlalchemy import String
'''
def metadata_dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))

meta = MetaData()
example_table = Table('Example',meta,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(10), index=True))

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri, strategy='mock', executor=metadata_dump)

meta.create_all(bind=engine, tables=[example_table])
'''
#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_______ GET TABLE FROM METADATA _______*_________*_________*
#from sqlalchemy import create_engine
#from sqlalchemy import MetaData
#from sqlalchemy import Table

#db_uri = 'sqlite:///db.sqlite'
#engine = create_engine(db_uri)

# Create MetaData instance
metadata = MetaData(engine).reflect()
print(metadata.tables)

# Get Table
ex_table = metadata.tables['Example']
print(ex_table)

#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*______ CREATE TABLES TO METADATA ______*_________*_________*
#from sqlalchemy import create_engine
#from sqlalchemy import MetaData
#from sqlalchemy import Table
#from sqlalchemy import Column
#from sqlalchemy import Integer, String

#db_uri = 'sqlite:///db.sqlite'
#engine = create_engine(db_uri)
meta = MetaData(engine)

# Register t1, t2 to metadata
t1 = Table('EX1', meta,
           Column('id',Integer, primary_key=True),
           Column('name',String))

t2 = Table('EX2', meta,
           Column('id',Integer, primary_key=True),
           Column('val',Integer))
# Create all tables in meta

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)

meta = MetaData(engine)
t1 = Table('Table_1', meta,
           Column('id', Integer, primary_key=True),
           Column('name',String))
t2 = Table('Table_2', meta,
           Column('id', Integer, primary_key=True),
           Column('val',Integer))
t1.create()


#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*___ CREATE TABLES WITH SAME COLUMNS ___*_________*_________*
from sqlalchemy import (
    create_engine,
    inspect,
    Column,
    String,
    Integer)

from sqlalchemy.ext.declarative import declarative_base

db_url = "sqlite://"
engine = create_engine(db_url)

Base = declarative_base()

class TemplateTable(object):
    id   = Column(Integer, primary_key=True)
    name = Column(String)
    age  = Column(Integer)

class DowntownAPeople(TemplateTable, Base):
    __tablename__ = "downtown_a_people"

class DowntownBPeople(TemplateTable, Base):
    __tablename__ = "downtown_b_people"

Base.metadata.create_all(bind=engine)

# check table exists
ins = inspect(engine)
for _t in ins.get_table_names():
    print(_t)

#________*_________*_________*_________*_________*_________*_________*_________*
#________*_________*_________*  JOIN TWO TABLES  *_________*_________*_________*
#join() - Joined Two Tables via “JOIN” Statement
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select

db_uri = 'sqlite:///db.sqlite'
engine = create_engine(db_uri)

meta = MetaData(engine).reflect()
email_t = Table('email_addr', meta,
      Column('id', Integer, primary_key=True),
      Column('email',String),
      Column('name',String))
meta.create_all()

# get user table
user_t = meta.tables['user']

# insert
conn = engine.connect()
conn.execute(email_t.insert(),[
   {'email':'ker@test','name':'Hi'},
   {'email':'yo@test','name':'Hello'}])
# join statement
join_obj = user_t.join(email_t,
           email_t.c.name == user_t.c.l_name)
# using select_from
sel_st = select(
   [user_t.c.l_name, email_t.c.email]).select_from(join_obj)
res = conn.execute(sel_st)
for _row in res:
    print(_row)

            session.close()
finally:
    engine.dispose()