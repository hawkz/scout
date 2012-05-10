scout
=====

An Exchange SOAP client using Python suds.

# Background

Exchange's SOAP implementation is not 100% compatible with suds or any other tool:

 - Exchange hosts its WSDL using password protection. Normally, the WSDL can be
   obtained by querying:

       https://${hostname}/EWS/Exchange.asmx

   However, suds doesn't pass http authentication headers (including "Authentication") 
   to HttpTransport.open() (see http.py) when retrieving WSDL files. It's possible to 
   work around this problem by modifying suds or defining a custom transport, but...

 - Exchange's WSDL doesn't declare a SOAP service or port type, which just about every
   SOAP client expects and uses to generate client-side bindings. Since the WSDL needs
   to be modified anyway, a copy of the WSDL obtained from our server, along with
   its related XSD files are included in the resources/ directory here and used in
   when constructing the suds client.

 - Exchange's WSDL imports an XSD (from www.w3.org) that does not return a valid response
   when using HTTPS. Again, it's easier to have a local copy of this file.

# Dependencies

The Python suds library is required as are the WSDL and XSD files includes in the resources/
directory.

    pip install suds

# Creating the Client

    from scout import make_client

    client = make_client('user@example.com',
                         'secretpassword',
                         'https://example.com//EWS/Exchange.asmx',
                         '/path/to/resources/')

# Using the Client

