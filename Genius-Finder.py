
import requests
import json
import speech_recognition as sr
import pyaudio
import keyboard


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

    return response.json()



def format_results(response):

    section  = response.get("sections")
    filtered_list = [d for d in section if d["type"] == "lyric"]
    
    finds = []


    for song in filtered_list:
        for results in song["hits"]:
            object = results['result']

            title = object.get("full_title")
            artist = object.get("artist_names")

            for item in results["highlights"]:
                snippet = item.get("value")

                finds.append({"title":title,"artist":artist,"value": snippet})

    return finds



def get_speech_input():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        sample_rate = source.SAMPLE_RATE
        
        print("Press spacebar to start and stop recording...")
        while True:
            try:
                input_state = keyboard.is_pressed(' ')
                if input_state:
                    print("Recording...")
                    audio = r.listen(source, phrase_time_limit=30)
                    break
            except KeyboardInterrupt:
                break
        
        print("\n"+"Recording complete.")
        
        sample_width = audio.sample_width
        bytes_audio = audio.frame_data
        text = r.recognize_google(sr.AudioData(bytes_audio, sample_rate, sample_width), language='en')
        print(text)

    return text





def print_results(finds):

    print("\n" + "HERE ARE THE TOP RESULTS:" + "\n")

    for i in range(len(finds)):

        print("#" + str(i+1) + "\n")
        print("Title: " + finds[i]["title"])
        print("Artist: " + finds[i]["artist"])
        print("Snippet: " + finds[i]["value"].replace("\n"," "))
        print("\n")

    return



def get_option():

    proceed = 0

    while proceed == 0:

        choice  = input("Would you like to provide the lyris using text to speach or Keyboard input?" + "\n" + "1 for Keyboard" + "\n" + "2 for text-to-speech" + "\n")

        if choice  == "1":
            proceed = 1
        elif choice == "2":
            proceed = 1
        else:
            print("\n" + "Please enter a valid input...")

    return choice




if __name__ == "__main__":

    choice = get_option()

    if choice == "1":
        text = get_snippet()
    else:
        text = get_speech_input()

    print_results(format_results(get_results(text)))

    





