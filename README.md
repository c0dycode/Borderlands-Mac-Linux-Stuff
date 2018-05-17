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

### Mac (not tested/confirmed yet)
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

### Mac (not tested/confirmed yet)
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

# Credits and Thanks
- Me this time around, since the windows-version Bypasses were of no use
- Apocalyptech for testing and confirming the Linux-version bypasses