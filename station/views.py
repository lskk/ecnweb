import json
import logging

from datetime import timedelta
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.utils.datetime_safe import datetime

from station.mongomodels import Station, StationState, Accel

logger = logging.getLogger(__name__)

def home(request: HttpRequest):
    stations = list(Station.objects(state__ne=StationState.LOST, location__ne=None))
    logger.debug('Stations: %s', stations)

    template = loader.get_template('station/home.html')
    context = {
        # 'page_title': _("Terms of Service"),
        'stations': stations,
        'stations_json': json.dumps([station.to_dict() for station in stations]),
    }
    return HttpResponse(template.render(context, request))

def station_detail(request: HttpRequest, station_id: int):
    station = Station.objects(id=int(station_id)).first()
    logger.debug('Station %s: %s', station_id, station)
    station_name = station.name if station.name else 'Station ' + station.id
    now = datetime.utcnow()
    accel_id = '%s:%d' % (now.strftime('%Y%m%d%H'), station.id)
    second_of_hour = 60 * now.minute + now.second
    logger.debug('Accel %s second_of_hour=%d', accel_id, second_of_hour)
    if second_of_hour >= 6:
        # only up to the previous second (because current second is not yet avaiable)
        accel = Accel.objects(id=accel_id).fields(slice__z=[second_of_hour - 6, 5], slice__n=[second_of_hour - 6, 5],
                                                  slice__e=[second_of_hour - 6, 5]).first()
        time_start = (now - timedelta(seconds=6)).replace(microsecond=0)
        time_end = time_start + timedelta(seconds=5)
    else:
        # if we're at second close to 0, then return whatever avaialable for that hour (usually no data yet)
        accel = Accel.objects(id=accel_id).fields(slice__z=[0, second_of_hour], slice__n=[0, second_of_hour],
                                                  slice__e=[0, second_of_hour]).first()
        time_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_end = time_start + timedelta(seconds=second_of_hour)
    # Flatten
    if accel:
        accel_z_data = [item for sublist in accel.z for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]
        accel_n_data = [item for sublist in accel.n for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]
        accel_e_data = [item for sublist in accel.e for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]
    else:
        accel_z_data = []
        accel_n_data = []
        accel_e_data = []
    # logger.debug('z=%s', accel.z)
    # logger.debug('accel_z_data=%s', accel.z)

    template = loader.get_template('station/station_detail.html')
    context = {
        # 'page_title': _("Terms of Service"),
        'station': station,
        'station_name': station_name,
        'sample_rate': accel.sample_rate if accel else None,
        'station_json': json.dumps(station.to_dict()),
        'accel': accel,
        'accel_z_data_json': json.dumps(accel_z_data),
        'accel_n_data_json': json.dumps(accel_n_data),
        'accel_e_data_json': json.dumps(accel_e_data),
        'time_start': time_start.isoformat(),
        'time_end': time_end.isoformat(),
    }
    return HttpResponse(template.render(context, request))
