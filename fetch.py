from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import json
import pandas as pd

def main():
    url = "https://ws.duelbits.com/games/crash/history"
    html_source = fetch_and_display_html(url)

    json_data = extract_json_from_html(html_source)
    
    if json_data:
        process_and_save_to_csv(json_data, "data.csv")
        return json_data[0]
    else:
        return {}  # Data නැති වුණොත් Error එන එක නවත්වන්න හිස් අගයක් යවමු

def fetch_and_display_html(url):
    browser = None  # මෙතනින් තමයි UnboundLocalError එක විසඳන්නේ!
    try:
        options = Options()
        options.add_argument("--headless")  # අලුත් Selenium වලට ගැලපෙන විදිහ
        
        service = Service(GeckoDriverManager().install()) 
        browser = webdriver.Firefox(service=service, options=options)
        browser.get(url)

        browser.implicitly_wait(10)
        html_source = browser.page_source

        return html_source

    except Exception as e:
        print(f"Error fetching HTML: {str(e)}")
        return None
    finally:
        if browser is not None:
            browser.quit()

def extract_json_from_html(html_source):
    if not html_source:
        return []
        
    try:
        soup = BeautifulSoup(html_source, 'html.parser')
        json_div = soup.find('div', {'id': 'json'})
        
        if json_div:
            json_data = json.loads(json_div.text)
            return json_data.get("history", [])
        else:
            # සමහර වෙලාවට සයිට් එකෙන් කෙලින්ම JSON එවනවා නම් ඒක අල්ලගන්න
            try:
                json_data = json.loads(soup.text)
                if isinstance(json_data, dict) and "history" in json_data:
                    return json_data.get("history", [])
            except:
                pass
            print("Error: Unable to find div with id='json'")
            return []
    except Exception as e:
        print(f"Error parsing JSON: {str(e)}")
        return []

def process_and_save_to_csv(json_data, filename):
    if json_data:
        df = pd.DataFrame(json_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("Error: No JSON data to process and save")

if __name__ == "__main__":
    x = main()
    print(x)
