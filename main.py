from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from appium.options.android import UiAutomator2Options
from lib.navigation import find_and_click
import time

appium_service = AppiumService()

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "127.0.0.1:5555"


def main():
    try:
        appium_service.start()
        print("Appium server started!")
        launch_app(99)
    except Exception as e:
        print(f"Error Message: {e}")
    finally:
        appium_service.stop()


def launch_app(ads: int):
    ad = 0
    driver = webdriver.Remote("http://localhost:4723", options=options)
    repeat = False
    window_size = driver.get_window_size()
    window_x = window_size["width"]
    window_y = window_size["height"]
    print(f"{window_x}, {window_y}")
    driver.tap([(window_x / 5, window_y / 1.01)])
    driver.swipe(window_x / 2, window_y / 1.1, window_x / 2, window_y / 3, 550)
    time.sleep(5)
    while ad < ads:
        try:
            if repeat == False:
                driver = webdriver.Remote("http://localhost:4723", options=options)
                driver.tap([(window_x / 2, window_y / 2)])
                time.sleep(30)
            find_and_click(driver)
            game_view = driver.find_element(
                "xpath", '//android.view.View[@content-desc="Game view"]'
            )
            if game_view.is_displayed():
                ad += 1
                repeat = False
                print(f"Ad {ad}/{ads} completed. Waiting for the next ad...")
                driver.quit()
                time.sleep(1800)
            else:
                print("Game view not visible. Repeating process...")
                repeat = True

        except Exception as e:
            print(f"Error during ad handling: {e}")
            repeat = True


main()
