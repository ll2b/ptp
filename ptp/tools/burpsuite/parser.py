"""

:synopsis: Specialized :class:`ptp.libptp.parser.AbstractParser` classes for the tool BurpSuite.

.. moduleauthor:: DoomTaper

"""

import re

from lxml.etree import XMLSyntaxError

from ptp.libptp import constants
from ptp.libptp.exceptions import NotSupportedVersionError
from ptp.libptp.parser import XMLParser


class BurpXMLParser(XMLParser):
    """BurpSuite XML specialized parser."""

    __tool__ = 'burpsuite'
    __version__ = r'1\.[0-9]+(\.[0-9]+)?'

    @classmethod
    def is_mine(cls, pathname, filename='*.xml', light=False, first=True):
        """Check if it can handle the report file.

        :param str pathname: Path to the report directory.
        :param str filename: Regex matching the report file.
        :param bool light: `True` to only parse the ranking of the findings from the report.
        :param bool first: Only process first file (``True``) or each file that matched (``False``).

        :return: `True` if it supports the report, `False` otherwise.
        :rtype: :class:`bool`

        """
        try:
            stream = cls.handle_file(pathname, filename, first=first)
        except (TypeError, XMLSyntaxError):
            return False
        try:
            version = stream.attrib['burpVersion']
        except(KeyError):
            return False
        if version is None:
            return False
        if not re.findall(cls.__version__, version, re.IGNORECASE):
            return False
        return True

    def parse_metadata(self):
        """Parse the metadata of the report.

        :raises: :class:`NotSupportedVersionError` -- if it does not support the version of this report.

        :return: The metadata of the report.
        :rtype: dict

        """
        raw_metadata = self.stream.attrib['burpVersion']
        # Find the version of BurpSuite.
        version = re.findall(self.__version__, raw_metadata, re.IGNORECASE)
        if len(version) >= 1:  # In case we found several version numbers.
            version = version[0]
        # Reconstruct the metadata
        # TODO: Retrieve the other metadata likes the date, etc.
        metadata = {'version': version}
        if self.check_version(metadata):
            self.metadata = metadata
        else:
            raise NotSupportedVersionError('PTP does NOT support this version of BurpSuite.')
        return self.metadata

    def parse_report(self):
        """Parse the results of the report.

        :return: List of dicts where each one has a request and response.
        :rtype: :class:`list`

        """
        self.data = []
        data = []
        # TODO: maybe a better way to get base64 value
        if self.stream.find('.//request').attrib['base64'] == 'false':
            base64 = False
        else:
            base64 = True
        for item in self.stream.findall('.//item'):
            response_status_code = item.find('status').text
            if base64:
                request = item.find('request').text.decode('base64')
                response = item.find('response').text.decode('base64')
            else:
                request = item.find('request').text
                response = item.find('response').text
            response_headers, response_body = response.split('\r\n\r\n', 1)
            # Somehow follow naming conventions from http://docs.python-requests.org/en/master/
            data.append({
                'request': request,
                'status_code': response_status_code,
                'headers': response_headers,
                'body': response_body
            })
        self.data.append({'ranking': constants.UNKNOWN, 'transactions': data})
        return self.data
