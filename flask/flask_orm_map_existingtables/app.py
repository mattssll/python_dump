from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

app = Flask(__name__)
Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("sqlite:///flaskdb.db")

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
User = Base.classes.users
session = Session(engine)
# rudimentary relationships are produced
session.add(User(id=2, name="test"))
session.commit()

# collection-based relationships are by default named
# "<classname>_collection"
print (u1.address_collection)
@app.route('/')
def hello_world():
    return 'Hello, World!'


