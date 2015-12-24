from app import db
from models import Log

#create db
db.create_all()

#insert
db.session.add(Log("1st test Comment"))
#db.session.add(Log("2nd Comment"))

#commit
db.session.commit()
