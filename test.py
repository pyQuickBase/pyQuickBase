import quickbase

username = 'kvseelbach'
password = 'lt76tamu'
dbase    = 'bgjtvsftx'
url = 'https://www.quickbase.com'
token = 'cprti6xdbvvaxicv9pgtzd5h6w2g'

client = quickbase.Client(username, password, database=dbase, apptoken=token, realmhost='veil-technologies.quickbase.com')
response = client.do_query(qid=13, columns='3.4.5.6.7.8.9.10', num=50, skip=10, include_rids=True, structured=True)
print response
