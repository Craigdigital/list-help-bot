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

def creatDraft(parameters):
    categories = {'jeans': "11483", 'camera': "31388"}
    condtions = {'new': "1000", 'used': "3000"}

    item = parameters.get("item")
    condtion = parameters.get("condtion")
    brand = parameters.get("brand")
    model = parameters.get("model")


    url = "http://1f0cb7bf.ngrok.io/experience/consumer_selling/v1/listing_draft/create_and_open?mode=AddItem"

    payload = {
        "requestListing": {
            "item": {
                "title": item
            },
            "categoryId": categories[item],
            "condition": "1000"
        }
    }

    headers = {
        'Authorization': "Bearer v^1.1#i^1#r^1#f^0#I^3#p^3#t^Ul4xMF8yOjBEMUVDODQxMTZBMzQ2QkNFQjM4MUE1MkEyNDREOEIxXzFfMSNFXjUxNg==",
        'X-EBAY-C-ENDUSERCTX': "deviceId=4fe2d65bc464493aa9babd91aa259027,userAgent=Mozilla%2F5.0+%28iPad%3B+CPU+OS+7_0+like+Mac+OS+X%29+AppleWebKit%2F537.51.1+%28KHTML%2C+like+Gecko%29+Version%2F7.0+Mobile%2F11A465+Safari%2F9537.53",
        'X-EBAY-C-MARKETPLACE-ID': "EBAY-US",
        'Content-Type': "application/json",
        'X-EBAY-C-TRACKING': "cguid=049205231500a62960f4f874f775d8e2595427bd,tguid=049229b01504050a19118a10011c1e36595427bd,pageid=2380506,guid=049229b01504050a19118a10011c1e36",
        'Accept': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        responseJS = json.loads(response.content)
        return responseJS
    else:
        return response.status_code

def updateItem(draftId,data,startPrice):


    url = "http://1f0cb7bf.ngrok.io/experience/consumer_selling/v1/listing_draft/" + str(draftId) + "?mode=AddItem"

    payload = {
        "requestListing": {
            "item": {
                "itemSpecific": [
                    {
                        "name": "Brand",
                        "value": [
                            data["brand"]
                        ]
                    },
                    {
                        "name": "Model",
                        "value": [
                            data["model"]
                        ]
                    },
                    {
                        "name": "Series",
                        "value": [
                            "58mm"
                        ]
                    }
                ],
                "title": str(data["condition"]) + " " + str(data["brand"]) + " " + str(data["model"]) + " " + str(data["item"]),
                "picture": [
                    {
                      "url": "http://www.imaging-resource.com/PRODS/canon-t6i/Z-CANON-T6I-BEAUTY.JPG"
                    },
                    {
                      "url": "https://static.bhphotovideo.com/explora/sites/default/files/T6i_0.jpg"
                    },
                    {
                      "url": "http://bjselectronicsblog.com/wp-content/uploads/2016/02/Canon-Rebel-T6i-Best-Digital-SLR-Camera.jpg"
                    },
                    {
                      "url": "http://www.imaging-resource.com/PRODS/canon-t6i/Z-CANON-T6I-FRONTLEFT.JPG"
                    }
                  ],
                "description": "<div style=\"font-family: Arial; font-size:0.8125rem;\"><font face=\"Arial\" size=\"2\">add desc</font><br><br><br></div>"
            },
            "condition": "1000",
            "price": 20,
            "startPrice": startPrice,
            "format": "Auction",
            "listingInfo": {
                "conditionDescription": "New with box",
                "description": "<div style=\"font-family: Arial; font-size:0.8125rem;\"><font face=\"Arial\" size=\"2\">add desc</font><br><br><br></div>"
            },
            "categoryId": "31388",
            "previousShippingType": "SHIP_RECO_0",
            "serviceContextMeta": "{\"restrictedRevise\":false,\"sellerSegment\":\"NEW\",\"recommendedStartPrice\":0.99,\"recommendedBinPrice\":3.99,\"format\":\"FixedPrice\",\"price\":3.99,\"featureQualifiedList\":\"2033,2034\"}"
        },
        "updatedModules": [
            "PHOTOS",
            "ASPECTS_MODULE",
            "CONDITION",
            "DESCRIPTION",
            "PRICE",
            "LISTINGINFO"
        ],
        "userInteractedModules": "ASPECTS_MODULE,PHOTOS,DESCRIPTION,PRICE"
    }

    headers = {
        'Authorization': "Bearer v^1.1#i^1#r^1#f^0#I^3#p^3#t^Ul4xMF8yOjBEMUVDODQxMTZBMzQ2QkNFQjM4MUE1MkEyNDREOEIxXzFfMSNFXjUxNg==",
        'X-EBAY-C-ENDUSERCTX': "deviceId=4fe2d65bc464493aa9babd91aa259027,userAgent=Mozilla%2F5.0+%28iPad%3B+CPU+OS+7_0+like+Mac+OS+X%29+AppleWebKit%2F537.51.1+%28KHTML%2C+like+Gecko%29+Version%2F7.0+Mobile%2F11A465+Safari%2F9537.53",
        'X-EBAY-C-MARKETPLACE-ID': "EBAY-US",
        'Content-Type': "application/json"
    }

    response = requests.put(url, json=payload, headers=headers)
    responseJS = json.loads(response.content)

    return responseJS

def publishItem(draftId, paypal_account):

    url = "http://1f0cb7bf.ngrok.io/experience/consumer_selling/v1/listing_draft/" + str(draftId) + "/publish?mode=AddItem"

    payload = {
        "requestListing": {
            "paymentInfo": {
                "paypalEmailAddress": paypal_account
            }
        }
    }

    headers = {
        'Authorization': "Bearer v^1.1#i^1#r^1#f^0#I^3#p^3#t^Ul4xMF8yOjBEMUVDODQxMTZBMzQ2QkNFQjM4MUE1MkEyNDREOEIxXzFfMSNFXjUxNg==",
        'X-EBAY-C-ENDUSERCTX': "deviceId=4fe2d65bc464493aa9babd91aa259027,userAgent=Mozilla%2F5.0+%28iPad%3B+CPU+OS+7_0+like+Mac+OS+X%29+AppleWebKit%2F537.51.1+%28KHTML%2C+like+Gecko%29+Version%2F7.0+Mobile%2F11A465+Safari%2F9537.53",
        'X-EBAY-C-MARKETPLACE-ID': "EBAY-US",
        'Content-Type': "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    responseJS = json.loads(response.content)

    return responseJS


def makeWebhookResult(req):
    result = req.get("result")
    parameters = result.get("parameters")


    if req.get("result").get("action") == "item.create":
        item = parameters.get("item")
        brand = parameters.get("brand")
        condition = parameters.get("condtion")
        model = parameters.get("model")
        responseJS = creatDraft(parameters)
        draftId = responseJS["modules"]['SELL_NODE_CTA']['paramList']['draftId']
        startPrice = responseJS["modules"]['PRICE']['bestChanceToSell']['price']['value']
        with open('tempData.json', 'w') as f:
            json.dump({"latestDraftId": draftId,
                       "brand": brand,
                       "condition": condition,
                       "model": model,
                       "item":item,
                       "startPrice":startPrice}, f)
        speech = 'Sweet. We recommend you to sell with 7-day auctions starting at $' + startPrice + ' according to similar items.'\
                 'Want to go with that?'
        text = 'Sweet. We recommend you to sell with 7-day auctions starting at $' + startPrice + ' according to similar items.'\
                 'Want to go with that??'
        responseData = {}
    elif req.get("result").get("action") == "item.update":
        with open('tempData.json') as f:
            data = json.load(f)
        draftId = data["latestDraftId"]
        customPrice = parameters.get("unit-currency").get("amount")

        #update the start price
        with open("tempData.json", "r") as f:
            data = json.load(f)

        data["startPrice"] = customPrice

        with open("tempData.json", "w") as f:
            json.dump(data, f)


        updateItemResponse = updateItem(draftId, data, customPrice)
        speech = "Ok! \n We have changed your starting price to " + str(customPrice) + " Are you ready to list? "
        text = "Ok! \n We have changed your starting price to " + str(customPrice) + " Are you ready to list? "
        responseData = {}

    elif req.get("result").get("action") == "item.publish":
        paypal_account = parameters.get("paypal_account")
        with open('tempData.json') as f:
            data = json.load(f)
        draftId = data["latestDraftId"]
        customPrice = data["startPrice"]
        updateItemResponse = updateItem(draftId, data, customPrice)
        publishItemResponse = publishItem(draftId, paypal_account)
        itemId = publishItemResponse['meta']['requestParameters']['itemId']
        with open('item_papyal.json', 'a') as f:
            json.dump({itemId:paypal_account}, f)
        speech = 'Congratuations! Your item has been published successfully on eBay with item ID as displayed.'
        text = 'Congratuations! Your item has been published successfully on eBay with item ID ' + itemId +'.'
        responseData = {
        "google": {
        "expect_user_response": False,
        "rich_response": {
        "items": [
        {
        "simpleResponse": {
          "textToSpeech":"Congratuations! Your item has been published successfully on eBay touch to view."
        }
        },
        {
        "basicCard": {
            "title":str(data["condition"]) + " " + str(data["brand"]) + " " + str(data["model"]) + " " + str(data["item"]),
            "image": {
            "url":"http://www.imaging-resource.com/PRODS/canon-t6i/Z-CANON-T6I-BEAUTY.JPG",
            "accessibilityText":"Image alternate text"
            },
            "buttons": [
            {
                "title":"View my item",
                "openUrlAction":{
                "url":"http://www.qa.ebay.com/itm/" + str(itemId) + "?ssPageName=STRK:MESELX:IT&_trksid=p3984.m1555.l2649"
                }
            }
        ]
      }
    }
  ]
}
}
}
    else:
        return {}

    print("Response:")
    print(speech)
    print(text)

    return {
        "speech": speech,
        "displayText": text,
        "data": responseData,
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')


