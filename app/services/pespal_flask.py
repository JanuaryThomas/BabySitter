import requests
from bs4 import BeautifulSoup as bs
import pesapal


PESA_PAL_CONSUMER = 'IU5LNHtKJZSJjj3fLsV1iQKRIxnkzOFY'
PESA_PAL_SECRECT = 'jM2GRNgzUjgJcKthv2l6yoChP+A='

pesapal.consumer_key = PESA_PAL_CONSUMER
pesapal.consumer_secret = PESA_PAL_SECRECT
pesapal.testing = False

post_params = {
    'oauth_callback' : 'https://google.com'
}

request_data = {
  'Amount': '100',
  'Description': 'Meter Number',
  'Type': 'MERCHANT',
  'Reference': 'gdfshdyubnkuhd',
  'PhoneNumber': '0757123008'
}

url = pesapal.postDirectOrder(post_params, request_data)
response = requests.get(url)
headers = {'Content-Type': ''}
print (response.content)

f = open('pesapal.html', 'w')

soup = bs(response.content, 'html.parser', from_encoding="utf8")
print(soup)
with open(f, mode="w", encoding="utf8") as code:
    code.write(str(soup.prettify()))

f.close()
print(soup)


post_params = {
  'pesapal_merchant_reference': '000',
  'pesapal_transaction_tracking_id': '000'
}
url = pesapal.queryPaymentStatus(post_params)
response = requests.post(url)
print (response)