#!/usr/bin/python

import fileinput, re, collections


# Set how many unique apache errors will be displayed
APACHE_ERROR_SIZE = 30
# Set how many unique IP addresses will be displayed
IP_LIST_SIZE = 20


# Output email header
print "From: cloud@lps.usp.br"
print "To: cloud@lps.usp.br"
print "Subject: error.log AI"


print ''
print 'Unprocessed lines:'

lines = []
ipList = []

for line in fileinput.input():
    # Strip blank spaces
	line = line.strip()
	
	# Count IP occurence
	ipAddr = re.search(r'(?:\d{1,3}\.){3}\d{1,3}', line)
	if ipAddr:
		ipList.append(ipAddr.group(0))
	
	# Remove unique features
	line = re.sub(r'^\[[^]]*\]', '', line)
	line = re.sub(r'\[client [^]]*\]', '', line)
	line = re.sub(r'\[unique_id [^]]*\]', '', line)
	
	# Special processing for ModSecurity lines
	if re.search(r'\[error\]\s*ModSecurity', line):
		id = re.search(r'(\[id \"\d*\"\])', line)
		tag = re.search(r'(\[tag [^]]*\])', line)
		msg = re.search(r'(\[msg [^]]*\])', line)
		url = re.search(r'\[hostname "([^]]*)"\] \[uri "([^]]*)"\]', line)
		if id and tag and url:
			line = '[ModSecurity] ' + id.group(1) + ' ' + tag.group(1) + ' [URI ' + url.group(1)  + url.group(2) + ']'
		elif id and msg and url:
			line = '[ModSecurity] ' + id.group(1) + ' ' + msg.group(1) + ' [URI ' + url.group(1)  + url.group(2) + ']'
		else:
			print line

	# Append line
	lines.append(line)

# Count multiple instances and keep unique
errorCount = collections.Counter(lines)
ipCount = collections.Counter(ipList)


# Output in reverse occurence order
print ''
print '---apache error---'
for i in errorCount.most_common( APACHE_ERROR_SIZE ):
	print str(i[1]) + '\t\t' + i[0].strip()
print '---end of apache error---'

print ''
print '---IP listing---'
for i in ipCount.most_common( IP_LIST_SIZE ):
	print str(i[1]) + '\t\t' + i[0].strip()
print '---end of IP listing---'
