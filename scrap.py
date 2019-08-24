#Call dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser

#Activate driver
# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
!which chromedriver

#Start automated test software in Chrome
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

keywords = ['python', 'sql', 'mongodb', 'sqlalchemy', 'javascript']
for type_ in len(keywords):
    keyword = keywords[type_]
    #URL to be scraped
    source = "https://www.indeed.com.mx/trabajo?q="+ keyword +"&l=CDMX"
    
    #Retrieve web page
browser.visit(source)

job_title = []
job_desc = []
job_salary = []
job_company = []
job_link = []
job_type = []

for i in range(2,7):
    html_source = browser.html
    source_soup = BeautifulSoup(html_source, 'html.parser')
    job_card = source_soup.find_all('div', class_='jobsearch-SerpJobCard')
    
    for jb in job_card:
        try:
            html_jobTitle = jb.find('a', class_='jobtitle').text.strip().replace('\n', '')
            html_jobDesc = jb.find('div', class_='summary').text.strip().replace('\n', '')
            html_salary = jb.find('span', class_='salary').text.strip().replace('\n', '')
            html_company_name = jb.find('span', class_='company').text.strip().replace('\n', '')
            html_link = jb.a['href']
            if (html_jobTitle and html_jobDesc and html_salary and html_company_name and html_link):
                job_title.append(html_jobTitle)
                job_desc.append(html_jobDesc)
                job_salary.append(html_salary)
                job_company.append(html_company_name)
                job_link.append(html_link)
                job_type.append(keyword)
        except AttributeError as e:
            pass
    browser.click_link_by_partial_text(i)

job_list = list(zip(job_title,job_desc,job_salary,job_company,job_link,job_type))

jobs_df = pd.DataFrame(job_list, columns =['Job Title', 'Job Description', 'Job Salary', 'Job Company', 'Job Link', 'Job Type'])

print(len(jobs_df))