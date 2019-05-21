import csv, sys

# sparql query for glaciers and coordinates
# SELECT ?subj ?label ?coord
# WHERE
# {
# 	?subj wdt:P31 wd:Q35666 .
# 	?subj wdt:P625 ?coord .
# 	SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . ?subj rdfs:label ?label }
# }

with open(sys.argv[1]) as wikifile,  open(sys.argv[2]) as localGlacier, open('newGlacier.csv','w',newline='') as csv_file:
	reader = csv.DictReader(wikifile)
	glaciers = {}
	for row in reader:
		wid = row['subj']
		name = row['label']
		coord = row['coord']
		glaciers[name] = wid, coord

	localreader = csv.DictReader(localGlacier)


	localName = {}
	for row in localreader:
		key = row['Glacier Name (FINAL)']
		localName[key] = row


	for name in localName:

		if name in glaciers:
			newWID = glaciers[name][0]
			localName[name]['wikidata'] = newWID
		elif KeyError:
			continue

	# print(localName)
	fieldnames=['Glacier Name (FINAL)', 'Country','State/Province/First Order Administrative Area','Latitude','Longitude','Coverage Spatial','GLIMS ID','Historical or Variant Name',
	'Documentation Notes - CLEAN', 'Documentation Notes','wikidata']
	writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
	for key in localName.keys():
		writer.writerow(localName[key])

