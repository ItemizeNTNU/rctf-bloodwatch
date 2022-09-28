import os
import time
import requests
import sys
#from playsound import playsound

# Global data log
URL = "https://test.ctf.itemize.no"
LIVESCOREBOARD_URL = "http://localhost:3000"
challenges = {}
ids = {}

# Get challenges
headers = {
    "Authorization": "Bearer <token here>"
}
x = requests.get(f"{URL}/api/v1/challs", headers=headers)
for chall in x.json()["data"]:
    challenges[chall["id"]] = []
print(challenges)

x = requests.get(f"{URL}/api/v1/leaderboard/now?limit=100&offset=0", headers=headers)
leaderboard = x.json()["data"]["leaderboard"]
requests.post(f"{LIVESCOREBOARD_URL}/score", json={"score": leaderboard})
print(leaderboard)
#requests.post(f"{LIVESCOREBOARD_URL}/pwn", json={"team": "test", "challenge": "test-chall"})
#requests.post(f"{LIVESCOREBOARD_URL}/blood", json={"team": "test", "challenge": "test-chall"})
#sys.exit(0)


# First loop getting challenge solves
for chall in challenges:
    print(chall)
    x = requests.get(f"{URL}/api/v1/challs/{chall}/solves?limit=100&offset=0")
    solves = x.json()["data"]["solves"]
    for solve in solves:
        sid = solve["id"]
        if sid not in challenges[chall]:
            ids[sid] = {"team": solve["userName"], "time": solve["createdAt"]}
            challenges[chall].append(sid)


print("checking...")
# While loop to check for challenge solve updates
while True:
    print("checking..")
    time.sleep(2)
    # Push scoreboard
    x = requests.get(f"{URL}/api/v1/leaderboard/now?limit=100&offset=0", headers=headers)
    leaderboard = x.json()["data"]["leaderboard"]
    requests.post(f"{LIVESCOREBOARD_URL}/score", json={"score": leaderboard})
    
    # Check solves
    for chall in challenges:
        x = requests.get(f"{URL}/api/v1/challs/{chall}/solves?limit=100&offset=0")
        solves = x.json()["data"]["solves"]
        for solve in solves:
            sid = solve["id"]
            if sid not in challenges[chall]:
                team = solve["userName"]
                ids[sid] = {"team": team, "time": solve["createdAt"]}
                challenges[chall].append(sid)
                if len(challenges[chall]) == 1:
                    # First blood announce
                    #playsound("./blood.mp3")
                    print("[First blood]", team)
                    requests.post(f"{LIVESCOREBOARD_URL}/blood", json={"team": team, "challenge": chall})
                else:
                    # Pwn announce
                    #playsound("./pwn.mp3")
                    print("[PWN]", team)
                    requests.post(f"{LIVESCOREBOARD_URL}/pwn", json={"team": team, "challenge": chall})

