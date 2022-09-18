import os
import json

def get_min_max_quality_label(formats):
    formats = [f for f in formats if f.get("qualityLabel") is not None]
    formats.sort(key=lambda x: x.get("width"))
    min_format = formats[0]
    max_format = formats[-1]

    return min_format.get("qualityLabel") + " - " + max_format.get("qualityLabel")

def get_unique_mime_str(formats):
    mimes = []
    for f in formats:
        if f.get("mimeType") is not None:
            mime_short = f.get("mimeType").split(";")[0]

            if mime_short not in mimes:
                mimes.append(mime_short)

    mimes_str = ""
    for m in mimes:
        mimes_str += "`" + m + "` "

    return mimes_str

def get_structure_tree(data, depth = 0):
    result = ""

    for attribute in data:
        if isinstance(data[attribute], dict):
            result += ("│&nbsp;&nbsp;&nbsp;&nbsp;" * depth) + "├─`" + attribute + "`<br>"
            result += get_structure_tree(data[attribute], depth + 1)
        if isinstance(data[attribute], list):
            result += ("│&nbsp;&nbsp;&nbsp;&nbsp;" * depth) + "├─`[" + attribute + "]` (" + str(len(data[attribute])) + ")<br>"

    return result


markdown = ""
markdown += "| ID/ClientName/Version | Quality Formats | Features/Limitations/Attributes |\n"
markdown += "|---------------------------|-----------------|----------|\n"

working_clients_output = ""
working_versions = []


if not os.path.exists('results'):
    os.makedirs('results')

files = os.listdir('responses')

client_ids = []

for file in files:
    client_id = int(file.split('_')[0])
    if client_id not in client_ids:
        client_ids.append(client_id)

client_ids.sort()

for client_id in client_ids:
    client_files = [file for file in files if file.startswith(str(client_id) + '_')]
    client_files.sort(reverse=True) # highest version first 

    versions = []
    for file_name in client_files:
        version = file_name.split("_")[1]
        if version not in versions:
            versions.append(version)

    for client_file in client_files:
        response_data_raw = open('responses/' + client_file, 'r', encoding='utf-8').read()
        response_data = json.loads(response_data_raw)

        client_name = None
        client_version = client_file.split('_')[1].replace('.json', '')
        has_hls_format = ".m3u8" in response_data_raw
        has_mpeg_dash = "dashManifest" in response_data_raw

        try:
            client_name = response_data_raw.split('%26c%3D')[1].split('%26')[0]
        except Exception:
            try:
                client_name = response_data_raw.split('&c=')[1].split('&')[0]
            except Exception:
                continue
        
        working_clients_output += str(client_id) + ";" + client_name + ";" + client_version + "\n"

        if client_version not in working_versions:
            working_versions.append(client_version)

        formats_combined = []

        formatsStr = ""

        if response_data.get('streamingData'):
            formats = response_data.get('streamingData').get('formats')
            if formats is not None:
                formatsStr = "<details><summary>Formats (" + str(len(formats)) + ")</summary>"
                formats_combined += formats

                for format in formats:
                    formatsStr += str(format.get("itag")) + " - " + str(format.get("qualityLabel")) + " - " + str(format.get("mimeType")).split(';')[0] + "<br>"

                formatsStr += "</details>"

        adaptiveFormatsStr = ""

        if response_data.get('streamingData'):
            formats = response_data.get('streamingData').get('adaptiveFormats')
            if formats is not None:
                adaptiveFormatsStr = "<details><summary>Adaptive Formats (" + str(len(formats)) + ")</summary>"
                formats_combined += formats

                for format in formats:
                    adaptiveFormatsStr += str(format.get("itag")) + " - " + str(format.get("qualityLabel")) + " - " + str(format.get("mimeType")).split(';')[0] + "<br>"

                adaptiveFormatsStr += "</details>"

        formats_summary = "<b>" + get_min_max_quality_label(formats_combined) + "</b><br>"
        formats_summary += get_unique_mime_str(formats_combined) + "<br><br>"

        extraInfo = ""

        if "music.youtube.com" in client_file:
            extraInfo += "&bull; Music videos only<br>"

        if "www.youtubekids.com" in client_file:
            extraInfo += "&bull; \"For Kids\" content only<br>"


        if has_hls_format:
            extraInfo += "&bull; HLS Support<br>"

        if has_mpeg_dash:
            extraInfo += "&bull; MPEG-DASH Support<br>"

        if client_name == "TVHTML5_SIMPLY_EMBEDDED_PLAYER":
            extraInfo += "&bull; No Age-restrictions<br>"

        if "android" in client_name.lower():
            extraInfo += "&bull; Might require [`androidSdkVersion`](#params)<br>"


        ignore_attributes = ["videoDetails", "playerConfig", "responseContext", "playabilityStatus", "streamingData", "playbackTracking", "trackingParams", "adPlacements", "playerAds", "adParams", "adBreakParams", "onResponseReceivedEndpoints", "playerSettingsMenuData"]

        if extraInfo != "":
            extraInfo += "<br>"

        for attribute in response_data:
            if attribute not in ignore_attributes:
                extraInfo += "&bull; `" + attribute + "`<br>"

        if extraInfo != "":
            extraInfo += "<br>"

        extraInfo += "<details><summary>Show Response</summary>" + get_structure_tree(response_data) +"</details>"

        other_versions = ""
        if len(versions) > 1:
            other_versions = "<br><br><details><summary>All Versions</summary>" + "<br>".join(versions) +"</details>"


        markdown += "|ID: *" + str(client_id) + "*<br><b>" + client_name + "</b><br>" + client_version + other_versions + "|" + formats_summary + formatsStr + adaptiveFormatsStr + "|" + extraInfo  + "|\n"

        break

readme_template = open("templates/readme_template.md", "r").read()
readme_template = readme_template.replace("%table%", markdown)

f = open("results/working_clients.md", "w", encoding="utf-8")
f.write(markdown)
f.close()

f = open("results/working_clients.txt", "w")
f.write(working_clients_output)
f.close()

f = open("results/working_unique_versions.txt", "w")
for v in working_versions:
    f.write(v + "\n")
f.close()

f = open("readme.md", "w", encoding="utf-8")
f.write(readme_template)
f.close()
