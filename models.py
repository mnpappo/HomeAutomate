from app import db
from datetime import datetime

class Log(db.Model):
	__tablename__ = "logs"
	id = db.Column(db.Integer, primary_key=True)
	comment = db.Column(db.String(80))
	logtime = db.Column(db.DateTime)

	def __init__(self, comment, logtime=None):
		self.comment = comment
		if logtime is None:
			logtime = datetime.utcnow()
		self.logtime = logtime

	def __repr__(self):
		return '<Log time:  %r, Comment: %r>' % (self.logtime, self.comment)
