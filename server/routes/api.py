from flask import jsonify, request, abort
from server import app
from server.services.tweetService import TweetService
from server.routes import prometheus 

service = TweetService()

@app.route("/api/tweet-data", methods=['GET'])
@prometheus.track_requests
def get():
    """get a list of tweets"""
    start = request.args.get('start', default=0, type=int)
    end = request.args.get('start', default=50, type=int)
    data = service.getCachedTweets(start, end)
    return jsonify(data)

# curl -X POST -H "Content-Type: application/json" \
#    -d '{"text":"asjkdgasd"}' http://localhost:3000/api/parse-text
@app.route("/api/parse-text", methods=['POST'])
@prometheus.track_requests
def parse():
    """ parse text and try to extract covid data, then return in json form """
    data = request.get_json()
    if 'text' in data:
        text = data['text']
        return service.enrichTweetList([{'text': text}])[0]
    else:
        abort(400, 'Bad data')

@app.route("/api/tweet-data", methods=['POST'])
@prometheus.track_requests
def post():
    """create """
    state = {"status": "NOT_IMPLEMENTED"}
    return jsonify(state)

@app.route("/api/tweet-data", methods=['DELETE'])
@prometheus.track_requests
def delete():
    """delete specific tweet"""
    state = {"status": "NOT_IMPLEMENTED"}
    return jsonify(state)    


# check https://github.com/prometheus/client_python for help on prometheus  