#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright (c) 2018, CJ Kucera
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# This is just a short little commandline app to enable/disable the "sanity
# checks" in the Linux version of Borderlands 2 and Borderlands: The Pre-Sequel.
# That sanity check is in the game to prevent weird/broken/hacked gear.  This
# can happen when using mods from the Borderlands community, since the valid
# partlists for various items and weapons are often altered to accomodate the
# mods.
#
# Note that this does NOT create any backups of your binaries, though a file
# verification via Steam would fix it up for you.  The utility will NOT operate
# on a file which doesn't look "right."
#
# There are no commandline flags.  Perhaps there should be?
#
# Sample interaction:
#     
#     $ ./borderlands_sanity_linux.py 
#     
#     Found Borderlands 2
#       Item Sanity Check State: Edited (sanity checks OFF)
#       Weapon Sanity Check State: Edited (sanity checks OFF)
#     
#     Choose an option:
#       [E]nable the sanity checks
#       [Q]uit
#       (any other input will skip)
#     
#     Your Choice For Borderlands 2> 
#     
#     Found Borderlands: The Pre-Sequel
#       Item Sanity Check State: Edited (sanity checks OFF)
#       Weapon Sanity Check State: Edited (sanity checks OFF)
#     
#     Choose an option:
#       [E]nable the sanity checks
#       [Q]uit
#       (any other input will skip)
#     
#     Your Choice For Borderlands: The Pre-Sequel> 

import os
import sys

class Game(object):
    """
    Simple object to hold information about a game and perform some
    operations on it.
    """

    # The closest we can get to an enum without getting crazy
    (STATE_STOCK,
        STATE_EDITED,
        STATE_UNKNOWN) = range(3)

    # English versions of states
    STATE_2_ENG = {
            STATE_STOCK: 'Stock (sanity checks ON)',
            STATE_EDITED: 'Edited (sanity checks OFF)',
            STATE_UNKNOWN: 'Unknown',
        }

    def __init__(self,
            library_folders,
            name,
            directory,
            binary_name,
            app_manifest,
            item_sanity_loc,
            item_sanity_bytes,
            weapon_sanity_loc,
            weapon_sanity_bytes,
            ):
        self.name = name
        self.directory = directory
        self.binary_name = binary_name
        self.app_manifest = app_manifest
        self.item_sanity_loc = item_sanity_loc
        self.item_sanity_bytes = item_sanity_bytes
        self.weapon_sanity_loc = weapon_sanity_loc
        self.weapon_sanity_bytes = weapon_sanity_bytes

        # Grab our binary file location if we can, and get our
        # initial state
        self.binary_file = self.get_binary_location(library_folders)
        self.set_state()

    def set_state(self):
        """
        Sets the state of the binary
        """
        self.item_state = self.get_item_state()
        self.weapon_state = self.get_weapon_state()

    def get_game_dir(self, library_folders):
        """
        Find our game directory inside the list of `library_folders`.
        Returns a string with the library folder path.
        """
        for folder in library_folders:
            if os.path.exists(os.path.join(folder, self.app_manifest)):
                return folder
        return None

    def get_binary_location(self, library_folders):
        """
        Given a list of `library_folders`, return the path to the
        main binary for the game.
        """
        library_folder = self.get_game_dir(library_folders)
        if library_folder:
            binary_file = os.path.join(library_folder,
                    'common',
                    self.directory,
                    self.binary_name)
            if os.path.exists(binary_file):
                return binary_file
        return None

    def get_edit_state(self, location, byte_string):
        """
        Returns the state of the specified `location` versus the given
        `byte_string`
        """
        if self.binary_file:
            with open(self.binary_file, 'rb') as df:
                df.seek(location)
                data = df.read(len(byte_string))
                if data == byte_string:
                    return Game.STATE_STOCK
                elif data == b'\x90' * len(byte_string):
                    return Game.STATE_EDITED
        return Game.STATE_UNKNOWN

    def get_item_state(self):
        """
        Returns the state of our item sanity check
        """
        return self.get_edit_state(self.item_sanity_loc,
                self.item_sanity_bytes)

    def get_weapon_state(self):
        """
        Returns the state of our weapon sanity check
        """
        return self.get_edit_state(self.weapon_sanity_loc,
                self.weapon_sanity_bytes)

    def write_bytes(self, location, byte_string):
        """
        Write the specified `byte_string` to the specified `location`
        """
        if self.binary_file:
            with open(self.binary_file, 'r+b') as df:
                df.seek(location)
                df.write(byte_string)

    def enable_sanity(self):
        """
        Enables sanity checks for this game
        """
        self.write_bytes(self.item_sanity_loc,
                self.item_sanity_bytes)
        self.write_bytes(self.weapon_sanity_loc,
                self.weapon_sanity_bytes)
        self.set_state()

    def disable_sanity(self):
        """
        Disables sanity checks for this game
        """
        self.write_bytes(self.item_sanity_loc,
                b'\x90' * len(self.item_sanity_bytes))
        self.write_bytes(self.weapon_sanity_loc,
                b'\x90' * len(self.weapon_sanity_bytes))
        self.set_state()

