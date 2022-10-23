import sqlite3
class bd:
    def __init__(self, name ):
        self.connect = sqlite3.connect(name, check_same_thread=False)
        self.cursor = self.connect.cursor()
    def sms (self,product):
        p =  self.cursor.execute('SELECT * from bot_table WHERE Name = ? ',(product,)).fetchall()
        return p


    def price(self,m,f):
        result = self.cursor.execute('SELECT Price from bot_table WHERE Name = ? AND Diller = ?', (f.capitalize(),m,)).fetchall()
        return result

    def update(self,name,f):
        e = self.cursor.execute('SELECT Quantity from bot_table WHERE Name = ? AND Diller = ?  ', (name.capitalize(),f,)).fetchall()
        print(e)
        e = e[0]
        e = e[0]
        e = int(e) - 1
        e = str(e)
        print(e)
        with self.connect:
            self.cursor.execute('UPDATE bot_table SET Quantity = ? WHERE Name = ? AND Diller = ? ',(e,name.capitalize(),f,))



