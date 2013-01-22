import quickbase

username = 'kvseelbach'
password = 'lt76tamu'
dbase    = 'bgiv6iafj'
url = 'https://veil-technologies.quickbase.com'
token = 'cprti6xdbvvaxicv9pgtzd5h6w2g'

client = quickbase.Client(username, password, database=dbase, apptoken=token, base_url=url)

response = client.do_query(query="{'3'.EX.'1'}", structured=True, columns='3.7', database='bgjrjgcje')

for r in response:
    if r['7'] is not None:
        rid = r['3']
        fname = r['7']
        file = client.get_file(fname=fname, folder='app-images', fid='7', rid=rid, database='bgjrjgcje')
        print file
