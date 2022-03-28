import requests
import os

client_versions = open("client_versions.txt", "r").readlines()
data_template =  open("post_data.txt", "r").read()

headers = {
    "Origin": "https://www.youtube.com",
    "Referer": "https://www.youtube.com/",
    "Accept-Language": "de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.52"
}

if not os.path.exists('results'):
    os.makedirs('resuls')


for client_name_id in range(0, 100):
    for client_version in client_versions:
        client_version = client_version.replace("\n", "").replace("\r", "")
        if client_version == "":
            continue

        try_id = str(client_name_id) + "_" + client_version

        print(try_id)

        data = data_template.replace('%clientName%', str(client_name_id)).replace('%clientVersion%', client_version)

        try:
            response = requests.post("https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", data=data, headers=headers, timeout=5)

            print(response.status_code)

            if response.status_code == 200:
                out = open("results/" + try_id + ".json", "w+", encoding="utf-8")
                out.write(response.text)
                out.close()
        except Exception as ex:
            print(ex)
