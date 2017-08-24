# -- coding: utf-8 --
import csv, sys
from xml.etree import ElementTree as ET

with open(sys.argv[1], mode='w') as csvFile:
    with open(sys.argv[2], 'r') as xmlFile:
        writer = csv.writer(csvFile, lineterminator='\n')


        writer.writerow(("Classification_Number", "Subject"))

        tree = ET.parse(xmlFile)
        root = tree.getroot()
        for record in root.findall('{http://www.loc.gov/MARC21/slim}record'):
            data=record.find('{http://www.loc.gov/MARC21/slim}datafield[@tag="153"]')
            if data is None:
                continue
            else:
                subA = data.find('{http://www.loc.gov/MARC21/slim}subfield[@code="a"]')

                if subA is not None:
                    subA = subA.text

                else:
                    subA = 'None'

                subJ = data.find('{http://www.loc.gov/MARC21/slim}subfield[@code="j"]')

                if subJ is not None:
                    subJ = subJ.text
                else:
                    subJ='None'

                x=(subA,subJ)
                writer.writerow(x)

        # print(root)
        # for row in reader:
        #     handle = row['KUSW_URL']
        #     duplicateFlag=""
        #     if len(handle) > 0:
        #         dedupeFreq[handle] = dedupeFreq.get(handle, 0) + 1
        #         if dedupeFreq[handle] > 1:
        #             duplicateFlag = "duplicate"
        #             # print(handle, duplicateFlag)
        #
        #         if not handle.strip():
        #                 handle = dedupeHandles.get(handle, "")
        #     x=(row["Author"], row["Department"], row["Title"], row["Year_Published"],row["DOI"], row["Journal"],
        #        row["Publisher"], row["Published_URL"], handle, row["Rights_to_Share"], row["Conditions"], row["SourceFile"], duplicateFlag)
        #     writer.writerow(x)
