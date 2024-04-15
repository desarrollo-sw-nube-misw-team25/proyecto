import uuid
from src.extensions import db
from datetime import datetime


class Video(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('uploaded', 'processed', 'deleted', name='status_types'), default='uploaded')
    download_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return '<Video %r>' % {self.filename}

    def get_id(self):
        return self.id

    def get_filename(self):
        return self.filename

    def get_timestamp(self):
        return self.timestamp

    def get_status(self):
        return self.status

    def set_status(self, status):
        # Validate the input status
        valid_statuses = {'uploaded', 'processed','deleted'}
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Valid statuses are {valid_statuses}.")
        self.status = status
        db.session.commit()
