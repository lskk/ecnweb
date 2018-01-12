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
    accel = Accel.objects(id=accel_id).fields(slice__z=[now.minute, 1], slice__n=[now.minute, 1], slice__e=[now.minute, 1]).first()
    logger.debug('Accel %s minute=%d: %s', accel_id, now.minute, accel)
    if accel.z[0]:
        logger.debug('Accel z=%s n=%s e=%s', len(accel.z[0]), len(accel.n[0]), len(accel.e[0]))
        if accel.z[0][0]:
            logger.debug('Samples/second: z=%s n=%s e=%s', len(accel.z[0][0]), len(accel.n[0][0]), len(accel.e[0][0]))
    now_second = now.second
    if now_second > 5:
        # only the previous seconds (because current second is not yet avaiable)
        accel.z[0] = accel.z[0][now.second - 5 : now.second]
        accel.n[0] = accel.n[0][now.second - 5 : now.second]
        accel.e[0] = accel.e[0][now.second - 5 : now.second]
        time_start = now.replace(second=now.second - 1, microsecond=0)
        time_end = time_start + timedelta(seconds=5)
    else:
        # if we're at second 0, then return only that second (usually no data yet)
        accel.z[0] = accel.z[0][now.second: now.second + 5]
        accel.n[0] = accel.n[0][now.second: now.second + 5]
        accel.e[0] = accel.e[0][now.second: now.second + 5]
        time_start = now.replace(second=now.second, microsecond=0)
        time_end = time_start + timedelta(seconds=5)
    accel_z_data = [item for sublist in accel.z[0] for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]
    accel_n_data = [item for sublist in accel.n[0] for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]
    accel_e_data = [item for sublist in accel.e[0] for item in (sublist if sublist else [None for i in range(accel.sample_rate)])]

    template = loader.get_template('station/station_detail.html')
    context = {
        # 'page_title': _("Terms of Service"),
        'station': station,
        'station_name': station_name,
        'station_json': json.dumps(station.to_dict()),
        'accel': accel,
        'accel_z_data_json': json.dumps(accel_z_data),
        'accel_n_data_json': json.dumps(accel_n_data),
        'accel_e_data_json': json.dumps(accel_e_data),
        'time_start': time_start.isoformat(),
        'time_end': time_end.isoformat(),
    }
    return HttpResponse(template.render(context, request))
