import time
# import math
# import array
# import librosa #python3 -m pip install --upgrade librosa
# import pyrubberband as pyrb # python3 -m pip install pyrubberband
# import pyaudio     #python3 -m pip install --upgrade PyAudio
# import wave
# import numpy
# from threading import Thread

import pygame #sudo apt-get install freepats #python3 -m pip install -U pygame --user
from midiutil.MidiFile import MIDIFile #python3 -m pip install MIDIUtil
import tkinter
from tkinter import *
from tkinter import ttk
CHAR_DIESE = "#"
CHAR_BEMOL ="♭"
CHAR_DELTA = "Δ"
CHAR_PHI = "ø"
CHAR_DEG ="°"
GAMME = ["DO","RE","MI","FA","SOL","LA","SI"]
ALTERATIONS = ["","#","♭"]
ALTERATIONSDICT = {"":0,"#":1,"♭":-1}
INTERS_MAJEUR = {"DO":0,"RE":2,"MI":4,"FA":5,"SOL":7,"LA":9,"SI":11}
INTERS_GAMME = {"1":0,"2":2,"3":4,"4":5,"5":7,"6":9,"7":11,}

CHORDS = {"Triades":
           {
               #Majeur
               'M':{"composition":["1","3","5"],"alt_names":"Majeur"},
               "SUS":{"composition":["1","4","5"],"alt_names":"4,SUS4,SUSPENDU"},
               "(♭5)":{"composition":["1","3","5-"],"alt_names":"5-,5♭,5dim"},
               "+":{"composition":["1","3","5+"],"alt_names":"aug,5+,#5"},
               #Mineur
               "m":{"composition":["1","3-","5"],"alt_names":"-,mineur"},
               "m(♭5)":{"composition":["1","3-","5-"],"alt_names":"°,-5♭"},
               "m+":{"composition":["1","3-","5+"],"alt_names":"°,m5+"},
            },
           "Tétrades":
           {
               #Majeur
               '6':{"composition":["1","3","5","6"],"alt_names":"add6"},
               '7M':{"composition":["1","3","5","7"],"alt_names":"Δ,M7,MAJ7"},
                '7':{"composition":["1","3","5","7-"],"alt_names":"7ème de dominante"},
                'add9':{"composition":["1","3","5","9"],"alt_names":""},
                '7 sus':{"composition":["1","4","5","7-"],"alt_names":""},
                '7(♭5)':{"composition":["1","3","5-","7-"],"alt_names":"7-5"},
                '+7':{"composition":["1","3","5+","7-"],"alt_names":"7+,7+5,7aug,7(#5)"},
                '+7M':{"composition":["1","3","5+","7"],"alt_names":""},
                #mineur
                'm6':{"composition":["1","3-","5","6"],"alt_names":"madd6,-6"},
                'm7M':{"composition":["1","3-","5","7"],"alt_names":"-Δ,-MAJ7"},
                'm7':{"composition":["1","3-","5","7-"],"alt_names":"-7,mi7,min7"},
                'madd9':{"composition":["1","3-","5","9"],"alt_names":""},
                'm7(♭5)':{"composition":["1","3-","5-","7-"],"alt_names":"ø"},
                '°':{"composition":["1","3-","5-","6"],"alt_names":"dim7,dim,7-"},
                '°(7M)':{"composition":["1","3-","5-","7"],"alt_names":"°Δ,mi(7M♭5)"},

            },
           "5sons":
           {
               #Majeur
               '7M9':{"composition":["1","3","5","7","9"],"alt_names":"9(7M)"},
               '9':{"composition":["1","3","5","7-","9"],"alt_names":"79"},
               '7(♭9)':{"composition":["1","3","5","7-","9-"],"alt_names":"9♭,9-"},
               '7(#9)':{"composition":["1","3","5","7-","9+"],"alt_names":"9#,9+"},
               '9sus':{"composition":["1","4","5","7-","9"],"alt_names":""},
               '69':{"composition":["1","3","5","6","9"],"alt_names":"6/9"},
               '11(omit3)':{"composition":["1","5","7-","9","10"],"alt_names":""},
               #mineur
               'm9(7M)':{"composition":["1","3-","5","7-","9"],"alt_names":"-9(7M)"},
               'm9':{"composition":["1","3-","5","7","9"],"alt_names":"-79"},
               'm7(♭9)':{"composition":["1","3-","5","7-","9-"],"alt_names":"-79♭"},
               'm9(♭5)':{"composition":["1","3-","5-","7-","9"],"alt_names":"-79♭5"},
               'm7(♭9♭5)':{"composition":["1","3-","5-","7-","9-"],"alt_names":""},
            },
           "6sons":
           {
               #majeur
               '11':{"composition":["1","3","5","7-","9","11"],"alt_names":""},
               '9(#11)':{"composition":["1","3","5","7-","9","11+"],"alt_names":""},
               '7(#11♭9)':{"composition":["1","3","5","7-","9-","11+"],"alt_names":""},
               '11(7M)':{"composition":["1","3","5","7","9","11"],"alt_names":""},
               '9(#11 7M)':{"composition":["1","3","5","7","9","11+"],"alt_names":""},
               #Mineur
               'm11':{"composition":["1","3-","5","7-","9","11"],"alt_names":""},
               'm9(#11)':{"composition":["1","3-","5","7-","9","11+"],"alt_names":""},
               'm7 (#11♭9) ':{"composition":["1","3-","5","7-","9-","11+"],"alt_names":""},
               'm11 (♭5) ':{"composition":["1","3-","5-","7-","9","11"],"alt_names":""},
               'm11 (♭5♭9) ':{"composition":["1","3-","5-","7-","9-","11"],"alt_names":""},
               'm11 (7M) ':{"composition":["1","3-","5","7","9","11"],"alt_names":""},
                #'11-13':{"composition":["1","3","5","7","9","11+","13"],"alt_names":""},
            }
           }


