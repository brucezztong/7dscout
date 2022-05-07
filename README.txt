7 Days POI Scout

This little application is provided as-is. I needed a tool, so I threw one
together. I started with some code from Liam Brandt, found on GitHub. Since
Liam's code was covered by the GPLv3, this effort is also covered by the GPLv3
as a derivitive work.

This code is provided without any promise of support beyond what you find in
this file. It is not my goal to support it as a tool. You're free to take it,
extend it, make it awesome, however you might want.

This application requires you have Python3 installed.

The application should work in either a Windows Command Shell or a BASH shell.
I'm partial to Linux (and Windows Subsystem for Linux) for tools like these,
but threw in a Windows BAT file for the convenience of others.

I run the application like this...

    1. Invoke a command line environment. (CMD or bash)

    2. cd to the poiscout directory.

    3. Issue this command (Windows)

        7dscout.bat <path-to-POIs>

    3. Issue this command (Linux, Mac or WSL)

        ./7dscout.py <path-to-POIs>

EXAMPLES:

    Windows:
        7dscout.bat "%APPDATA%\7DaysToDie\Mods\ZZTong-Prefabs\Prefabs\POIs"

    WSL:
       ./7dscout.py /mnt/c/Users/zzton/AppData/Roaming/7DaysToDie/Mods/ZZTong-Prefabs/Prefabs/POIs/ 

LIMITATIONS

The application does NOT know how to recurse through a tree of directories.
That means you have to scout out each directory individually. You cannot just
turn it loose on the top level directory.

The resulting files will be placed in the directory that was evaluated. You'll
get these files for each POI:

    7dscout-blocks.csv
    7dscout-loot.csv

LOOT.JSON

This file defines which blocks should appear in the loot reports. The "value",
uhh, value is unused. It was an aborted attempt to compute a POI's loot value
as if it could be rated. That's a much bigger analysis than I really needed to
do, so I dropped it.

OUTPUT FILES

The CSV files are text files but formatted such that you could open them with
a variety of tools, including spreadsheets and databases. Or, you can just use
your favorite text editor. Here's some example output:

    Block,Count
    cntWeaponsBagSmall,1
    cntWeaponsBagLarge,1
    cntAmmoPileSmall,1
    cntAmmoPileMedium,1
    cntFoodPileMedium,1
    cntBookcaseGoodRandomLootHelper,1
    cntBookcasePoorRandomLootHelper,5
    cntBagsRandomLootHelper,6
    cntCollapsedWorkbench,1
    cntShippingCrateHero,2
    cntShippingCrateLabEquipment,1
    cntShippingCrateCarParts,1
    cntShippingCrateConstructionSupplies,2
    cntLootCrateShamway,4
    cntHardenedChestSecure,1
    cntQuestRandomLootHelper,5
    cntChest01,1

There is 1 cntWeaponsBagLarge block in the POI.

ADVANCED USES

Combine this with grep, or many other command line text tools, and some handy
queries become available. Want to know which of your POIs contain a certain
block? Use "grep" (Linux, Mac) or "findstr" (Windows) on the *temp.blocks.csv
files and there's your list.
