import csv
import re
import time
import calendar
import os
# 3rd party
import requests
# local
import config

REQUEST_METHODS = ['GET', 'POST', 'PUT', 'HEAD']
CSV_FIELDS = ['timestamp', 'response_time', 'status_code', 'down']

for site in config.SITES:
    if 'url' not in site:
        print 'No URL for that site: %s' % site
        continue

    if 'http_method' not in site or site['http_method'] not in REQUEST_METHODS:
        site['http_method'] = 'GET'

    if 'timeout' not in site:
        site['timeout'] = config.GLOBAL_TIMEOUT

    # Do request
    r = requests.request(site['http_method'], site['url'], timeout=site['timeout'])

    # Check response body lines
    string_match = None

    if r.status_code == 200 and 'body_string' in site:
        string_match = False

        for line in r.iter_lines():
            if not re.search(site['body_string'], line):
                continue

            string_match = True
            break

    # Create CSV line
    csv_line = {}
    csv_line['timestamp'] = calendar.timegm( time.gmtime() )
    csv_line['url'] = r.url
    csv_line['status_code'] = r.status_code
    csv_line['response_time'] = float(r.elapsed.seconds) + float(r.elapsed.microseconds)/1000000.0

    if string_match is not None and not string_match:
        csv_line['down'] = 'Y'
    elif r.status_code <> 200:
        csv_line['down'] = 'Y'
    else:
        csv_line['down'] = 'N'

    monitor_filename = config.MONITOR_FILE.format(**site)
    monitor_new = False

    try:
        file_stat = os.stat(monitor_filename)

        if file_stat.st_size < 5:
            monitor_new = True

    except OSError:
        monitor_new = True

    with open(monitor_filename, '%sb' % 'w' if monitor_new else 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, CSV_FIELDS, extrasaction='ignore')

        if monitor_new:
            csv_writer.writeheader()

        csv_writer.writerow(csv_line)