class midiWrite():
    def __init__(self):
        self.filename = "output.mid"
        # create your MIDI object
        self.mf = MIDIFile(1)     # only 1 track
        self.track = 0   # the only track
        
        self.time = 0    # start at the beginning
        self.mf.addTrackName(self.track, self.time, "Sample Track")
        self.mf.addTempo(self.track, self.time, 120)
        # add some notes
        self.channel = 0
        self.volume = 100
    def addNote(self,pitch,tim):
        duration = 1         # 1 beat long
        self.mf.addNote(self.track, self.channel, pitch, tim, duration, self.volume)
    def writeFile(self):
        outf =open("output.mid", 'wb')
        self.mf.writeFile(outf)
        self.mf.close()
        
class MidiPlay():
    def __init__(self):
        self.midi_filename = 'output.mid'
        # mixer config
        freq = 44100  # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024   # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)

    def play_music(self):
        '''Stream music_file in a blocking manner'''
        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.midi_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished





class PlayChord():
    def __init__(self,chord,inst_filename,sample_root_note,alteration,tone,gamme):
        self.gamme = gamme
#         self.sample_root_note = sample_root_note
        self.chord = chord
        self.alteration = alteration
        self.tone = tone
#         self.SoundBinTab = []
#         self.fullBuff= b''
#         self.durationEvent = 60.0/120./4.0
        self.fname=inst_filename
    def playChord(self):
        pitches = self.chord.get("inter")
        pitches.append(-12)
        corrected_pitches = []
        for pitch in pitches :
            correctedpicth = pitch+ALTERATIONSDICT.get(self.alteration)+INTERS_MAJEUR.get(self.tone)
            corrected_pitches.append(correctedpicth)
        pitches = corrected_pitches
        mymidiWrite = midiWrite()
        for pitch in pitches :
            mymidiWrite.addNote(pitch+60, 0)
        mymidiWrite.writeFile()
        myplay = MidiPlay()
        myplay.play_music()
    def playGamme(self):
        pitches = self.gamme
        corrected_pitches = []
        for pitch in pitches :
            correctedpicth = pitch#+INTERS_MAJEUR.get(self.tone)
            corrected_pitches.append(correctedpicth)
        pitches = corrected_pitches
        mymidiWrite = midiWrite()
        index= 0
        for pitch in pitches :
            mymidiWrite.addNote(pitch+60, index)
            index+=1
        mymidiWrite.writeFile()
        myplay = MidiPlay()
        myplay.play_music()
