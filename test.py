#!/usr/bin/env python
'''Command line wrapper for suds client'''

from optparse import OptionParser
from scout import make_client, folders, calendar
from suds.sax.date import DateTime

import sys
import os
import logging
import getpass

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.INFO)

    try:
        oparser = OptionParser(usage="%prog [options]\n"
                               "or: %prog --help\n")
        oparser.add_option("-u","--username",
                           dest="username",
                           help="Exchange username\n")
        oparser.add_option("-p","--password",
                           dest="password",
                           help="Exchange password (omit to enter via getpass())\n")
        oparser.add_option("--hostname",
                           dest="hostname",
                           help="Exchange server hostname\n")
        oparser.add_option("--url",
                           dest="url",
                           help="Exchange server url\n")
        oparser.add_option("-r","--resources",
                           dest="resources",
                           help="Resources directory path\n",
                           default="%s/resources" % (os.getcwd()))
    

        (options, args) = oparser.parse_args(sys.argv[1:])

        if not options.username:
            oparser.error('Please specify an Exchange username')

        if not options.hostname and not options.url:
            oparser.error('Please specify the Exchange server hostname or url')

        if not options.password:
            options.password = getpass.getpass()

        if options.url:
            url = options.url
        else:
            url = 'https://%s/EWS/Exchange.asmx' % (options.hostname)

        client = make_client(options.username,
                             options.password,
                             url,
                             options.resources)


        for calendar in calendar.itercalendar(client,
                                              options.username,
                                              DateTime('2012-04-28T00:00:00'),
                                              DateTime('2012-05-01T00:00:00')):
            print calendar

    except Exception, e:
        print e


