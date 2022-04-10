import requests

output = open("android_versions.txt", "w")

response = requests.get("https://androidapksfree.com/devapk/google-inc/")

#print(response.text)

split_html = response.text.split('<a href="')
for x in split_html:
    apk_link = x.split('"')[0]

    if not apk_link.startswith("https://"):
        continue

    try:
        response_apk = requests.get(apk_link)
        apk_version = response_apk.text.split("latest apk version ")[1].split('"')[0].split(" ")[0].split("_")[0]
        print(apk_version)

        output.write(apk_version.strip() + "\n")
        output.flush()
    except Exception as ex:
        print(ex)

output.close()