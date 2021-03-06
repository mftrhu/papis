import re
import papis.downloaders.base


class Downloader(papis.downloaders.base.Downloader):

    def __init__(self, url):
        papis.downloaders.base.Downloader.__init__(self, url)

    @classmethod
    def match(cls, url):
        """
        >>> Downloader.match(\
                'blah://pubs.acs.org/doi/abs/10.1021/acs.jchemed.6b00559'\
            ) is False
        False
        >>> Downloader.match(\
                'blah://pubs.acs.org/!@#!@$!%!@%!$che.6b00559'\
            ) is False
        False
        >>> Downloader.match(\
                'acs.com/!@#!@$!%!@%!$chemed.6b00559'\
            ) is False
        True
        """
        if re.match(r".*acs.org.*", url):
            return Downloader(url)
        else:
            return False

    def getDoi(self):
        # http://pubs.acs.org/doi/whatever/10.1021/acs.jchemed.6b00559
        mdoi = re.match(r'.*acs.org/doi/[^/]+/(.*)', self.getUrl())
        if mdoi:
            doi = mdoi.group(1).replace("abs/", "").replace("full/", "")
            self.logger.debug("[doi] = %s" % doi)
            return doi
        else:
            self.logger.error("Doi not found!!")

    def getDocumentUrl(self):
        # http://pubs.acs.org/doi/pdf/10.1021/acs.jchemed.6b00559
        durl = "http://pubs.acs.org/doi/pdf/" + self.getDoi()
        self.logger.debug("[doc url] = %s" % durl)
        self.logger.error("Retrieving urls does not work for acs yet")
        raise Exception
        return durl

    def getBibtexUrl(self):
        url = "http://pubs.acs.org/action/downloadCitation"\
              "?format=bibtex&cookieSet=1&doi=%s" % self.getDoi()
        self.logger.debug("[bibtex url] = %s" % url)
        return url

# vim-run: python3 -m doctest %
