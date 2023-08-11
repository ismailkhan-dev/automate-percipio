from selenium.webdriver.common.by import By

"""
Locators are separated by page name.
"""


class LoginPageLocators:
    LOGIN_BTN = (By.XPATH, "//*[@id='samlrenderer']/div[2]/button")


class SSOPageLocators(object):
    USERNAME = (By.XPATH, "//*[@id='inputUsername']")
    PASSWORD = (By.XPATH, "//*[@id='inputPassword']")
    SIGNIN_BTN = (By.XPATH, "//*[@id='buttonSignOn']")


class CoursePageLocators(object):
    TAKE_TEST_PANE = (By.XPATH, "//*[contains(text(), 'Take Test')]")
    RETAKE_TEST_PANE = (By.XPATH, "//*[contains(text(), 'Retake Test')]")
    TAKE_TEST_BTN = (
        By.XPATH,
        "//*[@id='maincontentid']/div/div[3]/div[2]/div/div/div[2]/div[4]/div/div/div[1]/section/div[2]/a",
    )


class ExamPageLocators(object):
    START_EXAM = (
        By.XPATH,
        "//*[contains(text(), 'Start Test') or contains(text(), 'Start New Test')]",
    )
    COURSE_TITLE = (
        By.XPATH,
        '//*[@id="maincontentid"]/div/div[2]/div[1]/div/div[1]/h1',
    )
