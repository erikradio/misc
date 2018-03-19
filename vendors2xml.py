# -- coding: utf-8 --
import csv, sys, time, datetime, xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

# https://developers.exlibrisgroup.com/resources/xsd/rest_vendor.xsd
xmlFile = 'newVendors.xml'
xmlData = open(xmlFile, 'w')
# dataFile=sys.argv[1]

ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

root = Element('vendors')
root.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')

tree = ET.ElementTree(root)




with open(sys.argv[1], 'rU',errors='ignore') as csvfile:
    reader = csv.DictReader(csvfile)



    for row in reader:


        vendor = SubElement(root, 'vendor')
        code = SubElement(vendor,'code')
        code.text = row['code']
        name = SubElement(vendor,'name')
        name.text = row['name']
        contactInfo = SubElement(vendor,'contact_info')
        addresses = SubElement(contactInfo, 'addresses')
        address = SubElement(addresses, 'address')
        address.set('preferred','true')
        line1 = SubElement(address,'line1')
        line1.text = row['line1']
        if len(row['line2']) > 0:
            line2 = SubElement(address,'line2')
            line2.text = row['line2']
        city = SubElement(address, 'city')
        city.text = row['city']

        if len(row['state_province']) > 0:
            stateprov = SubElement(address, 'state_province')
            stateprov.text = row['state_province']
        if len(row['postal_code']) > 0:
            postalcode = SubElement(address, 'postal_code')
            postalcode.text = row['postal_code']

        address_types = SubElement(address, 'address_types')
        address_type = SubElement(address_types, 'address_type')
        address_type.text = row['address_types']

        emails = SubElement(contactInfo, 'emails')
        email = SubElement(emails, 'email')
        email.set('preferred', 'true')
        emailaddress = SubElement(email,'email_address')
        if len(row['email_address']) > 0:
            emailaddress.text = row['email_address']
        else:
            emailaddress.text = 'No email available'

        if len(row['phone_number']) > 0:
            phones = SubElement(contactInfo, 'phones')
            phone = SubElement(phones, 'phone')
            phone.set('preferred','true')
            phoneno = SubElement(phone, 'phone_number')
            phoneno.text = row['phone_number']


        accounts = SubElement(vendor,'accounts')
        account = SubElement(accounts, 'account')
        accCode = SubElement(account, 'account_code')
        accCode.text = row['code']
        accDesc = SubElement(account, 'description')
        accDesc.text = row['name']
        payments = SubElement(account, 'payment_methods')
        payment = SubElement(payments, 'payment_method')
        payment.set('desc', 'Accounting Department')
        payment.text = 'ACCOUNTINGDEPARTMENT'

        vendorCurrencies = SubElement(vendor, 'vendor_currencies')
        currency = SubElement(vendorCurrencies, 'currency')
        currency.set('desc', 'US Dollar')
        currency.text = 'USD'

        ediInfo = SubElement(vendor, 'edi_info')
        ediCode = SubElement(ediInfo,'code')
        ediCode.text = row['code']

        perOrgUnits = SubElement(vendor, 'per_organization_units')
        perOrgUnit = SubElement(perOrgUnits, 'per_organization_unit')
        orgUnit = SubElement(perOrgUnit, 'organization_unit')
        orgUnit.text = 'azu'
        orgCode = SubElement(perOrgUnit, 'edi_code')
        orgCode.text = row['code']
        # add per org unit

        eanAccounts = SubElement(vendor, 'ean_accounts')
        eanAccount = SubElement(eanAccounts, 'ean_account')
        eanAccount.text = row['code']
        eanCode = SubElement(eanAccount, 'ean_code')
        eanCode.text = '123456'

        # print tostring(root)

        contactPerson = SubElement(vendor, 'contact_person')
        contactPerson.text = 'None Listed'


tree.write('newVendors.xml',xml_declaration=True, encoding="UTF-8")
