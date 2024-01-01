from requests import get
from pprint import PrettyPrinter
import json

printer = PrettyPrinter()

def read_api_key(file_path='config.json'):
    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get('api_key')
            if api_key:
                return api_key
            else:
                raise ValueError('API key not found in the configuration file.')
    except FileNotFoundError:
        raise FileNotFoundError(f'Configuration file not found: {file_path}')
    except json.JSONDecodeError:
        raise ValueError(f'Error decoding JSON in configuration file: {file_path}')
    
BASE_URL = "https://api.cricapi.com/"
API_KEY = read_api_key()

def cricketSeriesList():
    endpoint = f"/v1/series?apiKey={API_KEY}&offset=0"
    url = BASE_URL + endpoint
    response = get(url).json()
    # print(data)
    for series in response['data']:
        seriesName = series['name']
        startDate = series['startDate']
        endDate = series['endDate']
        print(f"Name - {seriesName} || {startDate} - {endDate}")
    print()
    return
    
def searchCricketSeries():
    userInput = input("Enter the series you want to search for: ")
    endpoint = f"/v1/series?apikey={API_KEY}&offset=0&search={userInput}"
    url = BASE_URL + endpoint
    
    response = get(url).json()
    # print(data)
    seriesName = response['data'][0]['name']
    shortName = response['data'][0]['shortName']
    startDate = response['data'][0]['startDate']
    endDate = response['data'][0]['endDate']
    squads = response['data'][0]['squads']
    matches = response['data'][0]['matches']
    
    print(f"Name - {seriesName} ({shortName})")
    print(f"Start Data - {startDate}")
    print(f"End Date - {endDate}")
    print(f"Matches - {matches}")
    print(f"Squads - {squads}")
    print()
    return

def currentCricketMatches():
    endpoint = f"/v1/matches?apiKey={API_KEY}&offset=0"
    url = BASE_URL + endpoint
    response = get(url).json()
    # print(data)
    
    for match in response['data']:
        _id = match['id']
        teams = match['name']
        matchType = match['matchType']
        venue = match['venue']
        date = match['date']
        scoreTeam1 = None
        scoreTeam2 = None
        
        if "score" in match:
            scoreTeam1 = match['score'][0]
            scoreTeam2 = match['score'][1]
            
        status = match['status']

        # print(f"Match ID - {_id}")
        print(f"{teams}")
        print(f"Venue: {venue}")
        print(f"Date: {date}")
        print(f"Status: {status}")
        if scoreTeam1 and scoreTeam2:
            print(f"Score of {match['teams'][0]}: {scoreTeam1['r']}-{scoreTeam1['w']}, {scoreTeam1['o']}")
            print(f"Score of {match['teams'][1]}: {scoreTeam2['r']}-{scoreTeam2['w']}, {scoreTeam2['o']}")
        print()
    return
        
def playersList():
    endpoint = f"/v1/players?apikey={API_KEY}&offset=0"
    url = BASE_URL + endpoint
    response = get(url).json()
    # print(response)
    print("PLAYERS LIST IS AS FOLLOWS")
    print('==========================')
    players = response['data']
    for player in players:
        playerName = player['name']
        country = player['country']
        
        print(f"Name: {playerName}")
        print(f"Country: {country}")
        print()
    return
        
def searchAllPlayers():
    userInput = input("Enter the name of the player you want to search for: ")
    player_id = getPlayerInfo(userInput)
    if player_id == None:
        print("Player not found in database.")
        print()
        return
    
    endpoint = f"/v1/players_info?apikey={API_KEY}&offset=0&id={player_id}"
    url = BASE_URL + endpoint
    response = get(url).json()
    
    # dateOfBirth = None
    print(f"Name: {response['data']['name']}")
    
    if 'dateOfBirth' in response['data']:
        print(f"Date of Birth: {response['data']['dateOfBirth']}")
        
    print(f"Country: {response['data']['country']}")
    print(f"Role: {response['data']['role']}")
    print(f"Batting Style: {response['data']['battingStyle']}")
    print(f"Bowling Style: {response['data']['bowlingStyle']}")
    print()
    return

def getPlayerInfo(playerName):
    endpoint = f"/v1/players?apikey={API_KEY}&offset=0"
    url = BASE_URL + endpoint
    response = get(url).json() 
    
    players_list = response['data']
    for player in players_list:
        if player['name'].lower() == playerName.lower():
            return player['id']
    return None


def main():
    print("\n\t\t\tLIVE CRICKET SCORES")
    print("\t\t\t==================")
    print("Please select one of the following options:")
    print("1. Get cricket series list")
    print("2. Search for a series")
    print("3. View current live scores")
    print("4. Get list of all players")
    print("5. Search for player information")
    print("6. Quit the program")

    while True:
        try:
            command = int(input("\nEnter your command (1-6): "))
            print()
            if command == 1:
                cricketSeriesList()
            elif command == 2:
                searchCricketSeries()
            elif command == 3:
                currentCricketMatches()
            elif command == 4:
                playersList()
            elif command == 5:
                searchAllPlayers()
            elif command == 6:
                print("Program successfully exited. Thank you for using!")
                exit(0)
            else:
                print("Invalid command. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

        
if __name__ == '__main__':
    main()
    
    
    
    