"""
This module is used to provide functionalities to perform the storing phase of the package.

The core functionalities in this module are the login process at instagram and the
downloading and saving of html files.

"""
from instagram.data.config import *
from random import randint
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from pprint import pprint
from lxml import etree, html
from pathlib import Path
import json

"""
Constants to calculate the sleep timer.
"""
MIN_TIME = 3
INCR_UPPER_BOUND = 10



def login(username, password):
    """
    The function is used to perform the login process at instagram.com.
    It also accepts the cookie banner and saves the login information.

    Args:
        username (str): The username which is used to log in.
        password (str): The password which is used to log in.
    """
    driver.get(base_url)
    random_sleep(5)
    if driver.find_elements_by_xpath("//*[contains(., 'Cookies') or contains(., 'cookies')]"):
        cookie_consent()
        random_sleep(5)

    # Log into account only if not already logged in.
    if driver.find_elements_by_xpath("//*[text()='Log In']") or driver.find_elements_by_xpath("//*[text()='Anmelden']"):
        driver.find_element_by_name("username").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        if driver.find_elements_by_xpath("//*[text()='Log In']"):
            driver.find_element_by_xpath("//*[text()='Log In']").click()
        else:
            driver.find_element_by_xpath("//*[text()='Anmelden']").click()
        random_sleep(10)


    if "onetap" in driver.current_url:  # "Save your Login?"-Page
        if driver.find_elements_by_xpath("//*[text()='Save Info']"):
            driver.find_element_by_xpath("//*[text()='Save Info']").click()
        else:
            driver.find_element_by_xpath("//*[text()='Informationen speichern']").click()

    random_sleep(10)


def cookie_consent():
    """
    Accepts the cookie banner, if it exists. Otherwise the downloaded html-files
    are obfuscated by the banner.
    """
    if driver.find_elements_by_xpath("//*[text()='Akzeptieren']"):
        driver.find_element_by_xpath("//*[text()='Akzeptieren']").click()
    elif driver.find_elements_by_xpath("//*[text()='Accept']"):
        driver.find_element_by_xpath("//*[text()='Accept']").click()


def convert_links(source):
    """
    Converts relative to absolute links in a given string by appending a base-url, which is specified
    in the config-file.
    Only links which are the content of the html attributes href, src, or srcset, or of a dictionary
    will be changed.

    Example:
        Let's assume the base_url is https://instagram.com
        <a href="/sta/exmpl.css"> will be converted to <a href="https://instagram.com/sta/exmpl.css">
        dic = {a: "/sta/exmpl.css"} will be converted to dic = {a: "https://instagram.com/sta/exmpl.css"}

    Args:
        source (str): The string representation of the parsed html file.

    Returns:
        str: The same string as source, but with converted links.
    """
    # remove javascript inline script parts
    source = re.sub(r'(?is)<script[^>]*>(.*?)</script>', '', source)

    # remove javascript import links
    source = re.sub(r'<link.*?type="text/javascript".*?/>', '', source)

    # converts relative to absolute links
    source = re.sub(r'(href="|src="|srcset="|:")/', r'\1' + base_url, source)
    return source


def save_html(url):
    """
    Saves the html content of a website and saves it in a file.
    Depending on the input, the function will either save the content of the "posts" intsagram subdirectory,
    the "tagged" subdirectory, or the "IGTV" subdirectory.

    Args:
        url (dict): Containts the url to the website that has to be saved, as well as the type in terms of
                    "posts", "tagged", or "IGTV". It also contains a path where the generated files are going
                    to be saved.
    """

    driver.get(str(url["href"]))
    random_sleep(10)
    latest_story_timestamp()

    content = convert_links(driver.execute_script("return new XMLSerializer().serializeToString(document);"))
    pre_download(url)

    with open(os.path.join(monitoring_folder, url["monitoring_folder"], "new.html"), "w") as f:
        f.write(content)


def latest_story_timestamp() -> int:
    """
    Checks if an active story exists.

    Returns:
        int: timestamp of last story, 0 if none exists
    """
    for request in driver.requests:
        if request.response:
            if 'graphql' in request.url:
                reply_content = request.response.body.decode('utf-8')
                if 'latest_reel_media' in reply_content and 'edge_suggested_users' not in reply_content:  # Identifying correct request
                    reply_json = json.loads(reply_content)
                    return reply_json['data']['user']['reel']['latest_reel_media']
    return 0


def random_sleep(max_time):
    """
    Pauses the program sequence for a pseudo random time, depending on the input.
    The program sequence will be paused for at least 3 seconds.

    Args:
        max_time (int): Determines how long the program sequence is paused at most.
    """
    if max_time < MIN_TIME:
        max_time = MIN_TIME + INCR_UPPER_BOUND
    random_time = randint(MIN_TIME, max_time)
    sleep(random_time)


def pre_download(url):
    """
    If a file already exists in the monitoring folder, it's name will be changed
    to old.html.
    If there is already an old file, it will be deleted.

    Args:
        url (dict): Containts the path of the monitoring folder and one of the types
                    "posts", "tagged", or "IGTV" to determine the file path.
    """
    folder = os.path.join(monitoring_folder, url["monitoring_folder"])
    newFilepath = os.path.join(monitoring_folder, url["monitoring_folder"], "new.html")
    oldFilepath = os.path.join(monitoring_folder, url["monitoring_folder"], "old.html")
    try:
        Path(folder).mkdir(parents=True, exist_ok=True)            
        if os.path.exists(oldFilepath):        
            os.remove(oldFilepath)
        if os.path.exists(newFilepath):        
            os.rename(newFilepath, oldFilepath) 

    except Exception as e:
        eType = e.__class__.__name__
        logger.error("error in pre-download phase.\nException message: "  + eType + ": "+ str(e))


