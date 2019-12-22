from flask import Flask, render_template, request, Response
import requests
import json
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app)


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
    
    data = {
        'query': query,
        'tweets': list(fullText),
        'numTweets': len(fullText),
    }
    resBody = json.dumps(data)
    res = Response(resBody, status=200, mimetype='application/json')
    res.headers['host'] = 'localhost:5000'
    return res
    # return render_template('index.html', query=query, tweets=fullText, numTweets=len(fullText))

if __name__ == '__main__':
    app.run(host='localhost', debug=True)