from email import contentmanager
from seleniumwire import webdriver  # Import from seleniumwire
from seleniumwire.utils import decode
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import requests

def extended_filter(elms):
    fl = 0
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    # Create a new instance of the firefox driver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    # Go to the Google home page
    driver.get('http://1000mg.jp/')
    detect_elm = ""
    detect_body = ""
    # Access requests via the `requests` attribute
    for request in driver.requests:
        try:
            content_type = request.response.headers['Content-Type']
        except:
            break
        
        if ("text/html" in content_type) or ("text/javascript" in content_type):
            body = requests.get(request.url, verify=False).text
            print(body)
            for elm in elms:
                if elm in body:
                    detect_body = body
                    detect_elm = elm
                    fl = 1
                    break
            else:
                continue
    print(detect_body)
    print(detect_elm)
    return fl

if __name__ == '__main__':
    with open("filter_extend.txt","rt") as f:
        elms = f.read().splitlines()
    fl = extended_filter(elms)
    print(fl)