
# Trip Extraction

### Project setup

- poetry
  - pre-commit
    - flake8
    - black
    - mypy
    - isort


### Distance Calculate

In the file trip-extration/const.py there is two way to calculate distance using the libary geopy, we currently using distance geodesic, but we can also change the const  `DISTANCE_FORMULA` to use great_circle
