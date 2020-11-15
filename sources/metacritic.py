import re
import requests

from bs4 import BeautifulSoup
from typing import List, Optional

from database import GamesRepository
from loguru import logger
from utils.helpers import get_standard_headers, sterilize

from . import Service, Platform


class MetaCritic:

    BASE_URL = "https://www.metacritic.com"
    FG_PATH  = "/feature/new-free-games-playstation-xbox-pc-switch"

    def __init__(self):

        self.repo = GamesRepository()

    def run(self):

        logger.info("Initiated MetaCritic")

        url     = self._build_url(self.FG_PATH)
        headers = self._get_headers()
        res     = self._make_request(url, headers)

        if res.status_code != 200:
            logger.error("Response code: {} for URL: {}".format(res.status_code, url))
            return

        soup  = BeautifulSoup(res.content, 'html.parser')
        games = self._get_games(soup)

        self._update_games(games)

        logger.info("Done")

    def _update_games(self, new_games: List[dict]):

        logger.info("Updating old games")

        old_games = self.repo.get_new_games()

        self.repo.replace_old_games(old_games)
        self.repo.replace_new_games(new_games)

    def _get_games(self, soup: BeautifulSoup) -> List[dict]:

        logger.info("Collecting games")

        tables = self._get_tables(soup)
        games  = []

        for table in tables:

            available = True
            rows      = self._get_rows(table)
            service   = self._get_service(table['header'])
            platform  = service.platforms[0] if len(service.platforms) == 1 else None

            for row in rows:

                try:
                    game = {}

                    if row.find('th'):
                        available = False
                        continue

                    upper_data = self._get_upper_data(row, service.value, platform)
                    lower_data = self._get_lower_data(next(rows))

                    game.update(lower_data)
                    game['available'] = available

                    for data in upper_data:
                        game.update(data)
                        games.append(game)

                        # logger.info("Found: {}".format(game['title']))

                        if game['title'] == 'Imperator: Rome':

                            print("Game: ", game)

                except IndexError:
                    next(rows)
                    logger.warning("Could not get game from row: {}".format(row))

        logger.info("Total games found: {}".format(len(games)))

        return games

    def _get_service(self, header: str) -> Service:

        service_map = {
            'free for everyone'   : Service.SELF,
            'humble choice'       : Service.HUMBLE,
            'playstation now'     : Service.PS_NOW,
            'playstation plus'    : Service.PS_PLUS,
            'prime gaming'        : Service.PRIME,
            'stadia pro'          : Service.STADIA,
            'xbox games with gold': Service.MICROSOFT,
            'xbox game pass'      : Service.MICROSOFT,
        }

        for string, service in service_map.items():

            if string in header.lower():
                return service

        return Service.SELF

    def _get_platform(self, service: Service):

        if len(service.platforms) == 1:

            return service.platofrms[0]

    def _get_lower_data(self, lower) -> dict:

        genre_year = lower.text.rsplit(",", 1)

        if len(genre_year) != 2:

            return {}

        genre, year = genre_year

        return {
            "genre": sterilize(genre),
            "year" : sterilize(year)
        }

    def _get_upper_data(self, upper, service: str, platform: str=None) -> List[dict]:

        data = []

        link     = None
        # name     = None
        # platform = None
        # service  = None
        # from_    = None
        # to       = None

        cells = upper.find_all('td')

        if not len(cells) == 3:
            return data

        _, title, meta = cells

        title_anchor = title.find('a')

        if title_anchor:

            link     = title_anchor['href']
            name     = sterilize(title_anchor.text)

            if not platform:
                platform = sterilize(title.text.split(name)[1])

        else:
            name = sterilize(title.text)

        game = {
            "title"     : name,
            "platform"  : platform,
            "service"   : service,
            "link"      : link,
            "date_start": None,
            "date_end"  : None,
        }

        meta_anchors = meta.find_all('a')

        if not meta_anchors:
            data.append(game)
            return data

        services = [sterilize(anchor.text) for anchor in meta_anchors]

        pattern = "|".join(services)
        dates   = re.split(pattern, sterilize(meta.text))[1:]

        for period in dates:

            from_, to = self._parse_dates(period.strip())

            game = {
                "title"     : name,
                "platform"  : platform,
                "service"   : service,
                "link"      : link,
                "date_start": from_,
                "date_end"  : to,
            }

            data.append(game)

        return data

    def _parse_dates(self, dates):

        try:
            from_, to = dates.split("–")

        except ValueError:

            from_, to = dates.split("-")

        return from_, to

    def _get_rows(self, table) -> iter:

        content = table['content']
        rows = content.find('tbody').find_all('tr')

        return iter(rows)

    def _get_tables(self, soup: BeautifulSoup) -> List[dict]:

        article     = soup.find('div', 'grabarticle')
        table_tags  = article.find_all('table')
        h2_tags     = article.find_all('h2')[1:-1]
        titles      = [s.text for s in h2_tags]

        return [{'header': title, 'content': tag} for title, tag in zip(titles, table_tags)]

    def _build_url(self, path: str):

        return "{}{}".format(self.BASE_URL, path)

    @staticmethod
    def _make_request(url: str, headers: dict=None):

        if not headers:
            headers = {}

        return requests.get(url, headers=headers)

    def _get_headers(self):

        headers = {
            "cookie": '_BB.d=|||; _BB.bs=|; mc_s_s=a_1; prevPageType=article; _cb_ls=1; _cb=CEnLRDo9yFHDXgUtj; _chartbeat2=.1603607685730.1603607685730.1.BWEy6jCgUDG6DyTbDeDLo64DCvgk57.1; _cb_svref=https%3A%2F%2Fwww.google.com%2F; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; metapv=1; __utma=15671338.2036572794.1603607686.1603607686.1603607686.1; __utmc=15671338; __utmz=15671338.1603607686.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); s_vnum=1606199685939%26vn%3D1; s_invisit=true; s_getNewRepeat=1603607685942-New; s_lv_undefined=1603607685943; s_lv_undefined_s=First%20Visit; _pubcid=27167c4c-82c5-41d9-a986-335ee80c7600; trc_cookie_storage=taboola%2520global%253Auser-id%3D78cb1fee-a773-48fc-af81-e23aa5271614-tuct5d13ab5; s_ecid=MCMID%7C22457278815792362282312733887959996374; s_cc=true; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=1585540135%7CMCIDTS%7C18561%7CMCMID%7C22457278815792362282312733887959996374%7CMCAAMLH-1604212485%7C12%7CMCAAMB-1604212485%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1603614886s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aam_uuid=22692242447088555482328345368937812654; utag_main=v_id:01755e7769e2001e1e8bfedf290203072004c06a00bd0$_sn:1$_ss:1$_pn:1%3Bexp-session$_st:1603609490969$ses_id:1603607685602%3Bexp-session$vapi_domain:metacritic.com; QSI_HistorySession=https%3A%2F%2Fwww.metacritic.com%2Ffeature%2Fnew-free-games-playstation-xbox-pc-switch~1603607691318; RT="z=1&dm=metacritic.com&si=b6a33b99-0358-4e70-b449-1946b7565e3e&ss=kgoqlzpd&sl=1&tt=5pp&bcn=%2F%2F684d0d3b.akstat.io%2F&ul=qjhy"; __utmb=15671338.2.9.1603608929504; OptanonConsent=isIABGlobal=false&datestamp=Sun+Oct+25+2020+12%3A25%3A29+GMT%2B0530+(India+Standard+Time)&version=6.7.0&hosts=&consentId=e8e50673-7419-4a17-b17e-5b896effd94e&interactionCount=1&landingPath=https%3A%2F%2Fwww.metacritic.com%2Ffeature%2Fnew-free-games-playstation-xbox-pc-switch&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1%2C5%3A1',
            "referer": "https://www.google.com/",
        }

        headers.update(get_standard_headers())

        return headers
