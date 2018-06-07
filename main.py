import csv
import json
import requests

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome(executable_path=r"chromedriver")

#######################################
#			Examboard/Subject Extraction		#
#######################################
def get_examboard():
	examboards = []
	subject_urls = []
	with open('subjects.json') as fp:
		subject_urls = json.load(fp)
	for url in subject_urls:
		driver.get(url)
		# get examboard url
		links = driver.find_elements_by_css_selector("a.examspec-picker__button-link")
		for link in links:
			examboards.append(link.get_attribute("href"))
		if len(links) is 0:
			examboards.append(url)
	with open('examboards.json', 'w') as fp:
		json.dump(examboards, fp, sort_keys=True, indent=4)

###########################
#			Topic Extraction		#
###########################
def get_topics():
	subject_urls = []
	with open('examboards.json', 'r') as fp:
		subject_urls = json.load(fp)
	topics = {} #eg. {"Biology AQA": ["url1","url2"...],}
	for url in tqdm(subject_urls, desc="Subjects", total=len(subject_urls)):
		if "education/examspecs" not in url:
			driver.get(url)
			title = driver.find_element_by_css_selector("h1.context-panel__header").text
			link_elements = driver.find_elements_by_css_selector("a.topic-block__content-link")
			if len(link_elements) is 0:
				link_elements = driver.find_elements_by_css_selector(".topic__subitem-link")
			links = []
			for link in link_elements:
				links.append(link.get_attribute("href"))
			topics[title] = links
		else:
			continue


	with open('topic_urls.json', 'w') as fp:
		json.dump(topics, fp, sort_keys=True, indent=4)

#########################
#			Quiz Scraping			#
#########################
def get_quiz():
	topic_urls = {}
	# with open('topic_urls.json', 'r') as fp:
	# 	topic_urls = json.load(fp)
	topic_urls = {"test": ["https://www.bbc.com/education/guides/zqt7k7h"]}
	for subject_name, subject_urls in topic_urls.items():
		for url in subject_urls:
			driver.get(url + '/test')
			quiz = {}
			for prompt in driver.find_elements_by_css_selector('.question-prompt'):
				print(prompt)

			for radio in driver.find_elements_by_css_selector("input[type='radio'][value='a']"):
				driver.execute_script("arguments[0].click();", radio)

			#
			#click this: div.radio-answer:nth-of-type(1) input
			#submit
			#check answers

get_quiz()

