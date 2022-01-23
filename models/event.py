from extention import db

class Event (db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.String(250),nullable=True)
    ticket_price = db.Column(db.FLOAT,nullable=False)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(cls):
        return cls.query.filter_by()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
