<h1>Sniffing for Services</h1>

<p>
The Commonwealth Scientific and Industrial Research Organisation (CSIRO) is an independent Australian Federal government agency responsible for scientific research. 

As a result, CSIRO publishes a large amount of scientific data both internally and externally. Some of the data it publishes is via web services, both standard and custom. Despite sophisticated server management tools, it is very hard to know what services are installed across all CSIRO publication systems as a lot of the data services are ad hoc and not catalogued. It’s even harder to know, centrally, what the published data is about. 

The main goal of the project is to help CSIRO identify and catalogue data services. The outcome of the project should help users like research scientists in CSIRO to search and discover what data services are available on the CSIRO network. A NASA web service, based on Thredds data server, is a good example for the project to start with to make query, which contains a catalogue for different datasets.

This project is to write code to interrogate CSIRO’s internal and external web presences and hunt for particular service technologies. This involve polling for open ports known to support specific applications and testing endpoints with a range of requests standard services are known to answer. Once discovered and identified, it is required to design a data structure like a database that is used to make queries of the descriptions of data exposed by the services and map them to standard dictionaries of data description terms.

<strong>Objective</strong>

The goal of this project is to harvest NetCDF files from THREDDS servers across CSIRO network. Not only the files are found, but also the files are are also categorised by different data service types, such as OpenDAP, WMS, WMC, HTTP etc for each host.
This program is customised to be used only within CSIRO network but can be modified for general purpose.

<strong>Outcome</strong>

A database is created to store all metadata in SQlite. The database is easy to maintain. More than 3000 unique  NetCDF files have been found and the number of files will be keep growing. In the database, host description, host URL, data service type are also captured.



Please check <a href="https://drive.google.com/file/d/1on3AIzCGQ0RNjU-ekA0VLm2iZv2f_2Rw/view?usp=sharing">Project ERD</a>

<strong>Technlogy</strong>

In this project, overall, pure Python is used to perform NetCDF file scraping. 

Furthermore, a range of Python libraries and packages is used:

<ul>
    <li>Python Request</li>
    <li>Beautiful Soup</li>
    <li>RE</li>
    <li>NMAP</li>
    <li>XML</li>
    <li>urlsplit</li>
</ul>

These tools are useful and handy to use especially Beautiful Soup. Not only it can dig data but also it can be used to transform unstructured data.

<strong>Project Schema</strong>

main.py<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- scan.py ( To scan network and get valid host return )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- tds_host.py ( To capture host description terms and data service types to database ) <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- store.py ( SQL Query function to capture data to database )<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| -- helper.py ( helper functions)<br>
</p>


<strong>Find me on</strong>

www.woodylouis.me

<strong>Contact</strong>

louisli@woodylouis.me

Wenjin.Li@csiro.au

