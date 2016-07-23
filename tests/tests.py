__author__ = 'Kevin V Seelbach'
import os
import unittest
import quickbase
import pprint
from lxml import etree

QUICKBASE_USER = os.environ['QUICKBASE_USER']
QUICKBASE_PASSWORD = os.environ['QUICKBASE_PASSWORD']
TEST_APP_TOKEN = # Your app token
TEST_APP_DBID = # Your app dbid
TEST_TABLE_DBID = # The table you are working with
TEST_BASE_URL = # Your QuickBase URL
pp = pprint.PrettyPrinter(indent=4)
module_dir = os.path.dirname(__file__)

class APITestCase(unittest.TestCase):
    username = QUICKBASE_USER
    password = QUICKBASE_PASSWORD
    app_dbid = TEST_APP_DBID
    table_dbid = TEST_TABLE_DBID
    import_csv_dbid = TEST_TABLE_DBID
    test_csv_file = # Your test file path
    test_csv_clist =  # Your test clist (string period delimited)
    realm = TEST_BASE_URL
    apptoken = TEST_APP_TOKEN

    @classmethod
    def setUpClass(cls):
        cls._client = quickbase.Client(username=cls.username, password=cls.password, database=cls.app_dbid,
                                       base_url=cls.realm, apptoken=cls.apptoken)

    @classmethod
    def tearDownClass(cls):
        cls._client.sign_out()

class GetSchemaTests(APITestCase):
    def test_get_app_schema(self):
        schema = self._client.get_schema(self.app_dbid)
        self.assertIsNotNone(schema)

    def test_get_table_schema(self):
        schema = self._client.get_schema(self.table_dbid)
        self.assertIsNotNone(schema)
        for field in schema:
            self.assertIn('field_type', field)
            self.assertIn('base_type', field)
            self.assertIn('id', field)

class AuthTestCase(APITestCase):
    def test_login(self):
        self.assertIsNotNone(self._client.ticket)
        self.assertIsNotNone(self._client.user_id)

class DoQueryTests(APITestCase):
    def test_do_query_with_qid_structured(self):
        response = self._client.do_query('', '6', database=self.table_dbid, structured=True)
        self.assertIsNotNone(response)

    def test_do_query_with_qid_unstructured(self):
        response = self._client.do_query('', '6', database=self.table_dbid, structured=False)
        self.assertIsNotNone(response)

    def test_do_query_with_query_unstructured(self):
        response = self._client.do_query("{'3'.XEX.''}", columns='a', database=self.table_dbid, structured=False)
        self.assertIsNotNone(response)

    def test_do_query_with_query_structured(self):
        response = self._client.do_query("{'3'.XEX.''}", columns='a', database=self.table_dbid, structured=True)
        self.assertIsNotNone(response)

    def test_do_query_count(self):
        query = "{'3'.XEX.''}"
        response = self._client.do_query_count(query, database=self.table_dbid)
        print "%d records match query." % (response)
        self.assertGreaterEqual(response, 0)


class EditRecordTests(APITestCase):
    def test_edit_record_named_friendly(self):
        rid = '1'
        fields = {'Match Value': '45', 'CLIST': '84.123.66.33'}
        response = self._client.edit_record(rid, fields, named=True, database=self.table_dbid)
        self.assertEqual(response['rid'], rid, "Record ID is equal.")
        self.assertLessEqual(int(response['num_fields_changed']), len(fields))

    def test_edit_record_named(self):
        rid = '1'
        fields = { 'match_value': '3', 'clist': '8.4.3.2.1' }
        response = self._client.edit_record(rid, fields, named=True, database=self.table_dbid)
        self.assertEqual(response['rid'], rid, "Record ID is equal.")
        self.assertLessEqual(int(response['num_fields_changed']), len(fields))

    def test_edit_record_fids(self):
        rid = '1'
        fields = {'7': '95', '8': '7.94.92.101'}
        response = self._client.edit_record(rid, fields, named=False, database=self.table_dbid)
        self.assertEqual(response['rid'], rid, "Record ID is equal.")
        self.assertLessEqual(int(response['num_fields_changed']), len(fields))


class AddRecordTests(APITestCase):
    def test_add_record_fids(self):
        response = self._client.add_record({'7': '124', '8': '842.111.22'}, named=False, database=self.table_dbid)
        self.assertGreaterEqual(response, 1)

    def test_add_record_named(self):
        response = self._client.add_record({'Match Value': '333', 'clist': '43.22.11', 'slist': '88.23.54'},
                                           named=True, database=self.table_dbid)
        self.assertGreaterEqual(response, 1)

def valid_XML_char_ordinal(i):
    return ( # conditions ordered by presumed frequency
             0x20 <= i <= 0xD7FF
             or i in (0x9, 0xA, 0xD)
             or 0xE000 <= i <= 0xFFFD
             or 0x10000 <= i <= 0x10FFFF
    )


class ImportFromCSVTests(APITestCase):
    def test_import_from_csv_rids_and_delete(self):
        test_data = open(self.test_csv_file, 'r').read()
        test_data = ''.join(c for c in test_data if valid_XML_char_ordinal(ord(c)))
        response = self._client.import_from_csv(test_data, clist=self.test_csv_clist,
                                                clist_output='3.6.7',
                                                database=self.import_csv_dbid)
        self.assertIsNotNone(response)
        num_rec_added = response.findtext('num_recs_added')
        rows = []
        for item in response.iterfind('.//fields'):
            tmp = {}
            for field in item.iterchildren():
                tmp.update({(field.get('id')): field.text})
            rows.append(tmp)


if __name__ == '__main__':
    unittest.main()
