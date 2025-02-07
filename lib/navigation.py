import time
from appium.webdriver.common.appiumby import AppiumBy


class TimeoutException(Exception):
    pass


def find_and_click(driver, debug=None, timeout=180):
    end_time = time.time() + timeout
    ad_cases = get_ad_cases()

    while time.time() < end_time:
        remaining_time = end_time - time.time()
        print(f"Time remaining (To Abort): {remaining_time:.2f}")

        for by, locators in ad_cases.items():
            for locator in locators:
                try:
                    if debug:
                        print(f"🔍 Trying to find element: [{by}] {locator}")

                    if by == "google_play":
                        google_play = driver.find_elements(AppiumBy.XPATH, locator)
                        if google_play and google_play[0].is_displayed():
                            driver.press_keycode(4)
                            print(
                                "🔙 Google Play search detected, pressing back button."
                            )

                    elif by == "game_view":
                        game_view = driver.find_elements(AppiumBy.XPATH, locator)
                        if game_view and game_view[0].is_displayed():
                            print("✅ Detected game view panel. Ad watching completed.")
                            return True

                    else:
                        time.sleep(0.5)
                        elements = driver.find_elements(
                            getattr(AppiumBy, by.upper()), locator
                        )
                        if elements and elements[0].is_displayed():
                            elements[0].click()
                            print(f"✅ Clicked element with locator: [{by}] {locator}")
                except Exception as e:
                    print(f"⚠️ Error: {e}")

    print("⏳ Timeout reached, exiting function.")
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
            '//android.widget.ImageView[@resource-id="com.rapidfiregames.backpackbrawl:id/ia_iv_close_button"]',
            '//android.widget.Image[@text="close"]',
            '//android.widget.Button[@resource-id="next-button"]',
            '//android.widget.Image[@resource-id="closeBtnImg"]',
        ],
        "id": [
            "closeButton",
            "com.rapidfiregames.backpackbrawl:id/ia_iv_close_button",
            "Close",
            "skipPlayableButton",
        ],
        "google_play": ['//android.view.View[@content-desc="Search Google Play"]'],
        "game_view": ['//android.view.View[@content-desc="Game view"]'],
        # "tag name": ["button"],
    }
