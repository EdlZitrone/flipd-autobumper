from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import undetected_chromedriver as uc
import time
from config import username, password

# pip install selenium==4.12.0
# pip install undetected-chromedriver

class LinkBumper:

    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument("--window-size=920,600")
        self.driver = uc.Chrome(use_subprocess=True, options=options)
        self.wait = WebDriverWait(self.driver, 40)
        self.main_url = "https://flipd.gg/"
        self.username = username

        self.login(username, password)
        self.bumper()

    # loop to keep bumping all the threads as long as user is logged in
    def bumper(self):
        while True:
            links = self.get_links()
            self.bump_threads(links)
            time.sleep(1800 - len(links) * 7)

    # try to log in to the website with given user credentials
    def login(self, username, password):
        self.driver.get('https://google.com')
        time.sleep(15)
        self.driver.get(self.main_url + 'login')
        user_xpath = '//*[@id="fullcontainment"]/div/form[2]/table/tbody/tr[1]/td/label/input'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, user_xpath))).send_keys(username)
        pass_xpath = '//*[@id="fullcontainment"]/div/form[2]/table/tbody/tr[2]/td/label/input'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, pass_xpath))).send_keys(password)
        login_xpath = '//*[@id="fullcontainment"]/div/form[2]/table/tbody/tr[4]/td/span/input'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, login_xpath))).click()
        time.sleep(10)

    # check if user is still logged in. return True is he is
    def logged_in(self) -> bool:
        self.driver.get(self.main_url + 'usercp.php')
        time.sleep(2)
        username_xpath = '//*[@id="fullcontainment"]/div[1]/div[2]/div[2]/div/div/div/div/div/div/a[1]'
        elements = self.driver.find_elements(By.XPATH, username_xpath)
        return len(elements) > 0

    # get list of active shop threads for logged in user
    def get_threads(self) -> list:
        links = []
        with open('threads.txt') as file:
            for line in file:
                links.append(line)
        return links

    # get list of newreply links with given thread link list
    def get_links(self) -> list:
        threads = self.get_threads()
        links = []
        for link in threads:
            self.driver.get(link)
            newreply_xpath = '//*[@id="noa-posttransition"]/div[2]/div/div/a'
            element = self.wait.until(ec.visibility_of_element_located((By.XPATH, newreply_xpath)))
            reply_link = element.get_attribute('href')
            links.append(reply_link)
        return links

    # iterates through newreply list and bumps each
    def bump_threads(self, threads: list):
        for link in threads:
            self.bump(link)
        print('Successfully bumped all threads!')

    # bumps thread by given rewreply link
    def bump(self, link: str):
        self.driver.get(link)
        title_xpath = '//*[@id="fullcontainment"]/div[1]/form/table/tbody/tr[2]/td/span/strong'
        elements = self.driver.find_elements(By.XPATH, title_xpath)
        if len(elements) == 0:
            time.sleep(5)
            self.driver.refresh()
            self.bump(link)
            return
        title_element = self.wait.until(ec.visibility_of_element_located((By.XPATH, title_xpath)))
        title = title_element.text.split('THREAD: ')[1]
        self.wait.until(ec.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe')))
        self.wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body'))).send_keys(title)
        self.driver.switch_to.default_content()
        button_xpath = '//*[@id="fullcontainment"]/div[1]/form/div[2]/input[1]'
        self.wait.until(ec.element_to_be_clickable((By.XPATH, button_xpath))).click()
        print('Bumped: ' + title)
        time.sleep(7)