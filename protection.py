'''
protection.py
Created: Saturday, 22nd October 2022 2:21:59 pm
Matthew Riche
Last Modified: Saturday, 22nd October 2022 2:30:07 pm
Modified By: Matthew Riche

Sets up script nodes that run after file load, hoping to delete problematic nodes before they can
deliver their 'payload'
'''

import maya.cmds as cmds
import os

from . import nodes
from . import scriptjobs

def register_protection_script():
    """Puts a script job meant to delete problem nodes before they run.  Will execute on the next 
    file open
    """    

    print("Registering sr_anti_viral protection script.")
    # Backup userSetup.py
    backup_usersetup()
    # Create a script job that calls the clean-up modules.
    av_job = cmds.scriptJob(
        event=['PostSceneRead', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )
    av_early_job = cmds.scriptJob(
        event=['SceneOpened', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )
    av_reading_job = cmds.scriptJob(
        ct=['readingFile', 'sr_anti_viral.protection.full_clean()'], pro=True, ro=False
        )    
    print (
        "Protective 'post-scene-read' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_job, av_job)
        )
    print (
        "Protective 'scene-opened' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_early_job, av_early_job)
        )
    print (
        "Protective 'pre-scene-read' script-job has been added: {}.  Use \"pm.scriptJob( kill={}, force=True)\" to " 
        "remove it if needed.".format(av_reading_job, av_reading_job)
        )

    
def full_clean():
    """Will execute of a cleaning of suspect nodes in this scene, followed by prepping script jobs
    for pre-read, during-read, and post-read of new files.
    """    
    print("SR_ANTI_VIRAL is working now-- Messages will be in triplicate for pre-read, during read "
        "and post read.")
    nodes.clean_bad_nodes()
    scriptjobs.clean_jobs()
    scriptjobs.clean_viewport_updates()


def backup_usersetup():
    '''
    Some problematic script nodes overwrite the usersetup.
    This holds onto a copy of it.
    '''

    print("SR_ANTI_VIRAL is backing up your userSetup.py...")

    suspect_lines = [
        "cmds.evalDeferred('leukocyte = vaccine.phage()')",
        "cmds.evalDeferred('leukocyte.occupation()')",
        "import vaccine",
        ]

    for line in suspect_lines:
        line = line.strip()

    us_path = (cmds.internalVar(userAppDir=True) + 'scripts/userSetup.py')
    backup_name = (cmds.internalVar(userAppDir=True) + 'scripts/backup_userSetup.py')

    print("...SR_ANTI_VIRAL: Opening {}".format(us_path))
    try:
        f = open(us_path, 'r')
        clean_lines = []
    except:
        print("Couldn't open {}".format(us_path))
        cmds.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working."
            "See script editor.")

    print("...SR_ANTI_VIRAL: Reading your usersetup.py line by line...")
    # Read userSetup line by line looking for problem code.
    for line in f:
        if(line.strip() in suspect_lines):
            print(
                "Found a suspicious line in {}...\n{} <-- Linked to a problematic scriptjob.".
                format(us_path, line)
                )
            cmds.confirmDialog(
                title='ShaperRigs Anti-Viral', 
                message=("Found a suspicious line in {}; Linked to a problematic scriptjob.".
                    format(us_path, line)), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )
        else:
            clean_lines += line
    print("...SR_ANTI_VIRAL: Done reading usersetup.py...")
    f.close()

    try:
        os.remove(us_path)
    except:
        print("SR_ANTI_VIRAL: Couldn't delete old {}".format(us_path))
        cmds.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See"
        "script editor.")

    try:
        fo = open(us_path, 'w')
    except FileNotFoundError:
        print("SR_ANTI_VIRAL: Couldn't write new {}".format(us_path))
        cmds.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working.  See"
        "script editor.")
    
    fo.writelines(clean_lines)
    try:
        fb = open(backup_name, 'w')
    except FileNotFoundError:
        print("SR_ANTI_VIRAL: Couldn't open backup; {}".format(us_path))
        cmds.error("SR_ANTI_VIRAL critical failure.  It might not be safe to continue working."
            "See script editor.")
    fb.writelines(clean_lines)
    fo.close()
    fb.close()


def restore_backup_usersetup():
    '''
    Copies the backup_usersetup.py that was stored at the start of the session.
    '''

    print("Loading old usersetup backup...")
    try:
        back_path = (pm.internalVar(userAppDir=True) + 'scripts/backup_userSetup.py')
    except:
        print("There was no backed up usersetup.py.")
        return

    us_path = (pm.internalVar(userAppDir=True) + 'scripts/userSetup.py')
    f = open(back_path, 'r')
    fout = open(us_path, 'w')

    content = f.readlines()
    fout.writelines(content)

    f.close()
    fout.close()

    return
