import argparse
import logging
import json
import io
import os
import time
from selenium import webdriver

from web51job.ehire51job_pages import EHire51JobLoginPage, EHire51JobSearchWYPage
from candidate.candidate_info import CandidateInfo
from excel.excelparser import ExcelParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(u"sr")
logger.setLevel(logging.INFO)


class SearchResumes(object):
    EXPORT_EXCEL_COLUMNS = [CandidateInfo.ID, CandidateInfo.GENDER,
                            CandidateInfo.AGE, CandidateInfo.LOCATION, CandidateInfo.WORK_YEARS,
                            CandidateInfo.RECENT_WORK_YEARS, CandidateInfo.RECENT_WORK_POSITION,
                            CandidateInfo.RECENT_WORK_COMPANY, CandidateInfo.EDUCATION,
                            CandidateInfo.EDUCATION_SCHOOL, CandidateInfo.EDUCATION_MAJOR,
                            CandidateInfo.SKILLS, CandidateInfo.CURRENT_SALARY,
                            CandidateInfo.EXPECTED_SALARY, CandidateInfo.EXPECTED_LOCATION,
                            CandidateInfo.ONBOARD_DATE, CandidateInfo.RESUME_UPDATE, CandidateInfo.SOURCE]

    def __init__(self):
        self.inputParameters = None
        self.browser = None
        self.mainWeb51Job = None
        self.loginSucceed = False
        self.args = None

    def process_args(self):
        parser = argparse.ArgumentParser(description="Search and dump resumes information from website")
        parser.add_argument(u"-j", "--json", action="store", dest="json", required=True,
                            help="Specify the input arguments to search resumes, see 'input.json' as an example")
        parser.add_argument(u"-d", "--details", action="store_true", dest="details", required=False,
                            help="Parse and save more experience details into output excel.")
        parser.add_argument(u"-v", "--verbose", action="store", dest="verbose",
                            help="verbose log mode, 'debug', 'fatal', 'error', 'warning', 'info'")

        self.args = parser.parse_args()
        if self.args.verbose:
            v = self.args.verbose.lower()
            if "debug" == v:
                logger.setLevel(logging.DEBUG)
            elif "fatal" == v:
                logger.setLevel(logging.FATAL)
            elif "error" == v:
                logger.setLevel(logging.ERROR)
            elif "warning" == v:
                logger.setLevel(logging.WARNING)
            elif "info" == v:
                logger.setLevel(logging.INFO)

        try:
            with io.open(self.args.json, encoding='utf-8') as jsonFile:
                self.inputParameters = json.loads(jsonFile.read())

            if "webMain" not in self.inputParameters:
                logger.info(u"Please specify the 'webMain' in 'input.json' to start the website!")
                exit(1)
            if "searchConditions" not in self.inputParameters:
                logger.info(u"Please specify the 'searchConditions' in 'input.json' to search candidates!")
                exit(1)
            for searchCondition in self.inputParameters["searchConditions"]:
                if "profileName" not in searchCondition:
                    logger.info(u"Please specify the 'profileName' in 'input.json' to save an excel!")
                    exit(1)
                if "keyWords" not in searchCondition:
                    logger.info(u"Please specify the 'keyWords' in 'input.json' to search candidates!")
                    exit(1)
        except Exception:
            logger.exception(u"Cannot load '{}', please check the json format!".format(self.args.json))
            exit(1)

    def execute(self):
        searchPage = None
        try:
            self.browser = webdriver.Firefox()
            self.browser.maximize_window()

            self.mainWeb51Job = EHire51JobLoginPage(self.browser, self.inputParameters)
            self.mainWeb51Job.open()

            if self.mainWeb51Job.is_ready():
                self.loginSucceed = self.mainWeb51Job.login()

            if self.loginSucceed:
                searchConditions = self.inputParameters["searchConditions"]
                for conditions in searchConditions:
                    searchPage = EHire51JobSearchWYPage(self.browser, self.inputParameters, conditions)
                    searchPage.open()
                    searchPage.search()
                    candidates = searchPage.load_candidates()
                    if candidates:
                        excelData = self.prepare_excel_data(candidates)
                        currentPath = os.path.dirname(os.path.abspath(__file__))
                        path = os.path.join(currentPath, conditions["profileName"]+".xlsx").replace(u"\\", "/")
                        excel = ExcelParser(path, mode=ExcelParser.MODE_WRITE, excelData=excelData)
                        excel.export()

                    if logging.DEBUG == logger.level:
                        break
        finally:
            if self.loginSucceed and searchPage:
                searchPage.logout()

            if self.browser:
                time.sleep(2)
                self.browser.quit()

    def prepare_excel_data(self, candidates):
        excelTables = []
        columns = self.EXPORT_EXCEL_COLUMNS
        if self.args.details:
            columns.append(CandidateInfo.EDUCATION_DETAILS)
            columns.append(CandidateInfo.PROJECTS_DETAILS)
            columns.append(CandidateInfo.WORK_DETAILS)
        excelTableData = {ExcelParser.Sheet.NAME: "51jobExport", ExcelParser.Sheet.HEADER: columns}
        listHashData = []
        for candidate in candidates:
            listHashData.append(candidate.export_hash())
        logger.debug(u"listHashData size: {}".format(len(listHashData)))
        excelTableData[ExcelParser.Sheet.DATA] = listHashData
        excelTables.append(excelTableData)
        return excelTables


sr = SearchResumes()
sr.process_args()
sr.execute()
