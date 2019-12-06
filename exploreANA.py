#!/usr/bin/env python

"""
Name:    extract_java_server_faces_viewstate
Purpose: Extract and parse the Java Server Faces viewstate
Date:    20150620
Author:  Don C. Weber (@cutaway) of InGuardians, Inc.

Resources:
    http://wiki.apache.org/myfaces/Secure_Your_Application
    http://www.synacktiv.com/ressources/JSF_ViewState_InYourFace.pdf
    https://github.com/frohoff/inyourface/blob/master/src/java/inyourface.java
    https://prezi.com/t-lzwbqm2vwn/jsf-security/ - video shows fully encrypted viewstate value

TODO:
    Identify if MAC has been enabled
    Add functionality to grab a single page. For now just use Burp Suite.
"""

import urllib2
import base64
import gzip
from cStringIO import StringIO
import re
from copy import copy
import entropy as ent


def search_vs(data, relist=['pass', 'user', 'secret', 'key']):
    '''
    Search parsed viewstate data for key terms
    Inputs:
        data: Parsed viewstate
        relist: list of terms to search
    '''
    results = {}
    for e in re.split(r'\x00*', data):
        for n in relist:
            if re.search(n, e):
                if results.has_key(n):
                    results[n].append(e)
                else:
                    results[n] = [e]
    return results


def detect_vs(data, term='java'):
    '''
    Search parsed viewstate data for term that indicates unencrypted data
    This test mimics SpiderLabs deface: https://github.com/SpiderLabs/deface
    Inputs:
        data: Parsed viewstate
        term: term to use to detected unecrypted data
    '''
    for e in re.split(r'\x00*', data):
        if re.search(term, e):
            return True
    return False


def extract_vs(data, param='value'):
    '''
    Extract a viewstate value from a line of HTML.
    Inputs:
        data: Single line of html with the viewstate parameter
        param: the name of the viewstate parameter
    '''

    # Line will have spaces to separate values
    for e in data.split(" "):
        # Value will be separated by an "=" but only split on first occurrence
        n = e.split("=", 1)
        # Viewstate should be the "value" parameter
        if not n[0] == param:
            continue
        else:
            # Remove quotes from beginning and end
            # Returns base64 encoded viewstate
            return n[1].replace("\"", "")
    return None


def parse_vs(data):
    '''
    Parse the viewstate data by decoding and unpacking it.
    Inputs:
        data: Single line of base64 encoded viewstate. URLENCODED data is okay
    '''

    # URL Encoding
    urldelim = "%"

    # Check to see if the viewstate data has urlencoded characters in it and remove
    if re.search(urldelim, data):
        d1 = urllib2.unquote(data).decode('utf8')
    else:
        d1 = copy(data)

    # Base64 decode
    d2 = base64.decodestring(d1)
    print d2
    # Generate a StringIO object since gzip wants a file descriptor
    d3 = StringIO(d2)

    # Decompress data
    d4 = gzip.GzipFile(mode='rb', fileobj=d3)

    # Get data from gzip file object
    d5 = d4.read()

    # Print viewstate and manually review for useful information
    # Happy Hunting
    return d5




def print_vs(data):
    '''
    Print the viewstate by converting from 'iso-8859-1' to 'utf8' encoding
    Inputs:
        data: Single line of parsed viewstate
    '''
    print data.decode('iso-8859-1').encode('utf8')

d = "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"

print_vs(d)

#
# if __name__ == "__main__":
#     '''
#     # Usages:
#     # Extract Viewstate values from Burp Request/Response Extract file
#     grep javax.faces.ViewState burp_requests_responses.txt > burp_requests_responses_viewstate.txt
#
#     # Print parsed viewstate
#     data = open("burp_requests_responses_viewstate.txt",'r').readlines()
#     for e in data:
#         tmp = vs.extract_vs(e)
#         if tmp:
#             print "\n============\n"
#             print repr(vs.parse_vs(tmp))
#             print "\n============\n\n\n"
#
#     # Parse and search viewstate for key words
#     data = open("burp_requests_responses_viewstate.txt",'r').readlines()
#     for e in data:
#         tmp = vs.extract_vs(e)
#         if tmp:
#             results = vs.search_vs(vs.parse_vs(tmp))
#             if results:
#                 for v in results.keys():
#                     print v + ":",results[v]
#                 print "\n===========\n\n"
#     '''
#     # Update "data" with data copied from viewstate
#     # d = "data"
#     d = sys.argv(1)
#     print parse_vs(d).decode('iso-8859-1').encode('utf8')

