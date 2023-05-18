import requests
from datetime import datetime, timedelta
from token_data import Token
import time
import telebot
import logging
import os
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filename='app.log', filemode='w')

#logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# creating console handler, setting level to INFO and setting formatter
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

# creating file handler, setting level to DEBUG and setting formatter
#log_path = os.path.join(os.getcwd(), 'app.log')
#fh = logging.FileHandler(log_path)
#fh.setLevel(logging.INFO)
#fh.setFormatter(formatter)
logging.getLogger('').addHandler(console)
# adding handlers to logger
#logger.addHandler(console)
#logger.addHandler(fh)


account = 'A2B1w2fpwuJZrF9b69KBFb6Cn4Cp7siKGqQwPBJEGLYj'  # account name needed for data extraction
last_change_id = None

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    message_text = 'Welcome to SolscanBot v0.01'
    bot.reply_to(message, message_text)
    while True:
        send_updates(chat_id)
        time.sleep(120)


def convert_time(blocktime):
    kyiv_timezone = timezone('Europe/Kyiv')
    minutes_to_add = 4
    t_date = datetime.fromtimestamp(blocktime, tz=kyiv_timezone)+timedelta(minutes=minutes_to_add)
    return t_date.strftime('%d/%m/%Y %H:%M:%S')


def get_account_transactions_url(account):  # returns url for Solscan Account transactions
    beginning = 'https://api.solscan.io/account/token/txs?address='
    end = '&offset=0&limit=40'
    return beginning+account+end

def get_data(url):  # returns raw transactions data from Solscan
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logging.debug(f'Raw data status -- {response.status_code}')
        return data
    except requests.exceptions.HTTPError as e:
        logging.error("Http Error occurred during raw data extraction process", exc_info=True)


def get_transactions(data):  # process transactions data and filter by LastChangeID, returns a list of new transactions
    # ready to be filtered by necessary parameters
    transactions_data = data['data']['tx']['transactions']
    transactions = []
    global last_change_id
    logging.debug(f'Last change id (since last retrieve) -- {last_change_id}')
    for transaction in transactions_data:
        if transaction['change']['_id'] == last_change_id:
            logging.debug("Transaction break, reached the id of previously retrieved transaction")
            break
        transactions.append(transaction)
    last_change_id = transactions_data[0]['change']['_id']
    logging.debug(f'Last change id (the id of last transaction in this bulk) -- {last_change_id}')
    logging.debug(f'List of transactions(no filter) -- {transactions}')
    logging.info(f'{len(transactions)} - transactions(no filter) received')
    return transactions


def process_transactions(transactions):  # transactions list is filtered by 'changeAmount' field(must be equal +1)
    # those which have 'tokenName'(must be Cathlete) or link, are added to list. Returns list of dictionaries {
    # date:value, solscan_token_link:value, seller_signature:value}
    filtered_transactions = []
    for transaction in transactions:
        if str(transaction['change']['changeAmount']) == '1':
            transaction_dict = {}
            logging.debug(f"Token with +1 value found -- blockTime -- {transaction['blockTime']} -- changeAmount -- {transaction['change']['changeAmount']}")
            if 'tokenName' in transaction['change']:
                logging.debug(f"Token has a name -- {transaction['change']['tokenName']}")
                if not "Cathlete" in transaction["change"]["tokenName"]:
                    logging.debug(f'Transaction with name {transaction["change"]["tokenName"]} skipped')
                    break
                logging.debug('Transaction with Cathlete')
                try:
                    seller_signature = transaction['change']['signature'][0]
                except:
                    logging.error(f'Seller signature not available')
                transaction_dict['date'] = convert_time(transaction['blockTime'])
                transaction_dict['solscan_token_link'] = 'https://api.solscan.io/account?address=' + transaction[
                    "change"]["tokenAddress"]
                transaction_dict['transaction_signature'] = seller_signature
                logging.debug(f"Transaction: {transaction_dict['date']} -- {transaction_dict['solscan_token_link']} --"
                              f" {transaction_dict['transaction_signature']} is added")
            else:
                seller_signature = transaction['change']['signature'][0]
                transaction_dict['date'] = convert_time(transaction['blockTime'])
                transaction_dict['solscan_token_link'] = 'https://api.solscan.io/account?address=' + \
                                                         transaction["change"]["tokenAddress"]
                transaction_dict['transaction_signature'] = seller_signature
                logging.debug(f"Transaction: {transaction_dict['date']} -- {transaction_dict['solscan_token_link']} -- "
                              f"{transaction_dict['transaction_signature']} is added")
            filtered_transactions.append(transaction_dict)
    logging.debug(f'Filtered transactions: \n{filtered_transactions}')
    logging.info(f'{len(filtered_transactions)} - filtered transactions received')
    return filtered_transactions


