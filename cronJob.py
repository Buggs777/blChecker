import telebot
import mechanize
import csv
import os
 
TOKEN = ''
CHAT_ID = ''

bot = telebot.TeleBot(TOKEN)

def check_url(url, root_domain):
    try:
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent', 'Mozilla/5.0')]
        
        response = browser.open(url)
        page_content = response.read().decode('utf-8')
        
        return root_domain in page_content
    except Exception as e:
        print(f"Error checking URL {url}: {str(e)}")
        return False

def main():
    csv_filename = "/root/blChecker/blChecker/bl_list.csv"
    
    if not os.path.isfile(csv_filename):
        print(f"Error: {csv_filename} not found.")
        return

    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']
            root_domain = row['root_domain']
            
            if not check_url(url, root_domain):
                message = f"Lien vers : '{root_domain}' non trouvé sur l'url: {url}"
                bot.send_message(CHAT_ID, message)
                print(message)

if __name__ == "__main__":
    main()
