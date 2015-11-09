# OpenPPL Creator

OpenPPL Creator is a tool used to order your openPPL code a bit better.

## Features
- Read your source .oppl and .ohf and combine it (read recursive directories).
- Accept hands format like 66+ or A5s+.
- Auto create lists from range 0 to 100.
- Accept configuration for each openPPL file.
- Option to calculate and add % range for current hand lists.

## Instalation
### Linux
```bash
git clone https://github.com/MacedonianTree/openppl-creator
sudo mv openppl-creator /opt/
sudo chmod +x /opt/openppl-creator/openppl-creator
sudo ln -s /opt/openppl-creator/openppl-creator /usr/bin/
```

## Usage
Copy template where you want, write your code, change default config and just run in console:
```bash
openppl-creator
```