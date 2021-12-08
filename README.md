# osu MapID to Collection DB 

## Dependencies:

- Python 3: [Download link](https://www.python.org/downloads/)
- Python `requests` module: Enter this command in cmd or a terminal: `pip install requests`
- .NETCore 3.1.0: [Download link](https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-desktop-3.1.20-windows-x64-installer)

**Note: Some collection names or HTML/HTM names may cause issues. If you get errors try using a basic name such as `collection.db` or `collection.html` instead.**

## How to use for osu!Collector collections:
1. Run "launcher.py", enter "y" to the osu!Collector prompt, enter the osu!Collector collectionID or URL, and the output path for the collection DB. 

    Note: When downloading with a difficulty sort osu!Collector pages (one page = 100 maps) are grabbed at 1 per 5 seconds. Otherwise all maps are grabbed instantly and all at once.
2. You should have your collection.

Need hundreds of osu!Collector collections, a dump of the entire site, or archives of deleted collections? Join my [discord server](https://discord.gg/T5vEAh4ruF) for downloads.

## How to use a HTML/HTM file:
1. Run "launcher.py", enter "y" to the HTML/HTM prompt, enter in the path to the HTML/HTM file, your API key and the output path for the collection DB. 


    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.

## How to use with manual mapID list:
1. Add your list of mapIDs, map links, or set links to "list.txt". (Raw setIDs are not supported. Make sure your setIDs have the prefix of either `https://osu.ppy.sh/s/` or `https://osu.ppy.sh/beatmapsets/`)
2. Run "launcher.py", enter in your API key and the output path for the collection DB.

    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.

</br>

###### Huge thanks to [The1Divider](https://github.com/The1Divider) for his contributions to the project.