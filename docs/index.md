# Home

Hello 👋, thank you for taking the time to review this technical challenge.
This documentation micro-site, encloses the brief description of the technical elements used to complete the technical challenge.


## Tasks

1. The task is to create an automated E2E test suite for the following public website: https://nl.tommy.com/
1. The tests should cover the following functionality: Create a new user account.
1. Browser support: Google Chrome
1. The test suite should support desktop and mobile versions of the website. For mobile tests please use Chrome mobile emulation.

## Accomplished

- [x] Automated Suite
- [x] Create a new user account
- [x] Browser support Google Chrome
- [x] Desktop website
- [ ] Mobile Website

## Scenarios

- [x] Account creation
- [x] Email confirmation with new account
- [x] Image entropy validation for current website (Guarantee for color and styles)
- [x] Object Character Recognition (OCR) on images
- [ ] Verify errors during registration process
- [ ] New address

## Assumptions

I decided to focus my submission in the main test scenario for account creation.
I assume that the idea of using an external email system, and the concept of E2E validation was the priority. 

## Contribution
Base on our conversation about the current challenges of the team regarding the validation of styles, or the use of `machine learning` in different areas of the test automation scope, I incorporated __2 features__ one that makes use of a simple computation for image comparisson, and the other one that uses OCR for retrieving email addresses from an image.

Overall, I enjoyed the challenge and I hope that the implementation meets your assessment criteria.