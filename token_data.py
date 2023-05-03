from playwright.sync_api import sync_playwright
import html_to_json
import logging
from playwright_stealth import stealth_sync

logger = logging.getLogger(__name__)

class Token:
    def __init__(self, path, time):
        self.path = path
        self.time = time
        self.full_token_info()

    def __repr__(self):
        return f'Name: {self.name}\nRarity: {self.rarity}\nEnergy: {self.energy}\nBreed count: ' \
               f'{self.breed_count}\nLevel: {self.level}\nGems current: {self.gems_current}\nGems lef: ' \
               f'{self.gems_left}\nStrength: {self.strength}\nStamina: {self.stamina}\nSpeed: {self.speed}\nBody: ' \
               f'{self.body}\nEars: {self.ears}\nFace: {self.face}\n Path: {self.path}\n Time: {self.time}\n Max ' \
               f'attribute: {self.max_attr}'

    def __str__(self):
        return f"{self.name}+'  '+{self.rarity}+'  '+{self.level}+'/'+{self.breed_count}+'  '+'Max:'+' '+" \
               f"{self.max_attr}\n'Body: '+{self.body}\nEars: {self.ears}\nFace: {self.face}\n'Time: '+{self.time}"


    def full_token_info(self):
        with sync_playwright() as p:
            for browser_type in [p.chromium]:
                browser = browser_type.launch(headless=True, timeout=60000)
                context = browser.new_context(extra_http_headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9'})
                page = context.new_page()

                #stealth_sync(page)
                page.goto(self.path)
                page.wait_for_selector("span[class^=\"RarityItem__Text\"]")
                page_content = page.content()
                logging.debug('Playwright extracted page content')
                output = html_to_json.convert(page_content)
                browser.close()
        self.name = self.get_name(output)
        self.rarity = self.get_rarity(output)
        self.energy = self.get_energy(output)
        self.breed_count = self.get_breed_count(output)
        self.level = self.get_level(output)
        self.gems_current = self.get_gems_current(output)
        self.gems_left = self.get_gems_left(output)
        self.strength = self.get_strength(output)
        self.stamina = self.get_stamina(output)
        self.speed = self.get_speed(output)
        self.body = self.get_body(output)
        self.ears = self.get_ears(output)
        self.face = self.get_face(output)
        self.max_attr = self.get_max_attr()


    def get_name(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['span'][
            0]['_value']
        except:
            return "Name not available"

    def get_rarity(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
            'span'][0]['_value']
        except:
            return "Rarity not available"

    def get_energy(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][1]['div'][1]['div'][1]['div'][0]['div'][0]['span'][0]['_value'] + '/' + \
            output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][
                1]['div'][1]['div'][1]['div'][0]['div'][0]['span'][2]['_value']
        except:
            return "Energy not available"

    def get_breed_count(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][1]['div'][2]['div'][1]['div'][0]['div'][0]['span'][0]['_value']
        except:
            return "Breed count not available"

    def get_level(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][2]['div'][0]['div'][0]['div'][0]['div'][0]['span'][0]['_value']
        except:
            return "Level not available"

    def get_gems_current(self, output):
       try:
           return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
               'div'][2]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['span'][0]['_value']
       except:
           return "Current gems not available"

    def get_gems_left(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][2]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['span'][1]['_value']
        except:
            return "Gems left not available"

    def get_strength(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][2]['div'][0]['div'][0]['div'][2]['div'][0]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][0][
                '_value'] + '/' + \
            output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][
                2]['div'][0]['div'][0]['div'][2]['div'][0]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][2][
                '_value']
        except:
            return "Strength not available"

    def get_stamina(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][2]['div'][0]['div'][0]['div'][2]['div'][1]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][0][
                '_value'] + '/' + \
            output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][
                2]['div'][0]['div'][0]['div'][2]['div'][1]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][2][
                '_value']
        except:
            return "Stamina not available"

    def get_speed(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][2]['div'][0]['div'][0]['div'][2]['div'][2]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][0][
                '_value'] + '/' + \
            output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][
                2]['div'][0]['div'][0]['div'][2]['div'][2]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][2][
                '_value']
        except:
            return "Speed not available"

    def get_body(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][2]['div'][0]['span'][1]['_value']
        except:
            return "Body not available"

    def get_ears(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][4]['div'][0]['span'][1]['_value']
        except:
            return "Ears not available"

    def get_face(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][5]['div'][0]['span'][1]['_value']
        except:
            return "Face not available"

    def get_max_attr(self):
        stamina = int(self.stamina.split('/')[0])
        speed = int(self.speed.split('/')[0])
        strength = int(self.strength('/')[0])
        return max(strength, stamina, speed)