import re

from mainApp import models
from loguru import logger
# import dnstwist_fixed
from . import dnstwist_fixed


def save_active_urls():
    try:
        banks = models.Banks.objects.all()
        for bank in banks:
            for domain in bank.urls:
                is_social = False
                parsed_domain = domain.split('/', 4)
                for site in ['t.me', 'ok.ru', 'facebook.com', 'instagram.com', 'vk.com', 'youtube.com', 'twitter.com', 'zen.yandex.ru']:
                    if parsed_domain[2] in [f'www.{site}', f'{site}'] or bool(re.search('livejournal', domain)):
                        is_social = True

                if not is_social and not bool(re.search('[а-яА-Я]', domain)):
                    possible_fake_domains = url_generator(domain=domain)
                    logger.info(possible_fake_domains)
                    for fake_domain in possible_fake_domains[1:]:
                        if f'https://{fake_domain}' not in bank.urls and f'http://{fake_domain}' not in bank.urls:
                            logger.info(fake_domain)
                            bank.fakeurls_set.create(url=fake_domain, colors=[])
    except Exception as e:
        logger.error(e)
    else:
        return logger.info('Success')


def url_generator(domain):
    try:
        logger.info(f'processing {domain}')
        data = dnstwist_fixed.main(registered=True, domain=domain, format=list)
        # logger.info(data)
    except Exception as e:
        logger.error(e)
    else:
        return data


if __name__ == '__main__':
    # save_active_urls()
    d = url_generator('http://www.sberbank.ru')
    logger.info(d)
