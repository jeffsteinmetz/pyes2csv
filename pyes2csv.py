# Sample script by Jeff Steinmetz, Twitter:  @jeffsteinmetz
# MIT License
# V1.0, created 2014-01-17
#
# Requires the Python Elasticsearch client
# http://www.elasticsearch.org/blog/unleash-the-clients-ruby-python-php-perl/#python
#

import elasticsearch
import csv
import random
import unicodedata

#replace with the IP address of your Elasticsearch node
es = elasticsearch.Elasticsearch(["10.1.1.1:9200"])

# Replace the following Query with your own Elastic Search Query
res = es.search(index="YourIndexName", body=
	{"query": 
    {
	    "bool": {
	       "must": [
			            {"match": { "search_field":"search string"}}
			          , {"range": { "created_at": {"gte":"2013-10-01", "lte":"2014-01-29" }}},
			          , {"match": { "another_field":"foo"}}
	                ]
	      }
    }
}, size=500)  #this is the number of rows to return from the query... to get all queries, run script, see total number of hits, then set euqual to number >= total hits

random.seed(1)
sample = res['hits']['hits']
#comment previous line, and un-comment next line for a random sample instead
#randomsample = random.sample(res['hits']['hits'], 5);  #change int to RANDOMLY SAMPLE a certain number of rows from your query  

print("Got %d Hits:" % res['hits']['total'])

with open('outputfile.tsv', 'wb') as csvfile:   #set name of output file here
	filewriter = csv.writer(csvfile, delimiter='\t',  # we use TAB delimited, to handle cases where freeform text may have a comma
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
	# create header row
	filewriter.writerow(["id", "column2", "column3"])    #change the column labels here
	for hit in sample:   #switch sample to randomsample if you want a random subset, instead of all rows
		try:			 #try catch used to handle unstructured data, in cases where a field may not exist for a given hit
			col1 = hit["_id"]
		except Exception, e:
			col1 = ""
		try:
			col2 = hit["some"]["deeply"]["nested"]["field"].decode('utf-8')  #replace these nested key names with your own
			col2 = col2.replace('\n', ' ')
		except Exception, e:
			col2 = ""
		try:
			col3 = hit["someother"]["deeply"]["nested"]["field"].decode('utf-8')  #replace these nested key names with your own
			col3 = col3.replace('\n', ' ')
		except Exception, e:
			col3 = ""
		filewriter.writerow([col1,col2,col3])

