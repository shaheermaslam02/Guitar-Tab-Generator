# importing libraries
from cmu_112_graphics import *
from tkinter import *
import AudioProcessing as ap
import sounddevice as sd
from scipy.io.wavfile import write
import time
import random

# app started function
def appStarted(app):
    app.audio = ''
    app.count = 0
    app.screen = 'main'
    app.recordOnce = False
    app.pitchDetect = False
    app.beforeTime = ''
    app.params = ap.pitchInRealTimeWrapper()
    app.timerDelay = 1
    app.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink']
    app.guitarBackground = app.scaleImage(app.loadImage('GuitarBackground.jpg'), 1)
    app.note = ''
    # rows for strings
    app.strings = 6
    # columns for number of frets
    app.frets = 24

# timer fired function
def timerFired(app):
    if app.pitchDetect:
        properties = ap.pitchInRealTime(app.params[0], app.params[1], app.params[2], 
                           app.params[3], app.params[4], app.beforeTime)
        if properties[3] != None:
            app.note = str(properties[3])
        else:
            app.note = 'No note found.'
    if app.recordOnce:
        app.audio = ap.recordAudio()
        app.recordOnce = False

# key pressed function
def keyPressed(app, event):
    if event.key == 'Space': 
        app.screen = 'record'
        app.recordOnce = True
        app.beforeTime = time.time()
        app.pitchDetect = True

    if event.key == 's':
        sd.stop()
        app.screen = 'tab'
        app.pitchDetect = False
    
    if event.key == 'p':
        ap.playAudio(app.audio)

    if event.key == 'm':
        app.screen = 'main'

    if event.key == 'f':
        app.count += 1
        ap.saveFile(app.audio, app.count)

# mouse pressed function
def mousePressed(app, event):
    pass

# draw frets function (24 frets)
def drawFrets(app, canvas):
    initialBounds = (app.width/10, app.height/2)
    endBounds = (app.width*(9/10), app.height/1.3)
    fretHeight = (endBounds[1] - initialBounds[1])/app.strings
    fretLength = (endBounds[0] - initialBounds[0])/app.frets

    for string in range(app.strings):
        y0 = initialBounds[1] + string*fretHeight
        y1 = y0 + fretHeight
        fretChange = 0
        for fret in range(app.frets):
            x0 = initialBounds[0] + fret*fretLength + fretChange
            x1 = x0 + fretLength + fretChange
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'tan', outline = 'black', width = 4)
            fretChange -= .25

# drawing main screen function
def drawMainScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.guitarBackground))
    canvas.create_text(app.width/2, app.height/4, text = 'Guitar Tab Generator', 
                       font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/2, text = 'Press space to begin recording.', 
                       font = 'Arial 12 bold')

# draw recording screen function
def drawRecordingScreen(app, canvas):
    canvas.create_oval(app.width/2 - 110, app.height/4 - 110, app.width/2 + 110, 
                         app.height/4 + 110, fill = 'black')
    canvas.create_oval(app.width/2 - 100, app.height/4 - 100, app.width/2 + 100, 
                         app.height/4 + 100, fill = 'red')
    canvas.create_text(app.width/2, app.height/4, text = 'Recording', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/3.25, text = 'Press s to stop.', font = 'Arial 12 bold')
    
    if app.note == 'No note found.':
        canvas.create_text(app.width/2, app.height/2.15, text = app.note, font = 'Arial 24 bold', 
                       fill = 'darkRed')
    else:
        canvas.create_text(app.width/2, app.height/2.15, text = app.note, font = 'Arial 24 bold', 
                        fill = app.colors[random.randint(0, len(app.colors) - 1)])
    

# draw playing screen function
def drawTabScreen(app, canvas):
    canvas.create_text(app.width/2, app.height - 100, text = 'Press ''p'' to play recording.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height - 50, text = 'Press ''f'' to save recording as a file.', font = 'Arial 12 bold')

# redrawAll function
def redrawAll(app, canvas):
    if app.screen == 'main':
        drawMainScreen(app, canvas)
    elif app.screen == 'record':
        drawRecordingScreen(app, canvas)
        drawFrets(app, canvas)
    elif app.screen == 'tab':
        drawTabScreen(app, canvas)

# runApp function
def runGuitarTabGenerator():
    print('Running Guitar Tab Generator.')
    runApp(width = 1520, height = 800)

runGuitarTabGenerator()

