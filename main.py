import time
import os
import secret as secret
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

BASE_URL = "https://orangemethod.percipio.com/"
"TRACK -- https://orangemethod.percipio.com/track/14ac835a-65e0-4edd-9e6d-93f5a3f32dc0"
COURSE_URL = "https://orangemethod.percipio.com/courses/8757dc82-2a59-42aa-9618-6cb2e86a5a60/videos/4ca9ea0b-a3f0-41d6-825b-a61f929ba2ee"
SCREENSHOT_FOLDER_PATH = "D:/Codebase/automation/automate-percipio/screenshots"
course_folder = ""
driver = webdriver.Chrome()
# implicitly wait 10 seconds for each element to load
driver.implicitly_wait(30)


# setup chrome browser
def setup_browser():
    try:
        driver.maximize_window()
        print("success: setup_browser")
    except Exception as e:
        print(f"failure: setup_browser - {e}")


def open_percipio_url():
    try:
        driver.get(BASE_URL)
        print("success: open_percipio_url")
    except Exception as e:
        print(f"failure: open_percipio_url - {e}")


# login percipio
def click_sso_login_button():
    try:
        login_btn = driver.find_element(
            By.XPATH, '//*[@id="samlrenderer"]/div[2]/button'
        )
        login_btn.click()
        print("success: click_sso_login_button")
    except Exception as e:
        print(f"failure: click_sso_login_button - {e}")


# enter sso creds
def input_sso_creds():
    try:
        input_user = driver.find_element(By.XPATH, "//*[@id='inputUsername']")
        input_user.send_keys(secret.USERNAME)
        input_pass = driver.find_element(By.XPATH, "//*[@id='inputPassword']")
        input_pass.send_keys(secret.PASSWORD)
        signin_btn = driver.find_element(By.XPATH, "//*[@id='buttonSignOn']")
        signin_btn.click()
        time.sleep(2)
        print("success: input_sso_creds")
    except Exception as e:
        print(f"failure: input_sso_creds - {e}")


# navigate to journey page
def navigate_to_course_page():
    try:
        driver.get(COURSE_URL)
        print("success: navigate_to_course_page")
    except Exception as e:
        print(f"failure: navigate_to_course_page - {e}")


# click retake test
def select_take_test():
    try:
        # when on course panel page, try to click retake test panel, otherwise click take test panel instead
        try:
            take_test_pane = driver.find_element(
                By.XPATH,
                "//*[contains(text(), 'Take Test')]",
            )
            take_test_pane.click()
        except NoSuchElementException:
            retake_test_pane = driver.find_element(
                By.XPATH,
                '//*[@id="contentItem-17e15f8f-1ecd-41c3-a903-ea3394a304ac"]/a/div[2]/div[1]/span/span[1]/span',
            )
            retake_test_pane.click()

        # click retake test btn (will also click take test btn)
        take_test_btn = driver.find_element(
            By.XPATH,
            '//*[@id="maincontentid"]/div/div[3]/div[2]/div/div/div[2]/div[4]/div/div/div[1]/section/div[2]/a',
        )
        take_test_btn.click()
        time.sleep(4)
        print("success: select_take_test")

    except Exception as e:
        print(f"failure: select_take_test - {e}")


# start new test and take screen shots of answers
def start_test():
    try:
        # click start test button to commence test
        start_test = driver.find_element(
            By.XPATH,
            "//*[contains(text(), 'Start Test') or contains(text(), 'Start New Test')]",
        )
        start_test.click()

        # get course name text
        get_course_title = driver.find_element(
            By.XPATH,
            '//*[@id="maincontentid"]/div/div[2]/div[1]/div/div[1]/h1',
        )

        course_title_text = get_course_title.text
        print(f"COURSE NAME -- {course_title_text}")

        def mkdir_course(course_title_text):
            global course_folder
            parent_folder = os.path.abspath(SCREENSHOT_FOLDER_PATH)

            valid_course_name = "".join(
                c if c.isalnum() or c in (" ", "_") else "_" for c in course_title_text
            )

            course_folder = os.path.join(parent_folder, valid_course_name)
            if not os.path.exists(course_folder):
                os.makedirs(course_folder)

            return course_folder

        mkdir_course(course_title_text)

        take_test()

    except Exception as e:
        print(f"failure: start_test - {e}")


# function that selects checkbox multiple choice questions for course exam
def course_exam_answer_choice():
    try:
        exam_first_choice = driver.find_element(
            By.XPATH,
            "//*[contains(@class, 'Checkbox---checkboxContainer---2Hz1S Checkbox---spaced---1d8os')]",
        )
        exam_first_choice.click()

    except Exception as e:
        print(f"failure: course_exam_answer_choice - {e}")


# function that selects radio and checkbox multiple choice questions for final exam
def final_exam_answer_choice():
    QUESTION_RADIO_BUTTON = "//*[contains(@class, 'RadioButton---label---1dtPw RadioButton---spaced---aeCFF')]"

    QUESTION_CHECKBOX_BUTTON = "//*[contains(@class, 'Checkbox---checkboxContainer---2Hz1S Checkbox---spaced---1d8os')]"
    try:
        exam_first_choice = driver.find_element(
            By.XPATH,
            QUESTION_RADIO_BUTTON,
        )

        exam_first_choice.click()

    except NoSuchElementException:
        exam_first_choice = driver.find_element(
            By.XPATH,
            QUESTION_CHECKBOX_BUTTON,
        )
        exam_first_choice.click()
    finally:
        return


def submit_answer_btn():
    submit_answer_btn = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Submit Answer')]",
    )

    submit_answer_btn.click()


def take_screenshot(question_num):
    # save screenshot to course folder
    driver.save_screenshot(os.path.join(course_folder, f"answer{question_num}.png"))


def next_question_btn():
    # check if "next question" button or "done" button is available
    next_question_btn = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Next Question') or contains(text(), 'Done')]",
    )
    next_question_btn.click()


# execute multiple choice test and take screenshot
def take_test():
    # initalize the question number
    question_num = 0

    # run test logic as many times as there are questions. Applies to course tests and final exams.
    while True:
        try:
            question_num += 1
            # comment the function out which you don't need
            # course_exam_answer_choice()
            final_exam_answer_choice()
            # click and submit answer
            submit_answer_btn()
            time.sleep(2)
            take_screenshot(question_num)
            try:
                # after submitting answer, do the right/wrong one's appear. Take screenshot here
                # take_screenshot(question_num)
                # check if "next question" button or "done" button is available
                next_question_btn()

                print("success: next_question_btn")

            except Exception as e:
                print(f"failure: clicking next_question_btn - {e}")

        except Exception as e:
            print(f"failure: take_test - {e}")


# close browser
def close_browser():
    print("closing browser!")
    driver.quit()


def main():
    setup_browser()
    open_percipio_url()
    click_sso_login_button()
    input_sso_creds()
    navigate_to_course_page()
    select_take_test()
    start_test()
    close_browser()


if __name__ == "__main__":
    main()
