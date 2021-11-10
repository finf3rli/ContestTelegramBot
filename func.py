import datetime
import time
import emoji
import mysql.connector

def checkUserSub(chat_id, bot) -> bool:  # Check if user is subbed or not to channel(SHOULD BECOME -> BOOL TRUE FALSE)
    #if checkOnDB(id):
    #    bot.sendMessage(id, " Sei già presente in lista, alla posizione n." + str(printRank(id)))
    #else:
    try:
        member = bot.getChatMember("@@id channel", chat_id)    #chat_id represents users' unique id
        if member["status"] in ["administrator", "creator", "member"]:
            return True
            #member["user"]["username"] -> username
        else:
            return False
    except:
        bot.sendMessage(chat_id, "Errore inaspettato")

#select UNIX_TIMESTAMP(timeSub) from userList order by timeSub asc; query per selezionare in base a timestamp

def connectDB():
    c = mysql.connector.connect("""db parameters""")
    return c
'''
def p():
    list = ''
    cn = connectDB()
    cur = cn.cursor()
    cur.execute("SELECT * FROM userList")
    r = cur.fetchall()
    for i in r:
        list += str(i)
    return list
'''
def printList(chat_id, bot):
    list = ''
    cn = connectDB()
    cur = cn.cursor()
    cur.execute("SELECT * FROM  order by  asc")
    r = cur.fetchall()
    n = 1
    for i in r:
        try:
            member = bot.getChatMember("@id channel", str(i[0]))    #chat_id represents users' unique id
            if member["status"] in ["administrator", "creator", "member"]:
                list += str(n) + ': ' + str(i[1]) + '\n' #list += (str(i[0])+ ' - ' + str(i[2]) +'\n')
                n = n + 1
            else:
                cur.execute("DELETE FROM  where id = " + str(i[0]))
                cn.commit()
        except:
            print("errore in printList")
    closeDB()
    return list


def printRank(id, bot):
    out = ""
    cn = connectDB()
    cur = cn.cursor()
    if(checkOnDB(id)):
        cur.execute('select count(*), UNIX_TIMESTAMP(timeSub) from  where UNIX_TIMESTAMP() < (select UNIX_TIMESTAMP() from  where id = '+str(id)+')')
        r = cur.fetchall()
        out = "\U0001F396 Sei alla posizione n."+str(r[0][0]+1)
    else:
        out = emoji.emojize(":x:", use_aliases = True) + " Non sei ancora iscritto al contest. /iscrivimi"
    closeDB()
    return out

def addUser(id, bot):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cn = connectDB()
    cur = cn.cursor()
    member = bot.getChatMember("@id channel", id)
    username = member["user"]["username"]
    if checkUserSub(id, bot):
        if(checkOnDB(id) == False):
            cur.execute('insert into userList values(%s,%s,%s)',(id,username,timestamp))
            cn.commit()
            if checkOnDB(id):
                return True
        else:
                return True
    else:
        return False
            #printRank(id, bot)
    closeDB()
    #else:
        #bot.sendMessage(id, "Sei già iscritto al contest. posizione n...")
    #closeDB()#aggiunto dopo

def removeUser(id) -> bool:
    cn = connectDB()
    cur = cn.cursor()
    if checkOnDB(id):
        cur.execute('delete from  where id = '+str(id))
        cn.commit()
        closeDB()
        return True
    else:
        closeDB()
        #bot.sendMessage(id, "Non facevi già parte del contest. Azione annullata")
        return False
    #closeDB()

def emptyTable():
    cn = connectDB()
    cur = cn.cursor()
    cur.execute('truncate table ')
    cn.commit()
    closeDB()

def checkOnDB(id) -> bool:
    cn = connectDB()
    cur = cn.cursor()
    cur.execute('select * from  where id = '+str(id))
    r=cur.fetchone()
    closeDB()
    if(r == None):
        return False
    else:
        return True

def closeDB():
    connectDB().close()
