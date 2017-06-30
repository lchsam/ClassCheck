"""
This script goes logs in to umass spire and goes to your shopping cart and
see if identified class is full, if it is not full, it sends an email.
This script will run forever.

Author: LCH
Date: December 19, 2016
Version: 0.4 Alpha

Take a look at the send_email function to have it work properly
"""



from selenium import webdriver
import yagmail
from bs4 import BeautifulSoup
import time
import socket
import sys


def internet(host="8.8.8.8", port=53, timeout=3, tries=0):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    if tries == 10:
        return False
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print ex.message
        print '\tRetrying...Finding Internet Connection'
        time.sleep(3)
        return internet(tries=tries+1)


def open_page_log_in(link, browser, tries=0):
    # This is extremely weird, right now, 1/8/2017, spire is acting up and it's telling
    # me I entered the wrong password even though it's right, so what happens when it detects
    # a wrong password is it takes a while to refresh, so this part of the code crashes
    # Because of how slow spire is acting up from not able to properly identify a password.
    if tries == 5:
        print '\tAcquired image of login site because of 5 fail logins'
        browser.get_screenshot_as_file('login_page.png')
    try:
        # This lets Selenium wait and try (for finding elements) for at most 10 seconds before throwing any exceptions
        # caused by not finding a specific element
        # browser.implicitly_wait(10)
        # opens spire login
        browser.get(link)
        if tries > 0:
            time.sleep(tries*0.1)
        # Finds username and password input field
        username = browser.find_element_by_id("userid")
        password = browser.find_element_by_id("pwd")
        # Fills username and password field with data gotten from pythPhonian module
        username.send_keys('insert string username for spire account')
        password.send_keys('insert string password for spire account')
        if tries > 0:
            time.sleep(tries*0.1)
        # Submits password and username submitting through a tag with a value equal to 'Go'
        # It should locate it with the form tag (forms have a submit 'button') but I was too lazy
        browser.find_element_by_xpath("//*[@value='Go']").submit()
        print 'Logging in...'
    except:
        print 'Cannot Login...Retrying...'
        open_page_log_in(link, browser, tries=tries+1)


def get_link_find_element_link_text(browser, link, text, tries):
    """Opens link with browser, and finds element by link text and returns element.
    If it cannot find element, it retries after 0.3 seconds. Retries 10 times
    This is my workaround for the implicitly_wait function (It does not work for some reason)"""
    if tries == 10:
        print 'Cannot Find Specified Text Link:', text
    try:
        browser.get(link)
        if tries > 0:
            time.sleep(tries * 0.1)

        element = browser.find_element_by_link_text(text)
        return element
    except:
        print '\t Cannot find', text, '...Retrying...'
        return get_link_find_element_link_text(browser, link, text, tries + 1)


def go_to_shopp_cart(browser):
    # Extremely weird way of accessing the shopping cart
    # First, I  directly go to the search page for classes with a link and then I click on the 'add' tab
    # I originally thought to just press on 'enrollment' link from the home page but
    # Selenium cannot find the element for some reason
    # Really weird.
    try:
        search_link = 'https://www.spire.umass.edu/' \
                      'psc/heproda/EMPLOYEE/HRMS/c/' \
                      'SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?' \
                      'Page=SSR_CLSRCH_ENTRY&Action=U'
        get_link_find_element_link_text(browser, search_link, 'add', tries=0).click()
    except:
        time.sleep(0.4)
        go_to_shopp_cart(browser)


def semester_select(browser, semester, tries):
    if tries == 3:
        print 'Semester selection is likely gone for the time being, continuing program...'
        return
    try:
        class_name = 'PSRADIOBUTTON'
        # Find the table of semesters
        page_table = browser.find_element_by_xpath("//table[@id='SSR_DUMMY_RECV1$scroll$0']")
        # Parses the html content of that element with Beautiful Soup
        # Different Radio buttons correspond to different semesters
        # The if statement below is not perfect.
        # If you're in the fall semester, the order of the radio buttons go by: fall, spring
        # If you're in the spring semester, the order of the radio buttons become: spring, fall
        # If I am in the spring semester, and I input 'fall', I end up choosing spring instead.
        # if semester == 'spring':
        #     tab_index = 158
        # else:
        #     tab_index = 152
        row_one = page_table.find_element_by_xpath("//*[@id='trSSR_DUMMY_RECV1$0_row1']")
        # Row one always will have index 152 for the tab_index of the button
        row_two = page_table.find_element_by_xpath("//*[@id='trSSR_DUMMY_RECV1$0_row2']")
        # Row two will always have tab index 158 for the tab index of the button.
        row_one_text = row_one.find_element_by_xpath('//*[@id="TERM_CAR$0"]').text.lower()
        tab_index = 158
        if semester.lower() in row_one_text:
            tab_index = 152
        # Find button and click
        button = page_table.find_element_by_xpath(
            "//input[@class='" + class_name + "'][@tabindex='" + str(tab_index) + "']")
        button.click()
        # Press continue
        browser.find_element_by_xpath("//a[@tabindex='419']").click()
    except:
        print '\t Either semester selection is gone for the time being or page is not loaded properly\n' \
              '\t\tRetrying...'
        time.sleep(0.1)
        semester_select(browser, semester, tries + 1)


def locate_enrollment_shopping_cart(browser, semester):
    """Go to shopping cart and select the right semester"""
    go_to_shopp_cart(browser)
    if semester is not None:
        semester_select(browser, semester, tries=0)
    print 'Going to Shopping Cart...'


