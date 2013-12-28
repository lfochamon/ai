"Artificial Ignorance" server monitoring
========================================

Artificial Ignorance (AI) is a web server log monitoring technique presented in Ivan Ristic's "Apache Security". It was invented by Marcus J. Ranum (http://www.ranum.com/security/computer_security/papers/ai/). This is simply a **Python 2.7** implementation of the idea.

Note: _These scripts require Python 2.7._



The AI process
--------------

The process is actually very simple:

1. Remove lines that you know are safe to ignore;
2. Remove parts that are unique for every entry, such as time stamp and IP addresses;
3. Count and remove repeated occurrences keeping only unique ones;
4. Reverse sort by occurrence numbers.


In these implementations, instead of removing "noisy" lines (lines that are safe to ignore), a threshold for displaying entries. Noisy lines (such as those shown during apache restart) will hardly appear many times. And if they do, well then you probably have a problem.


Implementations
---------------

### ai_error.py

Checks the Apache's error log. It processes ModSecurity entries separately to output more concise entries. It also displays the IPs that most commonly show up on your error files. You should set up the threshold to accomodate your server's traffic and your time/patience to read logs.

### ai_msmtp.py

Checks msmtp log. Basically tracks recipients emails and "emails per day". It's very useful to check if your server is being used for spamming.


Use
---

The script takes either a text file or reads inputs from stdin. You can use (I use msmtp to send emails, but you can change it to sendmail or whatever you prefer)

```
cat /path/to/logs/error.log | /path/to/script/ai_error.py 2>&1 | msmtp email@host.com
```

or

```
cat /path/to/logs/msmtp.log | /path/to/script/ai_msmtp.py 2>&1 | msmtp email@host.com
```

You can set up a cron job for it, but be careful with log rotation.

