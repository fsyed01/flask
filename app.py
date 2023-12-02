from flask import Flask, jsonify, request, abort
import json
app = Flask(__name__)

# Load tweet data from the file
with open('100tweets.json', 'r', encoding='utf-8', errors='ignore') as file:
    # Use json.loads to handle decoding manually
    tweets_data = json.loads(file.read())

@app.route('/')
def hello_world():
    return "Hello World!"

@app.route('/tweets', methods=['GET'])
def get_all_tweets():
    query_param = request.args.get('filter')
    if query_param:
        filtered_tweets = [tweet for tweet in tweets_data if query_param.lower() in tweet['text'].lower()]
        return jsonify(filtered_tweets)
    else:
        return jsonify(tweets_data)

@app.route('/tweet/<int:tweet_id>', methods=['GET'])
def get_tweet_by_id(tweet_id):
    try:
        tweet = next(tweet for tweet in tweets_data if tweet['id'] == tweet_id)
        return jsonify(tweet)
    except StopIteration:
        abort(404)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)

# Example curl request for the endpoint that returns hello world
# curl http://localhost:5001/
## Expected response: Hello world
# Example curl request for the endpoint that returns all tweets
# curl http://localhost:5000/tweets
# Expected response: JSON data of all tweets
# Example curl request for the endpoint that returns a specific tweet by ID
# curl http://localhost:5000/tweet/123
# Expected response: JSON data of the tweet with ID 123
# Example curl request for the endpoint that adds a new tweet
# curl -X POST -H "Content-Type: application/json" -d '{"text": "New tweet"}' http://localhost:5000/tweet
# Expected response: JSON data of the newly added tweet
