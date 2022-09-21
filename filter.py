from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import ast
import json

def integrated_filter(urls,elms,associative,driver):
    urllib3.disable_warnings(InsecureRequestWarning)
    fl_network = 0
    fl_extend = 0
    ret_network_dict = {}
    ret_extend_dict = {}
    for i in range(1,len(associative)+1):
        print(i)
        print(associative[i])
        fl_network = 0
        fl_extend = 0

        try:
            driver.get(associative[i])
        except Exception:
            ret_extend_dict[i] = fl_extend
            ret_network_dict[i] = fl_network
            continue

        # Access requests via the `requests` attribute
        for request in driver.requests:
            #network filter
            if fl_network == 0:
                for url in urls:
                    if url in request.url:
                        fl_network = 1
                        break
            #extend filter
            if fl_extend == 0:
                try:
                    content_type = request.response.headers['Content-Type']
                    if ("html" in content_type) or ("javascript" in content_type):
                        body = requests.get(request.url, verify=False, timeout=30.0).text
                        for elm in elms:
                            if elm in body:
                                fl_extend = 1
                                break
                        else:
                            continue
                    if fl_extend == 1:
                        break
                except Exception:
                    continue
                
        ret_extend_dict[i] = fl_extend
        ret_network_dict[i] = fl_network
        del driver.requests
    
    return ret_extend_dict, ret_network_dict

def filter():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    #options.page_load_strategy = 'eager'
    # Create a new instance of the firefox driver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)

    with open("filter_extend_2.txt","rt") as f:
        elms_extend = f.read().splitlines()
    
    with open("filter_network_2.txt", "rt") as f:
        elms_network = f.read().splitlines()

    with open("associative_array2.txt","rt") as f:
        # str to dict
        associative = ast.literal_eval(f.read())
    
    dict_extend, dict_network = integrated_filter(elms_network, elms_extend, associative, driver)
    return dict_extend, dict_network

def make_dict(dict_extend, dict_network):
    # both possible
    ret_dict = {}
    length = len(dict_extend)
    for i in range(1,length+1):
        ret_dict[i] = {"network": dict_network[i], "extend": dict_extend[i]}
    return ret_dict

if __name__ == '__main__':
    dict_extend, dict_network = filter()
    final_dict = make_dict(dict_extend, dict_network)

    with open("akusei_output_2.json","wt") as f:
        f.write(json.dumps(final_dict))
