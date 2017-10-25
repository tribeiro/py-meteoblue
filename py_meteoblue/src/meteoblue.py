
import json
import urllib3
import logging
from astropy.io import ascii

log = logging.getLogger(__name__)

class MeteoBlue(object):

    _params = {'package': {'arg': 'http://my.meteoblue.com/packages/', 'value': 'basic-1h?*', 'required': True,
                       'description': 'This identifies the address and our basic data package in hourly resolution.',
                       'valid': None},
               'apikey': {'arg': '?apikey=', 'value': None, 'required': True,
                          'description': 'add your personal API Key', 'valid': None},
               'lat': {'arg': '&lat=', 'value': None, 'required': True,
                       'description': 'WGS84 coordinates for location; altitude in meters above mean sea level; '
                                      'if no altitude is specified, the elevation will be determined and used',
                       'valid': None},
               'lon': {'arg': '&lon=', 'value': None, 'required': True,
                       'description': 'WGS84 coordinates for location; altitude in meters above mean sea level; '
                                      'if no altitude is specified, the elevation will be determined and used',
                       'valid': None},
               'asl': {'arg': '&asl=', 'value': None, 'required': True,
                       'description': 'WGS84 coordinates for location; altitude in meters above mean sea level; '
                                      'if no altitude is specified, the elevation will be determined and used',
                       'valid': None},
               'tz': {'arg': '&tz=', 'value': None, 'required': False,
                      'description': 'IANA timezone of selected place', 'valid': None},
               'name': {'arg': '&name=', 'value': None, 'required': False,
                        'description': 'Name of city or place. Will be passed to the response directly',
                        'valid': None},
               'city': {'arg': '&city=', 'value': None, 'required': False,
                        'description': 'Name of city or place. Will be printed on the image', 'valid': None},
               'lang': {'arg': '&lang=', 'value': None, 'required': False,
                        'description': 'language for images (iso2 code)',
                        'valid': ['es', 'de', 'fr', 'it', 'es', 'pt', 'tr', 'ro', 'ru', 'nl', 'hu']},
               'temperature': {'arg': '&temperature=', 'value': None, 'required': False,
                               'description': 'Temperature unit. Celsius (C) and Fahrenheit (F)',
                               'valid': ['C', 'F']},
               'windspeed': {'arg': '&windspeed=', 'value': None, 'required': False,
                             'description': 'Wind speed unit. meter per second (ms-1), kilometer per hour (kmh), '
                                            'miles per hour (mph), knot (kn), beaufort (bft)',
                             'valid': ['ms-1', 'kmh', 'mph', 'kn', 'bft']},
               'winddirection': {'arg': '&winddirection=', 'value': None, 'required': False,
                                 'description': 'wind direction unit. degrees (degree), 2 character (2char), '
                                                '3 character (3char)', 'valid': ['degree', '2char', '3char']},
               'timeformat': {'arg': '&timeformat=', 'value': None, 'required': False,
                              'description': 'time format. YYYY-MM-DD hh:mm, YYYYMMDD hh:mm, timestamp_utc, '
                                             'timestamp_ms_utc, iso8601',
                              'valid': ['YYYY-MM-DD hh:mm', 'YYYYMMDD hh:mm', 'timestamp_utc',
                                        'timestamp_ms_utc', 'iso8601']},
               'format': {'arg': '&format=', 'value': 'csv', 'required': False,
                          'description': 'output format. json or csv', 'valid': ['json', 'csv']},
               }
    def __init__(self, config=None):

        self.load_configuration(config)

        # Check that the required configuration was passed. Issue warning if not
        for key in self._params.keys():
            if self._params[key]['required'] and self._params[key]['value'] is None:
                log.warning('Required parameter "%s" not set. Won\'t be able to purge information from server.' % key)

    def make_query_url(self):

        query_str = self._params['package']['arg']+self._params['package']['value']

        for key in self._params.keys():

            if self._params[key]['required'] and self._params[key]['value'] is None:
                raise IOError('Required parameter "%s" not set. Won\'t be able to purge '
                              'information from server.' % key)

            elif key != 'package' and self._params[key]['value'] is not None:
                query_str += '%s%s' % (self._params[key]['arg'], self._params[key]['value'])

        return query_str

    def load_configuration(self, config):
        # Load configuration

        if config is not None:
            with open(config) as fp:
                params = json.loads(fp.read())
                for key in params.keys():
                    if key in self._params:
                        log.info('Setting %s -> %s' % (key, params[key]))
                        self._params[key]['value'] = params[key]
                    else:
                        log.warning('Parameter "%s" not in parameter list.' % key)

    def query(self, unpack=True, skip_error=False):

        query_str = self.make_query_url()
        http = urllib3.PoolManager()
        query_result = http.request('GET', query_str)

        if "error_message" in query_result.data.decode('utf-8') and (not skip_error or unpack):
            raise IOError(query_result.data.decode('utf-8'))
        elif "error_message" in query_result.data.decode('utf-8'):
            log.warning(query_result.data.decode('utf-8'))

        if unpack:
            return ascii.read(query_result.data.decode('utf-8'))

        return query_result
