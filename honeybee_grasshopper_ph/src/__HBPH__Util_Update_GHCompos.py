"""
Updates all the GH-Components in the Source dir (Github)
-
EM April 22, 2022
"""

ghenv.Component.Name = "__HBPH__Util_Update_GHCompos"
ghenv.Component.NickName = "HBPH_Update_Source"
ghenv.Component.Message = 'APR_22_2022'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Honeybee-PH"
ghenv.Component.SubCategory = "00 | Utils"

import os
import Grasshopper.Kernel as ghK
import shutil


class AllComponents():
    def __init__(self, _source_dir, _ghdoc, _ghK):
        self.source_dir = _source_dir
        self.compos = []
        self.ghdoc = _ghdoc
        self.ghK = _ghK
    
    def __enter__(self):
        print('Adding all the Components to the Canvas')
        ghuserFileNames = os.listdir(self.source_dir)
        
        for eachCompoName in ghuserFileNames:
            if '.' == eachCompoName[0]: continue # Fucking Mac OS....
            if 'HBPH' not in eachCompoName: continue
            if '__' == eachCompoName[:2]: continue
            
            compo_address = self.source_dir + eachCompoName
            compo = self.ghK.GH_UserObject(compo_address).InstantiateObject()
            self.ghdoc = ghenv.Component.OnPingDocument()
            self.ghdoc.AddObject(compo, False)
            
            self.compos.append(compo)
            
        return self
      
    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('Cleaning Up the Canvas')
        for compo in self.compos:
            self.ghdoc.RemoveObject(compo, False)


def copy_py_code(_save_address):
    """Copy all the PyPH ghuser python code on the Canvas to another folder"""
    print '- '*25, 'Writing GHUser Component Python code to file', '- '*25
    
    doc = ghenv.Component.OnPingDocument()
    objs = list(doc.Objects)
    
    for obj in objs:    
        if obj.Category not in ['Honeybee-PH', 'HB-PH']:
            continue
        
        if 'Code' not in dir(obj):
            # -- Value Lists items don't have Py code
            continue
        
        if 'HBPH' in obj.Name[:10]:
            address = _save_address + obj.Name + '.py'
            
            if os.path.exists(address):
                os.remove(address)
            
            print 'Writing {} code to: --> {}'.format(obj.Name, address)
            with open(address, 'wb') as f:
                code_text = obj.Code.replace("\", "\").encode('utf-8')
                for line in code_text.split("\"):
                    f.write(line)


def copy_ghuser(_source_address, _save_address):
    """Copy the HBPH ghuser component on the Canvas over to another folder"""
    print '- '*25, 'Copying GHUser Component Files', '- '*25
    
    doc = ghenv.Component.OnPingDocument()
    objs = list(doc.Objects)
    
    for obj in objs:
        if obj.Category not in ['Honeybee-PH', 'HB-PH']:
            continue
        
        if 'HBPH' in str(obj.Name)[:10]:
            srcAddress = _source_address + obj.Name + '.ghuser'
            saveAddress = _save_address + obj.Name + '.ghuser'
            
            print 'Copying: {} --> {}'.format(srcAddress, saveAddress)
            
            if os.path.exists(srcAddress):
                shutil.copy(srcAddress, saveAddress)


def make_dir(_dir_address):
    if not os.path.exists(_dir_address):
        try:
            os.mkdir(_dir_address)
        except:
            _dir_address = False
            print('Please provide a valid save directory. Maybe try adding/removing the backslash to the end?')



if _runIt:
    #------ Sort out the folders
    source_dir = str(r"/Users/em/Library/Application Support/McNeel/Rhinoceros/7.0/Plug-ins/Grasshopper (b45a29b1-4343-4035-989e-044e8580d9cf)/UserObjects/honeybee_ph/user_objects/")
    save_dir_ghuser    = str(r"/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/honeybee_ph/honeybee_grasshopper_ph/user_objects/")
    save_dir_ghuser_py = str(r"/Users/em/Dropbox/bldgtyp-00/00_PH_Tools/honeybee_ph/honeybee_grasshopper_ph/src/")

    with AllComponents(source_dir, ghdoc, ghK):
        copy_ghuser(source_dir, save_dir_ghuser) #----- Copy over the HBPH GH-Components
        copy_py_code(save_dir_ghuser_py) #----- Copy over all the PY Code from HBPH GH-Components