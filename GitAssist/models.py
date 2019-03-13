from GitAssist.app import db


class Log(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    repository = db.Column(db.String(120))
    working_branch = db.Column(db.String(100))
    target_branch = db.Column(db.String(100))
    operation = db.Column(db.String(100))
    operation_status = db.Column(db.Integer(1))
    time_stamp = db.Column(db.DateTime(), unique = True, nullable = False)

    # log = Log(sno = id, username = username, time_stamp = time_stamp)
    # log = Log(sno, username, repository, working_branch, target_branch, operation, operation_status, time_stamp)
    # log.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

db.create_all()
