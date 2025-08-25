"""
Copyright IBM All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
"""

import json
import requests


def get(*args, **kwargs):
    kwargs['method'] = 'get'
    return request(*args, **kwargs)


def put(*args, **kwargs):
    kwargs['method'] = 'put'
    return request(*args, **kwargs)


def post(*args, **kwargs):
    kwargs['method'] = 'post'
    return request(*args, **kwargs)


def delete(*args, **kwargs):
    kwargs['method'] = 'delete'
    return request(*args, **kwargs)


def request(
        end_point,
        api_key=False,
        params=[],
        data={},
        method='',
        opentoken_headers={},
        region=''
    ):
    if not end_point:
        print('No endpoint specified.')
        return False

    if not api_key and not opentoken_headers:
        print('Authorization key and/or token missing.')
        return False

    methods = ['GET','PUT','POST','DELETE']

    method = method.upper()
    if not method or method not in methods:
        print('No valid method specified. get, put, post, delete are supported methods.')
        return False

    if 'https://' in end_point:
        url = end_point
    else:
        if region:
            region = f'-{region}'
        # Assume it's v3 if we're just getting the endpoint.
        # Note that then endpoint should have a leading slash.
        # /users, /business-mappings, etc.
        url = f'https://api{region}.cloudability.com/v3{end_point}'


    auth = (api_key, '')

    if method == 'get':
        headers = {'Accept': 'Application/json'}
    else:
        headers = {'content-type': 'application/json'}

    if opentoken_headers:
        headers = headers | opentoken_headers
        auth = ()

    payload = None
    if data:
        payload = json.dumps(data)

    request = requests.Request(
        method=method,
        url=url,
        auth=auth,
        params=params,
        data=payload,
        headers=headers
    ).prepare()

    response = requests.Session().send(request)
    
    if response.ok:
        if response.content:
            response = response.json()
        return response


    print('Request failed:')
    print('URL:', url)
    print('Method:', method)
    print('Data:')
    print(json.dumps(data, indent=2))
    print(str(response.status_code) + ' ' + response.reason)
    print(response.json())
    return response


def report_parser(response):
    dimensions = response['columnHeaders']['dimensions']
    metrics = [m['name'] for m in response['columnHeaders']['metrics']]

    rows = []
    for row in response['rows']:
        row_dimensions = row['dimensions']
        row_dimensions = dict(zip(dimensions, row_dimensions))
        row_metrics = [m['sum'] for m in row['metrics']]
        row_metrics = dict(zip(metrics, row_metrics))

        rows.append(row_dimensions | row_metrics)

    return rows


def get_report_from_params(params, api_key='', opentoken_headers={}, silent=False):

    '''
    Sample params:
    report_params = {
            'start': '2025-01-01',
            'end': '2025-01-31',
            'dimensions': ['account_identifier', 'enhanced_service_name'],
            'metrics': ['unblended_cost', 'total_adjusted_amortized_cost', 'usage_quantity'],
            'filters': ['enhanced_service_name==AWS EBS', f'resource_identifier=={resource_id}'],
            'viewId': '0'
        }
    '''

    uri_base = 'https://api.cloudability.com/v3/internal/reporting/cost/run?'
    joined_params = []
    for key, value in params.items():
        if type(value) is list:
            for obj in value:
                joined_params.append(f'{key}={obj}')
        else:
            joined_params.append(f'{key}={value}')
    end_point = uri_base + '&'.join(joined_params)
    if not silent:
        print('Creating report with the following parameters:')
        for param in joined_params:
            print(f'\t-{param}')
    response = get(end_point, api_key=api_key, opentoken_headers=opentoken_headers)
    if 'columnHeaders' not in response:
        return False

    return response


def parse_and_print_bm_errors(mapping, response):
    # Use this when PUT/POST to the BM endpoint gets a 400 error
    if isinstance(response,dict):
        return
    
    if response.status_code == 400:
        error_json = response.json()
        if 'error' not in error_json:
            print('Error: ', error)
            return
        
        if 'messages' not in error_json['error']:
            print('Error: ', error_json['error'])
            return
        
        split_errors = error_json['error']['messages'][0].split('\n')
        
        for error in split_errors:
            statement_number = False
            column = False
            key = False
            split_message = error.split(' ')
            if 'statement' in split_message:
                statement_number = split_message.index('statement') + 1
                statement_number = split_message[statement_number]
                # removing the 1st and last character of string
                statement_number = statement_number[1:-1]
                # print('statement_number')

            if 'column' in split_message:
                column = split_message.index('column') + 1
                column = split_message[column]

            if 'matchExpression:' in split_message:
                key = 'matchExpression'
            elif 'valueExpression:' in split_message:
                key = 'valueExpression'

            if statement_number and column and key:

                print(f'Error in statement: {statement_number}')
                print(f'Error in {key} at column {column}-ish')
                value = mapping['statements'][int(statement_number)-1][key]
                print(f'"{key}": "{value}"')
                # print carrot under the error
                col_padding = len(key) + 4
                print(' ' * (int(column)-5 + col_padding) + '^^^^^^^^')
    return