from selenium.webdriver.common.by import By


class EHire51JobLoginLocators(object):
    MEMBER_NAME = (By.NAME, "txtMemberNameCN")
    USER_NAME = (By.NAME, "txtUserNameCN")
    PASSWORD = (By.NAME, "txtPasswordCN")
    LOGIN_BT = (By.NAME, "Login_btnLoginCN")


class EHire51JobSearchWYLocators(object):
    LOGOUT_BT = (By.ID, "MainMenuNew1_hl_LogOut")

    SEARCH_MENU = (By.ID, "MainMenuNew1_m3")

    KEYWORDS = (By.ID, "search_keyword_txt")
    SEARCH_BUTTON = (By.CLASS_NAME, "search-people-btn")
    PAGES_NUM = (By.XPATH, '//*[@id="form1"]/div[3]/div/div[7]/div[2]/ul/li[2]/span')
    CANDIDATES_LIST = (By.CLASS_NAME, "position-list-asd")
    NEXT_PAGE = (By.ID, "pagerBottomNew_nextButton")


class EHire51JobCandidateWYLocators(object):
    RESUME_UPDATE_DATE = (By.ID, "lblResumeUpdateTime")
    ID = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[1]/span')

    BASIC_INFO = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[1]')

    RECENT_WORK_YEARS = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]')
    RECENT_WORK_POSITION = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]')
    RECENT_WORK_COMPANY = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]')

    EDUCATION = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]')
    EDUCATION_SCHOOL = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[3]/td[2]')
    EDUCATION_MAJOR = (By.XPATH, '//*[@id="divResume"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]')

    ADDITIONAL_INFO_TABLE = (By.ID, 'divInfo')
