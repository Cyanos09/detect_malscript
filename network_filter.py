from seleniumwire import webdriver  # Import from seleniumwire
from seleniumwire.utils import decode
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def network_filter(urls):
    fl = 0
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    # Create a new instance of the firefox driver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    # Go to the Google home page
    driver.get('http://1000mg.jp/')

    # Access requests via the `requests` attribute
    for request in driver.requests:
        for url in urls:
            if url in request.url:
                fl = 1
                break
        else:
            continue
    
    return fl

if __name__ == '__main__':
    with open("filter_network.txt","rt") as f:
        urls = f.read().splitlines()
    fl = network_filter(urls)
    print(fl)