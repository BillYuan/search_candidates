# -*- coding: UTF-8 -*-


class CandidateInfo(object):
    RESUME_UPDATE = u"简历更新时间"
    ID = u"ID"
    GENDER = u"性别"
    AGE = u"年龄"
    LOCATION = u"居住地"
    WORK_YEARS = u"总工作年限"

    RECENT_WORK_YEARS = u"最近工作年限"
    RECENT_WORK_POSITION = u"最近工作职位"
    RECENT_WORK_COMPANY = u"最近工作公司"

    EDUCATION = u"最高学历"
    EDUCATION_SCHOOL = u"学校"
    EDUCATION_MAJOR = u"专业"

    SKILLS = u"技能特长"

    CURRENT_SALARY = u"目前收入"
    EXPECTED_SALARY = u"期望薪酬"
    EXPECTED_LOCATION = u"期望工作地"
    EXPECTED_JOB = u"期望职位"
    ONBOARD_DATE = u"到岗时间"

    EDUCATION_DETAILS = u"教育经历"
    PROJECTS_DETAILS = u"项目经验"
    WORK_DETAILS = u"工作经验"

    SOURCE = u"来源"

    def __init__(self, params):
        self.params = params

        self.resumeUpdateTime = ""
        self.id = ""
        self.gender = ""
        self.age = ""
        self.location = ""
        self.workYears = ""

        self.recentWorkYears = ""
        self.recentWorkPosition = ""
        self.recentWorkCompany = ""

        self.education = ""
        self.educationSchool = ""
        self.educationMajor = ""

        self.skills = ""

        self.currentSalary = ""
        self.expectedSalary = ""
        self.expectedLocation = ""
        self.expectedJob = ""

        self.onboardDate = ""

        self.educationDetails = ""
        self.projectDetails = ""
        self.workDetails = ""

        self.source = ""

    def export_hash(self):
        info = {self.RESUME_UPDATE: self.resumeUpdateTime, self.ID: self.id, self.GENDER: self.gender,
                self.AGE: self.age, self.LOCATION: self.location, self.WORK_YEARS: self.workYears,
                self.RECENT_WORK_YEARS: self.workYears, self.RECENT_WORK_POSITION: self.recentWorkPosition,
                self.RECENT_WORK_COMPANY: self.recentWorkCompany, self.EDUCATION: self.education,
                self.EDUCATION_SCHOOL: self.educationSchool, self.EDUCATION_MAJOR: self.educationMajor,
                self.SKILLS: self.skills, self.CURRENT_SALARY: self.currentSalary,
                self.EXPECTED_SALARY: self.expectedSalary, self.EXPECTED_LOCATION: self.expectedLocation,
                self.ONBOARD_DATE: self.onboardDate, self.SOURCE: self.source,
                self.EDUCATION_DETAILS: self.educationDetails, self.PROJECTS_DETAILS: self.projectDetails,
                self.WORK_DETAILS: self.workDetails}
        return info
