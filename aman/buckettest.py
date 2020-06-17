import sqlite3
from random import choice
superHeroes = ['Ironman', 'Captain Amperica','Wonder Woman','Superman']
tvseries = ['Game of Thrones', 'Money Heist', 'Peaky Blinders', '13 reasons Why']
anime = ['Goku', 'Naruto', 'Pokemon', 'Death Note']
games = ['PUBG', 'God Of War', 'GTA-V', 'CyberPunk']

def bucket(preferences):
    preferences = preferences.split(',')
    suggest = []
    for tic in preferences:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT productId, name, image FROM products WHERE name = ?', (tic, ))
            k = cur.fetchall()
            suggest.append(k)
    conn.close()
    ans = []
    ans.append(choice(suggest[0]))
    ans.append(choice(suggest[1]))
    ans.append(choice(suggest[2]))
    ans.append(choice(suggest[3]))
    return ans


preferences = 'Captain America,Game of Thrones,Death Note,God Of War'
ans = bucket(preferences)
print(ans)