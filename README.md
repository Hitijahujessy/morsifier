# Morsifier

A Kivy application to translate text to-, listen to- and download morsecode.

<div align="center">
    <img width="450px" src="morsifier.png" />
</div>

## Description

Morsifier is an application that allows users to translate text to morse code. The outputted morse code can be read, listened to and seen in the form of a simulated flashlight. The audiofiles containing the morse code can be saved to the user's computer.

Morsifier currently only allows text-to-morse.

### Step-by-step

Start by choosing a tempo given in words-per-mimnute (wpm) by clicking one of the numbered buttons.
Type in the alphanumerical text you want to translate to morse into the input box
Press proceed
The morse translation will show up in the box below and the corresponding morse sound will play

- Press the sideways 8 button to continuously loop over the morse code
- Press the speaker icon to mute/unmute the sound
- Pressing the arrow pointing into a box icon will prompt a new window allowing you to save the morse sound file as a .wav to your computer
- Pressing the "toggle flashlight" button enables a box that simulates morse code with a flashlight

To translate another text press the reset button to enable the text input again.

## Getting Started

### Dependencies

- Python 3.10
- Kivy
- NumPy

### Installing dependencies

#### Install Python 3.10.0

Download the Python installer from <a href="https://www.python.org/downloads/">Python's official website</a>, or install with <a href="https://brew.sh">Homebrew</a> by typing the following command in your terminal:
```
brew install python@3.10
```

#### Install Kivy 2.1.0

**The Kivy installation guide is copied from Kivy's docs. Review their page if you run into any trouble. Installing Kivy with [full] dependencies.**

#### Setup terminal and pip¶

Before Kivy can be installed, Python and pip needs to be pre-installed. Then, start a new terminal that has Python available. In the terminal, update pip and other installation dependencies so you have the latest version as follows (for linux users you may have to substitute python3 instead of python and also add a `--user` flag in the subsequent commands outside the virtual environment):
```
python -m pip install --upgrade pip setuptools virtualenv
```
#### Create virtual environment

Create a new virtual environment for your Kivy project. A virtual environment will prevent possible installation conflicts with other Python versions and packages. It’s optional but strongly recommended:

Create the virtual environment named kivy_venv in your current directory:
```
python -m virtualenv kivy_venv
```
Activate the virtual environment. You will have to do this step from the current directory every time you start a new terminal. This sets up the environment so the new kivy_venv Python is used.

For Windows default CMD, in the command line do:
```
kivy_venv\Scripts\activate
```
If you are in a bash terminal on Windows, instead do:
```
source kivy_venv/Scripts/activate
```
If you are in linux or macOS, instead do:
```
source kivy_venv/bin/activate
```
Your terminal should now preface the path with something like (kivy_venv), indicating that the kivy_venv environment is active. If it doesn’t say that, the virtual environment is not active and the following won’t work.

#### Install Kivy

Finally, install Kivy using one of the following options:

##### - Pre-compiled wheels

The simplest is to install the current stable version of kivy and optionally kivy_examples from the kivy-team provided PyPi wheels. Simply do:
```
python -m pip install "kivy[base]"
```
This also installs the minimum dependencies of Kivy. To additionally install Kivy with audio/video support, install either kivy[base,media] or kivy[full]. See Kivy’s dependencies for the list of selectors.

##### - From source

If a wheel is not available or is not working, Kivy can be installed from source with some additional steps. Installing from source means that Kivy will be installed from source code and compiled directly on your system.

First install the additional system dependencies listed for each platform: Windows, macOS, Linux.

With the dependencies installed, you can now install Kivy into the virtual environment.

To install the stable version of Kivy, from the terminal do:
```
python -m pip install "kivy[base]" kivy_examples --no-binary kivy
```
To install the latest cutting-edge Kivy from master, instead do:
```
python -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
```
### Executing program

After installing all of the dependencies, run `main.py` in your editor of choice or type the following command in your terminal:
```
python3 main.py
```
or
```
python3.10 main.py
```


## Authors

- @Hitijahujessy
- @MrWaltTG1

## Version History

1.0
Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
