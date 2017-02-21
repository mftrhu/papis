#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Simple paper management program
# Copyright © 2016 Alejandro Gallo

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

MANUAL =\
"""
Yeah... well

TODO:
    - implement picker functionality
    - Continue
"""




#  Import modules {{{1  #
#########################

import os
import re
import sys
import yaml
import shutil
import requests
import tempfile
import argparse

from .config import Configuration

if sys.version_info < (3, 0):
    raise Exception("This script must use python 3.0 or greater")
    sys.exit(1)


#  data {{{1  #
###############

infoFileName = "info.yaml"

#  Utility functions {{{1  #
############################


def getUrlService(url):
    """TODO: Docstring for getUrlService.

    :url: TODO
    :returns: TODO

    """
    m = re.match(r".*arxiv.org.*", url)
    if m: # Arxiv
        printv("Arxiv recognised")
        return "arxiv"
    return ""

def add_from_arxiv(url):
    """TODO: Docstring for add_from_arxiv.
    :url: TODO
    :returns: TODO
    """
    data = {}
    filePath   = tempfile.mktemp()+".pdf"
    bibtexPath = tempfile.mktemp()
    m = re.match(r".*arxiv.org/abs/(.*)", url)
    if m:
        p_id = m.group(1)
        printv("Arxiv id = '%s'"%p_id)
    else:
        print("Arxiv url fromat not recognised, no document id found")
        sys.exit(1)
    infoUrl = "http://export.arxiv.org/api/query?search_query=%s&start=0&max_results=1"%p_id
    pdfUrl  = "https://arxiv.org/pdf/%s.pdf"%p_id
    printv("Pdf url  = '%s'"%pdfUrl)
    printv("Info url = '%s'"%infoUrl)
    response = requests.get(pdfUrl, stream=True)
    if response: # Download pdf
        fd = open(filePath, "wb")
        # fd.write(response.raw)
        shutil.copyfileobj(response.raw, fd)
        printv("Pdf saved in %s"%filePath)
        fd.close()
    return (filePath, data)

def getFolders(folder, recursive=False):
    """
    Get papers from a containing folder

    :folder: TODO
    :returns: TODO

    """
    import glob
    folders = list()
    if recursive:
        raise Exception("Recursively search is TODO")
    for f in glob.glob(os.path.join(folder, "*")):
        if os.path.isdir(f):
            if os.path.exists(os.path.join(f,infoFileName)):
                folders.append(f)
    return folders



def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="Simple papers administration program"
        )

    SUBPARSER_HELP = "For further information for every command, type in 'papis <command> -h'"
    subparsers = parser.add_subparsers(
        help=SUBPARSER_HELP,
        metavar="command",
        dest="command"
        )
    parser.add_argument("-v",
        "--verbose",
        help    = "Make the output verbose",
        default = False,
        action  = "store_true"
    )
    parser.add_argument(
            "--log",
            help="Logging level",
            choices=[
                "INFO",
                "DEBUG",
                "WARNING",
                "ERROR",
                "CRITICAL"
                ],
            action="store",
            default="WARNING"
            )
    # Parse arguments
    args = parser.parse_args()
    if args.verbose:
        args.log = "DEBUG"
    logging.basicConfig(level = getattr(logging, args.log))


    # for subparser_name in [ "add", "update", "list", "export", "check", "open", "edit", "test", "config" ]:
        # print(subparser_name)

    # Parse arguments
    args = parser.parse_args()
    config = Configuration()

    exec("import %s as command"%args.command)
    print(command)
    command.init()
    command.main(config,args)













#vim-run: python3 %
# vim:set et sw=4 ts=4 ft=python: