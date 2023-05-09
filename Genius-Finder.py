
import pip._vendor.requests as requests
import json


def get_snippet():

    print("please enter the lyrics you remember...")

    snippet_input = input()

    return snippet_input


def get_results(snippet_input):

    url = "https://genius-song-lyrics1.p.rapidapi.com/search/multi/"

    querystring = {"q":snippet_input,"per_page":"3","page":"1"}

    headers = {
        "X-RapidAPI-Key": "9c9d7e61c8mshd3fd72ea07587f2p15207cjsn8707a6422c05",
        "X-RapidAPI-Host": "genius-song-lyrics1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    #print(json.dumps(response.json(), indent=4))
    return response.json()

def format_results(responce):

    section  = responce.get("sections")
    filtered_list = [d for d in section if d["type"] == "lyric"]
    
    finds = []


    for song in filtered_list:
        for result in song["hits"]:
            object = result['result']
            
            title = object.get("full_title")
            artist = object.get("artist_names")
            finds.append({"title":title,"artist":artist})

    print(json.dumps(finds, indent = 4))

    return




if __name__ == "__main__":
    
    responce = get_results(get_snippet())
    format_results(responce)
    