def find_list_of_soupclasses(browser, wait):
    try:
        if wait != 0:
            time.sleep(wait)
        # Find table of classes
        table = browser.find_element_by_xpath("//table[@id='SSR_REGFORM_VW$scroll$0']/tbody")
        print 'Scanning Shopping Cart...'
        print 'Found Table'
        # Identify each row of class displayed
        classes = table.find_elements_by_xpath("//tr[contains(@id, 'trSSR_REGFORM_VW$0_row')]")
        print 'Found rows'
        array_of_soup = []
        # Add all rows of class parsed by Beautiful Soup to arraylist-ish thing
        # (Python calls it list, but it's a ArrayList)
        for soup_class in classes:
            array_of_soup.append(BeautifulSoup(soup_class.get_attribute('outerHTML'), 'html.parser'))
        return array_of_soup
    except:
        print '\tDidn\'t work...Retrying...(This often fails for its first time for some reason)'
        return find_list_of_soupclasses(browser, wait + 0.08)


def filtersoup(csoup):
    """Initial Soup parsing has newlines in between each td tags inside tr
    This returns a new ArrayList of soups with no newlines"""
    return list(filter(lambda child: child.name is not None, csoup.tr.children))


def get_name_from_tag(td_tag):
    contents = []
    stringy = ''
    if td_tag.a is None:
        contents = td_tag.span.contents
    else:
        contents = td_tag.a.contents
    stringy += unicode(contents[0]).encode('ascii', 'ignore')
    stringy += unicode(contents[1].string).encode('ascii', 'ignore').translate(None, '\n')
    return stringy


def get_string_from_tag(td_tag):
    return unicode(td_tag.span.string).encode('ascii', 'ignore')


def get_is_open_from_tag(td_tag):
    return td_tag.img['alt'] == 'Open'


def extract_and_output_to_classes_info(classes):
    cinfo = []
    for csoup in classes:
        columns_of_soup = filtersoup(csoup)
        name = get_name_from_tag(columns_of_soup[1])
        times = get_string_from_tag(columns_of_soup[2])
        room = get_string_from_tag(columns_of_soup[3])
        instructor = get_string_from_tag(columns_of_soup[4])
        credit = get_string_from_tag(columns_of_soup[5])
        is_open = get_is_open_from_tag(columns_of_soup[6])
        cinfo.append((name, times, room, instructor, credit, is_open))

    return cinfo


def print_info(classes_info):
    print
    print '-' * 65
    print 'Current Class Status'
    print '-' * 65
    print '     {0:<30}{1:<20}{2:<10}'.format('Class', ' Instr.', '  Open')
    print '_' * 65
    for n in classes_info:
        print '     {:<30}'.format(n[0]),
        print '{:<20}'.format(n[3]),
        print '{:<10}'.format(str(n[5]))
    print '_' * 65
    print


def class_exists(classname, teachername, classes_info):
    for clas in classes_info:
        if classname.upper() in clas[0] and teachername.upper() in clas[3].upper():
            return clas[0], clas[5]


def find_classes_info(browser, semester):
    # Since this method is run many times, I'm sure if Spire time outs
    # is depended on time or depended on activity. If it is depended on activity
    # This way of logging in is better since, it guarantees that I'll get to the shopping cart
    # If I use another method like, refreshing spire many times logging in, I'm sure if that'll continually work.
    umass_spire_login_url = 'https://www.spire.umass.edu/'
    open_page_log_in(umass_spire_login_url, browser)

    time.sleep(0.3)
    locate_enrollment_shopping_cart(browser, semester)
    soup_of_classes = find_list_of_soupclasses(browser, wait=0)
    # wait is for waiting for classes to load.
    # It's for those running the script with slow internet.

    return extract_and_output_to_classes_info(soup_of_classes)


def send_email():
    smtp_email_username = 'Insert Username'
    smtp_email_password = 'Insert password'
    yag = yagmail.SMTP(smtp_email_username, smtp_email_password)
    contents = ['Your teacher is found',
                'Please go to spire immediately']
    email_to_be_sent = 'insert Email'
    yag.send(email_to_be_sent, 'Here it is', contents)
    print 'Email notification is sent'


def determine_open_status(class_open):
    if class_open[1]:
        print '--' + class_open[0] + ' is OPEN'
        send_email()
        return True
    print class_open[0] + ' is not open'
    return False


def quit_program(browser):
    print 'Terminating Program'
    time.sleep(2)
    browser.quit()


def driver():
    browser = webdriver.PhantomJS()

    if not internet():
        print 'There is no internet'
        quit_program(browser)
        return

    semester = 'fall'
    classes_info = find_classes_info(browser, semester)
    print_info(classes_info)

    class_to_search = ''
    teacher_to_search = ''
    klass_exists = ''

    while True:
        class_to_search = raw_input('Please input class name or class number (e.g. compsci or 14811):\n')
        teacher_to_search = raw_input('Please input the corresponding teacher listed above:\n')
        klass_exists = class_exists(class_to_search, teacher_to_search, classes_info)
        if klass_exists is not None:
            break
        print 'Invalid Input...Please try again'

    print '------------------------------------------------'
    while klass_exists is not None:
        if determine_open_status(klass_exists):
            time.sleep(120)
        time.sleep(300)
        print '----------------------------------'
        if internet():
            klass_exists = class_exists(class_to_search, teacher_to_search, find_classes_info(browser, semester))
        else:
            print 'There is no internet'
            break
    else:
        print 'It seems class is removed from shopping cart'

    quit_program(browser)


def main():
    driver()


if __name__ == '__main__':
    main()

