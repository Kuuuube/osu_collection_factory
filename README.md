# osu! Collection Factory

## Dependencies:

- Python 3: [Download link](https://www.python.org/downloads/)
- Python `requests` and `dotenv` modules: To install them enter the following commands in cmd or a terminal: 

    ```
    pip install requests
    ```
    ```
    pip install python-dotenv
    ```

**Note: Some collection names or file names may cause issues. If you get errors try using a basic name such as `collection.db` or `collection.html` instead.**

## How to dump osu!Collector collections:
1. Run "main.py", enter "1" to the prompt, choose if you want any special sorting, and enter the osu!Collector collectionID or URL. 

    Note: When downloading with a star rating or bpm filter, osu!Collector pages (one page = 100 maps) are grabbed at 1 per second. Otherwise all maps are grabbed instantly and all at once.
2. You should have your collection.

Need hundreds of osu!Collector collections, a dump of the entire site, or archives of deleted collections? Join my [discord server](https://discord.gg/T5vEAh4ruF) for downloads.

## How to dump from a file:
1. Run "main.py", enter "2" to the prompt, enter in the path to the file, and your API key. 

    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.

## How to use with manual mapID list:
1. Add your list of mapIDs, map links, or set links to "list.txt" (the default "list.txt" path is `..\list.txt`). (Raw setIDs are not supported. Make sure your setIDs have the prefix of either `https://osu.ppy.sh/s/` or `https://osu.ppy.sh/beatmapsets/`)
2. Run "main.py", enter in the path to the file, and your API key. 

    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.

</br>

###### Huge thanks to [The1Divider](https://github.com/The1Divider) for his contributions to the project.
