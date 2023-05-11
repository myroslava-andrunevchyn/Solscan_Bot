from undetected_chromedriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import html_to_json
import logging

#module_logger = logging.getLogger('bot.token_data')


class Token:
    def __init__(self, path, time, seller):
        self.path = path
        self.time = time
        self.seller = seller
        self.full_token_info()

    def __repr__(self):
        return f'Name: {self.name}\nRarity: {self.rarity}\nEnergy: {self.energy}\nBreed count: ' \
               f'{self.breed_count}\nLevel: {self.level}\nGems current: {self.gems_current}\nGems left: ' \
               f'{self.gems_left}\nStrength: {self.strength}\nStamina: {self.stamina}\nSpeed: ' \
               f'{self.speed}\nColor: {self.color}\nEnvironment: {self.environment}\nBody: ' \
               f'{self.body}\nTail: {self.tail}\nEars: {self.ears}\nFace: {self.face}\n Path: {self.path}\n Seller:' \
               f' {self.seller}\nTime: {self.time}\n Max attribute: {self.max_attr}'

    def __str__(self):
        return f"{self.name}   {self.rarity}  {self.level}/{self.breed_count}   Max: {self.max_attr}\n\nGems " \
               f"current: {self.gems_current}\nGems left: {self.gems_left}\n\nColor: " \
               f"{self.color.rstrip('% have this gene')}\nEnvironment: {self.environment.rstrip('% have this gene')}\nBody:" \
               f" {self.body.rstrip('% have this gene')}\nTail: {self.tail.rstrip('% have this gene')}\nEars:" \
               f" {self.ears.rstrip('% have this gene')}\nFace: {self.face.rstrip('% have this gene')}\nTime: {self.time}\nSeller: {self.seller[-4:]}"

    def get_html_content(self):
        logging.info('Getting html content')
        driver = Chrome(headless=True, patcher_force_close=True, version_main=113)
        driver.get(self.path)
        element_present = EC.presence_of_element_located(
            (By.XPATH, '//*[@id="__next"]/main/div[1]/div/div/div/div[1]/div[2]/div[1]/div[1]/span'))
        WebDriverWait(driver, 30).until(element_present)
        content = driver.page_source
        driver.close()
        logging.info('Html content retrieved')
        return content


    def full_token_info(self):
        page_content = self.get_html_content()
        output = html_to_json.convert(page_content)
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
        self.color = self.get_color(output)
        self.environment = self.get_environment(output)
        self.body = self.get_body(output)
        self.tail = self.get_tail(output)
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
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][1]['div'][0]['div'][1]['div'][0]['span'][0]['_value']
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

    def get_color(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][0]['div'][0]['span'][1]['_value']
        except:
            return "Color not available"

    def get_environment(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][1]['div'][0]['span'][1]['_value']
        except:
            return "Environment not available"

    def get_body(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0][
                'div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][2]['div'][0]['span'][1]['_value']
        except:
            return "Body not available"

    def get_tail(self, output):
        try:
            return output['html'][0]['body'][0]['div'][0]['main'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][0]['div'][3]['div'][0]['div'][0]['div'][0]['div'][1]['div'][3]['div'][0]['span'][1]['_value']
        except:
            return "Tail not available"
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
        stamina = float(self.stamina.split('/')[1])
        speed = float(self.speed.split('/')[1])
        strength = float(self.strength.split('/')[1])
        return max(strength, stamina, speed)