from django.shortcuts import render
import tweepy
from textblob import TextBlob  
import simplejson as json
from matplotlib import pyplot as plt 
from langdetect import detect

# Create your views here.
def home(request):
    return render(request,'home.html')

def getLang(langList):
    dict = {}
    

def getAnalysis(Analysis):
    name = ['positive','nutral','nagative']
    count = [0,0,0]
    for i in Analysis:
        if i<0:
            count[2]+=1
        elif i==0:
            count[1]+=1
        else :
            count[0]+=1
    plt.bar(name,count)
    #plt.bar(name, count, align='center', alpha=0.5)
    plt.ylabel('Count')
    plt.title('Sentiment')
    plt.savefig(r"static\Analysis.png") 
    plt.clf()
    return   

def getLang(Analysis):
    name2 = ['English','Hindi','French','Japanesh','Chinesh','Russian','Other']
    count2 = [0,0,0,0,0,0,0]
    for i in Analysis:
        if i=='en':
            count2[0]+=1
        elif i=='hi':
            count2[1]+=1
        elif i=='fr':
            count2[2]+=1
        elif i=='ja':
            count2[3]+=1
        elif i=='zh-cn':
            count2[4]+=1
        elif i=='ru':
            count2[5]+=1                
        else :
            count2[6]+=1
            
    plt.bar(name2,count2)
    #plt.bar(name, count, align='center', alpha=0.5)
    plt.ylabel('Count')
    plt.title('Languages Analysis')
    plt.savefig(r"static\LangAnaly.png") 
    plt.clf()
    return 
     

    





def result(request):
    s=request.GET['search']
    print(s)
    consumer_key='81vF03XpNUTi3TlKkskujt35D'
    consumer_secret='haIjHArQTxndszj5Q9Vfs6HoASSLTCBwqDDbOsElfxd7Xw6YIl'
    access_token='1218525746697658368-ph7yuWluqdsMPtIWzrlSxsA1Z8SN5q'
    access_token_secret='smQXZ5iMk7vHzzCpyWjK708rHQN6BoqBvIv9uhpg0kP9w'
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)
    public_tweets=tweepy.Cursor(api.search,q=s).items(100)
    lsLocation = []
    lsTweets = []
    lsLang = []
    laAnalysis = []
    lsConti = set()
    setLang = set()
    setLoca = set()
    for tweet in public_tweets:
        #print(tweet.text)
        analysis=TextBlob(tweet.text)
        #print(analysis)
        laAnalysis.append(analysis.sentiment.polarity)
        lsLocation.append(tweet.user.location)
        setLoca.add(tweet.user.location)
        lsTweets.append(tweet.text)
        lsConti.add(tweet.user.id)
        tg = detect(tweet.text)
        lsLang.append(tg)
        setLang.add(tg)
        #print(tweet.user)
        #sdata = json.dumps(tweet.__json) 
        #print("###################################",tweet.user.location,"#####################################")
    getAnalysis(laAnalysis)
    getLang(lsLang)
    #print(lsLang)
    Info = {}
    Info['location'] = lsLocation
    #Info['tweets'] = lsTweets
    Info['languages'] = lsLang 
    Info['Analysis'] = laAnalysis
    Info['Analysis_Img'] = 'Analysis.png'
    Info['Contribut'] = len(lsConti) 
    Info['TotLang'] = len(setLang)
    Info['TotLoca'] = len(setLoca) 
    
    return render(request,'result.html',{'tweets':lsTweets,'keyword':s,'result':Info})