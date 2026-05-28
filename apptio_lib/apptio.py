"""
Copyright IBM All Rights Reserved.

SPDX-License-Identifier: Apache-2.0
"""

import os
import sys
import csv
import json
import locale
import requests
from datetime import datetime


def get_auth(region='', public=None, private=None):
    if not public and not private:
        print('No public and/or private keys given. Aborting.')
        return False
    if region:
        if region[0] != '-':
            region = f'-{region}'

    token_uri = f'https://frontdoor{region}.apptio.com/service/apikeylogin'
    token = token_getter(token_uri, public, private)

    return token


def token_getter(uri, key=None, secret=None):

    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    data = {
        "keyAccess": key,
        "keySecret": secret
    }
    data = json.dumps(data)

    response = requests.post(
        uri,
        data=data,
        headers=headers
    )

    if not response.ok:
        if response.status_code == 400:
            if 'deactivated' in response.content.decode('utf-8'):
                return 'deactivated'
            
        print(f'URI: "{uri}"\n\nError Code[{response.status_code}]\n\nError content: {response.content}')
        return False

    return response.cookies['apptio-opentoken']


def make_opentoken_headers(opentoken='', key='', secret='', env_id=''):
    if not env_id:
        print('No environment ID provided. Aborting.')
        return {}
    if not opentoken and not (key and secret):
        print('No OpenToken or key/secret provided. Aborting.')
        return {}
    if not opentoken:
        opentoken = token_getter(key, secret)
        if not opentoken:
            print('Failed to get OpenToken. Aborting.')
            return {}

    headers = {
            'Accept': 'text/csv',
            'apptio-opentoken': opentoken,
            'apptio-current-environment': env_id,
            'app-type': 'Flagship',
            'app-version': 'US'
    }


def get_environment_id(domain, token, region='', environment_name='main'):
    """
    Get environment ID from domain name using frontdoor API.
    
    Args:
        domain (str): The domain name (e.g., 'customer-name')
        token (str): The apptio-opentoken
        region (str): Region suffix ('', 'eu', 'au', 'me', etc.)
        environment_name (str): Environment name (default: 'main')
                               Some customers may have different environment names
    
    Returns:
        str: Environment ID or None if failed
    """
    if region and region[0] != '-':
        region = f'-{region}'
    
    url = f'https://frontdoor{region}.apptio.com/api/environment/{domain}/{environment_name}'
    headers = {
        'Content-Type': 'application/json',
        'apptio-opentoken': token
    }
    
    response = requests.get(url, headers=headers)
    
    if not response.ok:
        print(f'Failed to get environment ID for domain "{domain}" and environment "{environment_name}":')
        print(f'Status Code: {response.status_code}')
        print(f'Response: {response.content.decode("utf-8")}')
        return None
    
    try:
        env_data = response.json()
        return str(env_data['id'])
    except (KeyError, json.JSONDecodeError) as e:
        print(f'Error parsing environment ID response: {e}')
        return None


def setup_frontdoor_auth(public_key, private_key, domain, region='', environment_name='main'):
    """
    Complete frontdoor authentication setup.
    Gets token and environment ID, then returns headers ready for API calls.
    
    Args:
        public_key (str): Frontdoor public key
        private_key (str): Frontdoor private key
        domain (str): Domain name
        region (str): Region suffix (optional: '', 'eu', 'au', 'me')
        environment_name (str): Environment name (default: 'main')
                               Some customers may have different environment names
    
    Returns:
        dict: Headers with apptio-opentoken and apptio-current-environment,
              or None if authentication failed
    """
    if not public_key or not private_key:
        print('Error: Both public and private keys are required')
        return None
    
    if not domain:
        print('Error: Domain name is required')
        return None
    
    # Get token from frontdoor
    token = get_auth(region=region, public=public_key, private=private_key)
    if not token or token == 'deactivated':
        if token == 'deactivated':
            print('Error: API keys have been deactivated')
        else:
            print('Error: Failed to obtain authentication token')
        return None
    
    # Get environment ID
    env_id = get_environment_id(domain, token, region, environment_name)
    if not env_id:
        print('Error: Failed to get environment ID')
        return None
    
    # Create headers for API calls
    headers = {
        'apptio-opentoken': token,
        'apptio-current-environment': env_id,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    return headers

    return headers


def get_apptio_table(uri, token, env_id):
    headers = {
            'Accept': 'text/csv',
            'apptio-opentoken': token,
            'apptio-current-environment': env_id,
            'app-type': 'Flagship',
            'app-version': 'US'
        }

    response = requests.get(
        uri,
        headers=headers
    )

    if not response.ok:
        print(
            f'URI: "{uri}"\n\nError Code[{response.status_code}]\n\nError content: {response.content}')

    else:
        print(len(response.content))
        return response.content.decode(response.encoding or 'utf-8')
        return response.content
    

def format_fiscal_date(date, year_start=1):
    """
    Format a date into Apptio fiscal date format. e.g. "Jan:FY2023".
    args:
        date (str or datetime): 
            The date to format. Can be a string in 'YYYY-MM-DD' format or a datetime object.
        year_start (int): 
            The month when the fiscal year starts Default is 1.

    returns:
        str: 
            The formatted fiscal date string in the format "MMM:FYYYYY".
    """
    if not isinstance(date, datetime):
        try:
            date = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print(f"Invalid date format: {date}. Expected 'YYYY-MM-DD'.")
            return None

    # We need the English month abbreviations. e.g. Jan, Oct, Dec, etc.
    # this uses your locale, so we'll set it to US English.
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    month = date.strftime("%b")
    year = date.strftime('%Y')
    
    # If the fiscal year starts after January, we may need to adjust the year.
    if year_start > 1 and int(date.strftime('%m')) >= year_start:
        year = str(int(year) + 1)

    return f'{month}:FY{year}'


def load_config():
    """
    Load configuration from config.json file.
    Local files should only be used for testing and development.
    In production, use environment variables or a secure vault.
    
    Expected config structure:
    # Region should be, '', 'eu', 'au', 'me' etc. matching Frontdoor region in URL.
    # i.e. https://frontdoor-au.apptio.com
    # Only one authenticsation method is needed, either keyAccess/keySecret or cldyKey.
    {
        "cldyKey": "your_cloudability_api_key",
        "keyAccess": "your_access_key",
        "keySecret": "your_secret_key",
        "apptio-current-environment": "environment_name"
        "region": ''
    }
    
    Returns:
        dict: Configuration dictionary containing API credentials and environment
    """
    # See if file exists
    if not os.path.exists('config.json'):
        print('No config.json file found.')
        # Create blank config.json.
        with open('config.json', 'w') as f:
            json.dump({
                "cldyKey": "",
                "keyAccess": "",
                "keySecret": "",
                "apptio-current-environment": "",
                "region": ""
            }, f, indent=4)
        print('Created blank config.json file. Please edit it with your credentials.')
        return False
    
    with open('config.json', 'r') as f:
        return json.load(f)
