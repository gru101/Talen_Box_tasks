from bs4 import BeautifulSoup
import requests 
import json
import pandas as pd


def get_data(actor_name):
    """
    This function sends request to rotten tomatoes site and gets the raw data (JSONLD .i.e JSON linked data)
    """
    response = requests.get(f"https://www.rottentomatoes.com/celebrity/{actor_name}")
    print("Request sent")

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        return "Check if there are any spelling mistakes in the actor name ", response.status_code

    scripts_tag = soup.find_all('script', type='application/ld+json')
    return scripts_tag 

def get_filmography(scripts_tag):
    """
    This function extracts movie names and dates from the raw data by first converting it into json file.
    """
    movies = []
    dates = []

    for script_tag in scripts_tag:
        json_data = json.loads(script_tag.string)
        Movies = dict(json_data.get('itemListElement')[0])
        for i in range(len(Movies['itemListElement'])-1):
            movies.append(Movies['itemListElement'][i]['name'])
            dates.append(Movies['itemListElement'][i]['dateCreated'])
    print("Data Extracted")

    return movies, dates

def save_fimography_data(movies, dates, actor_name):
    """
    This function creates a dataframe and save the data in a CSV file.
    """
    data = pd.DataFrame({"Movies":movies, "Date Released": dates})
    data.to_csv(f"{actor_name}_Filmography.csv")
    print("Data saved")

if __name__ == "__main__":
    actor_name = input("Enter actor name: ").replace(" ","_").lower()
    data = get_data(actor_name=actor_name)
    movies, dates = get_filmography(data)
    save_fimography_data(movies=movies, dates=dates, actor_name=actor_name)


