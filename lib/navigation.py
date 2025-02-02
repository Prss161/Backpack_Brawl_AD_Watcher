import time
from appium.webdriver.common.appiumby import AppiumBy


def find_and_click(driver, timeout=10):
    end_time = time.time() + timeout
    ad_cases = get_ad_cases()
    while time.time() < end_time:
        for by, locators in ad_cases.items():
            for locator in locators:
                try:
                    print(f"Trying to find element: [{by}] {locator}")
                    element = driver.find_element(
                        getattr(AppiumBy, by.upper()), locator
                    )
                    if element.is_displayed():
                        element.click()
                        print(f"Clicked element with locator: [{by}] {locator}")
                        return True
                except:
                    time.sleep(0.5)
            google_play = driver.find_element(
                AppiumBy.XPATH,
                '//android.view.View[@content-desc="Search Google Play"]',
            )
            if google_play.is_displayed():
                driver.press_keycode(4)

    print(f"Failed to find and click any element: [{by}] {locator}")
    return False


def get_ad_cases():
    return {
        "xpath": [
            '//android.widget.ImageButton[@content-desc="Close"]',
            '//android.view.View[@resource-id="skipPlayableButton"]/android.view.View/android.view.View/android.widget.Image',
            '//android.view.View[@resource-id="skipPlayableButton"]'
            '//android.view.View[@resource-id="closeButton"]/android.view.View/android.view.View/android.widget.Image',
            '//android.view.View[@resource-id="skipButton"]/android.widget.TextView',
            '//android.view.View[@resource-id="storePromoContainer"]/android.view.View/android.widget.Image[1]',
            '//android.widget.TextView[@text=""]',
            '//android.widget.Button[@text="Close"]',
            # "//android.widget.Button", # This is bugged
            "//android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[2]/android.view.View[2]",
            '//android.view.View[@resource-id="end-screen-adapter"]/android.view.View[1]/android.widget.Image',
            '//android.widget.Image[@text="close"]',
            '//android.widget.Button[@resource-id="next-button"]',
        ],
        "id": [
            "closeButton",
            "com.rapidfiregames.backpackbrawl:id/ia_iv_close_button",
            "Close",
            "skipPlayableButton",
        ],
        # "tag name": ["button"],
    }
