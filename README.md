# top-run-time
Takes output from RedLime's SpeedRunIGT mod (igt_timer.log) to get the top run retime as per the rules in speedrun.com/mc as well as generating a new file for describing the splits.

It runs on console without a GUI, and will ask you what type of pause each one was. Just type it out using the key it prints (scp for settings change pause, dlp for dimension load pause, etc.) and hit enter.

if you'd like to run the .py directly, you'll need to install [python](https://www.python.org/downloads/) and then the best way to install the easygui dependency is to install [pip](https://pip.pypa.io/en/stable/installation/) and running 
> pip install easygui

If you're on windows, you can run this via the commands

> python -m pip install easygui

Depending on the setup you may need to replace 'python' with 'python3'.

The other dependencies are included by installing python.

You can then run it by double clicking on the .py file or going into terminal or command prompt and running it there after changing directories to wherever the .py is on your computer. For windows users on command prompt, just send
> py -3 top_run.py

For mac, it should be
> python3 top_run.py