class Application(Toplevel):
    def __init__(self, master, **kw):
        Toplevel.__init__(self, master, **kw)
        self.makeChordsList()
        self.MainPanel = PanedWindow(self,orient=VERTICAL)
        self.MainPanel.pack(fill=BOTH,expand=1)
        self.tone = "DO"
        self.alteration =""
        self.sample_root_note=-1
        self.inst_file_name = "guitar-onenote-vibro-fuzzyB.wav"
        self.chordName = self.listChords[0]
        self.chord = self.dictAllChords.get(self.chordName[0])
#         self.inst_label = Label(self.MainPanel, text="Instrument")
#         self.inst_label.pack()
#         inst_var = StringVar(value=["piano","guitare"])
#         self.inst_lb = Listbox(self.MainPanel,listvariable=inst_var,
#     height=4,)
#         self.inst_lb.pack()
#         scrollbar_inst = ttk.Scrollbar(self.inst_lb,orient='vertical',command=self.inst_lb.yview)
#         scrollbar_inst.pack(side = RIGHT)#, fill = BOTH)
#         self.inst_lb['yscrollcommand'] = scrollbar_inst.set
#         self.inst_lb.bind('<<ListboxSelect>>', self.instSelect)
#         self.MainPanel.add(self.inst_label)
#         self.MainPanel.add(self.inst_lb)
        
        self.tone_label = Label(self.MainPanel, text="Tonalité")
        self.tone_label.pack()
        self.MainPanel.add(self.tone_label)
        
        tone_var = StringVar(value=GAMME)
        self.tone_lb = Listbox(self.MainPanel,listvariable=tone_var,height=5)#,yscrollcommand=scrollbar_tone.set)#,height = 10,)#,height=10)
        scrollbar_tone = Scrollbar(self.tone_lb,orient='vertical')#,command=self.tone_lb.yview)
        self.tone_lb.config(yscrollcommand=scrollbar_tone.set)
        scrollbar_tone.config(command=self.tone_lb.yview)
        
#         scrollbar_tone.config( command = self.tone_lb.yview )
#         scrollbar_tone.pack( side = RIGHT, fill = Y )
        self.tone_lb.pack(side = LEFT,fill=BOTH,expand = True)#fill=BOTH,expand=1)

#         scrollbar_tone.pack(side = RIGHT,fill = BOTH,expand=False)#, fill = BOTH)
        self.tone_lb['yscrollcommand'] = scrollbar_tone.set
        self.tone_lb.bind('<<ListboxSelect>>', self.toneSelect)
        
        self.MainPanel.add(self.tone_lb)

        self.alteration_label = Label(self.MainPanel, text="Altération")
        alter_var = StringVar(value=ALTERATIONS)
        self.alter_lb = Listbox(self.MainPanel,listvariable=alter_var,
    height=3,)
        scrollbar_alter = ttk.Scrollbar(self.alter_lb,orient='vertical',command=self.alter_lb.yview,)
#         scrollbar_alter.pack(side = RIGHT)#, fill = BOTH)
        self.alter_lb['yscrollcommand'] = scrollbar_alter.set
        self.alter_lb.bind('<<ListboxSelect>>', self.alterSelect)
        self.MainPanel.add(self.alteration_label)
        self.MainPanel.add(self.alter_lb)
        
        
        self.chord_label = Label(self.MainPanel, text="Accord")
        listChords = []
        for chord in self.listChords:
            txt = chord[0]
            if len(chord[1])>0:
                txt += ", aussi noté : "+chord[1]
            listChords.append(txt)
        chord_var = StringVar(value=listChords)
        self.chord_lb = Listbox(self.MainPanel,listvariable=chord_var,
    height=10,)
        scrollbar_chord = ttk.Scrollbar(self.chord_lb,orient='vertical',command=self.chord_lb.yview)
#         scrollbar_chord.pack(side = RIGHT)#, fill = BOTH)
        self.chord_lb['yscrollcommand'] = scrollbar_chord.set
        self.chord_lb.bind('<<ListboxSelect>>', self.chordSelect)
        self.MainPanel.add(self.chord_label)
        self.MainPanel.add(self.chord_lb)
        
