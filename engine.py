from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pprint import pprint
from questions import loginFailQuestion, retryLogin
from progress.bar import Bar
import csv
import time

class Engine(object):
    def __init__(self, path, userName, password):
        self.username = userName
        self.password = password
        self.csvPath = path
        self.choices = []
        self.userEntries = []
        self._deleteAddress = []
        self._driver = None
        self.state = None

    # starts the web browser pass true to run headless
    def start_browser(self, headless):
        opts = Options()
        opts.set_headless(headless=headless)
        self._driver = Firefox(executable_path="./WebDriver/geckodriver", options=opts)
        self._driver.get('https://focus.eidexinsights.com')

    # reads in csv file and gets the headers for the search prompt
    def parse_csv(self):
        with open(self.csvPath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    self.choices = row
                    line_count += 1
                else:
                    self.userEntries.append(row)
                    line_count += 1
            print(f'CSV: Processed {line_count} rows')

    # handles login attempts into focus
    def login(self):
        username = self._driver.find_element_by_name('UserName')
        username.send_keys(self.username)

        password = self._driver.find_element_by_name('Password')
        password.send_keys(self.password)
        password.submit()

        try:
            ver = WebDriverWait(self._driver, 4).until(EC.presence_of_element_located((By.ID, 'currentUserEmail')))
        except TimeoutException:
            loginFailQuestion()
            creds = retryLogin()
            self.username = creds["refocus_name"]
            self.password = creds["refocus_password"]
            self.login()

    # starts the process of deleting users takes an array of your search criteria
    def begin_cleaning(self, selected):
        self._driver.get('https://focus.eidexinsights.com/Portal/UsersAdmin')
        select = Select(self._driver.find_element_by_id('statePulldown'))
        select.select_by_visible_text(self.state)
        
        print('loading... this will take 30 seconds')
        time.sleep(30)

        searchPatterns = self._build_search_terms(selected)
        searchBar = self._driver.find_element_by_id('usertable_filter')
        searchBar = searchBar.find_element_by_xpath('.//input')
        
        delete_from = self.fetch_delete_links(searchPatterns, searchBar)
        pprint(delete_from)
        # prompt for delete
        #self._do_it(delete_from)


    # gathers all the urls for deleting users takes an array of search querys and the input filter element
    def fetch_delete_links(self, search, searchBar):
        bar = Bar('Fetching links', max=len(search))
        deleteLinks = []
        for pattern in search:
            searchBar.clear()
            searchBar.send_keys(pattern)
            try:
                tab = self._driver.find_element_by_id('usertable')
                if len(tab.find_elements_by_xpath('.//tbody/tr')) > 1:
                    print(' Multiple users found with {}'.format(pattern))
                else:
                    link = tab.find_element_by_xpath('.//tbody/tr[1]/td[12]/a[last() - 1]')
                    deleteLinks.append(link.get_attribute('href'))
            except NoSuchElementException:
                print(' User Not Found {}'.format(pattern))
            bar.next()
        bar.finish()
        return deleteLinks

    # constructs the search queries takes an array containing your choices from the search prompt
    def _build_search_terms(self, searchPattern):
        identifiers = []
        for pattern in searchPattern:
           identifiers.append(self.choices.index(pattern))

        patterns = []
        for entry in self.userEntries:
            text = ""
            for ident in identifiers:
                text += entry[ident] + ' '
            patterns.append(text)
        return patterns

    def _do_it(self, lst):
        bar = Bar('Deleting', max=len(lst))
        self._driver.implicitly_wait(2)
        for target in lst:
            self._driver.get(target)
            the_button = self._driver.find_element_by_class_name('btn btn-default')
            the_button.click()
            bar.next()
        bar.finish()
            


            


    
