# flake8: noqa
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import test_data as td
import locators
import secret
import time

# globals
course_folder = ""
COURSE_ID = td.JourneyTestData.ENTERPRISE_TO_SOFTWARE_DEV
TRACK_LINK = "Track 1: Enterprise Developer"

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
def open_journey():
    name = open_journey.__name__
    base_url = td.TestData.BASE_URL
    id = COURSE_ID
    try:
        journey_url = base_url + "journey/" + id
        print("journey_url", journey_url)

        # wait for page to load
        WebDriverWait(driver, 10).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

        # get journey url
        driver.get(journey_url)
        print(f"success: {name}")
    except Exception as e:
        print(f"failure: {name} - {e}")


# open new track from current journey url page
def open_tracks():
    try:
        # wait for track link to be present in the the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, TRACK_LINK))
        )

        # find valid track link from journey apge
        link = driver.find_element(By.LINK_TEXT, TRACK_LINK)
        time.sleep(2)

        # click track link
        link.click()

        # start most recent course test from track page
        def start_course_test_from_track_page():
            # Get the total height of the page
            total_height = driver.execute_script("return document.body.scrollHeight;")
            # increase the height to ensure it reaches the bottom
            height_multiplier = 3
            print("total height of page:", total_height)
            total_height = total_height * height_multiplier

            # Scroll down slowly
            for i in range(
                0, total_height, 5
            ):  # Here, 5 is the scroll step. Adjust as necessary.
                driver.execute_script(f"window.scrollTo(0, {i});")
                time.sleep(0.01)  # Adjust sleep time as necessary

            time.sleep(1)  # Give some time before scrolling back up

            # Scroll back up slowly
            for i in range(total_height, 0, -5):
                driver.execute_script(f"window.scrollTo(0, {i});")
                # time.sleep(0.01)  # Adjust sleep time as necessary

            time.sleep(2)

            # find list of courses to take
            find_tests = driver.find_elements(
                By.XPATH,
                "//*[contains(text(), 'Take test')]",
            )

            time.sleep(2)

            print("list of all tests found to take: ", len(find_tests))

            # click most recent course test
            find_tests[0].click()

            time.sleep(2)

        start_course_test_from_track_page()

    except Exception as e:
        print(f"An error occurred: {e}")


# scroll to bottom of page
def scroll_to_bottom_then_top(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")


# major function: start new test of mc questions, and take screenshots of answers
def start_mc_test():
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

        take_mc_test_loop()
        print("success")

    except Exception as e:
        print("failed", e)

    # go back to track page to conduct a new test


QUESTION_RADIO_BUTTON = (
    "//*[contains(@class, 'RadioButton---label---1dtPw RadioButton---spaced---aeCFF')]"
)
QUESTION_CHECKBOX_BUTTON = "//*[contains(@class, 'Checkbox---checkboxContainer---2Hz1S Checkbox---spaced---1d8os')]"


def select_exam_choice():
    """Selects radio or checkbox answers."""
    try:
        radio_buttons = driver.find_elements(By.XPATH, QUESTION_RADIO_BUTTON)

        if radio_buttons:
            radio_buttons[0].click()
            return

        checkboxes = driver.find_elements(By.XPATH, QUESTION_CHECKBOX_BUTTON)
        if checkboxes:
            checkboxes[0].click()
            return

        print("No radio or checkbox button is found!")
    except Exception as e:
        print("Failed to select choice:", e)


def submit_answer():
    """Submits an answer."""
    try:
        submit_btn = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Submit Answer')]"
        )
        submit_btn.click()
    except Exception as e:
        print("Failed to submit answer:", e)


def take_screenshot(question_num):
    """Takes a screenshot and saves it."""
    try:
        driver.save_screenshot(os.path.join(course_folder, f"answer{question_num}.png"))
    except Exception as e:
        print("Failed to take screenshot:", e)


def click_next_or_done(question_num):
    """Clicks on the 'Next Question' or 'Done' button."""
    try:
        next_btn = driver.find_element(
            By.XPATH, "//*[contains(text(), 'Next Question')]"
        )
        next_btn.click()
        print(f"Success: clicked next_question_btn {question_num}")
    except Exception as no_next_btn_e:
        try:
            done_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Done')]")
            done_btn.click()
            print("Exam is done")
        except Exception as no_done_btn_e:
            print(
                f"Failed to click next or done button: {no_next_btn_e} - {no_done_btn_e}"
            )
            return False
    return True


# complete multiple choice test and take screenshot
def take_mc_test_loop():
    """Main loop for taking the test."""
    question_num = 0

    while True:
        try:
            question_num += 1
            select_exam_choice()
            submit_answer()
            time.sleep(2)
            take_screenshot(question_num)

            if not click_next_or_done(question_num):
                break

        except Exception as e:
            print(f"Failed in take_test:", e)
            break

    close_browser()


# close browser
def close_browser():
    print("closing browser!")
    driver.close()


# run main exam taker function
def run_exam_taker():
    open_percipio()
    click_login_btn()
    input_sso_creds()
    open_journey()
    open_tracks()
    start_mc_test()
    # close_browser()
    time.sleep(3)


if __name__ == "__main__":
    run_exam_taker()
