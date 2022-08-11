from config import db

class BusRoute(db.Model):
    ''' The data model'''
    # table name
    __tablename__ = 'BusRoute'
    routeid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    routename = db.Column(db.String())
    routenum = db.Column(db.String())
    routetype = db.Column(db.Integer())
    direction = db.Column(db.Integer())

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
