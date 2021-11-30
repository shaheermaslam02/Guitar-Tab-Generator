# GITHUB REPOSITORY LINK: https://github.com/shaheermaslam02/112TermProject 

# Main file to run the program using cmu_112_graphics for the UI

# change the app.alg variable to 'own' to run the pitch detection NOT using aubio
# change it to anything else to use pitch detection using aubio

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
    resetProgram(app)
def resetProgram(app):
    # app variables
    app.audio = ''
    # screen variable to swap screens
    app.screen = 'main'
    # other conditional variables
    app.recordOnce = False
    app.pitchDetect = False
    app.beforeTime = ''
    # pitch detection parameters
    app.params = ap.pitchInRealTimeWrapper()
    app.timerDelay = 1
    # random colors for note color
    app.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink']
    # guitar background image: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbe7p2TakHTliSZZLB6dBTBNIwyna2oLJ9Sg&usqp=CAU
    app.guitarBackground = ImageTk.PhotoImage(app.scaleImage(app.loadImage('GuitarBackground.jpg'), 1))
    app.kosbie = ImageTk.PhotoImage(app.scaleImage(app.loadImage('kosbie.png'), 1))
    app.note = ''
    # rows for strings
    app.strings = 6
    # columns for number of frets
    app.frets = 24
    app.tuneNote = 'No note selected.'
    app.comparisonNote = ''
    app.tune = ''
    app.tuneColor = 'black'
    app.tabs = set()
    # variable to keep track of guitar tab, 6 empty lists, 6 strings
    app.guitarTab = [['E', '|'], 
                     ['A', '|'], 
                     ['D', '|'], 
                     ['G', '|'], 
                     ['B', '|'], 
                     ['e', '|']]
    app.bpm = ''
    app.tempo = ''
    app.displayTime = 0
    app.measure = 1

    app.fakeTime = 0
    app.fake = False
    # moving through guitar tab
    app.initial = 0
    app.final = 0
    app.tab_x, app.tab_y = 0, 2
    app.storedNotes = []
    # original samples
    app.original = []
    # measure count
    app.count = 0
    # list of all readings from microphone
    app.samples = []
    # bar for loading screen
    app.bar = (app.width/4, app.height/2, app.width/4, app.height/2 + app.height/4)
    app.barCount = 0
    # using aubio library for pitch detection
    app.libraryNotes = []
    app.libraryIndexes = []
    app.libraryNoteTimes = []
    app.libraryFrequencies = []
    app.libraryIndex = -1
    # conditional variable of which alg. to use
    app.alg = 'own'
    
    app.auto = []

