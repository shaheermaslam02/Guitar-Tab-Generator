# importing libraries
from cmu_112_graphics import *
import AudioProcessing as ap
import sounddevice as sd
from scipy.io.wavfile import write
import time

# app started function
def appStarted(app):
    app.audio = ''
    app.count = 0
    app.screen = 'main'
    app.recordOnce = False
    app.pitchDetect = False
    app.params = ap.pitchInRealTimeWrapper()

# timer fired function
def timerFired(app):
    if app.recordOnce:
        app.audio = ap.recordAudio()
        app.beforeTime = time.time()
        app.recordOnce = False
    if app.pitchDetect:
        ap.pitchInRealTime(app.params[0], app.params[1], app.params[2], 
                           app.params[3], app.params[4], app.beforeTime)

# key pressed function
def keyPressed(app, event):
    if event.key == 'Space': # 
        app.screen = 'record'
        app.recordOnce = True
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

# drawing main screen function
def drawMainScreen(app, canvas):
    canvas.create_text(app.width/2, 100, text = 'Guitar Tab Generator', 
                       font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height/2, text = 'Press space to begin recording.', 
                       font = 'Arial 12 bold')

# draw recording screen function
def drawRecordingScreen(app, canvas):
    canvas.create_oval(app.width/2 - 110, app.height/2 - 110, app.width/2 + 110, 
                         app.height/2 + 110, fill = 'black')
    canvas.create_oval(app.width/2 - 100, app.height/2 - 100, app.width/2 + 100, 
                         app.height/2 + 100, fill = 'red')
    canvas.create_text(app.width/2, app.height/2, text = 'Recording', font = 'Arial 16 bold')
    canvas.create_text(app.width/2, app.height - 100, text = 'Press s to stop.', font = 'Arial 12 bold')

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
    elif app.screen == 'tab':
        drawTabScreen(app, canvas)

# runApp function
def runGuitarTabGenerator():
    print('Running Guitar Tab Generator.')
    runApp(width = 1520, height = 800)

runGuitarTabGenerator()

