pyQuickBase
=========
  
pyQuickBase is a Python interface to the QuickBase API. The modules adhere to the QuickBase API call naming convention, written in the Python syntax. Requests are made with [**Requests.py**][requests], and [**lxml**][lxml] is used for XML processing. 

This project is a work-in-progress. It is my intent to build a __*better*__ wrapper to QuickBase: one that is efficient, dependable, and enhances developer productivity. I chose the modules I did for their *speedy reputation*. It supports tokenization, SSL, and the mostly-unknown *realm option*, among other parameters.

Version
-

0.1

Requirements
-----------
* Python (2.6+)
* [lxml]
* [Requests]

Examples
--------------
    client = quickbase.Client(username, password, database=dbase, apptoken=token, base_url=url)
    response = client.do_query(query="'3'.XEX.''}", structured=True, columns='a', database='yourdbname')
    for r in reponse:
        print r

License
-
MIT

Developed by [**Kevin V Seelbach**][ks] for professional use at [VeilSun][vs]. Contact me by email at [kseelbach@veiltech.com][ks].

  [requests]: http://docs.python-requests.org/en/latest/ 
  [lxml]: http://lxml.de/
  [vs]: http:www.veilsun.com
  [ks]:kevinseelbach@gmail.com