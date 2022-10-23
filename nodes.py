'''
nodes.py
Created: Saturday, 22nd October 2022 2:21:59 pm
Matthew Riche
Last Modified: Saturday, 22nd October 2022 2:24:08 pm
Modified By: Matthew Riche
'''

import cmd
import maya.cmds as cmds
import os
from . import protection

# We may want to pull the names of nodes from a file at some point.  Some regular text-file that
# artists can quickly edit.


def clean_bad_nodes():
    """Check all nodes in the scene looking for targets.

    Was considering checking only for scriptNodes, but sometimes "unknown nodes" could be 
    responsible.
    """    

    # hard code node names:
    targets = ['vaccine_gene', 'breed_gene']

    nodes_to_scan = cmds.ls(type='script')

    # Flag to see if we have determined the need to protect the userSetup.py
    repair_usersetup = False

    count = 0
    ref_count = 0

    # Begin our scan
    for node in nodes_to_scan:
        name_check = node.name()
        # Adjust non-namespaced node strings to work with future string manipulation.
        if(':' not in name_check):
            name_check = ':' + name_check
        if(name_check.split(':')[1] in targets):
            # If were were checking nodes that we already eliminated, we'll continue.
            if(node.objExists() == False):
                print("{} was already removed (probably eliminated by unloading it's reference.)"
                    .format(node.name()))
                continue
            else:
                # If the problem node is still there, delete it.  It'll already have dropped it's 
                # payload though-- specific counters will come later.
                print(
                    "Removing \"{}\", a {} node known to cause issues..."
                    .format(node.name(), node.type())
                )

            cmds.confirmDialog(
                title='R Anti-Viral', 
                message=("Deleted \"{}\", a {} node known to cause issues."
                    .format(node.name(), node.type())), 
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No' )

            # Check and see if this is a reference:
            try:
                ref = cmds.system.FileReference(
                    cmds.PyNode(cmds.referenceQuery(node.name(), rfn=True)))
                cmds.confirmDialog(
                    title='R Anti-Viral', 
                    message=("Problem Nodes were found in the referenced file \"{}\".  Unloading "
                        "this reference now.  Please carefully clean this file by loading it "
                        "normally.".format(ref)),
                    button=['OK'], 
                    defaultButton='Okay', 
                    dismissString='No')
                ref.remove()
                ref_count += 1
                # Flagging repair of usersetup now.
                repair_usersetup = True
                continue
            except:
                cmds.delete(node)
                count += 1

        if(name_check.split(':')[1] in ['vaccine_gene', 'breed_gene']):
            # Special procedure for vaccine.py
            vaccine_path = cmds.internalVar(userAppDir=True) + 'scripts/vaccine.py'
            os.system('del {}'.format(vaccine_path))
            os.system('type nul > {}'.format(vaccine_path))
            os.remove(vaccine_path)
            # This flag set to true again, in the case that it is not a referenced node.
            repair_usersetup = True

    # If the userSetup is suspected to be messed with, restore it.
    if(repair_usersetup):
        protection.restore_backup_usersetup()

    if(ref_count > 0 or count > 0):
        cmds.warning(
            "Removed {} problematic reference from this scene and deleted {} problematic nodes."
            .format(ref_count, count)
            )
    return


