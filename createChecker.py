import os
import telebot
import mechanize
import csv

token = input("Token TLG : ")
chat_id = input("Chat ID : ")
root_domain = input("Root Domain : ")

bot_script = f"""
import telebot
import mechanize
import csv
import os

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
        browser.addheaders = [('User-agent', 'Mozilla/5.0')]
        
        response = browser.open(url)
        page_content = response.read().decode('utf-8')
        
        if ROOT_DOMAIN in page_content:
            result = "True"
            csv_filename = f"bl_list.csv"
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

filename = f"checklinks_{root_domain}.py"
with open(filename, 'w') as f:
    f.write(bot_script)

print(f"Bot généré : {{filename}}")
