import requests
import random
import time

class scraping:
    def __init__(self):
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.header  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        self.action  = 'query'
        self.format  = 'json'
        self.list    = 'categorymembers'
        self.cmtitle = 'Category: songs'
        self.cmlimit = 500
        self.params  =  {
            "action"  : self.action,
            "format"  : self.format,
            "list"    : self.list,
            "cmtitle" : self.cmtitle,
            "cmlimit" : self.cmlimit,
        }
    
    #########################################################################
    # - exploritory code to look through wikipedia categories manually      #
    # - used to decide which categories to look at for data to use          #
    # - categories will be used to prompt user later on certain descision   #
    #########################################################################
    def retrieve_allCategories(self):
        params = { "action" : "query",
                   "format" : "json",
                   "list"   : "allcategories",
                   "aclimit": 500, }

        # Send the API request
        response = requests.get(self.api_url, params=params, headers=self.header)

        # Add a random delay between requests
        delay = random.uniform(1, 3)
        time.sleep(delay)

        # Retry mechanism
        retries = 5
        while retries > 0:
            if response.status_code == 200:
                break
            print(f"Request failed with status code {response.status_code}. Retrying...")
            response = requests.get(self.api_url, params=params, headers=self.header)
            delay = random.uniform(1, 3)  # Add a random delay between retries
            time.sleep(delay)
            retries -= 1

        # Parse the JSON response
        data = response.json()

        # Extract the category names from the response
        categories = [category["*"] for category in data["query"]["allcategories"]]

        # return list of categories
        return categories

                        
    def retrieve_songsCategory(self):
        # Send the API request for the subcategories of the songs category 
        response = requests.get(self.api_url, params=self.params, headers=self.header)

        # Parse the JSON response
        data = response.json()
        
        songsSubCategories = []

        # Process the category members
        for member in data["query"]["categorymembers"]:
            songsSubCategories.append(member["title"])
                        
        return songsSubCategories
    
    def retrieve_songsBydate(self):
        # Parameter change for the API request
        self.cmtitle = 'Category:Songs by date'
        self.params.update(cmtitle = 'Category:Songs by date')

        # Send the API request
        response = requests.get(self.api_url, params=self.params, headers=self.header)

        # Parse the JSON response
        data = response.json()
 
        optionsList = []

        #Process the category members
        for member in data["query"]["categorymembers"]:
            optionsList.append(member["title"])
                        
        return optionsList
    
    
    
    ####################################################################################
    # - use this following code to prompt the user about which subcategory to look at  #
    #   songs by either century, decade or year and then preform some sort of          # 
    #   analysis to return to the user to inform them about music during these times   #
    ####################################################################################    
    
    def retrieve_givenChoice(self, choice):
        # Parameters for the API request
        self.cmlimit = 50
        self.params.update(cmlimit = 50)
        
        if choice == 'century':
            self.cmtitle = 'Category:Songs by century'
            self.params.update(cmtitle = 'Category:Songs by century')
        elif choice == 'decade':
            self.cmtitle = 'Category:Songs by decade'
            self.params.update(cmtitle = 'Category:Songs by decade')
        else:
            self.cmtitle = 'Category:Songs by year'
            self.params.update(cmtitle = 'Category:Songs by year')

        # Send the API request
        response = requests.get(self.api_url, params=self.params, headers=self.header)

        # Parse the JSON response
        data = response.json()
 
        top50 = []

        #Process the category members
        for member in data["query"]["categorymembers"]:
            top50.append(member["title"])
                        
        return top50
    
    
#     def retrieve_songsChoosen(self):
#         # Parameters for the API request
        
#         params = {
#             "action": "query",
#             "format": "json",
#             "list": "categorymembers",
#             "cmtitle": "Category:2023 songs",
#             "cmlimit": 500,  # Adjust the limit as per your needs
#         }

#         # Send the API request
#         response = requests.get(self.api_url, params=params, headers=self.header)

#         # Parse the JSON response
#         data = response.json()
        
#         members = []

#         #Process the category members
#         for member in data["query"]["categorymembers"]:
#             members.append(member["title"])
                        
#         return members
    
#     def retrieve_artist(self):
#         # Parameters for the API request
        
#         params = {
#             "action": "query",
#             "format": "json",
#             "list": "categorymembers",
#             "cmtitle": "3 Boys",
#             "cmlimit": 5,  # Adjust the limit as per your needs
#         }

#         # Send the API request
#         response = requests.get(self.api_url, params=params, headers=self.header)

#         # Parse the JSON response
#         data = response.json()
        
# #         members = []

# #         #Process the category members
# #         for member in data["query"]["categorymembers"]:
# #             members.append(member["title"])
                        
# #         return members

#         return data
    
    
    
   

    

            
                        