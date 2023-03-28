# Morsifier

A Kivy application to translate text to-, listen to- and download morsecode.

<div align="center">
    <img width="450px" src="morsifier.png" />
</div>

## Description

Morsifier is an application that allows users to translate text to morse code. The outputted morse code can be read, listened to and seen in the form of a simulated flashlight. The audiofiles containing the morse code can be saved to the user's computer.

Morsifier currently only allows text-to-morse.


## Getting Started

### Dependencies

- Python 3.10
- Kivy
- NumPy
- Pydub

### Installing dependencies

#### Install Python 3.10.0

Download the Python installer from <a href="https://www.python.org/downloads/">Python's official website</a>, or install with <a href="https://brew.sh">Homebrew</a> by typing the following command in your terminal:
```
brew install python@3.10
```

#### Installing kivy 2.1.0

To install kivy follow the steps in their <a href="https://kivy.org/doc/stable/gettingstarted/installation.html">official guide</a>.

Make sure to install the full dependency "kivy[full]":
```
python -m pip install "kivy[full]"
```

#### Install Numpy and pydub

In your terminal type the following command (preferably inside your virtual environment):
```
pip install numpy

pip install pydub
```

## Usage

### Executing the program

After installing all of the dependencies, run `main.py` in your editor of choice or navigate to the top folder in your virtual env and type the following command in your terminal:
```
python3 main.py
```
or
```
python3.10 main.py
```

### Step-by-step
<div align="center"><img src="images/mainscreen.png" alt="Screenshot of the window where 'Hello!' is translated to morse" width="400" height="370"></div>
Start by choosing a tempo given in words-per-mimnute (wpm) by clicking one of the numbered buttons.
Type in the alphanumerical text you want to translate to morse into the input box
Press proceed
The morse translation will show up in the box below and the corresponding morse sound will play

- Press the sideways 8 button to continuously loop over the morse code
- Press the speaker icon to mute/unmute the sound
- Pressing the arrow pointing into a box icon will prompt a new window allowing you to save the morse sound file as a .wav to your computer
- Pressing the "toggle flashlight" button enables a box that simulates morse code with a flashlight

To translate another text press the reset button to enable the text input again.


## Authors

- <a href="https://github.com/Hitijahujessy">@Hitijahujessy</a>
- <a href="https://github.com/MrWaltTG1">@MrWaltTG1</a>

## Version History

1.0
Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