def get_steam_base_path():
    """
    Returns our base Steam installation path, based on a few of
    the likely locations.
    """

    path = os.path.expanduser('~/.steam/steam')
    if os.path.exists(path):
        return path

    path = os.path.expanduser('~/.local/share/Steam')
    if os.path.exists(path):
        return path

    raise Exception('Steam base path could not be found')

def get_steam_library_folders():
    """
    Returns a list of library folders where we might find Borderlands
    2/TPS installations.
    """

    base_path = get_steam_base_path()
    folders = []

    # Our base install is almost certainly a library folder itself.
    base_library = os.path.join(base_path, 'steamapps')
    if os.path.exists(base_library):
        folders.append(base_library)

    library_index = os.path.join(base_path,
            'steamapps',
            'libraryfolders.vdf')
    if os.path.exists(library_index):
        with open(library_index) as df:
            for line in df.readlines():
                parts = line.split()
                if len(parts) == 2:
                    parts = [p.strip('"') for p in parts]
                    try:
                        library_idx = int(parts[0])
                        library_dir = os.path.join(parts[1], 'steamapps')
                        if os.path.exists(library_dir):
                            folders.append(library_dir)
                    except ValueError as e:
                        pass

    return folders

# Get our list of Steam library folders
library_folders = get_steam_library_folders()

# Set up a list of games to try
games = [
        Game(name='Borderlands 2',
            library_folders=library_folders,
            directory='Borderlands 2',
            binary_name='Borderlands2',
            app_manifest='appmanifest_49520.acf',
            item_sanity_loc=0xD267F0,
            item_sanity_bytes=b'\xE8\xA9\x24\x17\x00',
            weapon_sanity_loc=0xD26870,
            weapon_sanity_bytes=b'\xE8\xF7\x23\x17\x00',
            ),
        Game(name='Borderlands: The Pre-Sequel',
            library_folders=library_folders,
            directory='BorderlandsPreSequel',
            binary_name='BorderlandsPreSequel',
            app_manifest='appmanifest_261640.acf',
            item_sanity_loc=0xCFE148,
            item_sanity_bytes=b'\xE8\xCF\x94\x17\x00',
            weapon_sanity_loc=0xCFE1C8,
            weapon_sanity_bytes=b'\xE8\x0D\x94\x17\x00',
            ),
    ]

if __name__ == '__main__':

	# Loop through and do hex-editing
	for game in games:
		if game.binary_file:
			do_stuff = True
			while do_stuff:
				print('')
				print('Found {}'.format(game.name))
				print('  Item Sanity Check State: {}'.format(Game.STATE_2_ENG[game.item_state]))
				print('  Weapon Sanity Check State: {}'.format(Game.STATE_2_ENG[game.weapon_state]))
				print('')
				if (game.item_state == Game.STATE_UNKNOWN or
						game.weapon_state == Game.STATE_UNKNOWN):
					do_stuff = False
					print('Refusing to do anything with the binary in an unknown state!')
					print('')
					print('Press Enter to Continue...')
					sys.stdin.readline()
				else:
					offer_disable = (game.item_state == Game.STATE_STOCK or
							game.weapon_state == Game.STATE_STOCK)
					offer_enable = (game.item_state == Game.STATE_EDITED or
							game.weapon_state == Game.STATE_EDITED)
					print('Choose an option:')
					if offer_disable:
						print('  [D]isable the sanity checks')
					if offer_enable:
						print('  [E]nable the sanity checks')
					print('  [Q]uit')
					print('  (any other input will skip)')
					print('')
					sys.stdout.write('Your Choice For {}> '.format(game.name))
					sys.stdout.flush()
					user_input = sys.stdin.readline().strip().lower()
					if offer_disable and user_input == 'd':
						game.disable_sanity()
					elif offer_enable and user_input == 'e':
						game.enable_sanity()
					elif user_input == 'q':
						sys.exit(1)
					else:
						do_stuff = False
		else:
			print('')
			print('Install directory for "{}" not found.'.format(game.name))
			print('')
			print('Press Enter to Continue...')
			sys.stdin.readline()
