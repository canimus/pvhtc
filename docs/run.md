# Run

Considering that you successfully build the container, as explained in the previous section, the next step consists in simply running the container.
The only requirement for the container is to map an external volume from the host, where the test script is located, as explained in the command below:

``` sh
# Execution with needed volume
docker run -it --rm -v $PWD/src:/scripts pvhtcpy
```

## Steps

The following section describes the code that covers the main test scenario. The 4 steps described, enclose the test steps of the scenario of the challenge.

???- example "Test Scenario"

    === "s1: Email"

        This step visits a website that produces valid email addresses and is able to capture received emails to that account.

        ``` python
        driver = webdriver.Chrome(options=set_chrome_options())
        driver.get("https://emailfake.com/")
        print('EmailGenerator:' + driver.title)

        # Email is imaged as a pair of inputs
        inputs = driver.find_elements_by_tag_name("input")

        ocr = {'email' : 0, 'domain' : 2}
        list(map(lambda x: mc("screenshot", f'/scripts/{x[0]}.png')(inputs[x[1]]), ocr.items()))
        
        email, domain = [pytesseract.image_to_string(
            Image.open(f'/scripts/{i}.png')).strip() for i in ocr.keys()]

        print(f'Email:[{email}] Check=>{len(email)>0}')
        print(f'Domain:[{domain}] Check=>{len(domain)>0}')

        if len(email)>0 and len(domain)>0:
            print(chalk.cyan("Email Ok"))
        else:
            print(chalk.red("Sorry, my eyes are tired and couldn't parse your email"))
            sys.exit()

        # Induced garbage caracter in domain by image
        if ((not domain[0].isalnum()) or (domain[0].isupper())):
            domain = domain[1:]


        email_address = f'{email}@{domain}'
        print(chalk.magenta(email_address, bold=True))
        ```

        __Output__:
        ```
        EmailGenerator:Fake Email Generator - temp mail address
        Email:[gastroga] Check=>True
        Domain:[lotomoneymaker.com] Check=>True
        Email Ok
        gastroga@lotomoneymaker.com
        ```

    === "s2: Website"

        In this step we navigate to the Tommy Hilfiger website, and validate that the pictures match the captured entropy during authoring the script.
        ``` python
        # With an account lets try to register
        driver2 = webdriver.Chrome(options=set_chrome_options())
        driver2.maximize_window()
        driver2.get("https://nl.tommy.com/")
        driver2.get_screenshot_as_file('/scripts/tommy_0.png')

        screen_0 = Image.open("/scripts/tommy_0.png")
        assert np.isclose(screen_0.entropy(), 7, rtol=.15) 
        print("Entropy Close Verification")

        print("WebSite: " + driver2.title)
        assert "Tommy Hilfiger" in driver2.title
        ```

        __Output:__
        ```
        Entropy Close Verification
        WebSite: Tommy Hilfiger® Nederland | Officiële Online Winkel
        ```

    === "s3: Fill Form"

        I made use of two types of selectors: `xpath` and `css`.
        I personally think that the use of xpath is more convinient in most of the cases.

        In addition to the fill up of the form, additional tasks were completed like:
        
        1. Agreeing to the cookie policy of the website
        1. Closing the banner display on top of the page, offering free delivery

        ``` python hl_lines="1 9 16 23 31 38 45 52 59"
        # s3.1 Neutralize Pointer in Screen
        tommy_logo = driver2.find_element_by_xpath("//a[@title='Tommy Hilfiger']")
        ac = ActionChains(driver2)
        if tommy_logo:
            print('Pointer at Page Logo')
            ac.move_to_element(tommy_logo)
            driver2.get_screenshot_as_file(f'/scripts/tommy_1.png')

        # s3.2 Accept Cookie Policy
        accept_cookies_banner = driver2.find_element_by_xpath("//div[@class='cookie-notice__action']/button[1]")
        if accept_cookies_banner:
            print('Cookies Agreement Banner')
            accept_cookies_banner.click()
            driver2.get_screenshot_as_file(f'/scripts/tommy_2.png')

        # s3.3 Close Shipping Banner
        free_shipping_banner = driver2.find_element_by_xpath("//button[@class='slide__background--close']")
        if free_shipping_banner:
            print("Shipping Free Banner")
            free_shipping_banner.click()
            driver2.get_screenshot_as_file(f'/scripts/tommy_3.png')

        # s3.4 Open Registration Panel
        registration_button = driver2.find_element_by_xpath("//button[@class='header__link']")
        if registration_button:
            print("Opening Registration Panel")
            registration_button.click()
            WebDriverWait(driver2, 2).until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email' and @name='email1']")))
            driver2.get_screenshot_as_file(f'/scripts/tommy_4.png')

        # s3.5 Enter Email field
        email_field = driver2.find_element_by_xpath("//input[@type='email' and @name='email1']")
        if email_field:
            print("Entering Email")
            email_field.send_keys(email_address)
            driver2.get_screenshot_as_file(f'/scripts/tommy_5.png')

        # s3.6 Enter Password field
        password_field = driver2.find_element_by_xpath("//div[@class='register__passwords']//input[@type='password' and @name='logonPassword']")
        if password_field:
            print("Entering Password")
            password_field.send_keys("TommyChallenge2020")
            driver2.get_screenshot_as_file(f'/scripts/tommy_6.png')

        # s3.7 Enter Password Confirmation
        password_confirmation_field = driver2.find_element_by_xpath("//div[@class='register__passwords']//input[@type='password' and @name='logonPasswordVerify']")
        if password_confirmation_field:
            print("Confirmation Password")
            password_confirmation_field.send_keys("TommyChallenge2020")
            driver2.get_screenshot_as_file(f'/scripts/tommy_7.png')
        
        # s3.8 Accept Terms and Conditions
        accept_terms = driver2.find_element_by_xpath("//label[@for='signUpForTermsCondition1']")
        if accept_terms:
            print("Accept Terms and Conditions")
            accept_terms.click()
            driver2.get_screenshot_as_file(f'/scripts/tommy_8.png')

        # 3.9 Click Registration Button
        button_registration = driver2.find_element_by_xpath("//button[contains(text(), 'Registreren') and @type='submit']")
        if button_registration:
            print("Complete Registration")
            button_registration.click()
            WebDriverWait(driver2, timeout=10, poll_frequency=2).until(EC.title_contains('Mijn account'))
            driver2.get_screenshot_as_file(f'/scripts/tommy_9.png')
        ```

        __Output:__
        ```
        Pointer at Page Logo
        Cookies Agreement Banner
        Shipping Free Banner
        Opening Registration Panel
        Entering Email
        Entering Password
        Confirmation Password
        Accept Terms and Conditions
        Complete Registration
        ```

    === "s4: Confirmation"

        An email message is sent to the external website, and displayed in an internal panel.
        The information is displayed and captured in each of the snapshots captured during navigation.

        ``` python
        # TODO: Address the wait with Expected Condition. Left on purpose    
        time.sleep(EMAIL_WAIT_THRESHOLD)

        print(chalk.yellow("New Mail!"))

        # TODO: Actions.movo_to element but this also works
        email_body = driver.find_element_by_tag_name('body')
        email_body.send_keys(Keys.PAGE_DOWN)
        email_body.send_keys(Keys.PAGE_DOWN)
        
        driver.get_screenshot_as_file(f'/scripts/tommy_10.png')
        print(chalk.green("OK"))
        driver.quit()
        ```

        __Output:__
        ```
        New Mail!
        OK
        ```

This section covered the execution details, the next section details the accomplishments of the technical challenge.