#         self.goButton = Button(self.MainPanel,text="Play",command= self.Play)
#         self.MainPanel.add(self.goButton)
        self.gammeLabelContent = StringVar(value="Gam")
        self.gammeLabel = Label(self.MainPanel,textvariable=self.gammeLabelContent)
        self.gammeLabelContent.set("Gamme Majeure")
        self.MainPanel.add(self.gammeLabel)
        self.gammePanel = PanedWindow(self,orient=HORIZONTAL)
        self.gammePanel.pack()#fill=BOTH,expand=1)
        self.gammeText = Text(self.gammePanel,height=1)
        self.gammeText.insert(END, "1-DO 2-RE 3-MI 4-FA 5-SOL 6-LA 7")
        self.gammeText.delete("1.0", END)
        self.gammeText.insert(END, "1-DO 2-RE 3-MI 4-FA 5-SOL 6-LA 7-SI")
        self.gammeText.pack()
        self.playGammeButton=Button(self.gammePanel,text="PlayGamme",command = self.playGamme)
        self.playGammeButton.pack()
        self.gammePanel.add(self.gammeText)
        self.gammePanel.add(self.playGammeButton)
        self.MainPanel.add(self.gammePanel)
        self.chordLabelText = StringVar(value ="toto")
        self.chordlabel = Label(self.MainPanel,textvariable = self.chordLabelText)
        self.chordLabelText.set("DO M")
        self.MainPanel.add(self.chordlabel)
        self.chordPanel = PanedWindow(self,orient=HORIZONTAL)
        self.chordPanel.pack()#fill=BOTH,expand=1)
        self.chordText = Text(self.chordPanel,height=1)
        self.chordText.insert(END, "1-DO 3-MI 5-SOL")
        self.chordText.pack()
        self.playchordButton=Button(self.chordPanel,text="PlayChord",command = self.playChord)
        self.playchordButton.pack()
        self.chordPanel.add(self.chordText)
        self.chordPanel.add(self.playchordButton)
        self.MainPanel.add(self.chordPanel)
        
        
#         self.canvas =  Canvas(self.MainPanel,bg="black")#, height=20, width=50)
#         self.MainPanel.add(self.canvas)
        self.makeGamme()
    def toneSelect(self,event):
        selected_indice = self.tone_lb.curselection()
        if len(selected_indice)>0:
            self.tone = GAMME[selected_indice[0]]
        if event is not None :
            self.computeGammeChord()
        
    def alterSelect(self,event):
        selected_indice = self.alter_lb.curselection()
        if len(selected_indice)>0:
            self.alteration = ALTERATIONS[selected_indice[0]]
        if event is not None :
            self.computeGammeChord()

    def chordSelect(self,event):
        selected_indice = self.chord_lb.curselection()
        if len(selected_indice)>0:
            self.chordName = self.listChords[selected_indice[0]]
            self.chord = self.dictAllChords.get(self.chordName[0])
        if event is not None :
            self.computeGammeChord()
    def drawLine(self,x1,y1,x2,y2,color="white"):
        self.canvas.create_line(x1,y1,x2,y2,fill=color)
    def makeChordsList(self):
        self.listChords = []
        self.dictAllChords ={}
        for typeChord,chordsDict in CHORDS.items():
            for chordName,chordDict in chordsDict.items():
                nameChord = [chordName,chordDict.get("alt_names")]
                self.listChords.append(nameChord)
                inter =  []
                composition = chordDict.get("composition")
                for degre in composition:
                    oct = 0
                    deg = degre.replace("-","").replace("+","")
#                     print("deg",deg)
                    if int(deg) > 7 :
                        deg =str(int(deg)-7)
                        oct = 1
#                     print("deg2",deg)
                    hauteur = INTERS_GAMME.get(deg)
#                     print('hauteur',hauteur)
                    if len(degre)>1:
                        alter = degre[-1]
                        if alter =="-":
                            alter =-1
                        elif alter =="+":
                            alter = +1
                        else :
                            alter = 0
                    else :
                        alter = 0
                    interitem=hauteur+alter+12*oct
                    inter.append(interitem)
                self.dictAllChords[chordName]={"name":chordName,
                                               "alt_names":chordDict.get("alt_names"),
                                               "composition":composition,
#                                                "inter":chordDict.get("inter")
                                               "inter":inter
                                               }
