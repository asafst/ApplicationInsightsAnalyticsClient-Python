import requests
import dateutil.parser
import re
import numpy as np
import json

SERVICE_ENDPOINT = 'https://api.applicationinsights.io'
QUERY_ENDPOINT_PATH_TEMPLATE = 'beta/apps/{0}/query'

# Regex for TimeSpan
TIMESPAN_PATTERN = re.compile(r'((?P<d>[0-9]*).)?(?P<h>[0-9]{2}):(?P<m>[0-9]{2}):(?P<s>[0-9]{2})(.(?P<ms>[0-9]*))?')

class AnalyticsClient(object):
    """Analytics Client"""

    def __init__(self, app_id = None, app_key = None):
        if not app_id:
            self._get_app_config_from_file()
        else:
            self._app_id = app_id
            self._app_key = app_key

    def query(self, query, timespan=None):
        data = { 'query' :  query }
        if timespan:
            data['timespan'] = timespan
        headers = { 
            'x-api-key': self._app_key,
            'Content-Type': 'application/json',
            'Accept-Encoding': 'gzip,deflate'
            }
        full_url = '{0}/{1}'.format(SERVICE_ENDPOINT, QUERY_ENDPOINT_PATH_TEMPLATE.format(self._app_id))
        response = requests.post(full_url, headers=headers, json=data)
        
        # validate response was good
        response.raise_for_status()

        # get the data table
        data = response.json()
        tables = data["Tables"]
        data_table = tables[0]

        result_parser = AnalyticsResultParser(data_table)
        return result_parser.to_result_dictionary()

    def _get_app_config_from_file(self):
        import os.path
        local_config_file = '.analytics_client_config'

        file_path = os.path.join('.', local_config_file)
        if not os.path.isfile(file_path):
              file_path = os.path.join(os.path.expanduser('~'), local_config_file)
              if not os.path.isfile(file_path):
                  raise Exception('App id and key must be provided')
        
        with open(file_path) as data_file:
            data = json.load(data_file)

        self._app_id = data['appId']
        self._app_key = data['appKey']


###################
## Analytics Resposne Converters
###################
class AnalyticsTypesConverter(object):
    
    @staticmethod
    def convert_if_needed(value, data_type):
        types_to_convert = {'DateTime': AnalyticsTypesConverter.to_datetime, 'TimeSpan': AnalyticsTypesConverter.to_timedelta}
        if data_type in types_to_convert:
            return types_to_convert[data_type](value)
        else:
            return value

    @staticmethod
    def to_datetime(value):
        if value is None:
            return None
        return dateutil.parser.parse(value)

    @staticmethod
    def to_timedelta(value):
        if value is None:
            return None
        m = TIMESPAN_PATTERN.match(value)
        if m:
            return timedelta(
                days=int(m.group('d') or 0),
                hours=int(m.group('h')),
                minutes=int(m.group('m')),
                seconds=int(m.group('s')),
                milliseconds=int(m.group('ms') or 0))
        else:
            raise ValueError('Timespan value \'{}\' cannot be decoded'.format(value))

class AnalyticsResultParser(object):
    
    def __init__(self, json_result):
        self.json_result = json_result
        
    def to_result_dictionary(self):
        column_names = []
        column_types = []
        for c in self.json_result['Columns']:
            column_names.append(c['ColumnName'])
            column_types.append(c['DataType'])
        rows = self.json_result['Rows']

        result_dict = {}
        for row in rows:
            for index, value in enumerate(row):
                # if empty, create list of values
                if not (column_names[index] in result_dict):
                    result_dict[column_names[index]] = []
                
                # add to the result dict, convert type if needed
                result_dict[column_names[index]].append(AnalyticsTypesConverter.convert_if_needed(value, column_types[index]))

        return AnalyticsResult(column_names, result_dict)        


###################
## Analytics Result
###################
class AnalyticsResult(dict):
    def __init__(self, column_names, *args, **kwargs):
        super(AnalyticsResult, self).__init__(*args, **kwargs)
        self.column_names = column_names

    def row_iterator(self):
        return AnalyticsRowIterator(self)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            val = dict.__getitem__(self, self.column_names[key])
        else:
            val = dict.__getitem__(self, key)
        return np.asarray(val)


###################
## Analytics Row Iterator
###################
class AnalyticsRowIterator(object):
    """ Iterator over returned rows """
    def __init__(self, result_dict):
        self.result_dict = result_dict
        self.next = 0
        self.last = len(result_dict[0]) if len(result_dict) > 0 else 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.__next__()

    def __next__(self):
        if self.__next__ >= self.last:
            raise StopIteration
        else:
            single_row_dict = {}
            for column_name in list(self.result_dict.keys()):
                single_row_dict[column_name] = self.result_dict[column_name][self.__next__]
            self.next = self.next + 1
            return SingleRow(list(self.result_dict.keys()), single_row_dict)

class SingleRow(dict):
    """ Simple wrapper around dictionary, to enable both index and key access to rows in result """
    def __init__(self, column_names, *args, **kwargs):
        super(SingleRow, self).__init__(*args, **kwargs)
        # TODO: this is not optimal, if client will not access all fields.
        # In that case, we are having unnecessary perf hit to convert Timestamp, even if client don't use it.
        # In this case, it would be better for KustoResult to extend list class. In this case,
        # KustoResultIter.index2column_mapping should be reversed, e.g. column2index_mapping.
        self.column_names = column_names

    def __getitem__(self, key):
        if isinstance(key, int):
            val = dict.__getitem__(self, self.column_names[key])
        else:
            val = dict.__getitem__(self, key)
        return val



