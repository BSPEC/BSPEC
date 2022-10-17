# BSPEC
> BSPEC: A python based Plugin, Entity Component System (ECS) architecture designed with Business Specifications in mind. This package allows you to easily set up and use existing systems and components. Write custom systems and components that can be dynamically loaded. Its minimal dependencies and extensions make it ideal for projects that use Python 3.

# Status of the project

The BSPEC is still under initial development and is being tested with the Python 3.9.6 version.

The BSPEC will follow semantic versioning for its releases, with a `{MAJOR}.{MINOR}.{PATCH}{PYTAGNUM}` scheme for versions numbers, where:

* `MAJOR` versions might introduce breaking changes
* `MINOR` versions usually introduce new features and might introduce deprecations
* `PATCH` versions only introduce bug fixes
* `PYTAGNUM` PYTAG + NUM (no white-space in between), Tags are converted to a short form (-alpha -> a0)

# Overview
* [Status of the project](#status-of-the-project)
* [Requirements](#requirements)
  * [Python](#python)
  * [Dependencies](#dependencies)
* [Quickstart](#quickstart)
* [Changes to Repo](#changes-to-repo)

## Requirements
### Python
* Download and install [Python](https://www.python.org/downloads/) (suggested [3.9.6](https://www.python.org/downloads/release/python-396/)) if you do not already have it installed.
    * Ensure `pip` is installed (pip should be installed already because it comes with the latest versions of python) in case it is not, please install it from here: https://pip.pypa.io/en/stable/installing/
        * To check if pip is installed, you can run the following command in your terminal
```shell
python -m pip --version

```

## Setup

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
cd <Path To>/my_awesome_project

python -m venv venv

venv\Scripts\activate

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
cd <Path To>/my_awesome_project

python -m venv venv

source venv/bin/activate

```

### Dependencies

> Once you have installed Python and `pip` and activated your `environment`, you will need to install a dependency for the any plugins:
```shell
pip install --no-cache-dir -r requirements.txt

bumpver init

```

## Quickstart

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
pip install BSPEC

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
pip install BSPEC

```


## Changes to Repo

### Windows
* Open new terminal
    * "Windows-Key + R" will show you the 'RUN' box
    * Type "cmd" to open the terminal
```shell
bumpver update --minor

```
### Linux / Mac
* Open new terminal
    * "Control + Option + Shift + T" to open the terminal
```shell
bumpver update --minor

```
>**Note:** BumpVer integrates with your version control system. It’ll refuse to update your files if you have uncommitted changes in your repository.


You can change different versions with different key words:
> **Note:** `test` lets you see what the changes to a given version string would look like
```shell
bumpver test '1.2.3' 'MAJOR.MINOR.PATCH[PYTAGNUM]' --major
New Version: 2.0.0

bumpver test '1.2.3' 'MAJOR.MINOR.PATCH[PYTAGNUM]' --minor
New Version: 1.3.0

bumpver test '1.2.3' 'MAJOR.MINOR.PATCH[PYTAGNUM]' --patch
New Version: 1.2.4

bumpver test '1.2.3' 'MAJOR.MINOR.PATCH[PYTAGNUM]' --patch --tag=beta
New Version: 1.2.4b0

bumpver test '1.2.4b0' 'MAJOR.MINOR.PATCH[PYTAGNUM]' --tag-num
New Version: 1.2.4b1
```

To do this on a commit version, remove `test`, the number e.g. `'1.2.3'` and the structure format `'MAJOR.MINOR.PATCH[PYTAGNUM]'` resulting in:
```shell
bumpver update --patch

```

