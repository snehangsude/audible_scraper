import re
import csv
import time as ty
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

class Crawler:

    def getName(self):
        book = soup.findAll('h3')
        name = [item.getText().replace('\n', '').strip(' ') for item in book][1:]
        return name

    def getAuthor(self):
        auth = soup.findAll('li', class_='authorLabel')
        author = [item.getText().replace('\n', '').replace('Written by:', '').strip(' ') for item in auth]
        return author

    def getNarrator(self):
        narr = soup.findAll('li', class_='narratorLabel')
        narrator = [item.getText().replace('\n', '').replace('Narrated by:', '').strip(' ') for item in narr]
        return narrator

    def getRuntime(self):
        length = soup.findAll('li', class_='runtimeLabel')
        runtime = [item.getText().replace('\n', '').replace('Length:', '').strip(' ') for item in length]
        return runtime

    def getRelease(self):
        date = soup.findAll('li', class_='releaseDateLabel')
        release = [item.getText().replace('\n', '').replace('Release Date:', '').strip(' ') for item in date]
        return release

    def getLanguage(self):
        lang = soup.findAll('li', class_='languageLabel')
        language = [item.getText().replace('\n', '').replace('Language:', '').strip(' ') for item in lang]
        return language

    def getRatings(self):
        star = soup.findAll('li', class_='ratingsLabel')
        ratings = [item.getText().replace('\n', '').replace('Language:', '').strip(' ') for item in star]
        return ratings

    def getPrice(self):
        amount = soup.findAll(id='adbl-buy-box')
        re_price = [re.findall(r"(\d+\,?\d+\.\d+)", item.getText()) for item in amount]
        price = []
        for item in re_price:
            try:
                price.append(item[0])
            except IndexError:
                price.append('Free')
            
        return price


class Controller:

    def __init__(self, link) -> None:
        self.driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))
        self.driver.get(link)


    def getAllcategories(self):
        all_categories = self.driver.find_elements(By.CLASS_NAME, 'refinementFormLink')
        return all_categories[:-2]

    def getSubcategories(self):
        initial_list = self.driver.find_element(By.CLASS_NAME, 'bc-spacing-medium')
        sub_categories = initial_list.find_elements(By.CLASS_NAME, 'refinementFormLink')
        return sub_categories

    def gobackSub(self):
        go_sub = self.driver.find_element(By.CLASS_NAME, 'categories')
        back = go_sub.find_elements(By.TAG_NAME, 'li')
        back[1].click()

    def gobackCat(self):
        self.driver.find_element(By.LINK_TEXT, 'All Categories').click()    

    def totalLoot(self):
        count = len(self.driver.find_elements(By.CLASS_NAME, 'productListItem'))
        return count

    def getPages(self):
        page = self.driver.find_elements(By.CLASS_NAME, "pageNumberElement")
        pages = [item.text for item in page]
        return int(pages[-1])

    def apply_options(self):
        if not self.driver.find_element(By.NAME, 'feature_twelve_browse-bin').is_selected():
            self.driver.find_element(By.LINK_TEXT, 'Audiobook').click()
            # self.driver.find_element(By.LINK_TEXT, 'Interview, Speech, or Lecture').click()
            # self.driver.find_element(By.LINK_TEXT, 'Instructional Program').click()
            # self.driver.find_element(By.LINK_TEXT, 'Magazine or Newspaper').click()
            # self.driver.find_element(By.LINK_TEXT, 'Radio Programme or Performance').click()
        else:
            pass


spider = Crawler()
robot = Controller('https://www.audible.in/search?')

HEADER = 0 # helps us manage the headers to write in the csv file

total_cat = robot.getAllcategories()
cats = [cat.text for cat in total_cat]

for loop in range(len(total_cat)): # Loop 1
    robot.apply_options()
    audible_cat = robot.getAllcategories()
    audible_cat[loop].click()
    
    total_sub = robot.getSubcategories()
    for item in range(len(total_sub)): # Loop 2
        audible_sub = robot.getSubcategories()
        
        # Used to manage few wrong redirects in sub categories (Explained in ReadMe)
        trigger = True 
        if cats[loop] == 'Biographies & Memoirs' and (item == 2 or item == 5): 
            trigger = False
        
        if cats[loop] == 'Literature & Fiction' and (item == 10 or item == 11):
            trigger =False

        if cats[loop] == 'History' and (item == 5):
            trigger = False

        if cats[loop] == 'Mystery, Thriller & Suspense' and (item == 3):
            trigger = False

        if cats[loop] == 'Romance' and (item == 1 or item == 7 or item == 8):
            trigger = False

        if cats[loop] == 'Sports & Outdoors' and (item == 0 or item == 3 or item == 23):
            trigger = False
                    
        if trigger:
            audible_sub[item].click()
        
            pages = robot.getPages()
            for page in range(pages): # Loop 3
                counter = robot.totalLoot()
                index = robot.driver.page_source
                soup = bs(index, features='html.parser')
                main_content = soup.find('div', class_='adbl-impression-container')

                # Catches if the page doesn't load succesfully
                if main_content == None:
                    ty.sleep(2)
                    robot.driver.refresh()
                    main_content = soup.find('div', class_='adbl-impression-container')


                # Main loop for gathering the name, author and narrator            
                all_content = []
                for items in main_content.select('ul.bc-size-small'): #Loop 4
                        name = items.find('h2').text
                        auth = items.findAll('li', class_='bc-list-item')
                        all_list = [i.text.replace('\n', '') for i in auth]
                        
                        for i in all_list:
                            if 'Written' in i:
                                author = i.replace(' ','')
                            narrator=False
                            if 'Narrated' in i:
                                narrator = True
                                narr = i.strip().replace(' ','')
                            elif narrator:
                                narr = 'None' 
                        
                        temp = {
                            'name': name,
                            'author': author,
                            'narrator': narr,
                        }
                        all_content.append(temp)
                        
                        # Getting all the other information
                        time = spider.getRuntime()
                        release = spider.getRelease()
                        star = spider.getRatings()
                        lang = spider.getLanguage()
                        price = spider.getPrice()
                        for value in range(len(all_content)): # Loop 5
                            all_content[value].update([
                                ('time', time[value]),
                                ('releasedate', release[value]), 
                                ('language', lang[value]),
                                ('stars', star[value]),
                                ('price', price[value]),
                                ])
                
                # Writing the data into CSV
                headers = all_content[0].keys()
                with open("audible(trial).csv","a", encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if HEADER == 0:
                        writer.writerow(headers)
                    HEADER = 1
                    for row in all_content:
                        writer.writerow(row.values())
                
                # Clicking on the Next Page
                if counter == len(all_content):
                    try:
                        button = robot.driver.find_element(By.CLASS_NAME, 'nextButton').click()
                    except:
                        robot.driver.refresh()
                        button = robot.driver.find_element(By.CLASS_NAME, 'nextButton').click()

                # Going back to the sub category page
                if page == pages-1:
                    robot.driver.find_element(By.LINK_TEXT, cats[loop]).click()

            # Going back to the all category page
            if item == len(total_sub)-1:
                robot.gobackCat()
        else:
            continue