import os
import telebot
import mechanize
import csv
import random

token = input("Token TLG : ")
chat_id = input("Chat ID : ")
root_domain = input("Root Domain : ")

bot_script = f"""
import telebot
import mechanize
import csv
import os
import random
import time

TOKEN = '{token}'
CHAT_ID = '{chat_id}'
ROOT_DOMAIN = '{root_domain}'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['newurl'])
def check_url(message):
    try:
        url = message.text.split()[1]
        browser = mechanize.Browser()
        
        browser.set_handle_robots(False)
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]
        browser.addheaders = [('User-agent', random.choice(user_agents))]
        
        browser.addheaders = [
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('DNT', '1'),
            ('Connection', 'keep-alive'),
            ('Upgrade-Insecure-Requests', '1')
        ]
        
        time.sleep(random.uniform(1, 3))
        response = browser.open(url)
        page_content = response.read()
        try:
            page_content = page_content.decode('utf-8', errors='strict')
        except UnicodeDecodeError:
            bot.send_message(CHAT_ID, f"Impossible de décoder la page en utf8")
            return
        print(page_content)

        if ROOT_DOMAIN in page_content:
            result = "True"
            csv_filename = f"/root/blChecker/blChecker/bl_list.csv"
            file_exists = os.path.isfile(csv_filename)
            
            with open(csv_filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(['url', 'root_domain'])  # Write header if file is new
                writer.writerow([url, ROOT_DOMAIN])
        else:
            result = "False"
        
        bot.send_message(CHAT_ID, f"URL: {{url}}\\nRoot domain trouvé : {{result}}")
    except Exception as e:
        bot.send_message(CHAT_ID, f"Erreur : {{str(e)}}")

bot.polling()
"""

filename = f"checklinks_{root_domain.replace('.', '-')}.py"
with open(filename, 'w') as f:
    f.write(bot_script)
print(f"Bot genere : {filename}")