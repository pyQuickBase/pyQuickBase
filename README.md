pyQuickBase: Python Interface to QuickBase API
==============================================

![image](https://badge.fury.io/py/pyquickbase.png%0A%20:target:%20http://badge.fury.io/py/pyquickbase)

pyQuickBase is an MIT licensed client library for the Intuit QuickBase
API, using [Requests](http://docs.python-requests.org/en/latest/) for
HTTP, and [lxml](http://lxml.de/) is used for XML processing.

Version
-------

0.2.3
-----

-   Added a new return\_file function to retrieve a QuickBase file as a
    Python file object.

0.2.2
-----

-   Fixed a readme issue.

0.2.1
-----

-   Made the package pip installable.
-   Added support for uploading files with add\_record module.

Installation
------------

To install pyQuickBase, simply:

~~~~ {.sourceCode .bash}
$ pip install pyquickbase
~~~~

API Features
------------

-   add\_record
-   add\_replace\_db\_page
-   delete\_record
-   do\_query
-   do\_query\_count
-   edit\_record
-   get\_db\_page
-   get\_schema
-   granted\_dbs
-   import\_from\_csv
-   list\_db\_pages

Other Modules
-------------

-   get\_file -- used in conjunction with a query and specified
    attachment field ID, can download one or many files from a table to
    local folder.

Requirements
------------

-   Python (2.6+)
-   [lxml](http://lxml.de/)
-   [Requests](http://docs.python-requests.org/en/latest/)
-   chardet
-   cStringIO

Examples
--------

Initialize the client:

~~~~ {.sourceCode .pycon}
>>> import quickbase
>>> client = quickbase.Client(username, password, database=database,
        apptoken=token, base_url=url)
...
~~~~

List all records in a table:

~~~~ {.sourceCode .pycon}
>>> import datetime
>>> response = client.do_query(query="'3'.XEX.''}", structured=True,
        columns='a', database=database)
>>> for record in response:
        dt = datetime.datetime.fromtimestamp(int(r['1']) / 1000).strftime('%m-%d-%Y')
        print "Record ID# %s was created on %s" % (record['3'], dt)
...
~~~~

License
-------

MIT, See license file.

Developed by [Kevin V Seelbach](http://www.kevinseelbach.com). You may
[email me directly](kevin.seelbach@gmail.com) if you have questions or
need help.

Contribute
----------

1.  Fork [the repository](http://github.com/kevinseelbach/pyQuickBase)
    on GitHub to start making your changes to the **master** branch (or
    branch off of it).
2.  Write a test which shows that the bug was fixed or that the feature
    works as expected.

