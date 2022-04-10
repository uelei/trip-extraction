
# Trip Extraction

Project to extract trips from a list of Waypoints

The trip extraction uses the following logic:

A trip is considered ended when a moving vehicle remains within a circle of 20 meters radius for longer than 5 minutes.
A trip is considered started when the vehicle moves outside the circle of 20 meters radius around its rest position.
If the change in distance is more than 10 km per minute, the waypoint "jumps" and should be ignored.

### Install

Python version used was 3.10.2
Install all dependencies using poetry

```shell
pyenv local 3.10.2
poetry install
```


### Usage

```shell
python trip-extraction.py --help

Usage: trip-extraction.py [OPTIONS] FILENAME

  This program process a filename with Waypoints and save all resulting trips
  into an output.

Arguments:
  FILENAME  [required]

Options:
  --output PATH                   Filename for the result output.  [default:
                                  trips.json]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
````



### Project code checks

- poetry
  - pre-commit
    - flake8
    - black
    - mypy
    - isort

```shell
pre-commit run --all-files

trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check yaml...............................................................Passed
check for added large files..............................................Passed
flake8...................................................................Passed
black....................................................................Passed
mypy.....................................................................Passed
isort....................................................................Passed
```



### Tests
```shell
pytest --cov=trip_extraction
=================================================================================== test session starts ====================================================================================
platform linux -- Python 3.10.2, pytest-7.1.1, pluggy-0.13.1
rootdir: /home/uelei/code/trip-extraction
plugins: cov-3.0.0
collected 16 items

tests/test_car.py ......                                                                                                                                                             [ 37%]
tests/test_cli.py ...                                                                                                                                                                [ 56%]
tests/test_trip.py .                                                                                                                                                                 [ 62%]
tests/test_trip_extraction.py .                                                                                                                                                      [ 68%]
tests/test_waypoint.py .....                                                                                                                                                         [100%]

---------- coverage: platform linux, python 3.10.2-final-0 -----------
Name                            Stmts   Miss  Cover
---------------------------------------------------
trip_extraction/__init__.py         8      0   100%
trip_extraction/calcs.py           10      1    90%
trip_extraction/const.py            4      0   100%
trip_extraction/exceptions.py       9      0   100%
trip_extraction/logger.py           9      0   100%
trip_extraction/model.py           75      0   100%
trip_extraction/processor.py       33      6    82%
---------------------------------------------------
TOTAL                             148      7    95%


==================================================================================== 16 passed in 0.40s ====================================================================================


```


PS. both trips distances are different from a sample data, I'm really curious where I miss.
