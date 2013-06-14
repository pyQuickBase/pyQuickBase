__author__ = 'Kevin V Seelbach'

import unittest
import quickbase
import pprint
import os

QUICKBASE_USER = os.environ(['QUICKBASE_USER'])
QUICKBASE_PASSWORD = os.environ(['QUICKBASE_PASSWORD'])
APPTOKEN = os.environ(['QUICKBASE_TOKEN'])

# Edit the tests with your values and desired FIDs. Tables must exist before running tests. In the future, I would like to add functionality to create an app, bootstrap with tables and test data, and cleanup after testing. 


class APITestCase(unittest.TestCase):
    username = QUICKBASE_USER
    password = QUICKBASE_PASSWORD
    app_dbid = # App dbid
    table_dbid = # Table you are using for testing
    realm = # Url of your realm, e.g. https://companyname.quickbase.com
    apptoken = 'ds6psqvbjrvkahmgbspfdy43d7v'

    @classmethod
    def setUpClass(cls):
        cls._client = quickbase.Client(username=cls.username, password=cls.password, database=cls.app_dbid, base_url=cls.realm, apptoken=cls.apptoken)

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
        query = "{'3'.EX.''}"
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


if __name__ == '__main__':
    unittest.main()
