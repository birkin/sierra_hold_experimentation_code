import logging, os, time

import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver import Firefox


## setup
SIERRA_API_URL = os.environ['HOLD_EXP__SIERRA_API_ROOT_URL']
SIERRA_API_USERNAME = os.environ['HOLD_EXP__SIERRA_API_HTTPBASIC_USERNAME']
SIERRA_API_PASSWORD = os.environ['HOLD_EXP__SIERRA_API_HTTPBASIC_PASSWORD']

SIERRA_PATRON_ID = os.environ['HOLD_EXP__SIERRA_PATRON_ID']
# SIERRA_ITEM_NUMBER = os.environ['TMP_SETTING__SIERRA_ITEM_NUMBER']

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', datefmt='%d/%b/%Y %H:%M:%S' )


## get token
token = 'init'
token_url = f'{SIERRA_API_URL}/token'
log.debug( 'token_url, ```%s```' % token_url )
try:
    r = requests.post( token_url,
        auth=HTTPBasicAuth( SIERRA_API_USERNAME, SIERRA_API_PASSWORD ),
        timeout=20 )
    log.debug( 'token r.content, ```%s```' % r.content )
    token = r.json()['access_token']
    log.debug( 'token, ```%s```' % token )
except:
    log.exception( 'problem getting token; traceback follows' )
    raise Exception( 'exception getting token' )


## show 'BEFORE'
log.info( 'showing classic-josiah BEFORE' )
def show_classic_josiah_bib():
    browser = Firefox()
    browser.implicitly_wait( 10 )
    url = 'http://josiah.brown.edu/record=b1815113'
    browser.get( url )
    time.sleep( 3 )
    browser.close()

show_classic_josiah_bib()


## place hold!
log.info( 'placing hold' )
request_url = f'{SIERRA_API_URL}/patrons/{SIERRA_PATRON_ID}/holds/requests'
custom_headers = {'Authorization': f'Bearer {token}' }
payload = '{"recordType": "i", "recordNumber": 10883346, "pickupLocation": "r0001", "note": "birkin_api_testing"}'  # ZMM item, https://library.brown.edu/availability_api/v2/bib_items/b1815113/
try:
    r = requests.post( request_url, headers=custom_headers, data=payload, timeout=30 )
    log.info( f'r.status_code, `{r.status_code}`' )
    log.info( f'r.url, `{r.url}`' )
    log.info( f'r.content, `{r.content}`' )
except:
    log.exception( 'problem hitting api to request item; traceback follows' )


## show 'AFTER'
seconds = 5
log.info( f'hold placed; waiting {seconds} seconds, then showing classic-josiah AFTER' )
time.sleep( seconds )
show_classic_josiah_bib()


## done
log.info( 'DONE' )
