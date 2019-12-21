from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='.')

@app.route('/', methods=['GET'])
def land():
    return render_template('index.html')

@app.route('/<query>', methods=['GET'])
def search(query):
    hostname = 'https://api.twitter.com/1.1/search/tweets.json'
    headers = {
        'User-Agent': 'MoodySwings v1.0',
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAGIJBgEAAAAAUxrixT7Yl%2FWaGJpbLS%2Fv57168iQ%3D2qHePT7eAiETsZRsO6tdD3jAuYkoaLLjl38XzzsvCSPbRl1ke6',
    }
    payload = {
        'q': query,
        'result_type': 'mixed',
        'count': 100,
        'tweet_mode': 'extended',
    }
    fullText = set()
    minId = -1

    # query up to 300 tweets
    for i in range(3):
        if i > 0: 
            payload['max_id'] = minId-1
        res = requests.get(url=hostname, headers=headers, params=payload)
        searchedTweets = res.json()['statuses']
        
        for tweet in searchedTweets:
            minId = min(minId, tweet['id'])
            if 'retweeted_status' in tweet:
                fullText.add('RT: ' + tweet['retweeted_status']['full_text'])
            else:
                fullText.add(tweet['full_text'])

    return render_template('index.html', query=query, tweets=fullText, numTweets=len(fullText))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)