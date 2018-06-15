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


newFile=open('uacr_'+date+'.xml','w')

sickle = Sickle('http://www.duo.uio.no/oai/request')
recs = sickle.ListRecords(metadataPrefix="oai_dc")
for r in recs:
    newFile.write(str(r))
    print (r)

# sickle = Sickle('http://arizona.openrepository.com/arizona/oai/request?')
# sets = sickle.ListSets()  # gets all sets
# for recs in sets:
#     for rec in recs:
#         # print(rec)
#         if rec[0] == 'setSpec':
#             try:
#                 records = sickle.ListRecords(metadataPrefix='oai_dc', set=rec[1][0], ignore_deleted=True)
#                 records.next
#                 for rec in records:
#                     print(rec)
#                     newFile.write(str(rec))
#             except IOError:
#                 pass
