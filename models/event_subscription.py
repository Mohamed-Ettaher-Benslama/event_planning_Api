from extention import db

class EventSubscription (db.Model):
    __tablename__ = "eventsubscription"
    userid = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey("event.id"), primary_key=True)

    @classmethod
    def get_subscriptions_by_user_id(cls, user_id):
        return cls.query.filter_by(userid=user_id)

    @classmethod
    def get_subscription_by_id(cls, user_id, event_id):
        return cls.query.filter_by(userid=user_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()