#!/usr/bin/env python3
# coding: utf-8

import requests, re, pprint, os, datetime, keyring

##### start modify these values
year    = 'YEAR_OF_ENROLMENT' # format r'\d{4}'
course  = 'YOUR_COURSE_CODE'  # format r'[A-Z]{4}\d{4}'
acct    = 'YOUR_STUDENT_ZID'  # format r'z\d{7}'
pwd     = keyring.get_password('zid', acct)
VERBOSE = 0                   # notify even if the course is full
##### end modify these values

s = requests.Session()
r = s.get("https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Fportal%2FadfAuthentication")
lt = re.findall(r'name="lt" value="(.*)" />\s+<input type="hidden" name="_eventId" value="submit" />', r.text)[0]
data = {
        'lt': lt,
        '_eventId': 'submit',
        'username': acct,
        'password': pwd,
        'submit': 'Agree+and+sign+on'
       }
r = s.post("https://ssologin.unsw.edu.au/cas/login?service=https%3A%2F%2Fmy.unsw.edu.au%2Fportal%2FadfAuthentication", data=data)

r = s.get("https://my.unsw.edu.au/active/studentClassEnrol/years.xml")
bsdsSequence = re.findall(r'bsdsSequence" value="(\d+)">', r.text)[0]
data = {
        'bsdsSequence': bsdsSequence,
        'year': year,
        'bsdsSubmit-update-enrol': ''
       }
r = s.post("https://my.unsw.edu.au/active/studentClassEnrol/years.xml", data=data)

patch_re    = re.compile(f'{course}<\/td>(.*)')
status_re   = re.compile(f'{course} is ((almost)? ?full)')
capacity_re = re.compile('<td class="text-center">(\d+) / (\d+)</td>')
patch       = patch_re.findall(r.text)[0]
status      = status_re.findall(patch)[0]
capacity    = capacity_re.findall(patch)[0]
time_now    = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

is_full = status[0] == 'full'
has_capacity = capacity[0] < capacity[1]

if (not is_full or has_capacity):
    os.system(f'/usr/local/bin/terminal-notifier -message "{time_now}\nSPACE AVAILABLE FOR {course}"')
    if (not VERBOSE):
        os.system(f'/usr/local/bin/terminal-notifier -message "{time_now}\n{course} is {status[0]} with {capacity}"')

if (VERBOSE):
    os.system(f'/usr/local/bin/terminal-notifier -message "{time_now}\n{course} is {status[0]} with {capacity}"')
