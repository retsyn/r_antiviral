# R Anti Viral
Simple suite that installs scriptJobs to counteract known "viral" scriptJobs spread through asset sharing.
Brought to you by ShapeShifters Creative.  https://shapeshifterscreative.com

Put the entire folder in your `...\Documents\maya\scripts` folder, then add the following to your `userSetup.py` or any other module that registers early in start-up:
```
# r_anti_viral Start:
import sr_anti_viral
sr_anti_viral.protection.register_protection_script()
# r_anti_viral End
```

Running the `register_protection_script()` will add script jobs on file-read of any type, which check for the addition of the script-nodes that create the "vaccine" virus. As soon as such nodes are loaded, imported, or references, measures to immediately reverse their payload and delete them are taken.  For loading and importing, this will delete the problem nodes and undo the effects of their payload.  For references, when a problem node is detected within, the reference it belongs to will be forcibly unloaded (and the payload effects reversed.)

Due to the specificity of the nodes it targets, we give an informal garuntee that your scenes won't be messed with (unless they rely on reference nodes pointing at infected files.)