# timer fired function
def timerFired(app):
    # fakeTime variable to keep track of time
    app.fakeTime += 1
    # if recording
    if app.pitchDetect:
        # getting current pitch and properties, personal alg. method
        if app.alg == 'own':
            currProperties = ap.pitchInRealTime(app.params[0], app.params[1], app.params[2], 
                            app.params[3], app.params[4], app.beforeTime)
        # getting current pitch and properties, aubio alg. method using autocorrelated samples
        else:
            currProperties = ap.autoCorrelatedPitchInRealTime(app.params[0], app.params[1], app.params[2], 
                            app.params[3], app.params[4], app.beforeTime)
        # indexes for notes based on samples of 1024
        app.libraryIndex += 1
        # resetting fakeTime when beginning recording
        if app.fake:
            app.fakeTime = 0
            app.fake = False
        # if we are on the beat of the metronome
        if app.fakeTime != 0 and app.fakeTime % (100*(app.tempo) / 2) <= 0:
            app.measure += 1
            if app.measure > 4:
                app.measure = 1   
                app.count += 1
                # appending '|' on new measure
                if app.count % 2 == 0:
                    for i in app.guitarTab:
                        i.append('|')
            else:
                # appending '-' on each beat
                for i in app.guitarTab:
                    i.append('-')
        # display time for recording screen
        app.displayTime = currProperties[2]
        # if there is a note found, get the note, otherwise get nothing
        if currProperties[3] != None:
            app.note = str(currProperties[3])
            app.tabs = ap.standard_guitar_dict.get(app.note, {})
        else:
            app.note = 'No note found.'
            app.tabs = {}
        
        # appending properties to list of properties for tab creation later, own method  
        if app.alg == 'own':      
            app.samples.append(currProperties)
        else:
            app.samples += currProperties[5]
        # using autoCorrelated method of pitch detection
        if currProperties[4] != None:
            app.libraryNotes.append(currProperties[4])
            app.libraryIndexes.append(app.libraryIndex)
            app.libraryNoteTimes.append(currProperties[2])
            app.libraryFrequencies.append(currProperties[0])

    # call record audio once
    if app.recordOnce:
        app.audio = ap.recordAudio()
        app.recordOnce = False
    # if the screen is the guitar tuner
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

    if app.screen == 'loading':
        # this method is by using the autocorrelation/zero crossing algorithm
        if app.alg == 'own':
            # turning samples into auto correlated samples
            autocorrelation = []
            # list of times for each 1024 sample
            times = []
            for i in range(len(app.samples)):
                autocorrelation += ap.AutoCorrelation(app.samples[i][5])
                times.append(app.samples[i][2])

            # getting frequencies, frequency indexes
            notes = []
            noteIndexes = []
            noteTimes = []
            j = 0
            while j < len(autocorrelation) / 1024:  
                frequency = ap.zeroCrossingRate(autocorrelation[j * 1024 : (j + 1) * 1024])
                # appending frequencies and indexes of frequencies
                temp = ap.pitchToNote(frequency)
                if temp != None:
                    notes.append(temp)
                    print('Note:', temp)
                    index = ((j + 1)*1024)
                    noteIndexes.append(index)
                    noteTimes.append(times[j])
                j += 1

            # finding peaks and peak indexes of the autocorrelated samples
            app.peaks, app.peakIndexes = ap.peakFinder(autocorrelation)
            app.auto = autocorrelation
            # padding guitar tab with '-' and '|'
            while (len(app.guitarTab[0]) - 1) % 7 != 0:
                for i in app.guitarTab:
                    i.append('-')
                if len(app.guitarTab[0]) % 7 == 0:
                    for k in app.guitarTab:
                        k.append('|')  
            # now, we want to store the notes we've found into the guitar tab itself
            ap.tabGeneration(notes, noteIndexes, noteTimes, app.tempo, app.peakIndexes, app.guitarTab)

            app.final = len(app.guitarTab[0])
            # changing screens
            app.screen = 'tab'
        # using alg. with autocorrelation and aubio's pitch detection
        else:
            app.peaks, app.peakIndexes = ap.peakFinder(app.samples)
            ap.tabGeneration(app.libraryNotes, app.libraryIndexes, app.libraryNoteTimes, app.tempo, app.peakIndexes, app.guitarTab)
            app.final = len(app.guitarTab[0])
            if app.final < 5:
                for i in range(0, 5):
                    for i in app.guitarTab:
                        i.append('-')
                for i in app.guitarTab:
                    i.append('|')
                app.final = len(app.guitarTab[0])
            app.screen = 'tab'

