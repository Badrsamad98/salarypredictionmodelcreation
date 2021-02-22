from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

'''Gets a specific information using a DOM link or returns -1'''


def get_information_by_link(driver, link):
    try:
        return driver.find_element_by_xpath(link).text
    except NoSuchElementException:
        return -1


'''Clicks on a specific button or prints a message if exception'''


def click_on_button_and_proceed(driver, link, exception_message):
    try:
        button = driver.find_element_by_xpath(link)
        button.click()
    except (ElementNotInteractableException, NoSuchElementException):
        print(exception_message)  # print exception message
        pass


'''The script that scrappes the pages'''


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.maximize_window()

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + \
        keyword+"&sc.keyword="+keyword+"&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
        # Test for the "Sign Up" prompt and get rid of it.

        click_on_button_and_proceed(
            driver, '//*[@id="onetrust-accept-btn-handler"]', 'Cookies policy not found')

        # Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("react-job-listing")
        # react-job-listing for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:
            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(1)
            collected_successfully = False

            # clicking on the X of the login modal.
            click_on_button_and_proceed(
                driver, './/span[@class="SVGInline modal_closeIcon"]', 'Modal close button not found')

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath(
                        './/div[@class="css-87uc0g e1tk4kwz1"]').text
                    location = driver.find_element_by_xpath(
                        './/div[@class="css-56kyx5 e1tk4kwz5"]').text
                    job_title = driver.find_element_by_xpath(
                        './/div[(@class="css-1vg6q84 e1tk4kwz4")]').text
                    job_description = driver.find_element_by_xpath(
                        './/div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            salary_estimate = get_information_by_link(driver,
                                                      './/span[@class="css-56kyx5 css-16kxj2j e1wijj242"]')

            rating = get_information_by_link(driver,
                                             './/span[@class="css-1m5m32b e1tk4kwz2"]')

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            try:
                driver.find_element_by_xpath(
                    '//*[@id="SerpFixedHeader"]/div/div/div[3]').click()

                size = get_information_by_link(driver,
                                               '//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]')
                founded = get_information_by_link(driver,
                                                  '//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]')
                type_of_ownership = get_information_by_link(driver,
                                                            '//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]')
                industry = get_information_by_link(driver,
                                                   '//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]')
                sector = get_information_by_link(driver,
                                                 '//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]')
                revenue = get_information_by_link(driver,
                                                  '//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]')

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                size = founded = type_of_ownership = industry = sector = revenue = - 1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element_by_xpath(
                './/li[@class="css-1yshuyv e1gri00l3"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)
