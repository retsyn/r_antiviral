'''
scriptjobs.py

Matt Riche
2021

Module for reading the scriptjobs active and identifying ones you want removed before they run.
'''

import maya.cmds as cmds
import re


def clean_viewport_updates(targets=[r'DCF_updateViewportList;']):
    """Cleans an annoying "update viewports" action, left behind by an unknown plug-in we
    sometimes encountered.

    Args:
        targets (list, optional): Commands to find and excise from uiConfigurationScriptNode. 
            Defaults to [r'DCF_updateViewportList;'].
    """
    must_restart = False
    # First we acquire the common configuration node:
    if cmds.objectExists("uiConfigurationScriptNode"):

        node = cmds.PyNode("uiConfigurationScriptNode")
        print("Working on the node {}".format(node))

        bs_content = cmds.scriptNode(node, q=True, bs=True)

        for target in targets:
            if(target in bs_content):
                cleaned_content = re.sub((target), '', bs_content)
                cmds.scriptNode(node, e=True, bs=cleaned_content)
                cmds.scriptNode(node, eb=True)
                must_restart = True

        if(must_restart):    
            cmds.confirmDialog(
                title='ShaperRigs Anti-Viral', 
                message=("Found a problem in uiConfigurationScriptNode: \"DCF_updateViewportList\"."
                "\nThis can create serious issues with the viewport in this session.  This file has" 
                "been cleaned, and you may save an iteration now.  This session however should be "
                "restarted immediately after saving."), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )


def clean_jobs(targets=['breed_gene']):
    """Checks a list of all active scriptJobs looking for ones listed in the block file.

    Args:
        targets (list, optional): List of names of nodes to search for. Defaults to ['breed_gene'].
    """
    # Add reading of the block file later, for now we are hard coding what we are looking for.
    print("R_Antiviral is looking for known problem script jobs...")
    jobs = cmds.scriptJob(lj=True)
    count = 0
    for job in jobs:
        for target in targets:
            if(target in job):
                # We found an example, get the number.
                print("Found this suspicious script-job:")
                print('\"{}\"'.format(job))
                job_number = int(job.split(':')[0])
                # Kill the job by number...
                cmds.scriptJob(kill=job_number, force=True)
                print ("Job {} deleted from stack.".format(job_number))
                count += 0

    if(count > 0):
        cmds.warning("Deleted {} suspicious script-jobs.".format(count))
    else:
        print("...SR_ANTI_VIRAL found no suspicious script jobs...")

    return