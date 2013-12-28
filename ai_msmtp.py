#!/usr/bin/python

import fileinput, re, collections

# Output email header
print "From: cloud@lps.usp.br"
print "To: cloud@lps.usp.br"
print "Subject: msmtp.log AI"


print ''
print 'Unprocessed lines:'

toList = []
dateList = []

for line in fileinput.input():
    # Strip blank spaces
	line = line.strip()
	
	# Count IP occurence
	recipient = re.search(r'recipients=([^\s]*)', line)
	if recipient:
		toList.append(recipient.group(1))
	else:
		print line

	# Emails per day
	date = re.search(r'^\w{3} \d{2}', line)
	if date:
		dateList.append(date.group(0))
	else:
		print line

# Count multiple instances and keep unique
toCount = collections.Counter(toList)
dateCount = collections.Counter(dateList)


# Output in reverse occurence order
print ''
print '---recipient list---'
for i in toCount.most_common():
	print str(i[1]) + '\t\t' + i[0].strip()
print '---end of recipient list---'

print ''
print '---Date list---'
for i in dateCount.most_common():
	print str(i[1]) + '\t\t' + i[0].strip()
print '---end of date list---'
