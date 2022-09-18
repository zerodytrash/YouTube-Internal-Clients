# YouTube-Internal-Clients

A script that discovers hidden internal clients of the YouTube (Innertube) API using bruteforce methods. The script tries `clientNames` with a sequential ID enumeration and crosses them with known `clientVersions`.
The goal was to find a client that has no age restrictions implemented. With success.

- [Clients](#clients)
- [Example Request](#example-request)
- [Params](#params)
- [API Keys](#api-keys)
- [Contributors](#contributors)

## Clients

The script has found the following working clients:

%table%

## Example Request
```http
POST /youtubei/v1/player?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8 HTTP/2
Host: www.youtube.com
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42
Accept: */*
Origin: https://www.youtube.com
Referer: https://www.youtube.com/
Accept-Encoding: gzip, deflate
Accept-Language: de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6

{
    "context": {
        "client": {
            "hl": "en",
            "gl": "US",
            "clientName": "WEB",
            "clientVersion": "2.20220916.00.00",
            "clientScreen": "WATCH",
            "androidSdkVersion": 31
        },
        "thirdParty": {
            "embedUrl": "https://www.youtube.com/"
        }
    },
    "videoId": "yvyAQiiKIN8",
    "playbackContext": {
        "contentPlaybackContext": {
            "signatureTimestamp": 19250
        }
    },
    "racyCheckOk": true,
    "contentCheckOk": true
}
```

## Params
| Param       | Description |
|-------------|-------------|
| `embedUrl`  | Required for some videos when using an embedded client. e.g. `WEB_EMBEDDED_PLAYER` |
| `signatureTimestamp` |  Required for web-based clients for videos with copyright claims (Stream URLs must be deciphered)
| `racyCheckOk`, `contentCheckOk` | Skips content warnings.
| `androidSdkVersion` | Partially required for Android clients. A corresponding user agent must also be set. (e.g. `com.google.android.youtube/17.10.35 (Linux; U; Android 12; GB) gzip`) (see [issue](https://github.com/zerodytrash/YouTube-Internal-Clients/issues/3))

## API Keys
| Name                      | Key                                       |
|---------------------------|-------------------------------------------|
| YouTube Web               | `AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8` |
| YouTube Web Kids          | `AIzaSyBbZV_fZ3an51sF-mvs5w37OqqbsTOzwtU` |
| YouTube Web Music         | `AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30` |
| YouTube Web Creator       | `AIzaSyBUPetSUmoZL-OhlxA7wSac5XinrygCqMo` |
| YouTube Android           | `AIzaSyA8eiZmM1FaDVjRy-df2KTyQ_vz_yYM39w` |
| YouTube Android Music     | `AIzaSyAOghZGza2MQSZkY_zfZ370N-PUdXEo8AI` |
| YouTube Android Embedded  | `AIzaSyCjc_pVEDi4qsv5MtC2dMXzpIaDoRFLsxw` |
| YouTube Android Creator   | `AIzaSyD_qjV8zaaUMehtLkrKFgVeSX_Iqbtyws8` |
| YouTube IOS               | `AIzaSyB-63vPrdThhKuerbB2N_l7Kwwcxj6yUAc` |
| YouTube IOS Music         | `AIzaSyBAETezhkwP0ZWA02RsqT1zu78Fpt0bC_s` |

## Contributors
- [@MinePlayersPE](https://github.com/MinePlayersPE) - Mapped some version numbers in a [Gist](https://gist.github.com/MinePlayersPE/9875f2051c2dfdeb090543b8c6a9f7e6), which helped a lot
- [@89z](https://github.com/89z) - Helped to find some missing clients and version numbers 
