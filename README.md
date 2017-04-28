# ClassCheck 
### Python 2.6
### Objective
This script checks the UMass classes on Spire through your Shopping Cart Repeatedly
### Why?
As a collge Freshman, it sucks to have the class I wanted to take to be full by the time I have the chance to enroll in it. I know it's a problem among my friends and it's also a problem for me as well. To fix this problem, I wrote this script that checks the Course catalogue website for UMass every 5 minutes to see if my class is open. It'll continuously check for it until that class is open. Once the class is open, the script sends an email to desired email address.

### Sample Run
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
After inputing required information, this script will go on a (in)finite loop to see if that class is open.

## Required Libraries
* Selenium
* Yagmail

## Note from Author
> Don't take my word for it. This actually works. Try it out if you can lol.
