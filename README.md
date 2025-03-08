# Backpack Brawl AD Watcher

This program automatically watches ads on the Backpack Brawl mobile app.

The project utilizes Python for scripting and automating the process of watching ads for you. It uses Appium for Android automation, leveraging XPATH for navigation through ads and the app menu. For further optimization, screenshots of ads are taken to classify "close" and "skip" buttons using labelimg. This data is then used with OpenCV and PyTorch to create a model for object recognition of the close and skip buttons in ads.

## First Steps

### Install Required Python Packages

Install the required Python packages using the following command:

```sh
pip install -r requirements.txt
```

### Install Appium

Install Appium globally using npm:

```sh
npm install -g appium
```

### Setup Bluestacks

1. Install Bluestacks.
2. Enable ADB in Bluestacks.
3. Set the resolution to `1280x720`.

## How to Use

1. Open Backpack Brawl via Bluestacks and navigate to the main menu.
2. Run the following command to start the script:

```sh
python .\main.py
```

> [!NOTE]  
> Program is still under development and may not work perfectly. If you face issues, please open an issue thread.
