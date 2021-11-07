# osu MapID to Collection DB 

**You will need Python 3 installed to run this**

**Note: Some collection names or HTML/HTM names may cause issues. If you get errors try using a basic name such as `collection.db` or `collection.html` instead.**

## How to use for osu!Collector collections:
1. Run "launcher.py", enter "y" to the osu!Collector prompt, enter the osu!Collector collectionID or URL, your API key and the output path for the collection DB. 

    Note: osu!Collector pages (one page = 100 maps) are grabbed at 1 per 5 seconds.
2. You should have your collection.

## How to use a HTML/HTM file:
1. Run "launcher.py", enter "y" to the HTML/HTM prompt, enter in the path to the HTML/HTM file, your API key and the output path for the collection DB. 


    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.

## How to use with manual mapID list:
1. Add your list of mapIDs, map links, or set links to "list.txt". (Raw setIDs are not supported. Make sure your setIDs have the prefix of either `https://osu.ppy.sh/s/` or `https://osu.ppy.sh/beatmapsets/`)
2. Run "launcher.py", enter in your API key and the output path for the collection DB.

    Note: osu! api calls (for converting mapID to MD5 and converting setIDs to mapIDs) are done at 1 per second.
3. You should have your collection.
