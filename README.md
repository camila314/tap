![tap logo](github_assets/TapLogo.png) 
## Tap: the best click bot for Geometry Dash
Tap an automate fake click tool coded in python with the goal of making the most realistic clicks possible for a given level.
### Tap only works for osXbot/wsX files
[osXbot](https://github.com/camden314/osxbot) is a macro recorder tool that was built for MacOS, and [wsX](https://github.com/camden314/wsX) is osXbot ported to windows. Tap takes osXbot/wsX macro files as an input, as well as xbot frame record macros, and zbot frame record macros. You can find more information about osXbot/wsX, the macro files, and Tap at my [discord server](https://discord.gg/5kPwTqb8MB)

## Build instructions
To get tap working, you first need to install the modules inside `requirements.txt`. You can do this with `pip install -r requirements.txt`. Afterwards you have 2 options as to how you want to use tap, either by bundling it into an executable or by directly running the python script

### Script
Tap accepts python 3 only. For Mac, run `run.py` with your python interpreter. For Windows, run `run_windows.py` with your python interpreter.

### Executable (Mac only)
For building the executable, you need to go into the TapPackage folder and run the Makefile. That should be all it takes to build the executable.


# Credit
Credit to [Alpha Ary](https://www.youtube.com/channel/UCqpKXLRstb8xfeMxzS8DnNg) who inspired me to make this and also helped me with some of the inner workings of it