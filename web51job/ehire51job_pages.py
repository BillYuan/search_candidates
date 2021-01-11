# -*- coding: UTF-8 -*-

import logging
import time
from website.webpage import MainPage, SearchPage, CandidateInfoPage
from website.element import Element
from web51job.ehire51job_locators import EHire51JobLoginLocators, EHire51JobSearchWYLocators, EHire51JobCandidateWYLocators
from selenium.webdriver.common.by import By

logger = logging.getLogger(u"sr")


class EHire51JobLoginPage(MainPage):
    def __init__(self, browser, params):
        super(EHire51JobLoginPage, self).__init__(browser, params)
        self.readyElementLocator = EHire51JobLoginLocators.LOGIN_BT
        self.memberNameElement = Element(self.browser, EHire51JobLoginLocators.MEMBER_NAME)
        self.userNameElement = Element(self.browser, EHire51JobLoginLocators.USER_NAME)
        self.passwordElement = Element(self.browser, EHire51JobLoginLocators.PASSWORD)
        self.loginButtonElement = Element(self.browser, EHire51JobLoginLocators.LOGIN_BT)


class EHire51JobSearchWYPage(SearchPage):
    def __init__(self, browser, params, conditions):
        super(EHire51JobSearchWYPage, self).__init__(browser, params, conditions)
        self.readyElementLocator = EHire51JobSearchWYLocators.KEYWORDS

        self.source = u"WuyouSearch"

        self.searchMenuElement = Element(self.browser, EHire51JobSearchWYLocators.SEARCH_MENU)

        self.conditionKeyWordsElement = Element(self.browser, EHire51JobSearchWYLocators.KEYWORDS)
        self.searchButtonElement = Element(self.browser, EHire51JobSearchWYLocators.SEARCH_BUTTON)
        self.pagesNumElement = Element(self.browser, EHire51JobSearchWYLocators.PAGES_NUM)
        self.candidatesListElement = Element(self.browser, EHire51JobSearchWYLocators.CANDIDATES_LIST)
        self.nextPageElement = Element(self.browser, EHire51JobSearchWYLocators.NEXT_PAGE)

        self.logoutButtonElement = Element(self.browser, EHire51JobSearchWYLocators.LOGOUT_BT)

    def open(self):
        logger.info(u"Open search webpage ..")
        self.searchMenuElement.click()

    def get_total_pages_num(self):
        try:
            if self.pagesNumElement:
                pageNumSummary = self.pagesNumElement.element.text
                logger.debug(u"pageNumSummary: '{}'".format(pageNumSummary))
                self.resultsPageNum = int(str(pageNumSummary.split("/")[1]))
        except Exception:
            if logging.DEBUG == logger.level:
                logger.exception(u"Cannot find the total page, might be only one page!")
            else:
                logger.warning(u"Cannot find the total page, might be only one page!")

    def load_candidate_page(self):
        candidatePage = EHire51JobWYCandidatePage(self.browser, self.params)
        handles = self.browser.window_handles
        logger.debug(handles)
        self.browser.switch_to_window(handles[1])
        time.sleep(1)
        return candidatePage


