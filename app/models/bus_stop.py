from config import db

class BusStop(db.Model):
    ''' The data model'''
    # table name
    __tablename__ = 'BusStop'
    stopid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    stopname = db.Column(db.String())
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
