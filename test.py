import quickbase

username = 'kvseelbach'
password = 'lt76tamu'
dbase    = 'bgjtvsftx'
url = 'https://veil-technologies.quickbase.com'
token = 'cprti6xdbvvaxicv9pgtzd5h6w2g'

client = quickbase.Client(username, password, base_url=url, database=dbase, apptoken=token)
response = client.do_query(qid=13, columns='a')
print response
