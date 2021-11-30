# 112TermProject

## Guitar Tab Generator

I attempt to create a Guitar Tab Generator, which creates a guitar tab (a form of “sheet music” for guitar) based on microphone input. The purpose of this is to eliminate the need to manually create guitar tabs by hand, where instead guitar can be played into the microphone to generate one. By processing audio from the microphone in real time, one can record their audio and visualize the notes they are playing. There is also a simple guitar tuner included.

### How To Use

The file to run the program is Main.py. All other files within the repository should be included within the same folder when running this code so that images and other processing files can be used in the Main.py file. 

### Main Screen

From the main screen, you can access the directions screen by pressing 'space', or you can move to the standard guitar tuner by pressing 't'. You can return to the main screen at any time by pressing 'm'.

### Directions Screen

From the directions screen, you can return to the main screen, but you can type in a certain BPM so that on the recording screen, tempo is tracked by the beat counter. There are also directions for how you should record for better results.

### Tuner Screen

From the tuner screen, you can select notes from standard guitar tuning (E, A, D, G, B, e), and tune your guitar to the pitch required.

### Recording Screen

From the recording screen, you can visualize your guitar notes as you're playing, see the beat tracking, and press 's' to finish recording.

### Loading Screen

This is just a loading screen while your tab is generated.

### Tab Screen

Here is where the guitar tab is displayed. You can change the notes, modify and extend the tab, and see what you've got! (You can press 'k' to see something interesting.)

### Libraries

The libraries included in this project are as follows:

* cmu_112_graphics
* tkinter
* sounddevice
* scipy
* aubio
* pyaudio
* numpy
* pandas
* requests

### Bugs
* MVC violation when going to recording screen at times
* If no notes detected, error when generating tab
