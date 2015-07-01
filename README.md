# Bind9 Parse script

## Requirements
* Python 2.7
* bind9, rndc

## Setup
1. Ensure named is configured to write stats to a file when `rndc stats` is called.
2. Copy bind9\_parse.py to /root.
3. Add to root crontab (`crontab -u root -e`):

	`*/5 * * * * /path/to/rndc stats;/root/bind9_parse.py < /path/to/named.stats >> /path/to/bind-request-count.log`

## Logging
Every 5 minutes, the script will parse the named stats file and track how many requests have been made. The result is
written to stdout in the format:

`<timestamp> <request_count>`

## Analysis
```$ bind9_analyze.pl < /path/to/bind-request-count.log > /path/to/analysis.log```
This will analyze the logged data and provide a time-stamped report of how many requests were received per reporting
interval and will end the report with the calculated requests-per-second.

## Heads Up
Named stats get reset when the service restarts. To account for this, the script watches for a resetting of the request
count and goes into an accumulation mode to account for the rebasing of the count. The best way to avoid missing counts
is to keep the time between cron runs low, 5 minutes in the example above. The best time will vary based on how often
your service is restarted.
