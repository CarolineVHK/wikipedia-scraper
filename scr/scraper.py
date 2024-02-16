import requests
from bs4 import BeautifulSoup
import re
import json 
from pprint import pprint

class WikipediaScraper:
    def __init__(self):
        self.base_url = 'https://country-leaders.onrender.com/'
        self.country_endpoint = self.base_url + 'countries/'
        self.leaders_endpoint =  self.base_url + 'leaders/' 
        self.cookies_endpoint =  self.base_url + 'cookie/'
        self.leaders_data = {}                                      #dict is a dictionary where you store the data you retrieve before saving it into the JSON file
        self.new_cookie()                                                    #object is the cookie object used for the API calls

    def new_cookie(self):
        self.cookie = requests.get(self.cookies_endpoint)
        self.cookie = self.cookie.cookies


    def get_first_paragraph(self, wikipedia_url):
        WIKI_TEXT = requests.get(wikipedia_url)
        soup = BeautifulSoup(WIKI_TEXT.text, "html.parser")
        paragraphs = []
        for tags in soup.find_all("p"):
            paragraphs.append(tags.text)
        first_paragraph = ""
        for p in paragraphs:
            if len(p) > 100:
                first_paragraph = p
                break
        patern_to_remove = r'\([^)]*\)|\(.*?\)|\[.*?\]'
        my_new_first_paragraph = re.sub(patern_to_remove,"",first_paragraph)
        return my_new_first_paragraph


    def get_leaders(self):
        #2. get the cookie
        self.new_cookie()
        #3. get countries
        countries = requests.get(self.country_endpoint, cookies=self.cookie).json()
        leaders_per_country = {}
        for country in countries:
            self.new_cookie()
            leaders = requests.get(self.leaders_endpoint, params = {'country': country}, cookies=self.cookie).json()
            '''Above gives a dictionairy for chosen country '''
            #need to search for the url in the leader and get the first pararaph
            for leader in leaders:
                if 'wikipedia_url' in leader:
                    first_paragraph = self.get_first_paragraph(leader['wikipedia_url'])
                    leader['first_paragraph'] = first_paragraph
                leaders_per_country[country] = leaders   # is the data collected from leaders in country x
        return leaders_per_country

    def write_to_file(self):
        with open('leaders.json',"w") as leaders_json_file:
            leaders_per_country = self.get_leaders()
            data_file = json.dumps(leaders_per_country)   #dict omzetten naar string 
            leaders_json_file.write(data_file)              #string schrijven naar file

    def read_file(self):
        with open('leaders.json',"r") as leaders_json_file:
            file_content = leaders_json_file.read()
            leaders_json = json.loads(file_content)                     #van string naar dict
            pprint(leaders_json)


test1 = WikipediaScraper()
print(test1.get_leaders())
