import requests
import time
import os
from slackclient import SlackClient
import json

### Specify slack API token
slack_token = os.environ["SLACK_BOT_TOKEN"]
sc = SlackClient(slack_token)

### Specify url to btc markets
base_url = "https://www.btcmarkets.net/"
api_base_url = "https://api.btcmarkets.net"

# function to get price of crypto currencies listed on BTC Market
# crypto_currency_list = ["BTC", "LTC", "ETH", "ETC", "XRP", "BCH"]
# against_list = ["BTC", "AUD"]
# method is which Slack API method you would like to use to post the message
# channel is which Slack channel you would like to send the message to

def slack_price(crypto, against, method, channel):
    # define url for the market data API
    uri = "/market/%s/%s/tick" % (crypto, against)
    url = api_base_url + uri

    # get the data from the url
    req = requests.get(url)

    # extract components of the data
    bid = req.json()["bestBid"]
    ask = req.json()["bestAsk"]
    last_price = req.json()["lastPrice"]
    currency = req.json()["currency"]
    instrument = req.json()["instrument"]
    volume_24h = req.json()["volume24h"]
    local_time = time.ctime(req.json()["timestamp"])

    # put it into 1 chunk of message
    message = """
        BTC Markets - {0}
        
        As of {1} (AEST), the following is accurate:
        - Best ask price (buy at):  {2} {6}
        - Best bid price (sell at): {3} {6}
        - Last trade price:         {4} {6}
        - Volume in the last 24h:   {5}
        """.format(instrument, local_time, ask, bid, last_price, volume_24h, currency)

    # prepare the content of the message - as an attachment
    attachment = json.dumps([
        {
            "fallback": "If unavailable, please follow this link - {0}".format(base_url),
            "text": message,
            "title_link": base_url,
            "color": "warning"
        }
    ])

    # last step - send the message to slack
    sc.api_call(
        method=method,
        channel=channel,
        attachments=attachment
    )

slack_price(crypto="crypto_you_want",
            against="against_BTC_or_AUD",
            method="chat.postMessage",
            channel="#yourchannel")