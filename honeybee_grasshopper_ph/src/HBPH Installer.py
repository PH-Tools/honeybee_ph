#
# Honeybee-PH: A Plugin for adding Passive-House data to LadybugTools Honeybee-Energy Models
# 
# This component is part of the PH-Tools toolkit <https://github.com/PH-Tools>.
# 
# Copyright (c) 2022, PH-Tools and bldgtyp, llc <phtools@bldgtyp.com> 
# Honeybee-PH is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Honeybee-PH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# For a copy of the GNU General Public License
# see <https://github.com/PH-Tools/honeybee_ph/blob/main/LICENSE>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
This component installs/updates the 'Honeybee-PH' plugin libraries for Ladybug Tools.
Please make sure that you gave Ladybug Tools with Honeybee-Energy fully installed before
proceeding with this installation. Make sure you are connected to the internet in 
order to download the latest version of the plugin libraries and components.
-
This tool will download and install several new libraries into the Ladybug Tools
python interpreter, and will download and install new Grasshopper components.
-
EM May 14, 2022
    Args:
        _install: (bool) Set to True to install Honeybee-PH on your computer.
        _branch_: (str) Optional branch to download. Default = 'main'
"""

ghenv.Component.Name = 'HBPH Installer'
ghenv.Component.NickName = 'HBPHInstall'
ghenv.Component.Message = 'DEV | MAY_14_2022'
ghenv.Component.Category = 'Honeybee-PH'
ghenv.Component.SubCategory = '0 | Installer'
ghenv.Component.AdditionalHelpFromDocStrings = '0'


from exceptions import IOError
from distutils import dir_util
import shutil
import System
import os
import urllib
import zipfile

import Rhino
from Grasshopper.Folders import UserObjectFolders
from Grasshopper.Kernel import GH_RuntimeMessageLevel as Message

import honeybee


def nukedir(target_dir, rmdir=False):
    # type: (str, bool) -> None
    """Delete all the files inside target_dir.

    This function has been copied from ladybug.futil.
    """
    d = os.path.normpath(target_dir)
    if not os.path.isdir(d):
        return
    
    files = os.listdir(d)
    for f in files:
        if f == '.' or f == '..':
            continue
        path = os.path.join(d, f)

        if os.path.isdir(path):
            nukedir(path)
        else:
            try:
                os.remove(path)
            except Exception as e:
                print e
                print("Failed to remove %s" % path)

    if rmdir:
        try:
            os.rmdir(d)
        except Exception:
            try:
                dir_util.remove_tree(d)
            except Exception as e:
                print e
                print("Failed to remove %s" % d)


def copy_file_tree(source_folder, dest_folder, overwrite=True):
    """Copy an entire file tree from a source_folder to a dest_folder.

    Args:
        source_folder: The source folder containing the files and folders to
            be copied.
        dest_folder: The destination folder into which all the files and folders
            of the source_folder will be copied.
        overwrite: Boolean to note whether an existing folder with the same
            name as the source_folder in the dest_folder directory should be
            overwritten. Default: True.
    """
    # make the dest_folder if it does not exist
    if not os.path.isdir(dest_folder):
        os.mkdir(dest_folder)
        

    # recursively copy each sub-folder and file
    for f in os.listdir(source_folder):
        # get the source and destination file paths
        src_file_path = os.path.join(source_folder, f)
        dst_file_path = os.path.join(dest_folder, f)

        # if overwrite is True, delete any existing files
        if overwrite:
            if os.path.isfile(dst_file_path):
                try:
                    os.remove(dst_file_path)
                except Exception:
                    raise IOError("Failed to remove %s" % f)
            elif os.path.isdir(dst_file_path):
                nukedir(dst_file_path, True)

        # copy the files and folders to their correct location
        if os.path.isfile(src_file_path):
            shutil.copyfile(src_file_path, dst_file_path)
        elif os.path.isdir(src_file_path):
            if not os.path.isdir(dst_file_path):
                os.mkdir(dst_file_path)
            copy_file_tree(src_file_path, dst_file_path, overwrite)


def get_paths(_repo="honeybee_ph", _branch='main'):
    # type: () -> Tuple[str, str]
    """Return the location of the url to download, and the target file location to save to."""
    
    download_url = "https://github.com/PH-Tools/{}/archive/refs/heads/{}.zip".format(_repo, _branch)
    download_folder = honeybee.config.folders.python_package_path
    download_file = os.path.join(download_folder, "main.zip")
    
    return download_url, download_file


def check_lbt_version(_min_version_allowed):
    # type: (Tuple[int, int, int]) -> None
    lbt_version_installed = honeybee.config.folders.honeybee_core_version # -> (1, 51, 8)
    
    for ver_num in zip(lbt_version_installed, _min_version_allowed):
        assert lbt_version_installed >= _min_version_allowed, "Warning: Honeybee-PH is not "\
            "compatible with the version of Ladybug Tools installed on this computer. Please "\
            "update your Ladybug Tools installation to the latest version before proceeding "\
            "with the installation. You can use the Ladybug 'LB Versioner' component to update "\
            "your installation, and then restart Rhino before trying again."


def download_honeybee_ph_from_github(_download_url, _download_file):
    # type: (str, str) -> str
    """Download the specified URL to the specified location on this computer."""
    try:
        urllib.urlretrieve(_download_url, _download_file)
        print "Downloaded the file: ", _download_url
        print "To: ", _download_file
        return _download_file
    except IOError as e:
        msg = "There was an error downloading the Honeybee-PH pacakge to your computer."\
            "If you have Ladybug Tools installed in you 'ProgramFiles' directory, (ie: if you"\
            "are using Pollination instead of the Food4Rhino LBT installer) you may"\
            "need to run Rhino 'as administrator' in order to install to this directory?"
        raise IOError(msg)
    except Exception as e:
        msg = "Error downloading the Honeybee-PH package to your computer."
        raise e


def unzip_file(source_file):
    # type: (str) -> None
    """Unzip a compressed file.
    
    Arguments:
    ----------
        * source_file: (str) Full path to a valid compressed file (e.g. c:/ladybug/testPts.zip)
    Returns:
    --------
        * unzip_folde: (str) The full path to the folder unzipped
    """
    dest_dir, fname = os.path.split(source_file)
    
    # extract files to destination
    with zipfile.ZipFile(source_file) as zf:
        for member in zf.infolist():
            words = member.filename.split('\\')
            for word in words[:-1]:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir, ''):
                    continue
                dest_dir = os.path.join(dest_dir, word)
            zf.extract(member, dest_dir)
    
    return os.path.join(dest_dir, zf.infolist()[0].filename.replace('/', ''))


def copy_honeybee_ph_py_packages(_unzipped_src_dir):
    # type: (str) -> None
    """Copy the Honeybee-PH core Python libraries from the unzip-folder up one folder level."""
    
    # get the folder 'up' one level from the unzipped source dir.
    site_pckgs_folder = os.path.split(_unzipped_src_dir)[0]
    
    print '- '*25
    print 'Copying Honeybee-PH Python Packages to: {}'.format(site_pckgs_folder)
    
    src_dirs_to_exclude = ['tests', 'docs', 'diagrams', 'honeybee_grasshopper_ph'] # don't copy these to site-packages
    for dir in os.listdir(_unzipped_src_dir):
        if dir in src_dirs_to_exclude:
            continue
        if not os.path.isdir(os.path.join(_unzipped_src_dir, dir)):
            continue

        copy_file_tree(os.path.join(_unzipped_src_dir, dir), os.path.join(site_pckgs_folder, dir))


def copy_honeybee_ph_ghcomponents(_unzipped_src_dir, _gh_user_objects_folder):
    # type: (str, str) -> None
    """Copy all of the GH-User objects from the unzipped source dir over the Grasshopper UserObjects dir."""
    
    hbph_gh_source_folder = os.path.join(_unzipped_src_dir, 'honeybee_grasshopper_ph', 'user_objects')
    target = os.path.join(_gh_user_objects_folder[0], 'honeybee_grasshopper_ph')
    
    print '- '*25
    print 'Copying Honeybee-PH Grasshoppper Components to: {}'.format(target)
    
    copy_file_tree(hbph_gh_source_folder, target)


def give_popup_message(message, window_title=''):
    """Give a Windows popup message with an OK button.

    Useful in cases where you really need the user to pay attention to the message.

    Args:
        message: Text string for the popup message.
        window_title: Text string for the title of the popup window. (Default: "").
    """
    icon = System.Windows.Forms.MessageBoxIcon.Information
    buttons = System.Windows.Forms.MessageBoxButtons.OK
    Rhino.UI.Dialogs.ShowMessageBox(message, window_title, buttons, icon)


if _install:
    # --------------------------------------------------------------------------
    # -- Check version compatibility
    honeybee_ph_version = '0.1'
    lbt_min_version = (1, 51, 8)
    check_lbt_version(lbt_min_version)
    
    
    # --------------------------------------------------------------------------
    # -- download honeybee-ph from github
    download_url, download_file = get_paths('honeybee_ph', _branch_ or 'main')
    download_file = download_honeybee_ph_from_github(download_url, download_file)
    unzipped_folder = unzip_file(download_file)
    
    
    # --------------------------------------------------------------------------
    # -- copy honeybee-ph core libraries
    copy_honeybee_ph_py_packages(unzipped_folder)
    
    
    # --------------------------------------------------------------------------
    # -- copy honeybee-ph grasshopper component
    copy_honeybee_ph_ghcomponents(unzipped_folder, UserObjectFolders)
    
    
    # ------------------------------------------------------------------------------------------
    # give a success message
    success_msg = 'Honeybee-PH {} has been successfully installed'.format(honeybee_ph_version)
    restart_msg = 'RESTART RHINO to load the new components + library.'
    for msg in (success_msg, restart_msg):
        print(msg)
    give_popup_message(''.join([success_msg, restart_msg]), 'Installation Successful!')
    
    
    # ------------------------------------------------------------------------------------------
    # remove the downloaded folder
    nukedir(unzipped_folder, True)
    os.remove(download_file)
    
    
else:  # give a message to the user about what to do
    print 'Make sure you have installed Ladybug Tools (v1.4.1 or newer), are connected to the internet, and set _install to True!'