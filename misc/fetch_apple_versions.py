import requests

html_all_apps = requests.get("https://apps.apple.com/us/developer/google-llc/id281956209?see-all=i-phonei-pad-apps")
html_all_apps_split = html_all_apps.text.split("\"")

all_apps = []
output = open("apple_versions.txt", "w")

for snippet in html_all_apps_split:
    if snippet.startswith("https://apps.apple.com/us/app/") and "\\" not in snippet and snippet not in all_apps:
        all_apps.append(snippet)

for app_link in all_apps:
    print("fetch " + app_link)
    app_html = requests.get(app_link).text
    app_version = app_html.split('version">Version ')[1].split("</p>")[0]
    output.write(app_version + "\n")

output.close()
