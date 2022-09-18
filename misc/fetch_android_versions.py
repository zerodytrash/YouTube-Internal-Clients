import requests

output = open("android_versions.txt", "w")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
}

response = requests.get("https://androidapksfree.com/devapk/google-inc/", headers=headers)

#print(response.text)

split_html = response.text.split('<a href="')
for x in split_html:
    apk_link = x.split('"')[0]

    if not apk_link.startswith("https://"):
        continue

    try:
        response_apk = requests.get(apk_link, headers=headers)
        apk_version = response_apk.text.split("latest apk version ")[1].split('"')[0].split(" ")[0].split("_")[0]
        print(apk_version)

        output.write(apk_version.strip() + "\n")
        output.flush()
    except Exception as ex:
        print(ex)

output.close()