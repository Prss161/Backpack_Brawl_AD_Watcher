from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from appium.options.android import UiAutomator2Options
from lib.navigation import find_and_click, TimeoutException
import time

appium_service = AppiumService()

options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "127.0.0.1:5555"

MAX_RETRIES = 3


def main():
    try:
        appium_service.start()
        print("✅ Appium server started!")
        launch_app(99)
    except Exception as e:
        print(f"🚨 Fatal error: {e}")
    finally:
        appium_service.stop()
        print("🛑 Appium server stopped.")


def launch_app(ads: int):
    ad = 0
    driver = None
    repeat = False
    try:
        driver = webdriver.Remote("http://localhost:4723", options=options)
        window_size = driver.get_window_size()
        window_x = window_size["width"]
        window_y = window_size["height"]
        if window_x != 720 or window_y != 1280:
            print(
                f"📱 Your screen size is: {window_x}, {window_y}. Recommended screen resolution is 720x1280"
            )
        print(f"📱 Screen size is: {window_x}, {window_y}")

        driver.tap([(window_x / 5, window_y / 1.01)])
        time.sleep(1)
        driver.swipe(window_x / 2, window_y * 0.1, window_x / 2, window_y / 1.1, 300)
        time.sleep(1)
        driver.swipe(window_x / 2, window_y / 1.1, window_x / 2, window_y / 3, 600)
        time.sleep(3)
        consecutive_failures = 0

        while ad < ads:
            if consecutive_failures >= MAX_RETRIES:
                print("❌ Too many consecutive failures. Exiting.")
                break

            if not repeat:
                driver = webdriver.Remote("http://localhost:4723", options=options)
                driver.tap([(window_x / 2, window_y / 2)])
                time.sleep(45)
            find_and_click(driver)
            game_view = driver.find_element(
                "xpath", '//android.view.View[@content-desc="Game view"]'
            )
            if game_view.is_displayed():
                ad += 1
                wait_time = 1800
                end_time = time.time() + wait_time
                while time.time() < end_time:
                    remaining_time = end_time - time.time()
                    minutes, seconds = divmod(remaining_time, 60)
                    print(
                        f"Ad {ad}/{ads} completed ✅. Waiting for the next ad. Time left: {int(minutes)}:{int(seconds):02d}",
                        end="\r",
                    )
                    time.sleep(1)
            else:
                print("⚠️ Game view not visible, retrying...")
                repeat = True
                consecutive_failures += 1

    finally:
        if driver:
            driver.quit()
            print("🚪 Driver closed.")


main()
