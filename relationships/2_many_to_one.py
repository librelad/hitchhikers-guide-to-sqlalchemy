from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, Sequence, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# base class for all of the models
Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    website_id = Column(Integer, ForeignKey('websites.id'))
    website = relationship('Websites')

class Websites(Base):
    __tablename__ = 'websites'
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)

# create a sqlite database in memory and show me the sql queries(echo=True)
engine = create_engine('sqlite:///:memory:')

# create all of the tables
Base.metadata.create_all(bind=engine)

# start session
Session = sessionmaker(bind=engine)
session = Session()

# create a website object
foot_fetish = Websites(url="https://ffetish.co/no_idea_where_this_leads")

# add object to sesssion
session.add(foot_fetish)

# fetch object from session
session.query(Websites).filter(Websites.id == 1).first()

# create person object relating to foot_fetish object
person1 = Person(name="Jeff", website_id=foot_fetish.id)
person2 = Person(name="Jeruska", website_id=foot_fetish.id)
person3 = Person(name="Bongani", website_id=foot_fetish.id)

# add persons to the session
session.add(person1)
session.add(person2)
session.add(person3)

# lets test our many to one by looking for the site url for Jeff
person_query = session.query(Person).filter(Person.name == "Jeff").first()

# accessing the one website from the person object
print "%s has been visiting" % person_query.name
print person_query.website.url

session.commit()
session.close()