import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle
import re
import flask
import praw
from flask import Flask, render_template, request

app=Flask(__name__)

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,_;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

flairs={1:"AskIndia",
2:"Non-Political",
3:"[R]eddiquette",
4:"Scheduled",
5:"Photography",
6:"Science/Technology",
7:"Politics",
8:"Business/Finance",
9:"Policy/Economy",
10:"Sports",
11:"Food",
12:"AMA"
}

@app.route('/')

@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/statistics')
def statistics():
    return flask.render_template('statistics.html')

@app.route("/register", methods=["POST"])
def register():
    if request.method=='POST':
        nm = request.form.get("url")
        mm=nm

        df1=pd.read_csv("cleaned_reddit_alphabeta.csv")
        df1.dropna(inplace=True)
        df1.columns=['index','combined','flair']  
        print (df1.head())

        X_train, X_test, y_train, y_test = train_test_split(df1['combined'],df1['flair'],random_state=0)

        # Fit the CountVectorizer to the training data
        vect = CountVectorizer().fit(X_train)
        X_train_vectorized = vect.transform(X_train)

        model = RandomForestClassifier(n_estimators=500, criterion='entropy')
        model.fit(X_train_vectorized, y_train)
        '''
        model = LogisticRegression(solver='lbfgs', multi_class='auto')

        model.fit(X_train_vectorized, y_train)
        #print(model.predict(vect.transform(['mbassador of ndia takes back my newly issued  card  suggests a pay for and fill out new application lease advise https  wwwredditcom r india comments bdfid1 ambassador of india takes back my newly issued   onestly  she and her supervisor behaved exactly how most of our government officers behave with residents of ndia nside ndia  they typically do such things to extract a bribe  cant say for sure if she has the same expectation#x200 ne option you have  if  matters so much to you  is to tweet your problem directly to ndias oreign inister  ushma waraj he is supposed to be proactive about such things  especially when it comes to matters like these where they like to project a good  but false  image of our government  and tweeting to her in front of millions of followers basically forces her hand into helping you lso  pulling strings this way by bringing in somebody influential to get what you want is very much the ndian way  and since you wish to become a quasicitizen of ndia  you might as well start learning our bad habits#x200   personally  am not a big fan of kowtowing to influential people or to our government officials  wouldnt have gone for an  to begin with  and if  absolutely had to for some reason  d try it once and drop the idea once it turned out to be too hard ou have already sunk enough costs for a card that is of little benefit  suggest dropping the idea entirely s a anadian   dont think youll have any trouble getting multiple entry tourist visa for frequent visits his lady sounds full of shit hy would an ambassador concern himself herself with  affairs ven if she isnt lying  its worth emailing the consulate embassy politely explaining the situation and ccing the ambassador if you can find their email f there are multiple consular missions in the country  try emailing them as well weet a summary with some details to ushma waraj   she has helped ppl in similar situations i  m sorry to hear that you had to go through this oud think these people would adapt to the local work culture ethic but it seems they are pushing their work culture and ethic on the locals  which shouldnt be the case#x200 lease tweet your issue to the minister of external affairs   https  twittercom ushmawarajref srctwsrc5google7twcamp5serp7twgr5author  https  twittercom ushmawarajref srctwsrc5google7twcamp5serp7twgr5author  #x200 make sure its public and that her twitter is tagged in your post he is very well known to bring visa officers in line when they refuse to carry out their duty o keep us posted about things you did for this issue f it is just for a visit  apply for a regular visa ou can always visit ndia as a tourist s regards your  card application  tweet or send a message to the xternal ffairs inister ushma waraj with your experience probably you are lying in fine details  or it is shitpost or karma whoringas an official  one can certainly say that  an ambassador is too busy to deal with  e drive 7 hours to the mbassy  getting pumped up to an audiobook set in ndia  yes  were nerds  r iamverysmart individuals  moreover  if any of the official encounters technical problems  it is impossible for them to say cannot be done because of bad mood   an embassy is not your regular post office branches the productivity level despite being in perpetual shortage of stuff is inspiring for all other government branches  if you have any kind of proof about your claims of misbehaviour get out of anonymity  go for appropriate mechanism    if you dont know the mechanism  pm me your proof  i will provide you'])))
        '''
        reddit = praw.Reddit(client_id='WBTxS7rybznf7Q', client_secret='vJUTUflXITBsQMxeviOfG8mCZoA', user_agent='projectreddit', username='Mysterious_abhE', password='Saxena0705')
        #url="https://www.reddit.com/r/MapPorn/comments/a3p0uq/an_image_of_gps_tracking_of_multiple_wolves_in/"
        submission = reddit.submission(url=nm)
        #print (submission.comments[0])
        #print (submission.title)
        submission.comments.replace_more(limit=0)
        #co=[]
        tr=[]
        c=''
        for top_level_comment in submission.comments:        
            c+=top_level_comment.body  


        tr=submission.title+nm+c
        #processed_tweets=[]
        #for tweet in range(len(tr)):  
        processed_tweet = re.sub(r'\W', ' ', str(tr))

            
        # Remove all the special characters
    
        processed_tweet = re.sub(r'http\S+', ' ', processed_tweet)
    
        #processed_tweet = re.sub(r'https?:\/\/+', ' ', processed_tweet)
    
        #processed_tweet=re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ',processed_tweet)
    
        processed_tweet=re.sub(r'www\S+', ' ', processed_tweet)
    
        processed_tweet=re.sub(r'co \S+', ' ', processed_tweet)
        # remove all single characters
        processed_tweet = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_tweet)
        # Remove single characters from the start
        processed_tweet = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_tweet) 
 
        # Substituting multiple spaces with single space
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)
 
        # Removing prefixed 'b'
        processed_tweet = re.sub(r'^b\s+', ' ', processed_tweet)
    
        processed_tweet = re.sub(r'\d','',processed_tweet)
    
        processed_tweet= re.sub(r'\s+', ' ', processed_tweet, flags=re.I)

 
        # Converting to Lowercase
        processed_tweet = processed_tweet.lower()
        processed_tweet=processed_tweet.replace('_',' ')
    
        #processed_tweets.append(processed_tweet)
    
        print ((processed_tweet))            #print(model.predict(vect.transform([tr])))
        #filename='comb_model.pkl'

        #pickle.dump(model, open(filename, 'wb'))
        #load_lr_model =pickle.load(open(filename, 'rb'))
        #print (load_lr_model.predict(vect.transform([tr])))


    return flask.render_template('result.html',prediction=flairs[int(model.predict(vect.transform([processed_tweet])))],url=mm)
        
