pyQuickBase
=========

pyQuickBase is a Python interface to the Intuit QuickBase API using [**Requests.py**][requests] for HTTP, and [**lxml**][lxml] is used for XML processing.


Version
-
## 0.2.1
- Added support for uploading files with add_record module.


API Features
-----------
+ add_record
+ add_replace_db_page
+ delete_record
+ do_query
+ do_query_count
+ edit_record
+ get_db_page
+ get_schema
+ granted_dbs
+ import_from_csv
+ list_db_pages

Other Modules
-----------
+ get_file -- used in conjunction with a query and specified attachment field ID, can download one or many files from a table to local folder.

Requirements
-----------
* Python (2.6+)
* [lxml]
* [Requests]
* chardet
* cStringIO

Examples
--------------
Initialize the client:

    :::python
        import quickbase

        client = quickbase.Client(username, password, database=database,
                                  apptoken=token, base_url=url)

List all records in a table:

    :::python
    import datetime
        response = client.do_query(query="'3'.XEX.''}", structured=True,
                                   columns='a', database=database)
        for record in reponse:
            dt = datetime.datetime.fromtimestamp(int(r['1']) / 1000).strftime('%m-%d-%Y')
            print "Record ID# %s was created on %s" % (record['3'], dt)

License
-
MIT, See license file.

Developed by [**Kevin V Seelbach**][kvs]. Contact me by email at [kevinseelbach@gmail.com][ks].

  [requests]: http://docs.python-requests.org/en/latest/
  [lxml]: http://lxml.de/
  [kvs]: http://www.kevinseelbach.com/
  [ks]:kevinseelbach@gmail.com
  [oyster]: https://github.com/oysterhotels/quickbase
