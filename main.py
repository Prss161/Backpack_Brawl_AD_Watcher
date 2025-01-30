from appium.webdriver.appium_service import AppiumService
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.android import UiAutomator2Options
import time

appium_service = AppiumService()
options = UiAutomator2Options()
options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "127.0.0.1:5555"  # Replace with your emulator/device ID

def main():
    try:
        appium_service.start()
        print("Appium server started!")

        launch_app(10)
    except Exception as e:
        print(f"Error Message: {e}")        
    finally:
        appium_service.stop()
        
def find_and_click(driver, by: By, locator: str, timeout=10):
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            element = driver.find_element(by, locator)
            if element.is_displayed():
                element.click()
                print(f"Clicked element with locator: {locator}")
                return True
        except:
            time.sleep(0.5)
    print(f"Element not found: {locator}")
    return False

def launch_app(ads: int):
    driver = webdriver.Remote('http://localhost:4723', options=options)
    
    # driver.tap([(165, 1530)])
    # driver.swipe(450, 1450, 450, 300, 500)
    # time.sleep(5)
    ad = 0
    repeat = False
    while ad < ads:
        if repeat == False:
            driver.tap([(450, 260)])
            time.sleep(45)
        find_and_click(driver, By.XPATH, '//android.widget.ImageButton[@content-desc="Close"]')
        find_and_click(driver, By.XPATH, '//android.view.View[@resource-id="skipPlayableButton"]/android.view.View/android.view.View/android.widget.Image')
        find_and_click(driver, By.XPATH, '//android.view.View[@resource-id="closeButton"]/android.view.View/android.view.View/android.widget.Image')
        find_and_click(driver, By.XPATH, '//android.view.View[@resource-id="skipButton"]/android.widget.TextView')
        find_and_click(driver, By.XPATH, '//android.view.View[@resource-id="storePromoContainer"]/android.view.View/android.widget.Image[1]')
        find_and_click(driver, By.XPATH, '//android.widget.ImageView[@resource-id="com.rapidfiregames.backpackbrawl:id/ia_iv_close_button"]')
        find_and_click(driver, By.XPATH, '//android.widget.TextView[@text=""]')
        find_and_click(driver, By.XPATH, '//android.widget.Button[@text="Close"]')
        find_and_click(driver, By.TAG_NAME, 'button')
        find_and_click(driver, By.CLASS_NAME, 'android.widget.Button')
        game_view = driver.find_element(By.XPATH, '//android.view.View[@content-desc="Game view"]')
        if game_view.is_displayed():
            ad += 1
            repeat = False
            print("Waiting for next ad")
            time.sleep(1805)
        else:
            print("Didn't find any element to close ad, repeating process")
            repeat = True
            continue

main()
