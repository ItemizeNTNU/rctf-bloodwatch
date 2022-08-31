import os
import time
import requests
from playsound import playsound

# Global data log
challenges = {"agent-console": [],"break-in-at-headquarters-1": [],"break-in-at-headquarters-3": [],"hidden-pages-and-robots": [],"log4j": [],"well-known": [],"agent-inspector": [],"break-in-at-headquarters-2": [],"break-in-at-headquarters-4": [],"is-this-the-metaverse": [],"react-obfuscation": [],"its-bugdroid": [],"learn-once-write-anywhere": [],"data-breach": [],"foss-enthusiast": [],"corrupted-image": [],"escaping-the-pyjail-2": [],"hashdump-1": [],"microsoft-and-zip": [],"scratched-qr-code": [],"escaping-the-pyjail-1": [],"escaping-the-pyjail-3": [],"hashdump-2": [],"sanity-check": [],"vimtastic": [],"2pow6-all-your-base-are-belong-to-us-based-1": [],"caesar-salad-and-notes-1": [],"numbers-encoding-1": [],"2pow6-image-based-2": [],"caesar-salad-and-notes-2": [],"zero-and-ones-encoding-2": []}
ids = {}

# First loop getting challenge solves
for chall in challenges:
    print(chall)
    x = requests.get(f"https://ctf.itemize.no/api/v1/challs/{chall}/solves?limit=10&offset=0")
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
    for chall in challenges:
        x = requests.get(f"https://ctf.itemize.no/api/v1/challs/{chall}/solves?limit=10&offset=0")
        solves = x.json()["data"]["solves"]
        for solve in solves:
            sid = solve["id"]
            if sid not in challenges[chall]:
                team = solve["userName"]
                ids[sid] = {"team": team, "time": solve["createdAt"]}
                challenges[chall].append(sid)
                if len(challenges[chall]) == 1:
                    # First blood announce
                    playsound("./blood.mp3")
                    print("[First blood]", team)
                else:
                    # Pwn announce
                    playsound("./pwn.mp3")
                    print("[PWN]", team)

