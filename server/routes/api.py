from flask import jsonify, request
from server import app
# from server.services import tweetService

@app.route("/api/tweet-data", methods=['GET'])
def get():
    """get a list of tweets"""
    start = request.args.get('start', default=0, type=int)
    end = request.args.get('start', default=50, type=int)
    # data = tweetService.getCachedTweets(start, end)
    data = {}
    return jsonify(data)

@app.route("/api/tweet-data", methods=['POST'])
def post():
    """create """
    state = {"status": "NOT_IMPLEMENTED"}
    return jsonify(state)

@app.route("/api/tweet-data", methods=['DELETE'])
def delete():
    """delete specific tweet"""
    state = {"status": "NOT_IMPLEMENTED"}
    return jsonify(state)    