class EHire51JobWYCandidatePage(CandidateInfoPage):
    def __init__(self, browser, params):
        super(EHire51JobWYCandidatePage, self).__init__(browser, params)
        self.readyElementLocator = EHire51JobCandidateWYLocators.ID

        self.recentUpdateDateElement = Element(self.browser, EHire51JobCandidateWYLocators.RESUME_UPDATE_DATE)
        self.idElement = Element(self.browser, EHire51JobCandidateWYLocators.ID)
        self.basicElement = Element(self.browser, EHire51JobCandidateWYLocators.BASIC_INFO)
        self.recentWorkYearsElement = Element(self.browser, EHire51JobCandidateWYLocators.RECENT_WORK_YEARS)
        self.recentWorkPositionElement = Element(self.browser, EHire51JobCandidateWYLocators.RECENT_WORK_POSITION)
        self.recentWorkCompanyElement = Element(self.browser, EHire51JobCandidateWYLocators.RECENT_WORK_COMPANY)
        self.educationElement = Element(self.browser, EHire51JobCandidateWYLocators.EDUCATION)
        self.educationSchoolElement = Element(self.browser, EHire51JobCandidateWYLocators.EDUCATION_SCHOOL)
        self.educationMajorElement = Element(self.browser, EHire51JobCandidateWYLocators.EDUCATION_MAJOR)
        self.additionalInfoTableElement = Element(self.browser, EHire51JobCandidateWYLocators.ADDITIONAL_INFO_TABLE)

        self.detailedInfo = {}

    def load_info(self):
        self.load_basic_info()
        if self.candidateInfo:
            self.load_additional_info()
        return self.candidateInfo

    def load_basic_info(self):
        try:
            self.candidateInfo.source = "51JobWYSearch"
            self.candidateInfo.id = self.idElement.element.text.replace(u"\"", "").replace(u"ID:", "").strip()
            self.load_summary_info()
            logger.debug(u"load_basic_info, CandidateInfo: {}".format(self.candidateInfo))
        except Exception:
            logger.exception(u"Load candidate basic information failure!")
            self.candidateInfo = None

    def load_summary_info(self):
        basicInfo = self.basicElement.element.text
        logger.debug(u"Basic summary info: {}".format(basicInfo))

        info = basicInfo.split(u"|")
        self.candidateInfo.gender = info[0].strip()
        self.candidateInfo.age = info[1].strip()
        self.candidateInfo.location = info[2].strip()
        self.candidateInfo.workYears = info[3].strip()

    def load_additional_info(self):
        try:
            self.load_details_info()
            self.fill_detailed_info()
            self.load_education_info()
            self.load_recent_info()
            logger.debug(u"load_additional_info, CandidateInfo: {}".format(self.candidateInfo))
        except Exception:
            logger.exception(u"Load candidate additional information failure!")

    def load_details_info(self):
        infoTables = self.additionalInfoTableElement.element
        tbodies = infoTables.find_elements(By.XPATH, './td/table/tbody')
        for tbody in tbodies:
            try:
                trs = tbody.find_elements(By.XPATH, './tr')
                if len(trs) >= 2:
                    self.detailedInfo[trs[0].text.strip()] = trs[1].text.strip()
            except Exception:
                logger.exception(u"parse tbody detailed information failure, skip it!")

        if logger.level == logging.DEBUG:
            logger.debug(u"parse detailed info: {}\n".format(len(self.detailedInfo)))
            for key, value in self.detailedInfo.items():
                logger.debug(u"<- {} ->\n{}\n".format(key, value))

    def fill_detailed_info(self):
        if u"求职意向" in self.detailedInfo:
            info = self.detailedInfo[u"求职意向"]
            for line in info.split(u"\n"):
                if u"期望薪资：" in line:
                    self.candidateInfo.expectedSalary = line.replace(u"期望薪资：", "").strip()
                elif u"地点：" in line:
                    self.candidateInfo.expectedLocation = line.replace(u"地点：", "").strip()
                elif u"职能/职位：" in line:
                    self.candidateInfo.expectedJob = line.replace(u"职能/职位：", "").strip()
                elif u"到岗时间：" in line:
                    self.candidateInfo.onboardDate = line.replace(u"到岗时间：", "").strip()
        if u"教育经历" in self.detailedInfo:
            self.candidateInfo.educationDetails = self.detailedInfo[u"教育经历"]
        if u"项目经验" in self.detailedInfo:
            self.candidateInfo.projectDetails = self.detailedInfo[u"项目经验"]
        if u"工作经验" in self.detailedInfo:
            self.candidateInfo.workDetails = self.detailedInfo[u"工作经验"]

        for key, value in self.detailedInfo.items():
            if u"技能特长" in key:
                self.candidateInfo.skills = self.detailedInfo[key]
            elif u"目前年收入" in key:
                self.candidateInfo.currentSalary = key.replace(u"目前年收入：", "").strip()

    def load_education_info(self):
        try:
            self.candidateInfo.education = self.educationElement.element.text
            self.candidateInfo.educationSchool = self.educationSchoolElement.element.text
            self.candidateInfo.educationMajor = self.educationMajorElement.element.text
            logger.debug(u"load_education_info, CandidateInfo: {}".format(self.candidateInfo))
        except Exception:
            logger.exception(u"load education info information failure!")

    def load_recent_info(self):
        try:
            self.candidateInfo.recentWorkYears = self.recentWorkYearsElement.element.text
            self.candidateInfo.recentWorkPosition = self.recentWorkPositionElement.element.text
            self.candidateInfo.recentWorkCompany = self.recentWorkCompanyElement.element.text
            self.candidateInfo.resumeUpdateTime = self.recentUpdateDateElement.element.text.replace(u"更新时间：", "").strip()
            logger.debug(u"load_recent_info, CandidateInfo: {}".format(self.candidateInfo))
        except Exception:
            logger.exception(u"load recent info information failure!")
