"""Programmet lytter til kommandoer fra serieporten.
NB! trenger installasjon av serial og pygame^ og kjores i python 3

Kommandoer som kan utfores
	1. Start opptak
	2. Stopp opptak
		Lagre som en lydfil med timestamp og lengde
	3. Start avspilling
		Spiller bare av lydfilen en gang
	4. Stopp avspilling
		Og klargjor til neste avspilling
Andre oppgaver:
	A. Si fra naar opptak er ferdig avspillt
"""


#Oppsett:
import serial, pygame, time, threading, datetime, serial.tools.list_ports, sys, wave, os, pyaudio



#Oppsett for seriallytting
riktigePortNavnElementer = ["cu.usbmodem", "Arduino", "Genuino", "ttiny", "tty"]
def kobleTilRiktigPort(baudRate):
	list = serial.tools.list_ports.comports()
	navn=""
	portene = []
	for element in list:
		for nokkel in riktigePortNavnElementer:
			if nokkel in element.device:
				return serial.Serial(element.device,baudRate)
		portene.append(element.device)
	print("Ingen kjente portnavn funnet. Saa ingen serieport kan bli lyttet til. Er alt koblet til?\nVurder aa legg til deler av folgende navn i 'riktigePortNavnElementer' om en av er riktig port: "+str(portene))
	return False

port = kobleTilRiktigPort(9600)
if not port:
	sys.exit("Programmet fungerer ikke uten aa kunne ta i mot kommandoer fra serieporten.")




#Oppsett for lydopptak
threadPause=0.0
FORMAT = pyaudio.paInt16
CHANNELS = 2
#RATE = 48000#44100 for andre mics?
#CHUNK = 8192#1024 for andre mics? men inputoverflow for meg
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3000 # Upper limit


def taOppLyd(): #Denne metoden skal kjore i bakgrunnen. Om det ikke funker helt maa vi vurdere deamon traader.
	while True:
		time.sleep(threadPause)
		if tarOppLyd:
			print("Tar opp lyd")
			audio = pyaudio.PyAudio()
			 # start Recording
			stream = audio.open(format=FORMAT, channels=CHANNELS,
							rate=RATE, input=True,
							frames_per_buffer=CHUNK)
			frames = []
			try:
				for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
					data = stream.read(CHUNK)
					frames.append(data)
					if not tarOppLyd:
						break
					#else:
					#	time.sleep(threadPause)
			except Exception as e:
				print(str(e))
				print("Om feilen ovenfor er 'exception_on_overflow' kan det muligens fikses ved aa sette 'CHUNK' til en hoyere verdi")
				pass

			stream.stop_stream()
			stream.close()
			audio.terminate()
			tempName = str(datetime.datetime.now()).replace(" ","_")+".wav"
			waveFile = wave.open(tempName, 'wb')
			waveFile.setnchannels(CHANNELS)
			waveFile.setsampwidth(audio.get_sample_size(FORMAT))
			waveFile.setframerate(RATE)
			waveFile.writeframes(b''.join(frames))
			waveFile.close()
			time.sleep(threadPause)
			print("Wrote file '"+tempName+"'")

tarOppLyd = False
opptakTraad = threading.Thread(target=taOppLyd)
opptakTraad.setDaemon(True)
opptakTraad.start()

#Oppsett for lydavspilling
lydFilNavn = "file.wav"  #Viktig at stemmer og er i samme mappe!-------------------------
pygame.init()
pygame.mixer.music.load(lydFilNavn)
spillerAvLyd = False















#Funksjon for kommando 1
def startOpptak():
	global tarOppLyd
	if(not tarOppLyd):
		print("starter opptak naa")
		tarOppLyd = True
	else:
		print("Arduino'n ba om aa starte opptak uten aa ha avsluttet det forrige. Saa vi bare fortsetter aa taa opp lyd. Men arduinokoden trenger kanskje litt oppmerksomhet.")

#Funksjon for kommando 2
def stoppOpptak():
	global tarOppLyd
	if(tarOppLyd):
		print("stopper opptak naa")
		tarOppLyd = False
	else:
		print("Arduino'n ba om aa stoppe opptak uten aa ha startet et opptak. Arduinokoden trenger kanskje litt oppmerksomhet.")

#Funksjon for kommando 3
def startLydAvspilling():
	global spillerAvLyd
	if(not pygame.mixer.music.get_busy()):
		print("starter avspilling naa")
		pygame.mixer.music.play() #Bare en avspilling
		spillerAvLyd = True
	else:
		print("Arduino'n ba om aa starte lydavspilling uten aa ha avsluttet det forrige eller latt forrige avspilling bli ferdig avspillt. Arduinokoden trenger kanskje litt oppmerksomhet.")
		#TODO Her kan vi kanskje heller starte lydavspilling paa nytt. og si fra om at avspillingen er ferdig.

#Funksjon for kommando 4
def stoppLydAvspilling():
	global spillerAvLyd
	if(pygame.mixer.music.get_busy()):
		print("stopper avspilling naa")
		pygame.mixer.music.stop()
		#pygame.mixer.music.rewind()
		spillerAvLyd = False
		siFraAtLydAvspillingErFerdig()
	else:
		print("Det er ingen lyd aa stoppe avspilling av.") # Skjer naar lydfilen blir spillt av helt ferdig













#Hjelpefunksjoner
def siFraAtLydAvspillingErFerdig():
	#print("Ferdig med lydavspilling")
	port.write("LydFil ferdig\r\n".encode());












#Her lyttr vi til serial og kaller riktige kommandoer, kjorer tilsvarende "loop" fra arduino.
while True:
	if (port.inWaiting()>0):
		data = port.readline()
		print("Fikk "+str(data)+" fra serieporten")
		if (data==b'Start opptak\r\n'):
			startOpptak()
		elif (data==b'Stopp opptak\r\n'):
			stoppOpptak()
		elif (data==b'Start avspilling\r\n'):
			startLydAvspilling()
		elif (data==b'Stopp avspilling\r\n'):
		  	stoppLydAvspilling()
	if(not pygame.mixer.music.get_busy()):#Om lydfilen ikke spilles av
		if(spillerAvLyd):#Men vi ikke stoppet den selv
			spillerAvLyd=False#Ma vi oppdatere vaar oversikt
			siFraAtLydAvspillingErFerdig()#Og si fra
	#print(str(spillerAvLyd)+"  ==  "+str(pygame.mixer.music.get_busy()))
