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

def creatDraft():
    url = "http://1f0cb7bf.ngrok.io/experience/consumer_selling/v1/listing_draft/create_and_open?mode=AddItem"

    payload = {
        "requestListing": {
            "item": {
                "title": "jeans"
            },
            "categoryId": "11483",
            "condition": "1000"
        }
    }

    headers = {
        'Authorization': "Bearer v^1.1#i^1#f^0#p^3#I^3#r^0#t^H4sIAAAAAAAAAOVWXWgcVRTOJJtoTNMq/hJE16mRYDoz987M/g3Zpdv81C3Nj91NaYNV7s7c2YzZnRnn3kmy6MM2aEAFX3wptEIq+GCFKn2Q+lBBLSKoIBZ88MVSkLYIggjWKlXvzGaTTdREJGDBZWH33Pvdc77znXMvB9Q6Oh9dfGzxWjd3S+tSDdRaOQ52gc6O9v7tba097S2gCcAt1R6uRRbargwQVCm72gFMXMcmODpfKdtECxfTvO/ZmoOIRTQbVTDRqK7ls6P7NVkEmus51NGdMh/NDaV5tWjKiqokE6m4iRWgslW74bPgpHkYT5rAjCGziPWkqhpsnxAf52xCkU3TvAxgQgBQkJWCDDX2jaXERDI1xUcPYo9Yjs0gIuAzIV0tPOs1cd2YKiIEe5Q54TO57Eh+PJsbGh4rDEhNvjLLOuQpoj5Zaw06Bo4eRGUfbxyGhGgt7+s6JoSXMvUIa51q2QaZf0E/lDqBQEpJFBEAJoS6am6JlCOOV0F0Yx7BimUIZgjVsE0tWt1MUaZG8Wms02VrjLnIDUWDn8d9VLZMC3tpfnhP9vBkfvgAH81PTHjOrGVgI8gUKjAO1ISSVPhMyaSYUPiUT5aj1F0ta7wuzKBjG1agGImOOXQPZpTxemFgkzAMNG6Pe1kWwwtxyRCnFoCqgVVco6KrNdyqmqaMWBGxC6JgFelyDGxFTTOBrNmJCQkXUVUI7noFeTOYumWkY0Fn4vgV7FmGpqpFNY50U1DkpC6oRkwXUqkYFmQcx3EZKSow1f9BaeuVpNSzij7FwZ3FFdbk6zeiI56FbaNcDVimeaI7Luajzcb6E+HTsdwZ8yTNT1PqapI0Nzcnzimi45UkGQAoHRrdn9encQXxK1hrc7BghT2iMw4Mr9Gqy3jMsxZkwe0SnwnOE+YAuZYYNIKoOxXJQT6dlkK2Ep53cZCRjnf7rCcbHb6GfGb96iaiZF03ZzREqRs3lSjszYKyglx3S7IdwrOr2daN/zbbyAI3/ZcZG3h2SzIeZG9XI+Hw/01YXZ3x+qfJSn979//03ktr56VMS/iBC5wKFjjARi4ggV64EzzU0TYZadvWQyyKRQuZIrFKNhsDPCzO4KqLLK+1gxuVqnfeaJrQlo6A+1ZmtM422NU0sIH7V3fa4Y57u2ECsDRlKMNYagrsXN2NwHsid/3UXfqZK353KtLz++5je+fbL9HX+0H3Cojj2lsiR2vP7Xvglx9PDtzNG9JvL0VfOPFZ36G3CmfPb39eGL96tf/tiydu//7o+CulcyT38uHeM8fyX73/yBu/7nrtjq+f2PGt/eTHR2Ze7Hj2+DNnvxT7zn148b2P3hzatfDBO/uu3Lj87ie9D56e/ObVS/CHRaOrb+r6hVt7j5/2b5s5eb01eer8hWuXt535/NMv6ur9AWBk0bK6CgAA",
        'X-EBAY-C-ENDUSERCTX': "deviceId=4fe2d65bc464493aa9babd91aa259027,userAgent=Mozilla%2F5.0+%28iPad%3B+CPU+OS+7_0+like+Mac+OS+X%29+AppleWebKit%2F537.51.1+%28KHTML%2C+like+Gecko%29+Version%2F7.0+Mobile%2F11A465+Safari%2F9537.53",
        'X-EBAY-C-MARKETPLACE-ID': "EBAY-US",
        'Content-Type': "application/json",
        'X-EBAY-C-TRACKING': "cguid=049205231500a62960f4f874f775d8e2595427bd,tguid=049229b01504050a19118a10011c1e36595427bd,pageid=2380506,guid=049229b01504050a19118a10011c1e36",
        'Accept': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        responseJS = json.loads(response.content)
        draftId = responseJS["modules"]['SELL_NODE_CTA']['paramList']['draftId']
        return draftId
    else:
        return response.status_code

def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")
    item = parameters.get("item")
    draftId = creatDraft()

    cost = {'jeans':25, 'shoes':100, 'iphone':500, 'bags':250}

    if req.get("result").get("action") == "item.cost":
        speech = "The recommended cost of " + item + " is "  + str(cost[item]) + " dollars."
    elif req.get("result").get("action") == "item.create":
        speech = 'Sure, I can help you sell your ' + item + ' on eBay with draftId' + str(draftId) + '. According to similar sold items, ' \
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


