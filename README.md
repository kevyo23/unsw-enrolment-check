# UNSW Course Enrolment Capacity Check  

![GitHub last commit](https://img.shields.io/github/last-commit/kevyo23/unsw-enrolment-check)
![Supported Python versions](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)

Simple script that logs into myUNSW via Web SSO and reports on the enrolment capacity of your desired course (it must already be loaded in your courses list).

This operation is passive and will not modify the state of your enrolment, only scrape and read off the static content of the course list page.

![Notifier Example](./notifier_example.png)


## Getting Started

### Install dependencies
`pip3 install -r requirements.txt`

### Configure keyring
With [keyring](https://pypi.org/project/keyring/) installed, configure your zid password in terminal `keyring set zid YOUR_ZID`

### Configure script variables

| Variable name      | Regex match        | Example value
| -------------      | -------------      | --------------
| Year of enrolment  | `r'\d{4}'`         | 2020
| Course code        | `r'[A-Z]{4}\d{4}'` | MATH3411
| Student zid        | `r'z\d{7}'`        | z0000000

Year of enrolment, Course code and Student zid will need to have valid values in `course_availability.py`. Optionally set VERBOSE for notifications even if desired course is full.

### Run manually
`python3 course_availability.py`

or

`sh course_availability.sh`

### Setup crontab
`crontab -e` -> `* * * * * sh ABSOLUTE_PATH_TO_SH`

Tailor schedule expressions on [Crontab Guru](https://crontab.guru/)

Debug crontab output by switching from `course_availability.sh` to `course_availability_DEBUG.sh`.

### Expected alert format
If there is space:
`SPACE AVAILABLE FOR COURSE_CODE`

If VERBOSE or there is space:
`COURSE_CODE is (almost full|full) with ('OCCUPIED', 'TOTAL')`

