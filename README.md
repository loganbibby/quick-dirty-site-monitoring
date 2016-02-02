# quick-dirty-site-monitoring
Checks the status of a site and writes the result to a CSV file.

## Prerequisites
You can run `pip install -r requirements.txt` to install any requsite libraries.

## Configuration
Configuration is done with the *config.py* file. An example is included in the repo.

*MONITOR_FILE* - Filename template for storing results. Each site gets it's own file. You can use any name in the site dictionary to format the filename.
*GLOBAL_TIMEOUT* - Timeout value given to Requests when _timeout_ value missing from site dictionary.
*SITES* - List of site dictionaries.

### Sites
*name* - Unique name for the site. Currently only used in the MONITOR_FILE config variable, so it's not necessary required.
*url* - Required. The exact URL to query.
*method* - One of GET, POST, PUT, or HEAD. Defaults to GET.
*body_string* - A regex string that should match a line of the response body if the site is up. (Script defaults to a status code 200 meaning UP.)
*wordpress* - Boolean for if the site is Wordpress or not. (Reserved for future use.)

## Usage
It's a simple `python monitor.py` run. It does it's job and exits. I have mine set to run each minute by crontab. 
