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
EM April 28, 2022
    Args:
        _install: Set to True to install Honeybee-PH on your machine.
"""

ghenv.Component.Name = 'HBPH Installer'
ghenv.Component.NickName = 'HBPHInstall'
ghenv.Component.Message = 'DEV | APR_28_2022'
ghenv.Component.Category = 'Honeybee-PH'
ghenv.Component.SubCategory = '0 | Installer'
ghenv.Component.AdditionalHelpFromDocStrings = '0'


import os
import System.Net
import shutil
import uuid
import zipfile
from distutils import dir_util

import Rhino
from Grasshopper.Folders import UserObjectFolders
from Grasshopper.Kernel import GH_RuntimeMessageLevel as Message

def nukedir(target_dir, rmdir=False):
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



def get_python_exe():
    """Get the path to the Python installed in the ladybug_tools folder.

    Will be None if Python is not installed.
    """
    home_folder = os.getenv('HOME') or os.path.expanduser('~')
    py_install = os.path.join(home_folder, 'ladybug_tools', 'python')
    py_exe_file = os.path.join(py_install, 'python.exe') if os.name == 'nt' else \
        os.path.join(py_install, 'bin', 'python3')
    py_site_pack = os.path.join(py_install, 'Lib', 'site-packages') if os.name == 'nt' else \
        os.path.join(py_install, 'lib', 'python3.7', 'site-packages')
    if os.path.isfile(py_exe_file):
        return py_exe_file, py_site_pack
    return None, None


def get_honeybee_ph_directory():
    """Get the directory where measures distributed with Ladybug Tools are installed."""
    home_folder = os.getenv('HOME') or os.path.expanduser('~')
    py_install = os.path.join(home_folder, 'ladybug_tools', 'python')
    py_site_pack = os.path.join(py_install, 'Lib', 'site-packages') if os.name == 'nt' else \
        os.path.join(py_install, 'lib', 'python3.7', 'site-packages')
    if os.path.exists(py_site_pack):
        return py_site_pack
    return None



def download_file_by_name(url, target_folder, file_name, mkdir=False):
    """Download a file to a directory.

    This function has been copied from ladybug_rhino.download.

    Args:
        url: A string to a valid URL.
        target_folder: Target folder for download (e.g. c:/ladybug)
        file_name: File name (e.g. testPts.zip).
        mkdir: Set to True to create the directory if doesn't exist (Default: False)
    """
    # create the target directory.
    if not os.path.isdir(target_folder):
        if mkdir:
            preparedir(target_folder)
        else:
            created = preparedir(target_folder, False)
            if not created:
                raise ValueError("Failed to find %s." % target_folder)
    file_path = os.path.join(target_folder, file_name)

    # set the security protocol to the most recent version
    try:
        # TLS 1.2 is needed to download over https
        System.Net.ServicePointManager.SecurityProtocol = \
            System.Net.SecurityProtocolType.Tls12
    except AttributeError:
        # TLS 1.2 is not provided by MacOS .NET
        if url.lower().startswith('https'):
            print('This system lacks the necessary security'
                  ' libraries to download over https.')

    # attempt to download the file
    client = System.Net.WebClient()
    try:
        client.DownloadFile(url, file_path)
    except Exception as e:
        raise Exception(' Download failed with the error:{}'.format(e))


def unzip_file(source_file, dest_dir=None, mkdir=False):
    """Unzip a compressed file.

    This function has been copied from ladybug.futil.

    Args:
        source_file: Full path to a valid compressed file (e.g. c:/ladybug/testPts.zip)
        dest_dir: Target folder to extract to (e.g. c:/ladybug).
            Default is set to the same directory as the source file.
        mkdir: Set to True to create the directory if doesn't exist (Default: False)
    """
    # set default dest_dir and create it if need be.
    if dest_dir is None:
        dest_dir, fname = os.path.split(source_file)
    elif not os.path.isdir(dest_dir):
        if mkdir:
            preparedir(dest_dir)
        else:
            created = preparedir(dest_dir, False)
            if not created:
                raise ValueError("Failed to find %s." % dest_dir)

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


def give_warning(message):
    """Give a warning message (turning the component orange).

    Args:
        message: Text string for the warning message.
    """
    ghenv.Component.AddRuntimeMessage(Message.Warning, message)


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



def download_repo_github(repo, target_directory, version=None):
    """Download a repo of a particular version from from github.

    Args:
        repo: The name of a repo to be downloaded (eg. 'lbt-grasshopper').
        target_directory: the directory where the library should be downloaded to.
        version: The version of the repository to download. If None, the most
            recent version will be downloaded. (Default: None)
        """
    # download files
    url = "https://github.com/PH-Tools/{}/archive/refs/heads/main.zip".format(repo)
    zip_file = os.path.join(target_directory, '%s.zip' % repo)
    print 'Downloading "{}"  github repository to: {}/...'.format(repo, target_directory)
    download_file_by_name(url, target_directory, zip_file)

    # unzip the file
    unzip_file(zip_file, target_directory)

    # try to clean up the downloaded zip file
    try:
        os.remove(zip_file)
    except:
        print 'Failed to remove downloaded zip file: {}.'.format(zip_file)

    # return the directory where the unzipped files live
    if version is None:
        return os.path.join(target_directory, '{}-main'.format(repo))
    else:
        return os.path.join(target_directory, '{}-{}'.format(repo, version))


def copy_honeybee_ph_py_packages(source):
    
    site_pckgs_folder = os.path.split(source)[0]
    print '- '*25
    print 'Copying Honeybee-PH Python Packages to: {}'.format(site_pckgs_folder)
    
    src_dirs_to_exclude = ['tests', 'docs', 'diagrams', 'honeybee_grasshopper_ph'] # don't copy these to site-packages
    for dir in os.listdir(source):
        if dir in src_dirs_to_exclude:
            continue
        if not os.path.isdir(os.path.join(source, dir)):
            continue

        copy_file_tree(os.path.join(source, dir), os.path.join(site_pckgs_folder, dir))
    
def copy_honeybee_ph_ghcomponents(source, target):
    print '- '*25
    print 'Copying Honeybee-PH Grasshoppper Components to: {}'.format(target)

    copy_file_tree(source, target)
    
# versions of the Ladybug Tools libraries and resources to install
honeybee_ph = '0.1'


if _install:
    
    # ------------------------------------------------------------------------------------------
    # ensure that Python has been installed in the ladybug_tools folder
    home_folder = os.getenv('HOME') or os.path.expanduser('~')
    py_exe, py_lib = get_python_exe()
    assert py_exe is not None, \
        'No Python installation was found at: {}.This is a requirement in ' \
        'order to contine with installation'.format(
            os.path.join(home_folder, 'ladybug_tools', 'python'))


    # ------------------------------------------------------------------------------------------
    # install the honeybee-ph core libraries
    print 'Installing Honeybee-PH core Python libraries {}.'.format(honeybee_ph)
    honeybee_ph_dir = get_honeybee_ph_directory()
    download_folder = download_repo_github('honeybee_ph', honeybee_ph_dir)
    copy_honeybee_ph_py_packages(download_folder)

    
    
    # ------------------------------------------------------------------------------------------
    # install the grasshopper components
    print 'Installing Ladybug Tools Grasshopper components.'
    hbph_gh_source_folder = os.path.join(download_folder, 'honeybee_grasshopper_ph', 'user_objects')
    uo_folder = UserObjectFolders[0]
    hbph_uo_folder = os.path.join(uo_folder, 'honeybee_ph', 'user_objects')
    copy_honeybee_ph_ghcomponents(hbph_gh_source_folder, hbph_uo_folder)

    # ------------------------------------------------------------------------------------------
    # give a success message
    success_msg = 'Honeybee-PH {} has been successfully installed'.format(honeybee_ph)
    restart_msg = 'RESTART RHINO to load the new components + library.'
    for msg in (success_msg, restart_msg):
        print(msg)
    give_popup_message(''.join([success_msg, restart_msg]), 'Installation Successful!')

    # ------------------------------------------------------------------------------------------ 
    # remove the downloaded folder
    nukedir(download_folder, True)
    
else:  # give a message to the user about what to do
    print 'Make sure you have installed Ladybug Tools, are connected to the internet, and set _install to True!'