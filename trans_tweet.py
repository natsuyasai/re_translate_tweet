"""
Twitterから取得したテキストデータを英訳後，日本語に再翻訳するプログラム
"""
# coding: utf-8
import json
import Access_Token
from requests_oauthlib import OAuth1Session
import time, calendar #日本時間変換用
import io,sys
from microsofttranslator import Translator #翻訳

#標準出力をutf-8にラップ
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#Twitter認証用
twitter = OAuth1Session(Access_Token.CONSUMER_KEY,
                        Access_Token.CONSUMER_SECRET,
                        Access_Token.ACCESS_TOKEN,
                        Access_Token.ACCESS_TOKEN_SECRET)
#翻訳用
my_translator = Translator(Access_Token.CLIENT_ID, Access_Token.CLIENT_KEY)

"""
タイムライン
"""
def HomeTimeLine():
    #タイムライン
    access_url_of_timline = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    params={} #パラメータ設定用

    #twitterインスタンスにより情報取得
    request = twitter.get(access_url_of_timline, params = params)
    #タイムライン情報のみ抜き出し(ユーザ情報等込み)
    timeline = json.loads(request.text)
    timeline.reverse() #逆順に変更
    ResultPrint(timeline,"name") #結果表示

"""
検索
"""
def TweetSerach(search_word):
    #検索ワード
    if search_word == "":
        search_word = "意識低い系"

    #検索結果
    access_url_of_search = "https://api.twitter.com/1.1/search/tweets.json?count=100&lang=ja&q=" + search_word
    params={'count':10} #パラメータ設定用(20161120：現状動いていない)

    request = twitter.get(access_url_of_search, params = params)
    timeline = request.json()["statuses"]
    timeline.reverse() #逆順に変更
    ResultPrint(timeline,"") #結果表示

"""
結果表示
"""
def ResultPrint(timeline,option):
    i=0
    if option == "name":
            #ツイート内容表示
            for tweet in timeline:
                try:
                    print("---------------------------------------------------------------------------------------")
                    #print("@" + tweet["user"]["screen_name"])
                    print("元：")
                    print(tweet["text"]) #ツイート内容のみ表示
                    print("再翻訳")
                    print(TweetTranslator(tweet["text"]))
                    print(YmdHMS(tweet["created_at"]))
                except:
                    print("Error")
                if i == 10:
                    break
                i+=1
    else:
        #ツイート内容表示
        for tweet in timeline:
            try:
                print("---------------------------------------------------------------------------------------")
                #print("@" + tweet["user"]["screen_name"])
                print("元：")
                print(tweet["text"]) #ツイート内容のみ表示
                print("再翻訳：")
                print(TweetTranslator(tweet["text"]))
                print(YmdHMS(tweet["created_at"]))
            except:
                print("Error")
            if i == 10:
                break
            i+=1


"""
日本時間変換
"""
def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return int(time.strftime("%Y%m%d%H%M%S", time_local))


"""
Bing翻訳
"""
def TweetTranslator(string_text):
    trans_en = my_translator.translate(string_text,from_lang="ja",to_lang="en") #英語に翻訳
    re_trans_ja = my_translator.translate(trans_en,from_lang="en",to_lang="ja") #日本語に再翻訳
    return re_trans_ja #再翻訳結果を返す
    #print(my_translator.translate(string_text,from_lang="ja",to_lang="en"))

if __name__=="__main__":
    args = sys.argv

    if len(args) == 1:
        print("TL,tl：タイムライン表示\nSEARCH,search：検索結果表示(第2引数に検索ワードを指定)")
    elif args[1] == "TL" or args[1] == "tl":
        HomeTimeLine()
    elif args[1] == "SEARACH" or args[1] == "search":
        if len(args) == 2:
            TweetSerach("")
        else:
            TweetSerach(args[2])
