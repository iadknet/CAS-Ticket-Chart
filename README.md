Parse CAS logs to track tickets granted per service over time.

Put chart.html and style.css in a web accessible directory such as /var/www/cas_chart/

Run the parser against your CAS log files.

Usage:

cat /path/to/cas.log | cas_parse.py > /var/www/cas_chart/cas_logs.json


