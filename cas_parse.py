#! /usr/bin/env python

import fileinput
import re

days = { }
global_service_counter = { }

for line in fileinput.input():
	
	# 2014-05-12 14:36:43,117 INFO [org.jasig.cas.CentralAuthenticationServiceImpl] - Granted service ticket [ST-720745-dFo5g7d5Bvl1gW5X3FxZ-cas] for service [https://my.csumb.edu/] for user [otte0123]
	
	# regular expression to grab day, time, service, user from line
	line_re = re.compile(r'(^\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}),\d+ INFO \[org.jasig.cas.CentralAuthenticationServiceImpl\] - Granted service ticket \[[^\]]*] for service \[([^\]]*)] for user \[([^\]]*)]')
	line_match = line_re.match(line)

	# if the match was successful
	if line_match:
		day = line_match.group(1)
		time = line_match.group(2)
		service = line_match.group(3)
		user = line_match.group(4)

		# strip service down to bare domain
		service_re = re.compile(r'^http[s]?:\/\/([^\/]+)\/.*')
		service = service_re.sub(r'\1', service)

		# track tickets granted per service, per day
		# if this day has not been initialized, create map
		if not days.has_key(day):
			days[day] = { } 

		# if the service on this day has not been initiazed, start counter, otherwise increment
		if not days[day].has_key(service):
			days[day][service] = 1
		else:
			days[day][service] += 1

		# track total tickets granted per service
		# if service has not been initialized, start counter, otherwise increment
		if not global_service_counter.has_key(service):
			global_service_counter[service] = 1
		else:
			global_service_counter[service] += 1


# start json object
print '{',
print '"cols": [',
print '{"id":"","label":"Date","pattern":"","type":"date"},',


# print the headers for each row, comma separated
# stepping through the services, sorted by most total tickets granted
# service[0] = service name # service[1] = total ticket count
print ','.join(['{"id":"","label":"%s (%s)","pattern":"","type":"number"}' % (service[0], service[1]) for service in sorted(global_service_counter.items(), key=lambda k: k[1], reverse=True)]),

# close header row
print '],',

# print rows of data
print '"rows": [',

# track rows to determine when to stop trailing comma
dcount = 0
total_day_count = len(days)

# sort the days in order so they render correctly on chart
for day in sorted(days):

	# increment the row counter
	dcount += 1

	# split the date into parts
	date_parts = day.split('-')

	year = date_parts[0]
	month = date_parts[1].lstrip("0")
	day_of_month = date_parts[2].lstrip("0")

	print '{"c":[{"v":"Date(%s, %s, %s)","f":null},' % (year, month, day_of_month),

	# insert data point for each service, sorted the same as headers
	print ','.join(['{"v":%d,"f":null}' % ( days[day].get(service[0], 0) ) for service in sorted(global_service_counter.items(), key=lambda k: k[1], reverse=True)]),

	print ']}',

	# print comma if not the last element
	if dcount != total_day_count:
		print ',',

print ']}',

