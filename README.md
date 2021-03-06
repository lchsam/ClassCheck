# ClassCheck 
### Python 2.7
### Objective
This script checks your UMass course shopping cart through Spire repeatedly.

### Sample Run
#### Access Spire
![alt text](http://i.imgur.com/veNbVsH.gif "Accessing Spire with Selenium")
#### Display result
```
-----------------------------------------------------------------
Current Class Status
-----------------------------------------------------------------
     Class                          Instr.               Open
_________________________________________________________________
     COMPSCI 220-01 (14811)         G. Anderson          False
     COMPSCI 220-01LN (14858)       Staff                True
     COMPSCI 230-01 (14817)         T. Richards          False
     COMPSCI 230-01AF (14898)       Staff                True
     COMPSCI 240-01 (14812)         A. McGregor          False
     COMPSCI 240-01AC (14851)       Staff                True
     COMPSCI 250-01 (14780)         D. Barrington        False
     COMPSCI 250-01AD (14849)       Staff                False
     ENGLWRIT 112-16 (11945)        T. McGill            False
     MATH 233-02 (15104)            None                 False
     MATH 233-03 (15105)            E. Farelli           False
     PHYSICS 151-01 (11331)         D. Kawall            False
     PHYSICS 151-99LQ (11421)       Staff                False
_________________________________________________________________

Please input class name or class number (e.g. compsci or 14811):
14849
Please input the corresponding teacher listed above:
Staff
```
After inputing required information, this script will go on a (in)finite number of loops to see if that class is open.
### Using this script
#### Required Libraries
* Selenium - Web Scrapping
* Yagmail  - Send Email

There are a few functions that needs to be edited for it to work properly
- ```send_email()```
     - This function is for sending email to a desired email address when this script finds that the class is open.'
     - You can get rid of this function and all of its reference if you don't want this. If you do, keep reading.
     - You have to assign the variables, ```smtp_email_username``` and ```smtp_email_password``` to an email account so that the script can use that account to send emails.
     - You also need to assign the variable, ```email_to_be_sent``` to the email address you want the email to be sent.
- ```driver()```
     - The driver uses the "browser" or webdriver, PhantomJS, a headless "browser" that does not have GUI and does not come with Selenium.
     - I recommend downloading the Chrome webdriver (which has GUI, like in the gif) and install it at the ```python/script``` folder assuming that folder is properly set in your machine's environment variables.
     - Once that is done, assign the variable ```browser``` to ```browser.Chrome()```
     - The ```semester``` variable may need to change depending on what time it is and what semester(s) are available.
- ```open_page_log_in(link, browser, tries=0)```
     - ```username.send_keys``` and ```password.send_keys``` are functions that take in your username and password as strings so that selenium can input the selected fields, i.e. the username and password variable.
     

