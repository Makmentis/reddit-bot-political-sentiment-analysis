import sqlite3
from praw import Reddit
from textblob import TextBlob
from textblob import sentiments
from bad_words_dict import russophobic_words as badWords

reddit = Reddit(client_id = 'l4REMOOgfgDHoA',
                     client_secret = 'GFqP4qtyZNLH6XqPATxGODNyZLs',
                     username = 'Yerundy',
                     password = 'redditsilver',
                     user_agent = 'reddit project')

dates = [1519227412, 1508598932, 1503338852, 1493198052, 1483294052, 1475345252]

subreddit = reddit.subreddit('europe+history+askhistorians+askeurope')

conn = sqlite3.connect('sampl.db')
c = conn.cursor()
k = 0

#ключевые слова для фильтрации заголовков и комментариев:
tags =              ['russia', 'russian','russians','moscow', 'soviet',          
                    'kremlin','saint petersburg', 'stalin', 'communists',
                    'ussr','soviet','putin','navalny', 'chechnya',
                    'ukraine','ukranian','ukranians']

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS comments_table(comment TEXT, negativity REAL)')

def data_entry(comment, negativity):
    c.execute("INSERT INTO comments_table VALUES(?, ?)",(comment, negativity))
    conn.commit()
    

#чекает длин и удаляет цитирования, чтобы не заносить комментарии в базу повторно:
def parse(comment):
    if len(comment)<1500 and len(comment)>70:   
        while '>' in comment:                   
            comment = comment[0:comment.find('>')] + comment[comment.find('\n',comment.find('>')):len(comment)] 
        return(comment)
       
    else:
        return (None)
    
def check_positivity(comment, i,k):
    
    if comment:
        blob = TextBlob(comment.lower())
        words = blob.words
        polarity = 0
        
        for x in badWords.keys():
            if x in comment:
                polarity += badWords[x]/10

        combined = polarity + blob.sentiment[0]
        if polarity<-0.6 or ((combined)<-0.4 and lists_overlap(words,tags)) or (polarity<-0.29 and lists_overlap(words,tags)) or ((combined)<-1.5):
            print(20*'-')
            try:
                
                print('polarity:', combined, '\nnumber of pos comms:', i,' submission  №',k)
                print('number of all the parsed comments:', h)
                data_entry(comment, combined)
                #print(i)
                return 1
            except Exception as e:
                    print(e)
            #print()
        
    return 0

def lists_overlap(a,b):                 
    return (bool(set(a) & set(b)))      #Возвращает True если два списка имеют одинаковые элементы
        


i = 0
h = 0

create_table()

for submission in subreddit.submissions(dates[1],dates[0]):
    #comments = [comment for comment in submission.comments.list()]
    k+=1
    if submission.num_comments>0:
        normalized_title = submission.title.lower()
        

        for title_tag in tags:
            if title_tag in normalized_title:
                
                submission.comments.replace_more(limit=None, threshold =10)     #подгружает скрытые комментарии
                    
                for comment in submission.comments.list():
                    
                    i+= check_positivity(parse(comment.body),i,k)
                    h+=1
                   
                break
    
c.close()
conn.close()   

