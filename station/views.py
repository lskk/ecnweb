import json
import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader

from station.mongomodels import Station, StationState

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
