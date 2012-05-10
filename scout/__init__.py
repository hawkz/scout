# scout/__init__.py

from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor
from suds.transport.http import HttpAuthenticated

def make_client(username,
                password,
                url,
                resources):
    '''Create a new Outlook compatible suds client'''

    
    wsdl = 'file://%s/outlook.wsdl' % (resources)
    
    # use Basic Authentication
    transport = HttpAuthenticated(username=username,
                                  password=password)

    # Work around the broken import
    imp = Import('http://www.w3.org/XML/1998/namespace',
                 location='file://%s/xml.xsd' % (resources))
    
    doctor = ImportDoctor(imp)
    
    client = Client(wsdl,
                    location=url,
                    doctor=doctor,
                    transport=transport)

    # Every request must specify the RequestServerVersion header
    # This wasn't that easy to figure out...

    # get enumeration of available versions
    versions = client.factory.create('ns1:ExchangeVersionType')
    # create version instance
    version = client.factory.create('t:RequestServerVersion')
    # set version instance's version from enumeration
    version._Version = versions.Exchange2010_SP1

    # set global header
    headers = {'RequestServerVersion':version}
    client.set_options(soapheaders=headers)

    return client
