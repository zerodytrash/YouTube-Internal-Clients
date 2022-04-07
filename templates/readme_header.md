# YouTube-Internal-Clients

A script that discovers hidden internal clients of the YouTube (Innertube) API using bruteforce methods. The script tries `clientNames` with a sequential ID enumeration and crosses them with known `clientVersions`.
The goal was to find a client that has no age restrictions implemented. With success.

## Contributors
- [@MinePlayersPE](https://github.com/MinePlayersPE) - Mapped some version numbers in a [Gist](https://gist.github.com/MinePlayersPE/9875f2051c2dfdeb090543b8c6a9f7e6), which helped a lot
- [@89z](https://github.com/89z) - Helped to find some missing clients and version numbers 

## Results

The script has found the following working clients tested on [this](https://www.youtube.com/watch?v=%videoId%) video:

