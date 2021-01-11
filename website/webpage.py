import logging
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from website.web_exception import KeyElementNotFoundException
from candidate.candidate_info import CandidateInfo

logger = logging.getLogger(u"sr")
DEBUG_DELAY = 2


class WebPage(object):
    def __init__(self, browser):
        self.browser = browser
        self.loadingTimeout = 30
        self.readyElementLocator = None
        self.website = None

    def open(self):
        if self.website:
            logger.info(u"Open website: {}".format(self.website))
            self.browser.get(self.website)

    def is_ready(self):
        try:
            if self.readyElementLocator:
                WebDriverWait(self.browser, self.loadingTimeout).until(
                    EC.presence_of_element_located(self.readyElementLocator)
                )
            return True
        except TimeoutException:
            return False

    def refresh(self):
        self.browser.refresh()

    def close(self):
        self.browser.close()


class MainPage(WebPage):
    def __init__(self, browser, params):
        super(MainPage, self).__init__(browser)
        self.params = params
        self.website = self.params["webMain"]
        self.readyElement = None
        self.memberNameElement = None
        self.userNameElement = None
        self.passwordElement = None
        self.loginButtonElement = None
        self.is_auto_login = True

    def login(self):
        logger.info(u"login the website ...")
        if self.memberNameElement and "loginMember" in self.params:
            self.memberNameElement.input_value(self.params["loginMember"])
        if self.userNameElement and "loginUser" in self.params:
            self.userNameElement.input_value(self.params["loginUser"])
        if self.passwordElement and \
                "loginPassword" in self.params and self.params["loginPassword"]:
            self.passwordElement.input_value(self.params["loginPassword"])
            if self.loginButtonElement:
                self.loginButtonElement.click()

        if self.is_auto_login:
            # Ask user to login by manual
            logger.info(u"Please login the website by manual because of AI checking in the website!")
            prompt = u"Do you login successfully and jump to the main page? (y/n)"
            if sys.version_info.major == 2:
                r = raw_input(prompt)
            else:
                r = input(prompt)
            return 'y' == str(r).lower()
        else:
            return True


class SearchPage(WebPage):
    def __init__(self, browser, params, conditions):
        super(SearchPage, self).__init__(browser)
        self.params = params
        self.conditions = conditions
        self.source = None
        self.resultsPageNum = 1

        self.candidates = []

        self.conditionKeyWordsElement = None
        self.searchButtonElement = None
        self.pagesNumElement = None
        self.candidatesListElement = None
        self.nextPageElement = None

        self.candidateIDElement = None

        self.logoutButtonElement = None

    def search(self):
        if not self.conditionKeyWordsElement:
            raise KeyElementNotFoundException(u"KeyWords element cannot be used!")
        if not self.searchButtonElement:
            raise KeyElementNotFoundException(u"Search button element cannot be used!")

        logger.info(u"Start to search key words: {}".format(self.conditions["keyWords"]))
        self.conditionKeyWordsElement.input_value(self.conditions["keyWords"])
        self.searchButtonElement.click()
        time.sleep(2)
        self.get_total_pages_num()
        logger.info(u"Searching finished, get total '{}' page(s)".format(self.resultsPageNum))

    def get_total_pages_num(self):
        pass

    def load_candidates(self):
        candidateNum = 1
        if self.candidatesListElement:
            currentPageNum = 1
            debugPageNum = 1
            while True:
                # keep loading until reach the max page num
                candidateElements = None
                try:
                    candidateElements = self.candidatesListElement.elements
                except Exception:
                    logger.exception(u"Cannot get candidates, double check your keep words!")
                    break

                if not candidateElements:
                    break

                logger.info(u"\nFind '{}' candidates in current page, start to parse".format(len(candidateElements)))
                debugCandidateNum = 1
                for candidateElement in candidateElements:
                    self.jump_to_detailed_page(candidateElement)
                    candidatePage = None
                    try:
                        logger.info(u"Loading and parsing candidate #{} in page '{}' ...".format(candidateNum, currentPageNum))
                        candidatePage = self.load_candidate_page()
                        if candidatePage.is_ready():
                            candidateInfo = candidatePage.load_info()
                        if candidateInfo:
                            self.candidates.append(candidateInfo)
                    finally:
                        if candidatePage:
                            if logging.DEBUG == logger.level:
                                time.sleep(DEBUG_DELAY)
                            candidatePage.close()
                        handles = self.browser.window_handles
                        self.browser.switch_to_window(handles[0])

                    candidateNum = candidateNum + 1

                    if logging.DEBUG == logger.level:
                        if debugCandidateNum > 1:
                            # debug mode, skip loop
                            break
                        else:
                            debugCandidateNum = debugCandidateNum + 1

                # go to next page
                if currentPageNum >= self.resultsPageNum:
                    break
                else:
                    self.nextPageElement.click()
                    currentPageNum = currentPageNum + 1

                if logging.DEBUG == logger.level:
                    if debugPageNum > 1:
                        break
                    else:
                        debugPageNum = debugPageNum + 1
        return self.candidates

    def jump_to_detailed_page(self, candidateElement):
        candidateElement.click()  # jump to the detailed page

    def load_candidate_page(self):
        return None

    def logout(self):
        logger.info("Logout the account")
        if self.browser:
            handles = self.browser.window_handles
            self.browser.switch_to_window(handles[0])
            if self.logoutButtonElement:
                time.sleep(1)
                self.browser.execute_script(u"return arguments[0].scrollIntoView(true);", self.logoutButtonElement.element)
                time.sleep(2)
                self.logoutButtonElement.click()


class CandidateInfoPage(WebPage):
    def __init__(self, browser, params):
        super(CandidateInfoPage, self).__init__(browser)
        self.params = params
        self.candidateInfo = CandidateInfo(params)

    def load_info(self):
        return self.candidateInfo
