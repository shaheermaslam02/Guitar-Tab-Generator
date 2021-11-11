# importing libraries
from cmu_112_graphics import *
import tkinter as tk
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
    app.tuneNote = 'No note selected.'
    app.comparisonNote = ''
    app.tune = ''
    app.tuneColor = 'black'
    

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
    if app.screen == 'tuner' and app.tuneNote != 'No note selected.':
        properties = ap.pitchInRealTime(app.params[0], app.params[1], app.params[2], 
                           app.params[3], app.params[4], 0)
        if properties[0] == 0:
            app.tune = 'Play something!'
            app.tuneColor = 'black'
        elif properties[3] == app.comparisonNote:
            app.tune = 'Good!'
            app.tuneColor = 'green'
        elif properties[0] < ap.note_dictionary[app.comparisonNote][0]:
            app.tune = 'Tune higher.'
            app.tuneColor = 'red'
        elif properties[0] > ap.note_dictionary[app.comparisonNote][0]:
            app.tune = 'Tune lower.'
            app.tuneColor = 'blue'
        

# key pressed function
def keyPressed(app, event):
    # to go to recording screen
    if event.key == 'Space' and app.screen == 'main': 
        app.screen = 'record'
        app.recordOnce = True
        app.beforeTime = time.time()
        app.pitchDetect = True
    # to stop recording
    if event.key == 's' and app.screen == 'record':
        sd.stop()
        app.screen = 'tab'
        app.pitchDetect = False
    # to play the audio
    if event.key == 'p' and app.screen == 'tab':
        ap.playAudio(app.audio)
    # to go back to main screen
    if event.key == 'm':
        app.screen = 'main'
    # to save as a file
    if event.key == 'f' and app.screen == 'tab':
        app.count += 1
        ap.saveFile(app.audio, app.count)
    # to go to tuner screen
    if event.key == 't':
        app.screen = 'tuner'
    # tuner conditions
    if app.screen == 'tuner':
        if event.key == 'E' or event.key == 'e':
            app.tuneNote = 'E'
            app.comparisonNote = 'E2'
        elif event.key == 'A' or event.key == 'a':
            app.tuneNote = 'A'
            app.comparisonNote = 'A2'
        elif event.key == 'D' or event.key == 'd':
            app.tuneNote = 'D'
            app.comparisonNote = 'D3'
        elif event.key == 'G' or event.key == 'g':
            app.tuneNote = 'G'
            app.comparisonNote = 'G3'
        elif event.key == 'B' or event.key == 'b':
            app.tuneNote = 'B'
            app.comparisonNote = 'B3'
        elif event.key == '#':
            app.tuneNote = 'High E'
            app.comparisonNote = 'E4'

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
        #fretChange = 0
        for fret in range(app.frets + 1): # app.frets + 1 since we must consider the open fret
            x0 = initialBounds[0] + fret*fretLength # + fretChange
            x1 = x0 + fretLength # + fretChange
            canvas.create_rectangle(x0, y0, x1, y1, fill = 'tan', outline = 'black', width = 4)
            # fretChange -= .25

# draw strings function (6 strings)
def drawStrings(app, canvas):
    initialBounds = (app.width/10, app.height/2)
    endBounds = (app.width*(9/10), app.height/1.3)
    fretHeight = (endBounds[1] - initialBounds[1])/app.strings
    firstString = app.height/2 + fretHeight/2
    for i in range(app.strings):
        canvas.create_line(0, firstString + i*(fretHeight), app.width, firstString + i*(fretHeight), 
                           fill = 'grey', width = 4)

# draw body of guitar function
def drawBody(app, canvas):
    initialBounds = (app.width/10, app.height/2)
    endBounds = (app.width*(9/10), app.height/1.3)
    fretHeight = (endBounds[1] - initialBounds[1])/app.strings
    canvas.create_rectangle(0, app.height/2, app.width/10, app.height/2 + fretHeight*6, 
                            fill = 'blue', outline = 'blue')
    
    canvas.create_polygon(0, app.height/2, app.width/6, app.height/2, app.width/3, app.height/2 - 4*fretHeight, 0, 
                          app.height/2 - 2*fretHeight, fill = 'blue', outline = 'blue')
    canvas.create_polygon(0, app.height/2 + fretHeight*6, app.width/6, app.height/2 + fretHeight*6, app.width/3, app.height/2 + 10*fretHeight, 0, 
                          app.height/2 + 8*fretHeight, fill = 'blue', outline = 'blue')
    canvas.create_rectangle(app.width/20, app.height/2, app.width/16, app.height/2 + 6*fretHeight, fill = 'black')
    canvas.create_rectangle(app.width*(9/10), app.height/2, app.width, app.height/2 + fretHeight*6, fill = 'black')
# draw guitar functions, uses helper draw functions
def drawGuitar(app, canvas):
    drawBody(app, canvas)
    drawFrets(app, canvas)
    drawStrings(app, canvas)

# drawing main screen function
def drawMainScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.guitarBackground))
    canvas.create_text(app.width/2 + app.width/4, app.height/4, text = 'Guitar Tab Generator', 
                       font = 'Arial 30 bold')
    canvas.create_text(app.width/2 + app.width/4, app.height/2, text = 'Press space to begin recording.', 
                       font = 'Arial 12 bold')
    canvas.create_text(app.width/2 + app.width/4, app.height/1.5, text = 'Press "t" to go to the standard guitar tuner.', font = 'Arial 12 bold')

# draw recording screen function
def drawRecordingScreen(app, canvas):
    canvas.create_oval(app.width/2 - 110, app.height/4 - 110, app.width/2 + 110, 
                         app.height/4 + 110, fill = 'black')
    canvas.create_oval(app.width/2 - 100, app.height/4 - 100, app.width/2 + 100, 
                         app.height/4 + 100, fill = 'red')
    canvas.create_text(app.width/2, app.height/4, text = 'Recording', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/3.25, text = 'Press s to stop.', font = 'Arial 12 bold')
    drawGuitar(app, canvas)
    # color changes depending on if there is a note or not
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

# draw tuning screen function
def drawTunerScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text = 'Guitar Standard Tuner! Note: ' + app.tuneNote, font = 'Arial 20 bold')
    canvas.create_text(app.width/2, app.height - app.height/8, text = 'Press "m" to go back to the main screen.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height/2, text = app.tune, font = 'Arial 20 bold', fill = app.tuneColor)
    canvas.create_text(app.width/2, app.height - app.height/6, text = 'Hit E, A, D, G, B, # (High E) to tune to a note', font = 'Arial 12 bold')

# redrawAll function
def redrawAll(app, canvas):
    if app.screen == 'main':
        drawMainScreen(app, canvas)
    elif app.screen == 'record':
        drawRecordingScreen(app, canvas)
    elif app.screen == 'tab':
        drawTabScreen(app, canvas)
    elif app.screen == 'tuner':
        drawTunerScreen(app, canvas)

# runApp function
def runGuitarTabGenerator():
    print('Running Guitar Tab Generator.')
    runApp(width = 1520, height = 800)

runGuitarTabGenerator()

