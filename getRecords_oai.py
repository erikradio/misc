from sickle import Sickle
import sys, json
from argparse import ArgumentParser
import logging
import requests


# https://memory.loc.gov/cgi-bin/oai2_0?verb=GetRecord&metadataPrefix=marc21&identifier=oai:lcoa1.loc.gov:loc.gmd/g3791p.rr002300
# updated 2017-08-14 to add data parameters
# date=sys.argv[1]
date=sys.argv[1]
# collection=sys.argv[3]



# log = logging.getLogger(__name__)
# logging.basicConfig(level="DEBUG")


newFile=open('cub_'+date+'.xml','w')

sickle = Sickle('https://oai.datacite.org/oai')
recs = sickle.ListRecords(metadataPrefix="datacite", set='CUB')
for r in recs:
    newFile.write(str(r))
    print (r)