# key pressed function
def keyPressed(app, event):
    # to go to directions screen
    if event.key == 'Space' and app.screen == 'main':
        app.screen = 'directions'
    # to go to recording screen
    elif event.key == 'Space' and app.screen == 'directions':
        app.tempo = 0.5/(120/int(app.bpm)) 
        app.screen = 'record'
        app.recordOnce = True
        app.beforeTime = time.time()
        app.pitchDetect = True
        app.fake = True
    if app.screen == 'directions':
        if event.key in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
            app.bpm += event.key
        elif event.key == 'Backspace':
            app.bpm = app.bpm[0:len(app.bpm) - 1]
    # to stop recording
    if event.key == 's' and app.screen == 'record':
        sd.stop()
        app.screen = 'loading'
        app.pitchDetect = False
    # to play the audio
    if app.screen == 'tab':
        # changing tab selected position
        if event.key == 'Right':
            app.tab_y += 1
            if app.tab_y >= app.final:
                app.final += 1
                if app.final >= 90:
                    app.initial += 1
                if (len(app.guitarTab[0]) - 1) % 6 == 0:
                    for i in app.guitarTab:
                        i.append('|')
                else:
                    for i in app.guitarTab:
                        i.append('-')
        elif event.key == 'Left':
            app.tab_y -= 1
            if app.tab_y < 0:
                app.tab_y += 1
            elif app.tab_y < app.initial:
                app.initial -= 1
                app.final -= 1
        elif event.key == 'Up':
            app.tab_x -= 1
            if app.tab_x < 0:
                app.tab_x += 1
        elif event.key == 'Down':
            app.tab_x += 1
            if app.tab_x > 5:
                app.tab_x -= 1
        # adjusting tab based on key input
        elif event.key in ap.frets:
            if app.guitarTab[app.tab_x][app.tab_y] == '-':
                app.guitarTab[app.tab_x][app.tab_y] = event.key
            elif app.guitarTab[app.tab_x][app.tab_y] in ap.frets and app.guitarTab[app.tab_x][app.tab_y] + event.key in ap.frets:
                app.guitarTab[app.tab_x][app.tab_y] = app.guitarTab[app.tab_x][app.tab_y] + event.key
        elif event.key == '-' and app.guitarTab[app.tab_x][app.tab_y] in ap.frets:
            app.guitarTab[app.tab_x][app.tab_y] = event.key
        elif event.key == '-' and app.guitarTab[app.tab_x][app.tab_y] == '|':
            for i in app.guitarTab:
                i[app.tab_y] = event.key
        elif event.key == '|' and (app.guitarTab[app.tab_x][app.tab_y] == '-' or app.guitarTab[app.tab_x][app.tab_y] in ap.frets):
            for i in app.guitarTab:
                i[app.tab_y] = event.key
        elif event.key == 'k':
            app.screen = 'kosbie'
    if event.key == 'g' and app.screen == 'tab':
        ap.graphAudio(app.auto, app.peaks, app.peakIndexes, app.libraryNotes, app.libraryIndexes, app.libraryFrequencies)
    if event.key == 'p' and app.screen == 'tab':
        ap.playAudio(app.audio)
    # to go back to main screen
    if event.key == 'm':
        app.screen = 'main'
        appStarted(app)
    # to save as a file
    if event.key == 'f' and app.screen == 'tab':
        app.count += 1
        ap.saveFile(app.audio, app.count)
    # to go to tuner screen
    if event.key == 't':
        app.screen = 'tuner'
    # tuner conditions to select note to tune to
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

def printNotes(notes):
    for i in notes:
        print(['Pitch: ' + str(i[0]), 'Volume: ' + str(i[1]), 
               'Time: ' + str(i[2]), 'Note: ' + str(i[3]), 'Tab: ' + str(i[4])])

