import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import test_data as td
import locators
import secret
import time

# globals
course_folder = ""

# setup chrome options and chrome driver manager
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# setup webdriver
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(15)


# start browser
def open_percipio():
    driver.get(td.TestData.BASE_URL)


# start login
def click_login_btn():
    name = click_login_btn.__name__
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locators.LoginPageLocators.LOGIN_BTN)
        ).click()
        print(f"success: {name}")
    except Exception as e:
        print(f"failure: {name} - {e}")


# input sso username and password, then click signin button
def input_sso_creds():
    name = input_sso_creds.__name__
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(locators.SSOPageLocators.SIGNIN_BTN)
        )

        input_user = driver.find_element(*locators.SSOPageLocators.USERNAME)
        input_pass = driver.find_element(*locators.SSOPageLocators.PASSWORD)
        signin_btn = driver.find_element(*locators.SSOPageLocators.SIGNIN_BTN)
        input_user.send_keys(secret.USERNAME)
        input_pass.send_keys(secret.PASSWORD)
        signin_btn.click()
        time.sleep(3)

        print(f"success: {name}")
    except Exception as e:
        print(f"failure: {name} - {e}")


# open journey. Only need if scanning tracks that are complete/incomplete. FUTURE TO-DO. For now, commented out.
# def open_journey():
#     name = open_journey.__name__
#     base_url = td.TestData.BASE_URL
#     id = td.JourneyTestData.AUTOMATED_TESTING_WITH_SELENIUM
#     try:
#         journey_url = base_url + "journey/" + id
#         print("journey_url", journey_url)
#         driver.get(journey_url)
#         print(f"success: {name}")
#     except Exception as e:
#         print(f"failure: {name} - {e}")


def open_course():
    name = open_course.__name__
    base_url = td.TestData.BASE_URL
    id = td.CourseTestData.STTDAT_COURSE1
    try:
        course_url = base_url + "courses/" + id
        print("course_url", course_url)
        driver.get(course_url)
        time.sleep(10)
        print(f"success: {name}")
    except Exception as e:
        print(f"failure: {name} - {e}")


# when on course panel page, try to click retake test panel, otherwise click take test panel instead
def select_take_test_pane():
    name = select_take_test_pane.__name__
    try:
        take_test_pane = driver.find_element(
            *locators.CoursePageLocators.TAKE_TEST_PANE
        )
        take_test_pane.click()
        print(f"success: {name}")
    except NoSuchElementException as e:
        retake_test_pane = driver.find_element(
            *locators.CoursePageLocators.RETAKE_TEST_PANE
        )
        retake_test_pane.click()
        print(f"failure: {name} - {e}")


# major function: start new test of mc questions, and take screenshots of answers
def start_test():
    try:
        # start test
        start_test = driver.find_element(*locators.ExamPageLocators.START_EXAM)
        start_test.click()

        # get text of course name
        get_course_title = driver.find_element(*locators.ExamPageLocators.COURSE_TITLE)
        course_title_text = get_course_title.text
        print(f"COURSE NAME -- {course_title_text}")

        # create directory of course to store screen caps
        def mkdir_course(course_title_text):
            global course_folder
            parent_folder = os.path.abspath(td.TestData.SCREENSHOT_FOLDER_PATH)

            valid_course_name = "".join(
                c if c.isalnum() or c in (" ", "_") else "_" for c in course_title_text
            )

            course_folder = os.path.join(parent_folder, valid_course_name)
            if not os.path.exists(course_folder):
                os.makedirs(course_folder)

            return course_folder

        mkdir_course(course_title_text)

        take_test_loop()
        print("success")

    except Exception as e:
        print("failed", e)
        # print(f"failure: {name} - {e}")


# complete multiple choice test and take screenshot
def take_test_loop():
    # initalize the question number
    question_num = 0

    # run test logic as many times as there are questions. Applies to course tests and final exams.
    while True:
        try:
            question_num += 1

            # function that selects radio and checkbox multiple choice questions for final exam
            def exam_choice_answer():
                try:
                    QUESTION_RADIO_BUTTON = "//*[contains(@class, 'RadioButton---label---1dtPw RadioButton---spaced---aeCFF')]"

                    QUESTION_CHECKBOX_BUTTON = "//*[contains(@class, 'Checkbox---checkboxContainer---2Hz1S Checkbox---spaced---1d8os')]"

                    # find radio button
                    radio_buttons = driver.find_elements(
                        By.XPATH, QUESTION_RADIO_BUTTON
                    )

                    if len(radio_buttons) > 0:  # if radio button found
                        print("radio buttons", radio_buttons)
                        radio_buttons[0].click()
                    else:  # if radio buttons not found, look for checkboxes
                        checkboxes = driver.find_elements(
                            By.XPATH, QUESTION_CHECKBOX_BUTTON
                        )

                        if len(checkboxes) > 0:
                            print("checkboxes", checkboxes)
                            checkboxes[0].click()
                        else:
                            print("No radio button or checkbox button is found!")
                except Exception as e:
                    print("failure", e)

            exam_choice_answer()

            # click and submit answer
            def submit_answer_btn():
                submit_answer_btn = driver.find_element(
                    By.XPATH,
                    "//*[contains(text(), 'Submit Answer')]",
                )

                submit_answer_btn.click()

            submit_answer_btn()
            time.sleep(2)

            # take screenshot
            def take_screenshot(question_num):
                # save screenshot to course folder
                driver.save_screenshot(
                    os.path.join(course_folder, f"answer{question_num}.png")
                )

            take_screenshot(question_num)

            try:

                def next_question_btn():
                    # check if "next question" button or "done" button is available
                    next_question_btn = driver.find_element(
                        By.XPATH,
                        "//*[contains(text(), 'Next Question') or contains(text(), 'Done')]",
                    )
                    next_question_btn.click()

                next_question_btn()

                print("success: next_question_btn")

            except Exception as e:
                print(f"failure: clicking next_question_btn - {e}")

        except Exception as e:
            print(f"failure: take_test - {e}")


# close browser
def close_browser(self):
    print("closing browser!")
    self.driver.close()


# run main exam taker function
def run_exam_taker():
    open_percipio()
    click_login_btn()
    input_sso_creds()
    # open_journey() -- Future implementation. Created
    # open_track() -- Future implementation. NOT created
    open_course()
    select_take_test_pane()
    start_test()
    close_browser()
    time.sleep(3)


if __name__ == "__main__":
    run_exam_taker()
