<h1>Sniffing for Services</h1>

CSIRO publishes a large amount of scientific data both internally and externally. Some of the data we publish is via web services, both standard and custom. Despite sophisticated server management tools, it's very hard to know what services are installed across all CSIRO publication systems. It's even harder to know, centrally, what the published data is about.
First part is to use Python to write a program to scan all the open ports known to support specific applications and testing endpoints with a range of requests standard services are known to answer.
The second part is to mine the descriptions of data exposed by the services and map them to standard dictionaries of data description terms. 

Once discovered and identified, the student will then write more difficult code to mine the descriptions of data exposed by the services and map them to standard dictionaries of data description terms. The result will be updated to a database

Outcomes
1.	a network sniffing bot with the ability to slot in multiple tests
2.	a starting set of web service tests to be implemented by the bot
3.	some code for specific service types to extract description terms
4.	(stretch goal) code to compare extracted description terms to standard dictionaries
5.	(stretch, stretch goal) code to write extracted and compared terms to an updatable database

Project Flowchat
[Please click here to see the flowchat](https://www.draw.io/#G192cdVPcxf24mYAUQ_fM0hfHQNZcx_Zat)


Contacts
Author:
<b>Wenjin Li</b><br>
Wenjin.Li@csiro.au