# draw frets function (24 frets)
def drawFrets(app, canvas):
    # bounds of the guitar frets
    initialBounds = (app.width/10, app.height/2)
    endBounds = (app.width*(9/10), app.height/1.3)
    fretHeight = (endBounds[1] - initialBounds[1])/app.strings
    fretLength = (endBounds[0] - initialBounds[0])/app.frets
    # drawing each string and fret, coloring green if note is found
    for string in range(app.strings):
        y0 = initialBounds[1] + string*fretHeight
        y1 = y0 + fretHeight
        for fret in range(app.frets + 1):
            x0 = initialBounds[0] + fret*fretLength
            x1 = x0 + fretLength
            if (string, fret) in (app.tabs):
                canvas.create_rectangle(x0, y0, x1, y1, fill = 'green', outline = 'black', width = 4)
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill = 'tan', outline = 'black', width = 4)

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
    fretLength = (endBounds[0] - initialBounds[0])/app.frets

    canvas.create_rectangle(0, app.height/2, app.width/10, app.height/2 + fretHeight*6, 
                            fill = 'black', outline = 'black')
    canvas.create_polygon(app.width/10 + 22*fretLength, app.height/2, app.width, app.height/2, app.width - app.width/6, app.height/2 - 4*fretHeight, 
                            app.width/10 + 22*fretLength, app.height/2 - 2*fretHeight, fill = 'blue', outline = 'blue')
    canvas.create_polygon(app.width/10 + 22*fretLength, app.height/2 + 6*fretHeight, app.width, app.height/2 + 6*fretHeight, app.width - app.width/6, app.height/2 + 10*fretHeight,
                            app.width/10 + 22*fretLength, app.height/2 + 8*fretHeight, fill = 'blue', outline = 'blue')
    canvas.create_rectangle(app.width/10 + 22*fretLength, app.height/2, app.width, app.height/2 + fretHeight*6, fill = 'blue', outline = 'blue')
    canvas.create_rectangle(app.width - app.width/20, app.height/2, app.width - app.width/16, app.height/2 + 6*fretHeight, fill = 'black')
    canvas.create_rectangle(app.width/10 - app.width/20, app.height/2, app.width/10, app.height/2 + 6*fretHeight, fill = 'grey')

# draw guitar functions, uses helper draw functions
def drawGuitar(app, canvas):
    drawBody(app, canvas)
    drawFrets(app, canvas)
    drawStrings(app, canvas)

# drawing main screen function
def drawMainScreen(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image = app.guitarBackground)
    canvas.create_text(app.width/2 + app.width/4, app.height/4, text = 'Guitar Tab Generator', 
                       font = 'Arial 30 bold')
    canvas.create_text(app.width/2 + app.width/4, app.height/2, text = 'Press space to read the directions.', 
                       font = 'Arial 12 bold')
    canvas.create_text(app.width/2 + app.width/4, app.height/1.5, text = 'Press "t" to go to the standard guitar tuner.', font = 'Arial 12 bold')

def drawDirectionsScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/6, text = 'Directions', font = 'Arial 24 bold')
    canvas.create_text(app.width/2, app.height/4.5, text = 'Preferably use a USB microphone in a quiet setting for best tab generation.', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/3, text = 'You can play slower for even better results.', font = 'Arial 14 bold', fill = 'red')
    canvas.create_text(app.width/2, app.height/2, text = 'Please type in a tempo (120 BPM is standard): ' + app.bpm, font = 'Arial 20 bold')
    canvas.create_text(app.width/2, app.height - app.height/8, text = 'Press space to begin recording!', font = 'Arial 20 bold')

# draw recording screen function
def drawRecordingScreen(app, canvas):
    canvas.create_oval(app.width/2 - 110, app.height/4 - 110, app.width/2 + 110, 
                         app.height/4 + 110, fill = 'black')
    canvas.create_oval(app.width/2 - 100, app.height/4 - 100, app.width/2 + 100, 
                         app.height/4 + 100, fill = 'red')
    canvas.create_text(app.width/2, app.height/4, text = 'Recording', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/3.25, text = 'Press s to stop.', font = 'Arial 12 bold')
    canvas.create_text(app.width/10, app.height/10, text = 'Tempo: ' + app.bpm + 'BPM', font = 'Arial 14 bold')
    canvas.create_text(app.width*(9/10), app.height/10, text = 'Time: ' + str(app.displayTime) + 's', font = 'Arial 14 bold')
    canvas.create_text(app.width/2, app.height*(9/10), text = 'Beat: ' + str(app.measure), font = 'Arial 16 bold')
    drawGuitar(app, canvas)
    # color changes depending on if there is a note or not
    if app.note == 'No note found.':
        canvas.create_text(app.width/2, app.height/2.15, text = app.note, font = 'Arial 24 bold', 
                       fill = 'darkRed')
    else:
        canvas.create_text(app.width/2, app.height/2.15, text = app.note, font = 'Arial 24 bold', 
                        fill = app.colors[random.randint(0, len(app.colors) - 1)])

