# Apptio-Tools-Lib
Python library for use with python scripts in Apptio-Tools repository.

## Overview

This library provides Python modules for interacting with Cloudability and Apptio APIs, including:
- **Cloudability API wrapper** - HTTP request handling for Cloudability v3 API
- **Apptio authentication** - Frontdoor public/private key authentication
- **Report parsing** - Utilities for processing API responses

## Usage

This library is primarily used with tools found in the [Apptio Tools](https://github.com/IBM/apptio-tools) repository, though you're welcome to use it with any of your own integrations and/or automations.

## Features

### Cloudability Module (`apptio_lib.cloudability`)

- HTTP methods: `get()`, `post()`, `put()`, `delete()`
- Supports both API key and frontdoor authentication
- Regional support (US, EU, APAC, ME)
- Report parsing utilities
- Business mapping error handling

### Apptio Module (`apptio_lib.apptio`)

- **Frontdoor Authentication:**
  - `get_auth()` - Obtain authentication token
  - `get_environment_id()` - Retrieve environment ID from domain
  - `setup_frontdoor_auth()` - Complete authentication setup
- **Utilities:**
  - `format_fiscal_date()` - Convert dates to fiscal format
  - `load_config()` - Load configuration from JSON

## Authentication

The library supports two authentication methods:

### 1. Cloudability API Key
```python
from apptio_lib import cloudability as cldy

api_key = 'your_api_key'
response = cldy.get('/account_groups', api_key=api_key)
```

### 2. Frontdoor Public/Private Keys
```python
from apptio_lib import apptio, cloudability as cldy

# Setup authentication
headers = apptio.setup_frontdoor_auth(
    public_key='your_public_key',
    private_key='your_private_key',
    domain='your_domain',
    region='',  # Optional: '', 'eu', 'au', 'me'
    environment_name='main'  # Optional: defaults to 'main'
)

# Make API calls
response = cldy.get('/account_groups', opentoken_headers=headers)
```

## State of the Project

The library is stable and production-ready. Tests need to be written, though.

## Installation

You can install this library using `pip` in several ways. Below are the recommended methods.

### Standard Installation from GitHub

This is the most common method for installing the latest stable version of the library directly from GitHub. This requires `git` to be installed on your system.

```bash
pip install git+https://github.com/IBM/Apptio-Tools-Lib.git
```

To install a specific version or release, you can specify a tag:

```bash
pip install git+https://github.com/IBM/Apptio-Tools-Lib.git@v1.0.0
```

### Installation without Git

If you do not have `git` installed, you can still install the library using the direct HTTPS URL to the repository's zip file.

```bash
pip install https://github.com/IBM/Apptio-Tools-Lib/archive/refs/heads/main.zip
```

You can also install a specific version by providing the URL to that version's zip file.

### Developer Installation

If you intend to contribute to the development of this library, you should clone the repository and install it in "editable" mode. This allows you to make changes to the source code and have them reflected in your environment without needing to reinstall the package.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/IBM/Apptio-Tools-Lib.git
    ```

2.  **Navigate to the project directory:**
    ```bash
    cd Apptio-Tools-Lib
    ```

3.  **Install in editable mode:**
    ```bash
    pip install -e .
    ```

Don't forget the period there! If you're unfmailiar with package development, that can be an easy thing to miss. It just means that we're pointing pip to the current directory we're in.

## Disclaimer
These tools are provided as-is and are primarily intended to be used as examples for your own integrations. IBM Apptio does not provide direct support for this library, but do feel free to report bugs by [opening an issue](https://github.com/IBM/Apptio-Tools-Lib/issues)