from datetime import datetime

from sqlalchemy import orm

from model import db
from utility.constants import Constants


class Group(db.Model):
    __tablename__ = 'GROUP'

    group_id = db.Column(db.Integer, primary_key=True)
    creator_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    modified_user_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'))
    name = db.Column(db.Text)
    is_removed = db.Column(db.Boolean)
    time_stamp = db.Column(db.DateTime)

    @orm.reconstructor
    def init_on_load(self):
        self.internal_id = None

    def __init__(self, input_parameters):
        self.internal_id = None
        self.is_removed = False

        self.update(input_parameters)

    def update(self, new_value):
        value = new_value.get(Constants.JSON.name)
        if value is not None:
            self.name = value

        value = new_value.get(Constants.JSON.is_removed)
        if value is not None:
            self.is_removed = value

        value = new_value.get(Constants.JSON.internal_id)
        if value is not None:
            self.internal_id = value

        value = new_value.get(Constants.JSON.user_id)
        if value is not None:
            self.modified_user_id = value

        self.time_stamp = datetime.utcnow()

    def to_json(self):
        json_object = {Constants.JSON.group_id: self.group_id,
                       Constants.JSON.name: self.name,
                       Constants.JSON.modified_user_id: self.modified_user_id,
                       Constants.JSON.is_removed: self.is_removed
                       }

        if self.creator_user_id is not None:
            json_object[Constants.JSON.creator_user_id] = self.creator_user_id

        if self.internal_id is not None:
            json_object[Constants.JSON.internal_id] = self.internal_id

        if self.time_stamp is not None:
            json_object[Constants.JSON.time_stamp] = self.time_stamp.isoformat()

        return json_object
