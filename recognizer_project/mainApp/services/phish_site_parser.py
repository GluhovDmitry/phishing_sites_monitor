import requests
import json
import urllib3
import certifi

from loguru import logger
from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection
from lxml import html
from bs4 import BeautifulSoup


def check_https_url(url):
    HTTPS_URL = f'https://{url}'
    try:
        HTTPS_URL = urlparse(HTTPS_URL)
        connection = HTTPSConnection(HTTPS_URL.netloc, timeout=2)
        connection.request('HEAD', HTTPS_URL.path)
        if connection.getresponse():
            return True
        else:
            return False
    except:
        return False


def check_http_url(url):
    HTTP_URL = f'http://{url}'
    try:
        HTTP_URL = urlparse(HTTP_URL)
        connection = HTTPConnection(HTTP_URL.netloc)
        connection.request('HEAD', HTTP_URL.path)
        if connection.getresponse():
            return True
        else:
            return False
    except:
        return False


def check_hsts_preload(url):
    # http = urllib3.PoolManager(
    #     cert_reqs='CERT_REQUIRED',
    #     ca_certs=certifi.where(),
    # )
    # check = http.request('GET', f'https://{url}', headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'})
    # response = check.headers
    # if 'strict-transport-security' in response:
    #     return True
    # else:
    #     return False

    url = f'https://hstspreload.com/api/v1/status/{url}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return True
    else:
        return False


def get_static(domain):
    try:
        url = f'https://{domain}'

        page = requests.get(url)
        tree = html.fromstring(page.content)
        # logger.info([x.attrib for x in tree.cssselect('img') if 'JPG' in x.attrib['data-src']])
        a = [x.attrib['data-src'] for x in tree.cssselect('img') if 'jpg' or 'png' or 'jpeg' in x.attrib['data-src']]
        for pic_link in a:
            with open('images/' + pic_link.split('/')[-1], 'wb') as f:
                f.write(requests.get(f'{url}{pic_link}').content)
    except Exception as e:
        logger.error(str(e))
        return 'Static not downloaded'
    else:
        return 'Static downloaded'


def get_side_hrefs(url):
    response = requests.get(f'https://{url}')
    soup = BeautifulSoup(response.text, 'html5lib')
    links = [
        a.get('href') for a in soup.find_all('a')
        if a.get('href') and a.get('href').startswith('h')]
    externalLinks = []
    for link in links:
        if link.split('/')[2] != f'www.{url}':
            externalLinks.append(link)
    return len(externalLinks)


def integration_urlscan_check(url):
    try:
        api_key = 'e276aca8-85b2-4152-963a-7a25181b2be3'
        data = {"url": url, "visibility": "public"}
        headers = {'API-Key': api_key,'Content-Type': 'application/json'}
        resp = requests.post(url=f'https://urlscan.io/api/v1/scan/',
                             data=json.dumps(data), headers=headers)
        if resp.status_code != 200:
            raise ConnectionError(f'Failed urlscan checks: {resp.text}')
    except Exception as e:
        logger.error(str(e))
    else:
        return resp.json()['result']


def main(url):
    """

    """
    #SSL check
    if check_https_url(url):
        logger.info('HTTPS enabled')
    elif check_http_url(url):
        logger.info('HTTPS disabled')
    else:
        logger.info('Some mistake in the url')

    #HSTS check
    hsts = check_hsts_preload(url)
    if hsts:
        logger.info('HSTS enabled')
    else:
        logger.info('HSTS not enabled')

    #side referencies check
    logger.info(f"We found {get_side_hrefs(url)} external links")

    #static gather beta
    logger.info(get_static(url))

    #urlscan integration
    logger.info(integration_urlscan_check(url))


if __name__ == '__main__':
    main('psbank.ru')

    # get_static('tinkoff.ru')
    # logger.info(get_side_hrefs('tinkoff.ru'))
    # main('sberbank-online-skachat.asvas.ru')



# def check_dnssec(url):
# import dns.name
# import dns.query
# import dns.dnssec
# import dns.message
# import dns.resolver
# import dns.rdatatype
#     # get nameservers for target domain
#     response = dns.resolver.resolve(url, rdtype=dns.rdatatype.NS)
#     # we'll use the first nameserver in this example
#     nsname = response.rrset[0].to_text()  # name
#     response = dns.resolver.resolve(nsname, dns.rdatatype.A)
#     nsaddr = response.rrset[0].to_text()  # IPv4
#
#     # get DNSKEY for zone
#     request = dns.message.make_query(url,
#                                      dns.rdatatype.DNSKEY,
#                                      want_dnssec=True)
#
#     # send the query
#     response = dns.query.udp(request, nsaddr)
#     logger.info(response)
#     if response.rcode() != 0:
#         return {'status': False, 'reason': f'SERVER ERROR OR NO DNSKEY RECORD'}
#     # answer should contain two RRSET: DNSKEY and RRSIG(DNSKEY)
#     answer = response.answer
#     if len(answer) != 2:
#         return {'status': False, 'reason': f'SOMETHING WENT WRONG'}
#
#     # the DNSKEY should be self signed, validate it
#     name = dns.name.from_text(url)
#     try:
#         dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
#     except dns.dnssec.ValidationFailure as e:
#         return {'status': False, 'reason': f'Validation error (SUSPICIOUS): {e}'}
#     except Exception as e:
#         return {'status': False, 'reason': f'Some error: {e}'}
#     else:
#         return {'status': True}

