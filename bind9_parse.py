#!/usr/bin/env python

import sys
import re
from datetime import datetime

first_time = None
current_time = None
prev_time = None
query_next = False
accum_queries = False
query_count = None
part_query_count = None 
tmp_query_count = -1

header_re = re.compile('\++\s+Statistics Dump\s+\++\s+\((\d+)\)')
footer_re = re.compile('\-+\s+Statistics Dump\s+\-+\s+\((\d+)\)')
req_re = re.compile('\++\s+Incoming Requests\s+\++')
query_re = re.compile('\s+(\d+)\s+QUERY')

for line in iter(sys.stdin):

	# look for header line
	m = header_re.match(line)
	if m:	# found a header
		current_time = int(m.group(1))
		if not first_time:
			first_time = current_time
		if prev_time:
			prev_time = current_time
				
	# look for footer line
	m = footer_re.match(line)
	if m:
		prev_time = current_time

	# look for query number
	if query_next:
		m = query_re.match(line)
		if m:
			tmp_query_count= int(m.group(1))
			if not query_count:	# initial state
				query_count = tmp_query_count
			elif not accum_queries:	# just read count and store
				if tmp_query_count < query_count:	# server was restarted between stat runs, enter accumuate mode
					accum_queries = True
					part_query_count = tmp_query_count
				else:
					query_count = tmp_query_count
			else:	# in accumulate mode
				if tmp_query_count < part_query_count:	# server was reset again, accumulate query count and restart part_query_count
					query_count += part_query_count
					part_query_count = tmp_query_count
				else:
					part_query_count = tmp_query_count
		query_next = False

	# look for line preceding query number
	m = req_re.match(line)
	if m:
		query_next = True

# collect uncounted non-sequential counts
if part_query_count:
	query_count += part_query_count

dt = str(datetime.today())
if query_count:
	print "%s %d" % (dt, query_count)
else:
	print "%s failed to read query count" % dt
