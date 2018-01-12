import logging

import mongoengine
from django.conf import settings
from django.utils.datetime_safe import datetime
from mongoengine import Document, StringField, FloatField, DateTimeField, GeoPointField, PointField

logger = logging.getLogger(__name__)

logger.info('Connecting to MongoDB...')
mongoengine.connect('ecn', host=settings.MONGODB_URI)
logger.info('Connected.')


class StationState:
    ALERT = 'A'
    READY = 'R'
    ECO = 'E'
    HIGH_RATE = 'H'
    NORMAL_RATE = 'N'
    LOST = 'L'


class Station(Document):
    kind = StringField(db_field='k', max_length='1', min_length='1', required=True)
    name = StringField(db_field='n')
    location = PointField(db_field='l', auto_index=False)
    elevation = FloatField(db_field='e')
    depth = FloatField(db_field='d')
    creation_time = DateTimeField(db_field='c', required=True)
    client_id = StringField(db_field='i')
    state = StringField(db_field='s', min_length='1', max_length='1', required=True)
    signal_time = DateTimeField(db_field='t')

    def to_dict(self):
        '''Used for both JSON (for JavaScript in web app) and GraphQL.'''
        return {
            'id': self.id, 'kind': self.kind, 'name': self.name,
            'location': self.location,
            'elevation': self.elevation,
            'depth': self.depth,
            'creation_time': self.creation_time.isoformat(),
            'client_id': self.client_id,
            'state': self.state,
            'signal_time': self.signal_time.isoformat(),
        }
