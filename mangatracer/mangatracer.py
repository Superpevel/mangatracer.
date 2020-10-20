from bs4 import BeautifulSoup
from telebot import types
import requests
import telebot
import config
import sqlite3
import re 
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36' , 'accept':'*/*'}

import requests

bot = telebot.TeleBot(config.token)
conn = sqlite3.connect("manga.db",check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Manga
                  (mangaid INTEGER PRIMARY KEY AUTOINCREMENT,manga_url text, 
                  manga text, 
                  actual_chapter text,savedchapter text,userid INT)
               """)                                  
    
def get_html(url,params=None):
  r = requests.get(url,headers=HEADERS, params = params)
  return r                                                                                                                    
def get_content(html,user,manid,i):
   soup = BeautifulSoup(html,'html.parser')
   manganame = soup.find('span', class_='name')
   
   chapter = soup.find('h4')
   print(chapter.text)
   with conn:
     cur = conn.cursor()
     
     print(manid)
     print(user)
     cur.execute(f"UPDATE Manga SET manga = '{manganame.text}',actual_chapter = '{chapter.text}' WHERE userid = '{user}' and mangaid = '{manid}'")
     conn.commit()                                                                                                                 
   
def parse(urls,user,mangaid,i):
   html = get_html(urls)
   if html.status_code == 200:
        get_content(html.text,user,mangaid,i)
   else:
     print('EROR')                                  
def parsit(message):
 username = name(message)
 mangaid = getmangaid(message)
 urls = getmangaurl(message)
 for i in range(len(urls)) :
     parse(urls[i],username[0],mangaid[i],i)
  




def getname(id):
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT manga FROM Manga")
    name = cur.fetchall()
    nam = list(name)
    return(nam[id])   
     
@bot.message_handler(commands=['start'])
def start(message):
   y=1
   conn = sqlite3.connect("manga.db",check_same_thread=False)

   cur = conn.cursor()
   cur.execute("SELECT username FROM USER  ")
   
   user  = cur.fetchall()
  
   for us in user :
        for u in user :
            if str(message.chat.id) == re.sub(r"[('),]", "",str(u)):
                print("ДАРОВА")
                print(y)
            else:
                conn = sqlite3.connect("Manga.db",check_same_thread=False)
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO USER VALUES (NULL,'{message.chat.id}',NULL)")
                conn.commit()
                break
                

def getid(id):
   y=1
   conn = sqlite3.connect("manga.db",check_same_thread=False)

   cur = conn.cursor()
   cur.execute("SELECT username FROM USER  ")
   user  = cur.fetchall()
   for us in user :
        for u in user :
            if str(id) == re.sub(r"[('),]", "",str(u)):
                
                
                return(y)
                break 
            else:
                y=y+1
                
                    
    
 
@bot.message_handler(commands=['update'])
def start_message(message):
    parsit(message.chat.id)
    username = name(message.chat.id)
    print(username)
    
   
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message.chat.id:
           if m[i-2] != m[i-1]:
                print(m[i-4] + m[i-3]+ m[i-2])
                bot.send_message(message.chat.id,"Вышла новая глава"+"  " + m[i-4] +"  "+ m[i-3]+  "  "+ m[i-2]) 
                with conn:
                   cur = conn.cursor()
                   cur.execute(f"UPDATE Manga SET savedchapter = '{m[i-2]}' WHERE userid = '{m[i]}' and mangaid = '{m[i-5]}'")
                   conn.commit()  
    bot.send_message(message.chat.id, 'Обновлено!')  
   

@bot.message_handler(commands=["manga"])
def manga(message):
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message.chat.id:
           bot.send_message(message.chat.id," Манга: "+ m[i-3]+  "  "+ m[i-2] + '            ' + 'Cсылка на мангу'+ m[i-4]) 
                
       
        

      

def getmangaurl(message):
    urls = []
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message:
           urls.append(m[i-4])
     return(urls)      ##mangaurl
def getmanga_name(message):
    manganame = []
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message:
           manganame.append(m[i-3])
     return(manganame)
def getmanga_chapter(message):
    chapter = []
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message:
           chapter.append(m[i-2])
    return(chapter)
                                  
def name(message):
    name = []
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message:
           name.append(m[i])
     return(name)      ##mangaurl
    
def getmangaid(message):
    mangaid = []
    with conn:
     cur = conn.cursor()
     cur.execute("SELECT * FROM Manga ")
     mangas = cur.fetchall()
     for m in mangas: 
      for i in range(len(m)) :
       if m[i] == message:
           mangaid.append(m[i-5])
     return(mangaid)      ##mangaurl  
       

@bot.message_handler(content_types=['text']) 
def get_text_messages(message): 
    if 'http' in message.text: 
     
     conn = sqlite3.connect("Manga.db",check_same_thread=False)
     cursor = conn.cursor()
     cursor.execute(f"INSERT INTO Manga VALUES (NULL,'{message.text}',NULL,NULL,NULL,'{message.chat.id}')")
     conn.commit() 
     bot.send_message(message.chat.id, 'Манга добавленна')
    else:
        pass
         
    
if __name__ == '__main__':
    bot.polling(none_stop=True)
