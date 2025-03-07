from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import sounddevice as sd

THRESHOLD = 1e-3  # Volume threshold

class MicrophoneManager(QObject):

    hearingInputSignal = pyqtSignal(bool)

    def __init__(self, parent = None):
        super().__init__(parent)
        self.muted = False
        self.volumeLevel = 0
        self.hearingInput = False

        devices = AudioUtilities.GetAllDevices()

        # Get the audio devices
        self.pyCawDevice = AudioUtilities.GetMicrophone()
        pyCawDeviceID = self.pyCawDevice.GetId()
        self.pyCawDeviceFriendlyName = ""

        for device in devices:
            if device.id == pyCawDeviceID:
                print("Found device!!")
                self.pyCawDeviceFriendlyName = device.FriendlyName

        self.interface = self.pyCawDevice.Activate(
            IAudioEndpointVolume._iid_, 
            1, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)

        self.muted = self.volume.GetMute() == 1

        # Find the corresponding device index in sounddevice
        self.sdDevice = self.GetDeviceIndex(self.pyCawDeviceFriendlyName)

        # Set the parameters for audio stream
        self.samplerate = 44100  # Sampling rate (Hz)
        self.channels = 1  # Mono audio
        self.chunk = 1024  # Number of samples per chunk

        # Start the audio stream in a non-blocking way using a callback
        self.stream = sd.InputStream(callback=self.AudioCallback,
                                     device=self.sdDevice,
                                     channels=self.channels,
                                     samplerate=self.samplerate,
                                     blocksize=self.chunk)
        self.stream.start()

    def AudioCallback(self, indata, frames, time, status):
        if status:
            print(status)
        
        # Calculate volume level (RMS value of the audio)
        volume = np.linalg.norm(indata) / np.sqrt(len(indata))
    
        hearingInput = volume > THRESHOLD
        if hearingInput != self.hearingInput:
            self.hearingInputSignal.emit(hearingInput)

        self.hearingInput = hearingInput

    def GetDeviceIndex(self, device_name):
        """ Find the device index that corresponds to the pycaw device name """
        # List all available input devices from sounddevice
        devices = sd.query_devices()
        
        for idx, device in enumerate(devices):
            # If the device name matches, return the index
            if device_name.lower() in device['name'].lower():
                return idx
        
        # If no match is found, raise an error
        raise ValueError(f"Device {device_name} not found in sounddevice.")

    def Update(self):
        self.muted = self.volume.GetMute() == 1
        pass

    def ToggleMute(self):
        self.muted = not self.muted

        self.volume.SetMute(1 if self.muted else 0, None)
        pass