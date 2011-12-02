#!/usr/bin/env python

########################################################################
# Group: Windows Package Manager A
# Name: Sebastian Imlay
# Group Members: Joshua Stein and Timothy James Telan
# Date: October 15, 2011
# Query database, perform web only given a db object
########################################################################

# re for regex, urllib2 for downloading.
from db_wrapper import *
import re, urllib2, logging

class app:

    # Initialize the application using the database object.
    def __init__(self, appName, dbObject, logFileName):

        #self.logger = logging.getLogger('Application')
        #self.logger.setLevel(logging.DEBUG)

        #logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=logFileName, filemode='a')
        self.name = appName
        self.db = dbObject
        self.href = ''
        self.version = ''

        #logging.info("Application: Initialized application using database for " + appName + ".")

    # abritrary delete function.
    def __del__(self):
        #logging.info("Application: Done using Application " + self.name + ".")
        pass


    # Queries the database for regex(s) and download site(s) then downloads
    # the webpage and checks the regex against it.
    #
    # Returns Boolean True means there is an newer version,
    #  false means no newer version found.
    def checkUpdates(self):
        #logging.info("Checking for updates for " + self.name + ".")

        newVersion = ''
        if self.href == '':
            allHREFS = self.getExeURLs()
            self.href = self.chooseHREF(allHREFS)

            newVersion = self.getVersionFromURL(self.href)

        validQuery, versionsInDB =  get_app_version(self.db, self.name)
        if validQuery:
            for currVersion in versionsInDB:

                # Found this version in the db.
                if str(currVersion) == newVersion:
                    return False

        # Did not find this version in the db.
        return True


    # Download the updates - check for updates first.
    def dlUpdates(self):

        if self.checkUpdates():
            print "Application: Updating " + self.name

            if self.href == '':
                allHREFS = self.getExeURLs()
                href = ''
                if allHREFS == []:
                    print 'Found no hyper links using that regular expression.'

                # More than one hyperlink.  Prompt user.
                elif(len(allHREFS) > 1):
                    href = self.chooseHREF(allHREFS)

                # Only one hyperlink in html.
                elif(len(allHREFS) == 1):
                    href = allHREFS[0]

                self.href = href

            if(self.href != ''):
                # assume that there is no quotes are found in hyperlink.
                print "Dowloading executable from:", self.href
                if self.version != '':
                    self.version = self.getVersionFromURL(self.href)


                if self.version == '':
                    self.downloadFileName = self.name + '.' + self.version + '.exe'
                else:
                    self.downloadFileName = self.name + '.exe'

                req = urllib2.urlopen(self.href)
                output = open(self.downloadFileName, 'wb')
                output.write(req.read())
                output.close()


                add_update_file(self.db, self.name, self.downloadFileName, self.version)



    # Choose a hyperlink.
    def chooseHREF(self, allHREFS):
        print "Found more than one href.  All hrefs are:"
        count = 0

        for href in allHREFS:
            print str(count) + ': ', href
            count = count + 1

        href = ''
        hrefNum = raw_input('Choose href (number): ')
        if int(hrefNum) > 0 and int(hrefNum) < len(allHREFS):
            href = allHREFS[int(hrefNum)]
        href = href.replace('"', '')
        return href


    def getVersionFromURL(self, href):
        validVersionRegexQuery, versionRegexList = get_app_version_regex(self.db, self.name)

        # apply version regex to the (possibly chosen) url.
        if validVersionRegexQuery and versionRegexList != []:
            versions = []
            version = ''

            # Get the version from the regex list.
            for regex in versionRegexList:
                versions = versions + re.findall(regex, href, re.IGNORECASE)

            # Found with more than one. Prompt the user.
            if (len(versions) > 1):
                print 'Found more than one version in with the version regular exprossion.'
                count = 0
                for version in versions:
                    print str(count) + ': ' + version
                    count = count + 1

                # Prompt.
                versionNum = raw_input('Please choose a number: ')
                if int(versionNum) > 0 and int(versionNum) < len(versions):
                    version = '.' + versions[int(versionNum)]
                    print 'Version regex found no version information in Hypelink.'

            # trivial case.
            elif(len(versions) == 1):
                version = versions[0]

            if(version != ''):
                print 'Found version in hyperlink: ' + version

            # Found nothing.
            else:
                print 'Version regex found no version information in Hypelink.'

            self.version = version
            return version


    def getExeURLs(self):
        allReturns = []
        #print 'urllist = ', urlList


        # Get the list of urls from the database.
        validURLQuery, urlList = get_app_urls(self.db, self.name)
        if validURLQuery and urlList != []:
            webHtml = ''

            # assume that the download url is  first in list.
            dlURL = urlList[1]

            print 'Application: Downloading webpage from ' + dlURL

            f = urllib2.urlopen(str(dlURL))
            webHtml = f.read()
            f.close()

            validRegxQuery, regexList = get_app_exe_regex(self.db, self.name)

            #print 'regex list = ', regexList

            if validRegxQuery and len(regexList) > 0:
                for app_regex in regexList:
                    allReturns = allReturns + re.findall(app_regex, webHtml, re.IGNORECASE)

                if allReturns == []:
                    otherDlUrl = urlList[0]
                    print 'Application: No returns, possibly download url is swapped with website url. Checking website URL: ' + otherDlUrl


                    # Try the other urls.
                    f = urllib2.urlopen(otherDlUrl)
                    webHtml = ''
                    webHtml = f.read()
                    f.close()

                    # Apply regex again.
                    others = []
                    for app_regex in regexList:
                        others = others + re.findall(app_regex, webHtml, re.IGNORECASE)

                    if(others != []):
                        print others
                        useOthers = raw_input('Other returns = %s. Use other returns? [y/n]:  ' % others)
                        if useOthers == 'y':
                            allReturns = others
                    else:
                        print 'found nothing in website url.'
        return allReturns