# draw loading screen function
def drawLoadingScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/2, text = 'Loading Tab', font = 'Arial 20 bold')  
    canvas.create_text(app.width/2, app.height/4, text = 'This may take awhile...', font = 'Arial 20 bold', fill = 'red')
    #canvas.create_rectangle(app.bar[0], app.bar[1], app.bar[2], app.bar[3], fill = 'blue', outline = 'black')

# draw playing screen function
def drawTabScreen(app, canvas):
    canvas.create_text(app.width/2, app.height - app.height/8, text = 'Press ''p'' to play recording.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height - app.height/16, text = 'Press ''f'' to save recording as a file.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height - app.height/32, text = 'Press ''k'' for a surprise...', font = 'Arial 8 bold', fill = 'red')
    canvas.create_text(app.width/2, app.height/12, text = 'Directions', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/6, text = 'Use the arrow keys to move around the tab, put in your own frets for each string, and extend the tab by moving to the right.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height - app.height/6, text = 'Press ''g'' to graph the audio.', font = 'Arial 12 bold')
    # setting initial bound for drawing tab
    initialBounds = (app.width/16, app.height/3)
    # drawing tab on screen
    for i in range(len(app.guitarTab)):
        height = (app.height/20)
        fret = 0 
        for j in range(app.initial, app.final):
            fret += 1
            if (i, j) == (app.tab_x,app.tab_y):
                canvas.create_text(initialBounds[0] + fret*(app.width/100), initialBounds[1] + i*(height), text = app.guitarTab[i][j], font = 'Arial 16 bold', fill = 'green')
            else:   
                canvas.create_text(initialBounds[0] + fret*(app.width/100), initialBounds[1] + i*(height), text = app.guitarTab[i][j], font = 'Arial 16 bold')

# draw tuning screen function
def drawTunerScreen(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text = 'Guitar Standard Tuner! Note: ' + app.tuneNote, font = 'Arial 20 bold')
    canvas.create_text(app.width/2, app.height - app.height/8, text = 'Press "m" to go back to the main screen.', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height/2, text = app.tune, font = 'Arial 20 bold', fill = app.tuneColor)
    canvas.create_text(app.width/2, app.height - app.height/6, text = 'Hit E, A, D, G, B, # (High E) to tune to a note', font = 'Arial 12 bold')

# fun draw kosbie screen
def drawKosbie(app, canvas):
    canvas.create_image(app.width/2, app.height/2, image = app.kosbie)
    canvas.create_text(app.width/2, app.height/2, text = 'KOSBIEEEEEEE!!', font = 'Arial 20 bold', 
                    fill = app.colors[random.randint(0, len(app.colors) - 1)])

# redrawAll function
def redrawAll(app, canvas):
    if app.screen == 'main':
        drawMainScreen(app, canvas)
    elif app.screen == 'directions':
        drawDirectionsScreen(app, canvas)
    elif app.screen == 'record':
        drawRecordingScreen(app, canvas)
    elif app.screen == 'loading':
        drawLoadingScreen(app, canvas)
    elif app.screen == 'tab':
        drawTabScreen(app, canvas)
    elif app.screen == 'tuner':
        drawTunerScreen(app, canvas)
    elif app.screen == 'kosbie':
        drawKosbie(app, canvas)
# runApp function
def runGuitarTabGenerator():
    print('Running Guitar Tab Generator.')
    runApp(width = 1520, height = 800)

runGuitarTabGenerator()

