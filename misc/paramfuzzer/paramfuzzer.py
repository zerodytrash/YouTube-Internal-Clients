import params_pb2
import base64
import urllib.parse
import requests
import json


for i in range(0, 100):
    g = params_pb2.params()

    g.p1 = i
    g.p2 = i
    g.p3 = i
    
    b64 = base64.b64encode(g.SerializeToString())
    b64_url = urllib.parse.quote(b64)

    post_data = {
        "context": {
            "client": {
                "hl": "en",
                "clientName": "WEB",
                "clientVersion": "2.20220331.06.00"
            }
        },
        "videoId": "8PNJCjXkrps",
        "params": b64_url
    }

    try:
        res = requests.post("https://www.youtube.com/youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8", data=json.dumps(post_data), headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29",
            "Content-Type": "text/plain;charset=UTF-8"
        })

        print(b64_url, res.status_code)

        if res.status_code == 200:
            f = open("results/" + str(i) + ".json", "w", encoding="utf-8")
            f.write(res.text)
            f.close()

    except Exception as ex:
        print(ex)