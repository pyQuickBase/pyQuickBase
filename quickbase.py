"""Python wrapper for the QuickBase API.

For detailed API information, see:
http://www.quickbase.com/api-guide/index.html

"""
import os
import requests
from lxml import etree
import chardet

class Error(Exception):
    """A QuickBase API error. Negative error codes are non-QuickBase codes internal to
    this module. For the list of QuickBase error codes, see:
    http://www.quickbase.com/api-guide/errorcodes.html

    """
    def __init__(self, code, msg, response=None):
        self.args = (code, msg)
        self.code = code
        self.msg = msg
        self.response = response

class ConnectionError(Error):
    pass

class ResponseError(Error):
    pass

class QuickBaseError(Error):
    pass

def to_xml_name(name):
    """Convert field name to tag-like name as used in QuickBase XML.

    >>> to_xml_name('This is a Field')
    'this_is_a_field'
    >>> to_xml_name('800 Number')
    '_800_number'
    >>> to_xml_name('A & B')
    'a___b'
    >>> to_xml_name('# of Whatevers')
    '___of_whatevers'

    """
    xml_name = ''.join((ch if ch.isalnum() else '_') for ch in name.lower())
    if not xml_name[0].isalpha():
        xml_name = '_' + xml_name
    return xml_name

class Client(object):
    """Client to the QuickBase API."""

    @classmethod
    def _build_request(cls, **request_fields):
        r"""Build QuickBase request XML with given fields. Fields can be straight
        key=value, or if value is a 2-tuple it represents (attr_dict, value), or if
        value is a list of values or 2-tuples the output will contain multiple entries.

        >>> Client._build_request(a=1, b=({}, 'c'), d=({'f': 1}, 'e'))
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><a>1</a><b>c</b><d f="1">e</d></qdbapi>'
        >>> Client._build_request(f=['a', 'b'])
        "<?xml version='1.0' encoding='UTF-8'?>\n<qdbapi><f>a</f><f>b</f></qdbapi>"
        >>> Client._build_request(f=[({'n': 1}, 't1'), ({'n': 2}, 't2')])
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><f n="1">t1</f><f n="2">t2</f></qdbapi>'

        """
        request = etree.Element('qdbapi')

        def add_sub_element(field, value):
            if isinstance(value, tuple):
                attrib, value = value
                attrib = dict((k, str(v)) for k, v in attrib.iteritems())
            else:
                attrib = {}
            sub_element = etree.SubElement(request, field, **attrib)
            if not isinstance(value, basestring):
                value = str(value)
            sub_element.text = value

        for field, values in request_fields.iteritems():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                add_sub_element(field, value)

        string = etree.tostring(request)
        return string

    @classmethod
    def _parse_records(cls, response):
        """Parse records in given XML response into a list of dicts."""
        records = []
        r = response.xpath('.//record')
        for row in r:
            record = {}
            for fields in row:
                if fields.tag == 'f':
                    record[fields.get('id')] = fields.text
                else:
                    record[fields.tag] = fields.text
            records.append(record)
        return records
    
    @classmethod
    def _parse_db_page(cls, response):
        """Parse DBPage from QuickBase"""
        from xml.sax import saxutils as su
        parser = etree.HTMLParser()
        r = response.xpath('.//pagebody')
        page = etree.tostring(r[0], encoding = 'utf-8')
        clean_page = su.unescape(page)
        return clean_page
    
    @classmethod
    def _parse_db_page2(cls, response):
        """Parse DBPage from QuickBase"""
        from xml.sax import saxutils as su
        r = response.xpath('.//pagebody/text()')
        return r
    
    @classmethod
    def _parse_list_pages(cls, response):
        """Parse list of pages with id, type, name"""
        pages = []
        r = response.xpath('.//page')
        for row in r:
            if row.attrib['id'] != '':
                pages.append([
                    row.attrib['id'],
                    row.attrib['type'],
                    row.text,
                ])
        return pages

    def __init__(self, username=None, password=None, base_url='https://www.quickbase.com',
                 timeout=30, authenticate=True, database=None, apptoken=None, realmhost=None, hours=12, ticket=None):

        """Initialize a Client with given username and password. Authenticate immediately
        unless authenticate is False.

        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.timeout = timeout
        self.database = database
        self.apptoken = apptoken
        self.realmhost = realmhost
        self.hours = hours
        if authenticate:
            self.authenticate()
        elif ticket != None:
            self.ticket = ticket

    def request(self, action, database, request, required=None, ticket=True,
                apptoken=True):
        """Do a QuickBase request and return the parsed XML response. Raises appropriate
        Error subclass on HTTP, response or QuickBase error. If fields list given,
        return dict with all fields in list (raises ResponseError if any not present),
        otherwise return parsed xml Element.

        """
        # Do the POST request with additional QuickBase headers
        url = self.base_url + '/db/' + database
        if ticket:
            request['ticket'] = self.ticket
        if apptoken:
            request['apptoken'] = self.apptoken

        request['encoding'] = 'UTF-8'
        request['msInUTC'] = 1
        if self.realmhost:
            request['realmhost'] = self.realmhost
        data = self._build_request(**request)
        headers = {
            'Content-Type': 'application/xml',
            'QUICKBASE-ACTION': 'API_' + action,
            }
        request = requests.post(url, data, headers=headers)
        response = request.content
        
        encoding = chardet.detect(response)['encoding']
        if encoding != 'utf-8':
            response = response.decode(encoding, 'replace').encode('utf-8')
        # print(response)
        error_code = ''
        try:
            parsed = etree.fromstring(response)
            error_code = parsed.findtext('errcode')
        except etree.XMLSyntaxError:
            print 'XML Parsing error.'
            # Ensure it's not a QuickBase error
        if error_code is None:
            raise ResponseError(-4, '"errcode" not in response', response=response)
        if error_code != '0':
            error_text = parsed.find('errtext')
            error_text = error_text.text if error_text is not None else '[no error text]'
            raise ResponseError(error_code, error_text, response=response)

        if required:
            # Build dict of required response fields caller asked for
            values = {}
            for field in required:
                value = parsed.find(field)
                if value is None:
                    raise ResponseError(-4, '"{0}" not in response'.format(field),
                        response=response)
                values[field] = value.text or ''
            return values
        else:
            # Return parsed XML directly
            return parsed

    def authenticate(self):
        """Authenticate with username and password passed to __init__(). Set the ticket
        and user_id fields.

        """
        request = {'username': self.username, 'password': self.password, 'hours': self.hours}
        response = self.request('Authenticate', 'main', request,
            required=['ticket', 'userid'], ticket=False)
        self.ticket = response['ticket']
        self.user_id = response['userid']

    def do_query(self, query=None, qid=None, qname=None, columns=None, sort=None,
                 structured=True, num=None, only_new=False, skip=None, ascending=True,
                 include_rids=False, database=None):
        """Perform query and return results (list of dicts)."""
        request = {}
        if len([q for q in (query, qid, qname) if q]) != 1:
            raise TypeError('must specify one of query, qid, or qname')
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid
        else:
            request['qname'] = qname

        if columns:
            request['clist'] = '.'.join(str(c) for c in columns)
        if sort:
            request['slist'] = '.'.join(str(c) for c in sort)
        if structured:
            request['fmt'] = 'structured'

        options = []
        if num is not None:
            options.append('num-{0}'.format(num))
        if only_new:
            options.append('onlynew')
        if skip is not None:
            options.append('skp-{0}'.format(skip))
        if not ascending:
            options.append('sortorder-D')
        if options:
            request['options'] = '.'.join(options)

        if include_rids:
            request['includeRids'] = 1

        response = self.request('DoQuery', database or self.database, request)
        return self._parse_records(response)

    def edit_record(self, rid, fields, named=False, database=None):
        """Update fields on the given record. "fields" is a dict of name:value pairs
        (if named is True) or fid:value pairs (if named is False). Return the number of
        fields successfully changed.

        """
        request = {}
        request['rid'] = rid
        attr = 'name' if named else 'fid'
        request['field'] = []
        for field, value in fields.iteritems():
            request_field = ({attr: to_xml_name(field) if named else field}, value)
            request['field'].append(request_field)
        response = self.request('EditRecord', database or self.database, request,
            required=['num_fields_changed'])
        return int(response['num_fields_changed'])

    def add_record(self, fields, named=False, database=None):
        """Add new record. "fields" is a dict of name:value pairs
        (if named is True) or fid:value pairs (if named is False). Return the new records RID
        """
        request = {}
        attr = 'name' if named else 'fid'
        request['field'] = []
        for field, value in fields.iteritems():
            request_field = ({attr: to_xml_name(field) if named else field}, value)
            request['field'].append(request_field)
        response = self.request('AddRecord', database or self.database, request,
            required=['rid'])
        return int(response['rid'])

    def import_from_csv(self, records_csv, clist, clist_output=None, skipfirst=False, database=None, msInUTC=True):
        request = {}
        request['records_csv'] = records_csv
        if clist is not None:
            request['clist'] = clist
        if clist_output is not None:
            request['clist_output'] = clist_output
        if skipfirst:
            request['skipfirst'] = skipfirst
        response = self.request('ImportFromCSV', database or self.database, request, required=['num_recs_added'])
        return int(response['num_recs_added'])

    def get_db_page(self, page, named=True, database=None):
        #Get DB page from a qbase app
        request = {}
        if named == True:
            request['pagename'] = page
        else:
            request['pageID'] = page
        response = self.request('GetDBPage', database or self.database, request)
        return self._parse_db_page2(response)

    def get_schema(self, database=None):
        """Perform query and return results (list of dicts)."""
        request = {}

        response = self.request('GetSchema', database or self.database, request)
        return response

    def granted_dbs(self, adminOnly=0, excludeparents=0, includeancestors=0, withembeddedtables=0, database='main'):
        """Perform query and return results (list of dicts)."""
        request = {}
        if adminOnly:
            request['adminOnly'] = adminOnly
        if excludeparents:
            request['excludeparents'] = excludeparents
        if includeancestors:
            request['includeancestors'] = includeancestors
        if withembeddedtables:
            request['withembeddedtables'] = withembeddedtables

        response = self.request('GrantedDBs', database or self.database, request)
        return response

    def list_db_pages(self, database=None):
        request = {}
        response = self.request('ListDBpages', database or self.database, request)
        return self._parse_list_pages(response)


    ##HELPER METHODS USED IN CONJUNCTION WITH API
    def get_file(self, fname, folder, rid, fid, database=None):
        url = self.base_url + '/up/' + database + '/a/r' + rid + '/e' + fid + '/v0'
        r = requests.get(url)
        response = r.content
        if not os.path.isdir(folder):
            os.makedirs(folder)
        new_file = os.path.join(os.getcwd(), folder, fname)
        g = open(new_file, "wb")
        g.write(response)
        g.close()
        return new_file


if __name__ == '__main__':
    import doctest
    doctest.testmod()
