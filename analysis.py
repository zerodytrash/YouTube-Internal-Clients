from email import charset
import mimetypes
from os import listdir
from urllib import response
import json

markdown = ""
markdown += "| Client Name | Client Version | Quality Formats | Features |\n"
markdown += "|-------------|----------------|-----------------|----------|\n"

txt_output = ""

files = listdir('results')

client_ids = []

for file in files:
    client_id = int(file.split('_')[0])
    if client_id not in client_ids:
        client_ids.append(client_id)

client_ids.sort()

for client_id in client_ids:
    client_files = [file for file in files if file.startswith(str(client_id) + '_')]
    client_files.sort(reverse=True) # highest version first 

    for client_file in client_files:
        response_data_raw = open('results/' + client_file, 'r', encoding='utf-8').read()
        response_data = json.loads(response_data_raw)

        client_name = None
        client_version = client_file.split('_')[1].replace('.json', '')
        has_hls_format = ".m3u8" in response_data_raw
        has_mpeg_dash = "dashManifest" in response_data_raw

        try:
            client_name = response_data_raw.split('&c=')[1].split('&')[0]
        except Exception as ex:
            continue
        
        txt_output += client_name + ";" + client_version + "\n"

        formatsStr = "<details><summary>Formats</summary>"

        if response_data.get('streamingData'):
            formats = response_data.get('streamingData').get('formats')
            if formats is not None and len(formats) > 0:
                for format in formats:
                    formatsStr += str(format.get("itag")) + " - " + str(format.get("qualityLabel")) + " - " + str(format.get("fps")) + " FPS - " + str(format.get("mimeType")).split(';')[0] + "<br>"

        formatsStr += "</details>"

        adaptiveFormatsStr= "<details><summary>Adaptive Formats</summary>"

        if response_data.get('streamingData'):
            formats = response_data.get('streamingData').get('adaptiveFormats')
            if formats is not None and len(formats) > 0:
                for format in formats:
                    adaptiveFormatsStr += str(format.get("itag")) + " - " + str(format.get("qualityLabel")) + " - " + str(format.get("fps")) + " FPS - " + str(format.get("mimeType")).split(';')[0] + "<br>"

        adaptiveFormatsStr += "</details>"

        extraInfo = ""
        if has_hls_format:
            extraInfo += "&bull; HLS Support"

        if has_mpeg_dash:
            extraInfo += "&bull; MPEG-DASH Support"


        markdown += client_name + "|" + client_version + "|" + formatsStr + adaptiveFormatsStr + "|" + extraInfo  + "|\n"

        break

f = open("working_clients.md", "w")
f.write(markdown)
f.close()

f = open("working_clients.txt", "w")
f.write(txt_output)
f.close()