import os
import time
import requests
import sys

# Constants
URL = "https://ctf.itemize.no"
LIVESCOREBOARD_URL = "http://localhost:3000"

# Global data log
challenges = {}
ids = {}

# Get challenges
headers = {
    "Authorization": f"Bearer {os.environ['RCTF_TOKEN']}"
}
x = requests.get(f"{URL}/api/v1/challs", headers=headers)
for chall in x.json()["data"]:
    challenges[chall["id"]] = []
print(challenges)

x = requests.get(f"{URL}/api/v1/leaderboard/now?limit=100&offset=0", headers=headers)
leaderboard = x.json()["data"]["leaderboard"]
requests.post(f"{LIVESCOREBOARD_URL}/score", json={"score": leaderboard})
print(leaderboard)


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

# Restart on crashes
while True:
    try:
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
                            print("[First blood]", team)
                            requests.post(f"{LIVESCOREBOARD_URL}/blood", json={"team": team, "challenge": chall})
                        else:
                            # Pwn announce
                            print("[PWN]", team)
                            requests.post(f"{LIVESCOREBOARD_URL}/pwn", json={"team": team, "challenge": chall})
    except:
        print("---")
        print("Program crashed, restarting...")
        print("---")

