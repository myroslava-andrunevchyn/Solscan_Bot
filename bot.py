import requests
from datetime import datetime, timezone
from token_data import Token
import time
import telebot

#token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# .eyJjcmVhdGVkQXQiOjE2ODIwNjIwOTg2NzksImVtYWlsIjoic21pdHRpYXJrYUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE2ODIwNjIwOTh9.FM1ZZkT9Xa70MKs9L_HTIpalCU6SdSaC1kxVyny6d2Q'
account = 'A2B1w2fpwuJZrF9b69KBFb6Cn4Cp7siKGqQwPBJEGLYj'  # needed for data extraction
last_change_id = None

BOT_TOKEN = '6239867437:AAEsbnqXcIMy1K97QDlgYu1O4REoz8HM-zE'
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def command_start(message):
    chat_id = message.chat.id
    bot.reply_to(message, "Hello, now I'll be sending you updates on tokens")
    while True:
        send_updates(chat_id)
        time.sleep(60)


def get_account_transactions_url(account):  # returns url for Solscan Account transactions
    beginning = 'https://api.solscan.io/account/token/txs?address='
    end = '&offset=0&limit=10'
    return beginning+account+end

def get_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        print("Http Error:", e)


def get_transactions(data):  # process transaction data and filter by LastChangeID, output list of new transactions
# ready to filter by necessary parameters
    transactions_data = data['data']['tx']['transactions']
    transactions = []
    global last_change_id
    for transaction in transactions_data:
        if transaction['change']['_id'] == last_change_id:
            print("Transaction break")
            break
        transactions.append(transaction)
    last_change_id = transactions_data[0]['change']['_id']
    #print(f'Last change id assignment: {last_change_id}')
    return transactions


def process_transactions(transactions):
    filtered_transactions = {}
    for transaction in transactions:
        if str(transaction['change']['changeAmount']) == '1':
            #print('Token with +1 value')
            #print("here it is ", transaction['blockTime'], transaction['change']['changeAmount'])
            if 'tokenName' in transaction['change']:
                #print('Token has a name')
                if "Cathlete" in transaction["change"]["tokenName"]:
                    #print('Transaction with Cathlete')
                    transaction_date = datetime.fromtimestamp(transaction['blockTime'], timezone.utc).isoformat(' ').replace("+00:00",
                    " (UTC)")
                    filtered_transactions[transaction_date] = 'https://api.solscan.io/account?address=' + transaction["change"][
                        "tokenAddress"]
                    #filtered_transactions[transaction['blockTime']]='https://api.solscan.io/account?address=' + transaction["change"]["tokenAddress"]
                    #print(f'Transaction added to dict {transaction["slot"]}')
                    #print(f'Token name: {transaction["change"]["tokenName"]}')
                    #print(f'Token address: {transaction["change"]["tokenAddress"]}')
                #else:
                    #print('Token name not Cathlete')
            else:
                transaction_date = datetime.fromtimestamp(transaction['blockTime'], timezone.utc).isoformat(
                    ' ').replace("+00:00", " (UTC)")
                filtered_transactions[transaction_date] = 'https://api.solscan.io/account?address=' + \
                                                          transaction["change"]["tokenAddress"]

                #filtered_transactions[transaction['slot']] = 'https://api.solscan.io/account?address=' + transaction[
                 #   "change"]["tokenAddress"]
                #print(f'No token name, transaction added {transaction["slot"]}')
                #print(f'Token address: {transaction["change"]["tokenAddress"]}')
    #print(f'Filtered transactions: \n{filtered_transactions}')
    return filtered_transactions


def get_external_link(tokens_data: dict):
    external_links = {}
    for key, value in tokens_data.items():
        int_token_data = get_data(value)
        #print(f'Internal token data:\n{int_token_data}')
        ipfs_link = int_token_data['data']['metadata']['data']['uri']
        #print(f'IPFS link: \n{ipfs_link}')
        ipfs_data = get_data(ipfs_link)
        #print(f'ipfs data: \n{ipfs_data}')
        external_link = ipfs_data['external_url']
        #print(f'External link: \n{external_link}')
        external_links[key]=external_link
    #print(f'External links: \n{external_links}')
    return external_links


def tokens(external_links: dict):
    tokens = []
    for key, value in external_links.items():
        external_token_data = get_data(value)
        print(f'External token data: \n{external_token_data}')
        token_attr = {'strength': external_token_data['attributes'][2]['value'], 'stamina': external_token_data['attributes'][3][
            'value'], 'speed': external_token_data['attributes'][4]['value']}
        print(f'Token attributes: \n{token_attr}')
        max_value = max(token_attr, key=token_attr.get)
        token = {'name': external_token_data['attributes'][0]['value'], 'rarity': external_token_data['attributes'][1]['value'],
                max_value: token_attr[max_value]}
        print(f'Token: \n{token}')
        tokens.append(token)
    print(f'Tokens: \n{tokens}')
    return tokens


def send_updates(chat_id):
    print(f'Chat id {chat_id}')
    account_url = get_account_transactions_url(account)
    account_data = get_data(account_url)
    print('Got account data')
    new_transactions = get_transactions(account_data)
    print('Got new transactions')
    filtered_transactions = process_transactions(new_transactions)
    print('Filtered transactions')
    external_links = get_external_link(filtered_transactions)
    print('Got external links')
    tokens_list = []
    for key, value in external_links.items():
        try:
            token_obj = Token(value)
            print('Got token')
            tokens_list.append(token_obj)
        except:
            print(f"Token {key, value} is not available")
    print('Got tokens list')
    for token in tokens_list:
        token_str = token.__str__()
        bot.send_message(chat_id=chat_id, text=token_str)

bot.polling()
