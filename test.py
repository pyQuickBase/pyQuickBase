import quickbase

username = 'kvseelbach'
password = 'lt76tamu'
dbase    = 'bgjtvsftx'
url = 'https://www.quickbase.com'
token = 'cprti6xdbvvaxicv9pgtzd5h6w2g'

client = quickbase.Client(username, password, database=dbase, apptoken=token, realmhost='veil-technologies.quickbase.com')
response = client.do_query(qid=13, columns='3', num=50, skip=10)
print response
