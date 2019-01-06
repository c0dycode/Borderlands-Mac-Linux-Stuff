# Info
On Linux the filesizes are about:

BL2 (36.4MB)

TPS (35.8MB)

and should be located somewhere here:

~/.steam/steam/steamapps/common/

For Mac:
BL2 (66.7MB)
TPS (60.5MB)

You'll most likely have moved a Patchfile into the "Binaries"-folder before, if you're here.
From there, you go up two folders. You should now see a folder called "MacOS". 
You be at something like:

Borderlands2.app\Contents\MacOS

Inside of that, there should be the file that you need to edit!


# BL2
## SanityCheck Bypass
### Linux
- Items
```
E8 A9 24 17 00
to
90 90 90 90 90
```

- Weapons
```
E8 F7 23 17 00
also to
90 90 90 90 90
```

### Mac
- Items
```
E8 FE A1 28 00
to
90 90 90 90 90
```

- Weapons
```
E8 58 A1 28 00
to
90 90 90 90 90
```
## Currencies (Not tested/confirmed yet)
### Linux
- Cash:
Address: 01BC886C
Default: FF E0 F5 05

- Eridium:
Address: 01BC8870
Default: F4 01 00 00

- Seraph:
Address: 01BC8874
Default: E7 03 00 00

- Torgue:
Address: 01BC887C
Default: E7 03 00 00

### Mac
For the values you need to change it to, refer to this:
https://github.com/c0dycode/BL2ModStuff/tree/master/Hexediting#increasing-max-eridium

Address is the address in the file you have to patch. Every Hexeditor should have a "goto"-feature these days.
Double check if your values match up with the default ones, listed below!

- Cash:
Address: 01A1D90C
Default: FF E0 F5 05

- Eridium:
Address: 01A1D910
Default: F4 01 00 00

- Seraph:
Address: 01A1D914
Default: E7 03 00 00

- Torgue:
Address: 01A1D91C
Default: E7 03 00 00

## Backpack
### Linux
- Not yet available

### Mac
```
Go to file-offset: 009DF51A
Find 
B9 27 00 00 00 0F

Change the 27 to the hexvalue you want your inventory to be.
For 100 Inventoryslots use 64 for example.
```

# TPS
## SanityCheck-Bypass
### Linux
- Items
```
E8 CF 94 17 00
to
90 90 90 90 90
```

- Weapons
```
E8 0D 94 17 00
to
90 90 90 90 90
```

### Mac
- Items
```
E8 0B 4A CF FF
to
90 90 90 90 90
```

- Weapons
```
E8 4F 49 CF FF
to
90 90 90 90 90
```

## Backpack
### Linux
- Not yet available

### Mac
```
Go to file-offset: 006B955A
Find 
B8 27 00 00 00 0F

Change the 27 to the hexvalue you want your inventory to be.
For 100 Inventoryslots use 64 for example.
```

# Credits and Thanks
- Me this time around, since the windows-version Bypasses were of no use
- Apocalyptech for testing and confirming the Linux-version bypasses, double/tripple checking things and Linux Currency offsets
- mopioid for testing and confirming the Mac-version bypasses
- wufeehd for testing Mac BL2 Backpack-patch