def get_external_link(tokens_data: list[dict]):  # extracts external link to get ipfs data, where walken links are
    # stored. Also tokens are filtered by Rarity attribute. Returns a list of dict items with walken links
    external_links = []
    for transaction_dict in tokens_data:
        int_token_data = get_data(transaction_dict['solscan_token_link'])
        logging.debug(f'Internal token data:\n{int_token_data}')
        try:
            ipfs_link = int_token_data['data']['metadata']['data']['uri']
            logging.debug(f'IPFS link: \n{ipfs_link}')
            ipfs_data = get_data(ipfs_link)
            logging.debug(f'ipfs data: \n{ipfs_data}')
            try:
                external_link = ipfs_data['external_url']
                logging.debug(f'External link: {external_link}')
            except:
                logging.error(f'Failed to retrieve external link from ipfs_data')
            if ipfs_data['attributes'][1]['value'] == 'Uncommon' or ipfs_data['attributes'][1]['value'] == 'Rare':
                logging.debug(f'Token filtered by rarity')
                logging.debug(f"Token added -- {transaction_dict['solscan_token_link']} -- external link: {external_link}")
                seller_link = 'https://api.solscan.io/transaction?tx=' + transaction_dict[
                    'transaction_signature'] + '&cluster='
                seller_data = get_data(seller_link)
                logging.debug('Extracted seller data')
                seller = seller_data['signer'][0]
                logging.debug(f'Seller: {seller}')
                transaction_dict['external link'] = external_link
                transaction_dict['seller'] = seller
                external_links.append(transaction_dict)
        except:
            logging.error(f'Ipfs link data for transaction {transaction_dict} failed', exc_info=True)
    logging.debug(f'External links: \n{external_links}')
    logging.info(f'{len(external_links)} - external links received')
    return external_links


def walken_token(external_links, chat_id):
    for token_data in external_links:
        try:
            t_path = token_data['external link']
            t_date = token_data['date']
            t_seller = token_data['seller']
            token_obj = Token(t_path, t_date, t_seller)
            token_str = token_obj.__str__()
            logging.debug(f'Token\n{token_obj.__str__()}')
            logging.info(f'Token {token_obj.name} with {token_obj.breed_count} breeds')
            if int(token_obj.breed_count) != 0:
                logging.info(f'Token skipped: {token_obj.name} {token_obj.path}')
                break
            logging.info(f'Token {token_obj.name} TG sent')
            tg_message = f"*{token_obj.name}*   *{token_obj.rarity}*  {token_obj.level}/{token_obj.breed_count}   " \
                         f"*Max: {token_obj.max_attr}*\n\n*Gems current*: {token_obj.gems_current}\n*Gems left*: " \
                         f"{token_obj.gems_left}\n\n*Color*: {token_obj.color.rstrip('% have this gene')}                " \
                         f"*Tail*: {token_obj.tail.rstrip('% have this gene')}\n*Environment*: " \
                         f"{token_obj.environment.rstrip('% have this gene')}  *Ears*: " \
                         f"{token_obj.ears.rstrip('% have this gene')}\n*Body*: " \
                         f"{token_obj.body.rstrip('% have this gene')}                 *Face*:" \
                         f" {token_obj.face.rstrip('% have this gene')}\n\n*Time*: {token_obj.time}\n*Seller*:" \
                         f" {token_obj.seller[-4:]}"
            bot.send_message(chat_id=chat_id, text=tg_message, parse_mode= 'Markdown')
        except:
            logging.error(f"Token {token_data} is not available", exc_info=True)


def send_updates(chat_id):  # method which runs the token data extraction flow
    logging.info(f'Chat id: {chat_id}')
    account_url = get_account_transactions_url(account)
    account_data = get_data(account_url)
    logging.info(f'Account data retrieved')
    new_transactions = get_transactions(account_data)
    filtered_transactions = process_transactions(new_transactions)
    external_links = get_external_link(filtered_transactions)
    logging.debug('Calling token_generator')
    walken_token(external_links, chat_id)
    logging.debug('Tokens sent')


bot.polling()