#         print(self.listChords)
#         print(self.dictAllChords)
    def computeGammeChord(self):
        self.chordSelect(None)
#         self.instSelect(None)
        self.alterSelect(None)
        self.toneSelect(None)
        self.makeGamme()
        self.makeChord()

    def playGamme(self):
        notesgamme = []
        lastinter = 0
        for note in self.gamme :
            inter = INTERS_MAJEUR.get(note[0])+note[1]
            if inter < lastinter :
                inter+=12
            notesgamme.append(inter)
            lastinter=inter
        note = self.gamme[0]
        notesgamme.append(12+ INTERS_MAJEUR.get(note[0])+note[1])
        myPlayChord = PlayChord(self.chord,self.inst_file_name,self.sample_root_note,self.alteration,self.tone,notesgamme)
        myPlayChord.playGamme()
    def playChord(self):
        myPlayChord = PlayChord(self.chord,self.inst_file_name,self.sample_root_note,self.alteration,self.tone,None)
        myPlayChord.playChord()
    def makeGamme(self):
        tone = self.tone  #RE
        alter = self.alteration # 0
        if self.alteration == "#":
            alter = 1
        elif self.alteration == "♭":
            alter =-1
        else :
            alter = 0
        gamme = []
        self.gamme = []
        for i in range(7):#2
            note=GAMME[(GAMME.index(tone)+i)%7]#FA
            internote =  INTERS_GAMME[str(GAMME.index(note)+1)]
            intertone =INTERS_GAMME[str(GAMME.index(tone)+1)] #inter(FA)-inter(RE) = 5-2 = 3
            intertrouve = internote-intertone
            if intertrouve < 0 :
                intertrouve +=12
            intervoulu =INTERS_GAMME[str(i+1)]#4
            alterationToNote = intervoulu-intertrouve+alter
            dictAlter = {0:"",1:"#",2:"##",-1:"♭",-2:"♭♭"}
            gamme.append(note+dictAlter.get(alterationToNote))
            self.gamme.append([note,alterationToNote])
        gammeTxt =""
        index = 1
        for note in gamme :
            gammeTxt = gammeTxt + str(index)+":"+note+" "
            index +=1
        self.gammeText.insert(END,gammeTxt)
        self.gammeText.delete("1.0",END)
        self.gammeText.insert(END,gammeTxt)

    def makeChord(self):
#         print("---")
        chord = self.chord
#         print(self.tone)
#         print(self.alteration)
#         print (chord)
        chordlabelText = self.tone+" "+self.alteration+" "+self.chord.get("name")+" aussi noté : "+self.chord.get("alt_names")
        self.chordLabelText.set(chordlabelText)
        chordText =""
#         print(self.chord.get("composition"))
#         print(self.gamme)
        for hauteur in self.chord.get("composition"): #5-
            chordText += hauteur
            ht = hauteur.replace("-","").replace("+","")
            if int(ht)>7:
                ht = str(int(ht)-7)
            note = self.gamme[int(ht)-1][0]
            althaut = 0
            if len(hauteur)>1 :
                if hauteur[-1]=="+":
                    althaut = 1
                elif hauteur[-1]=="-":
                    althaut = -1
                else :
                    althaut =0
#                 chordText += hauteur[-1]
            alt = self.gamme[int(hauteur[0])%7-1][1]+althaut
            if alt >0 :
                altsym = "#"*alt
            elif alt <0 :
                altsym = "♭"*(-alt)
            else : 
                altsym = ""
            chordText += ":"+note+altsym+"  "
        self.chordText.delete("1.0",END)
        self.chordText.insert(END, chordText)
        
    def printChord(self):
        print("PrintChord")
        composition = self.chord.get("composition")
        tone = self.tone+self.alteration
        print("PrintChordDone")
        

if __name__ == "__main__":
    tk = Tk()
    tk.withdraw()
    application = Application(tk)
    def on_closing():
        tk.destroy()
    application.protocol("WM_DELETE_WINDOW", on_closing)
    try:
        tk.mainloop()
    except KeyboardInterrupt:
        application.quit()


