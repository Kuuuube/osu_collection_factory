# osu! Collection Factory

## Dependencies:
- Python 3.10: [Download link](https://www.python.org/downloads/)
- Python `requests` and `dotenv` modules: To install them enter the following commands in cmd or a terminal: 

    ```
    pip install requests
    ```
    ```
    pip install python-dotenv
    ```
*Need hundreds of osu!Collector collections, a dump of the entire site, or archives of deleted
 collections? Join my [discord server](https://discord.gg/T5vEAh4ruF) for downloads.*

## How to dump osu!Collector collections:
1. Run "main.py", enter "1" to the prompt
2. Choose if you want any special sorting, and enter the osu!Collector collection ID or URL.
3. You should have your collection. <sup>[1](#1)</sup>

## How to dump from a file:
1. Run "main.py", enter "2" to the prompt
2. Enter the path to the file, and your API key.
3. You should have your collection.<sup>[2](#2)</sup>

## How to use with manual map ID list:
1. Add your list of map urls, or set urls to "list.txt". 
2. Run "main.py", enter "2" to the prompt, leave the path to the file blank, and enter your API key if not using `.env`.
3. You should have your collection.<sup>[2](#2)</sup>

## How to save your osu!api key:
1. Create file named `.env`
2. In `.env` write the following: `KEY="Your osu!api key here"`

You'll now be able to make osu!api calls without having to enter your key manually.

## How to change default collection name or path:
`settings.json` - if not found - is created with the default collection path and with the default collection name.
If you wish to change any of these, run `main.py`, enter "3", and follow the prompt to change the respective setting. (Recommended)
You can also change the values manually but the script with verify the paths you enter automatically.

### Notes:
<a name="1">1</a>: When downloading with a star rating or bpm filter, osu!Collector pages (one page = 100 maps) are
                   grabbed at 1 per second. Otherwise, all maps are grabbed instantly and all at once.

<a name="2">2</a>: osu!api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.

<br>

###### Huge thanks to [The1Divider](https://github.com/The1Divider) for his contributions to the project.
