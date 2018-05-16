# crowdsourcingTools

Our website is built is django and need following packages to be installed before it can be used

python 3

django (version 1, 10, 5,)

django-unixtimestampfield (Conversion of datetime to epoch time)

pyasn (IP to asn conversion)

pytz (Timezone conversion)

lxml (Parsing http page)

pyyaml ua-parser user-agents(Parsing of request header to get browser, OS , IP etc information)

django-user-agents (Parsing of request header to get browser, OS , IP etc information)

There is only one other tweek required with admin previllages. django-user-agent package, which has not been upgraded for python3 and latest django release. After installation of the package, you had to change part of middleware class using sudo. It is explained in following link

https://github.com/selwin/django-user_agents/pull/17/commits/e4da09156db99ff7319e11ed0bece822c2f1fcc7

pyasn uses routviews at the backend, which can be downloaded from http://data.4tu.nl/repository/uuid:d4d23b8e-2077-4592-8b47-cb476ad16e12

For Amazon Mturk API's to work

boto3 and Python3 are required
