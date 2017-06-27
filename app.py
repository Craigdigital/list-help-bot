#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
import requests

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get("item")

    cost = {'jeans':25, 'shoes':100, 'iphone':500, 'bags':250}

    if req.get("result").get("action") == "item.cost":
        speech = "The recommended cost of " + item + " is "  + str(cost[item]) + " dollars."
    elif req.get("result").get("action") == "item.create":
        draftId = 1
        speech = 'Sure, I can help you sell your ' + item + ' on eBay with draft Id ' + draftId + '. According to similar sold items, ' \
                 'It will list with 7 day auction with starting price of $' + str(cost[item]) + '. Can I publish for you?'
    else:
        return {}

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')


