def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"C:\sqlite\db\pythonsqlite.db")


# Import SQL Alchemy
from sqlalchemy import create_engine

# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float

# Create the Garbage class
class Garbage(Base):
    __tablename__ = 'garbage_collection'
    id = Column(Integer, primary_key=True)
    item = Column(String(255))
    weight = Column(Float)
    collector = Column(String(255))

# Create a connection to a SQLite database
engine = create_engine('sqlite:///garbage.db')

# Create the garbage_collection table within the database
Base.metadata.create_all(engine)

# To push the objects made and query the server we use a Session object
from sqlalchemy.orm import Session
session = Session(bind=engine)

# Create some instances of the Garbage class
garbage_one = Garbage(item="Sofa", weight=90.5, collector="Jacob")
garbage_two = Garbage(item="Broken TV", weight=10.75, collector="Paul")
garbage_three = Garbage(item="Burger", weight=0.55, collector="Phil")

# Add these objects to the session
session.add(garbage_one)
session.add(garbage_two)
session.add(garbage_three)
# Commit the objects to the database
session.commit()

# Update two rows of data
update_one = session.query(Garbage).filter(Garbage.id == 1).first()
update_one.collector = "Jacob Deming"
update_two = session.query(Garbage).filter(Garbage.id == 2).first()
update_two.weight = 11.25
# Commit the updates to the database
session.commit()

# Delete the row with the lowest weight
session.query(Garbage).filter(Garbage.id == 3).delete()
# Commit the delete to the database
session.commit()

# Collect all of the items and print their information
items = session.query(Garbage)
for item in items:
    print("-"*12)
    print(f"id: {item.id}")
    print(f"item: {item.item}")
    print(f"weight: {item.weight}")
    print(f"collector: {item.collector}")
