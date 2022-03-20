import sqlite3
conn = sqlite3.connect('emaildb.sqlite')

cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS user')
cur.execute('''
CREATE TABLE user(email TEXT,count INTEGER)
''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox.txt'
fh = open(fname, mode='r', encoding='utf-8')
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    i = email.index('@')
    email = email[i + 1:]
    cur.execute('SELECT count FROM user WHERE email = ?', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''
        INSERT INTO user(email,count)
        VALUES(?,1)''', (email,))
    else:
        cur.execute('UPDATE user SET count = count+1 WHERE email = ?', (email,))

conn.commit()

sqlstr = 'SELECT email, count FROM user ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

sqlstr1 = 'SELECT email, MAX(count) FROM user '

for row in cur.execute(sqlstr1):
    print(str(row[0]), row[1])

cur.close()