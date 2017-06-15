# encoding: utf-8
import os
import types
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException, NoAlertPresentException, ElementNotVisibleException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from tables import DetailedTable, OverviewTable, DataValidationError
from utils import patiently
from errors import XPathError, DownloadError, PageNotReady, EmptyFileError
import pdb

class AMS(object):
    def __init__(self, sleep=1.5):
        """ sleep (float): add extra sleep if connection is slow
        """ 
        self.download_dir = os.path.join(os.getcwd(), "tmp")
        self.save_dir = os.path.join(os.getcwd(), "data")
        self.sleep = sleep

        self._init_driver()


    def _init_driver(self):
        
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", self.download_dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver = make_patient(self.driver)

    def _open_page(self, url, attempt=0):
        d = self.driver

        def get_body():
            try :
                d.find_element_by_xpath("body")
            except UnexpectedAlertPresentException:
                try:
                    alert = d.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    pass
            except NoSuchElementException:
                sleep(2)
                pass

        d.get(url)
        attempt = 0
        try:
            print "trying to open page (%s)" % attempt
            get_body()
        except PageNotReady:
            attempt = attempt + 1
            if attempt < 10:
                get_body()

    def _open_start_page(self):
        start_url = "http://mstatkommun.arbetsformedlingen.se/"
        self._open_page(start_url)

    def _select_municipality(self, municipality):
        print "Select municipality (%s)" % municipality

        def select_municpality():
            muni_list.send_keys(municipality)

        def click_municpality():       
            elem = self.driver.find_element_by_xpath_patiently("//div[@title='%s']/../.." % municipality)
            elem.click()

        muni_list = self.driver.find_element_by_xpath_patiently("//div[contains(@title,'Välj kommun')]")
        muni_list.click()
        patiently(select_municpality, StaleElementReferenceException)
        patiently(click_municpality, NoSuchElementException)

    def _select_year_month(self, year, month):
        year_month = "%s-%02d" % (year, month)
        print "Select year-month (%s)" % year_month
        
        def click_month_list():
            xpath = "//div[contains(@title,'Månad')]"
            month_list = self.driver.find_elements_by_xpath_patiently(xpath)[1]
            month_list.click()
            sleep(self.sleep)
            return month_list

        #def select_year_month():

        def click_year_month():
            month_list.send_keys(year_month)
            elem = self.driver.find_element_by_xpath_patiently("//div[@title='%s']" % year_month)
            elem.click()
            sleep(self.sleep)

        month_list = patiently(click_month_list, IndexError, exception_to_raise=XPathError)
        #patiently(select_year_month, (ElementNotVisibleException, StaleElementReferenceException))
        patiently(click_year_month, (ElementNotVisibleException, StaleElementReferenceException))
        

    def _select_youth_only(self):
        print "Select youth only"
        def select_youth_only():
            elem = self.driver.find_elements_by_xpath_patiently("//div[@title='18-24 år']")[-1]
            elem.click()
        
        sleep(self.sleep)
        patiently(select_youth_only, NoSuchElementException)
        
    def _select_foreign_only(self):
        print "Select foreign only"
        def select_foreign_only():
            elem = self.driver.find_elements_by_xpath_patiently("//div[@title='Utrikesfödda']")[-1]
            elem.click()
        
        sleep(self.sleep)
        patiently(select_foreign_only, NoSuchElementException)

    def _download_file(self, xpath):
        print "Download file"
        d = self.driver
        """ Downloads a file given an xpath to the download link 
        """
        file_list_before = os.listdir(self.download_dir)

        # Download file
        def download_file():
            export_btn = d.find_element_by_xpath_patiently(xpath)
            export_btn.click()
        

        def get_filename():
            file_list_after = os.listdir(self.download_dir)
            diff = list(set(file_list_after) - set(file_list_before))
            if len(diff) == 0:
                raise DownloadError
            else:
                file_name = diff[0]
                if ".part" in file_name:
                    raise DownloadError
                else:
                    return file_name

        patiently(download_file, NoSuchElementException, seconds=3)
        file_name = patiently(get_filename, DownloadError)

        return self.download_dir + "/" + file_name

    def get_detailed(self, municipality=None, county=None, year=None, month=None, youth_only=False, foreign_only=False):
        d = self.driver
        self._open_start_page()

        # Select municipality
        if (municipality):
            self._select_municipality(municipality)

        # Select year-month
        if year and month:
            self._select_year_month(year, month)    

        if youth_only:
            self._select_youth_only()

        if foreign_only:
            self._select_foreign_only()


        downloaded_file = self._download_file("//td[contains(text(),'Exportera till Excel')]")
        def parse_downloaded():
            return DetailedTable().parse_downloaded_file(downloaded_file)
        print downloaded_file
        data = patiently(parse_downloaded, IndexError)

        # Dismiss dialog
        try:
            close_btn = d.find_element_by_xpath_patiently("//button[text()='OK']")
            close_btn.click()
        except:
            pass
        
        return data

    def _get_overview(self, year=None, month=None, youth_only=False, foreign_only=False):
        data = OverviewTable()
        d = self.driver
        self._open_start_page()

        sleep(self.sleep)
        tab_elem = self.driver.find_element_by_xpath_patiently('//td[text()="Utskriftsrapporter"]')
        tab_elem.click()
        sleep(self.sleep)

        # Select year-month
        if year and month:
            self._select_year_month(year, month)    

        if youth_only:
            self._select_youth_only()

        if foreign_only:
            self._select_foreign_only()

        def parse_downloaded():
            return data.parse_downloaded_file(downloaded_file)

        # [1] = "Arbetssökande antal/andel av den registerbaserade arbetskraften"
        # [2] = "Arbetssökande antal/andel av befolkningen"
        xpath = "(//td[contains(text(),'Exportera till Excel')])[1]"
        downloaded_file = self._download_file(xpath)
        data = patiently(parse_downloaded, IndexError)
        data.verify(year=year, month=month, youth_only=youth_only, foreign_only=foreign_only)



        return data

    def get_overview(self, year=None, month=None, youth_only=False, foreign_only=False):
        data = []
        while len(data) == 0:
            try:
                data = self._get_overview(year=year, month=month, youth_only=youth_only, foreign_only=foreign_only)
            except (StaleElementReferenceException, NoSuchElementException, XPathError, DownloadError, DataValidationError, EmptyFileError) as e:
                """ A number of things could go wrong. If it does, just try again.
                """
                print u"Caught an error (%s), but makes another attempt to get overview." % e.__class__.__name__
                data = self._get_overview(year=year, month=month, youth_only=youth_only, foreign_only=foreign_only)

        return data

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def make_patient(driver):
    driver.find_element_by_xpath_patiently = types.MethodType( find_element_by_xpath_patiently, driver )        
    driver.find_elements_by_xpath_patiently = types.MethodType( find_elements_by_xpath_patiently, driver )        
    return driver


def find_element_by_xpath_patiently(self, xpath, seconds=5):
    """ Attempts to find an element for n seconds. 
    """
    attempts = 10
    i = 0
    print "Find %s" % xpath
    while i < attempts: 
        try:
            return self.find_element_by_xpath(xpath)
        except NoSuchElementException:
            sleep( float(seconds) / float(attempts))
            i += 1
    raise NoSuchElementException(xpath)


def find_elements_by_xpath_patiently(self, xpath, seconds=4):
    attempts = 20
    i = 0
    print "Find %s" % xpath
    while i < attempts: 
        try:
            return self.find_elements_by_xpath(xpath)
        except NoSuchElementException:
            print i
            sleep( float(seconds) / float(attempts))
            i += 1
    raise NoSuchElementException(xpath)



