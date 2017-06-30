# ClassCheck 
### Python 2.7
### Objective
This script checks the UMass classes on Spire through your Shopping Cart Repeatedly
### Why?
As a college Freshman, it sucks to have the class I want to take to be full by the time I have the chance to enroll in it (Almost all the time it's inevitable because of my late enrollment date and other factors). I know it's a problem among my friends and it's also a problem for me as well. To fix this problem, I wrote this script that checks the Course catalogue website of UMass (also known as Spire) every 5 minutes to see if my class is open. It'll continuously check for it until that class is open. Once the class is open, the script sends an email to desired email address.

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
     - This function is for sending email to a desired email address when this script finds that the class is open.
     - You have to assign the variables, ```smtp_email_username``` and ```smtp_email_password``` to a email account so that the script can use that account to send emails.
     - You also need to assign the variable, ```email_to_be_sent``` to the email address you want the email to be sent to.
- ```driver()```
     - The driver uses the "browser" or webdriver, PhantomJS, a headless "browser" that does not have GUI and does not come with Selenium.
     - I recommend downloading the Chrome webdriver (which has GUI, like in the gif) and install it at the ```python/script``` folder assuming that folder is properly set in your machine's environmental variables.
     - The ```semester``` variable may need to change at different times.
     

