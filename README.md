# Apptio-Tools-Lib
Python library for use with python scripts in Apptio-Tools repository.

## Usage
This librarary is primarily used with tools found in the [Apptio Tools](https://github.com/IBM/apptio-tools) repository, though you're welcome to use it with any of your own integrations and/or automations.

## State of the Project
The libarary is stable. Tests need to be written, though.

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