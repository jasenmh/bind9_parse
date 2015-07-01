#!/usr/bin/env python

import sys
import re
from datetime import datetime

prev_dt = None
curr_dt = None
prev_count = None
curr_count = None
cma = None
cma_count = 0
init_avg = [ 0 ]
INIT_SZ = 16	# this needs to be an odd number + 1 (eg. 16 = 15 + 1)
real_count = -1
dt = None

def report_state():
	print "\n  *****"
	print "init_avg size: %s" % str(len(init_avg)) if init_avg else "None"
	print "prev_dt: %s\tcurr_dt: %s" % ( str(prev_dt) if prev_dt else "None", str(curr_dt) if curr_dt else "None")
	print "prev_count: %s\tcurr_count: %s" % (str(prev_count) if prev_count else "None", str(curr_count) if curr_count else "None")
	print "real_count: %s\t\tdt: %s" % (str(real_count) if real_count else "None", dt if str(dt) else "None")
	print "cma num: %s\tcma_count: %d" % (str(cma) if cma else  "None", cma_count)
	print "  *****\n"


for line in iter(sys.stdin):
	if line[0] == '#':
		continue	# skip comment lines

	dt_string = line[::-1][ (line[::-1].find(' ') + 1): ][::-1].replace('-', ' ')
	dt_string = dt_string.split('.')[0]
	prev_dt = curr_dt
	curr_dt = datetime.strptime(dt_string, '%Y %m %d %X')
	if prev_dt:
		dt  = (curr_dt - prev_dt).seconds

	prev_count = curr_count
	curr_count = int(line.split()[2])
	if prev_count:
		real_count = curr_count - prev_count

	# report_state()

	# write request count for that interval, req/sec doesn't make sense with < 300 reqs per interval
	if dt and real_count >= 0:
		print "%s %f" % (str(curr_dt), real_count)


	# calculate cummulative moving average
	if init_avg and len(init_avg) < INIT_SZ and real_count >= 0:	# fill list with initial values
		init_avg.append(real_count)
	
	if init_avg and len(init_avg) == INIT_SZ:			# calc initial average
		cma_count = float( len(init_avg) - 1 )
		cma = sum(init_avg) / cma_count
		init_avg = None
		
	if not init_avg:						# continue average
		cma = (real_count + (cma_count * cma)) / (cma_count + 1)
		cma_count += 1


if cma:
	rrate = cma / 300
	print "avg req/sec:%f" % rrate
else:
	print "avg req/sec:ERROR"

