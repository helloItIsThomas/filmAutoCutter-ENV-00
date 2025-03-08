import cv2
import aubio
import numpy as np
import pyaudio
import time
import logging
from config import load_config

class AudioVisualError(Exception):
    """Base class for all audio-visual exceptions"""
    pass

class VideoBeatSync:
    def __init__(self):
        self.config = load_config()
        self._init_logging()
        self._validate_dependencies()
        self._init_resources()

    def _init_logging(self):
        """Configure robust logging system"""
        self.logger = logging.getLogger('VideoBeatSync')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(handler)

    def _validate_dependencies(self):
        """Check critical dependency versions"""
        try:
            assert cv2.__version__ >= '4.9.0', "OpenCV version too old"
            assert aubio.version >= (0, 4, 9), "Aubio version mismatch"
        except AssertionError as e:
            raise AudioVisualError(f"Dependency error: {str(e)}")

    def _init_resources(self):
        """Safe resource initialization with cleanup"""
        try:
            self._init_audio()
            self._init_video()
            self._init_processing()
        except Exception as e:
            self._cleanup()
            raise AudioVisualError(f"Initialization failed: {str(e)}")

    def _init_audio(self):
        """Initialize audio resources with error recovery"""
        self.p = pyaudio.PyAudio()
        try:
            self.audio_stream = self.p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.config['SAMPLE_RATE'],
                input=True,
                frames_per_buffer=self.config['FRAMES_PER_BUFFER'],
                stream_callback=self._audio_callback
            )
            self.onset_detector = aubio.onset(
                "default", 
                self.config['FRAMES_PER_BUFFER'] * 2,
                self.config['FRAMES_PER_BUFFER'],
                self.config['SAMPLE_RATE']
            )
        except OSError as e:
            self.logger.error("Audio device error. Available devices:")
            for i in range(self.p.get_device_count()):
                info = self.p.get_device_info_by_index(i)
                self.logger.error(f"Device {i}: {info['name']}")
            raise

    def _init_video(self):
        """Video initialization with hardware acceleration"""
        self.cap = cv2.VideoCapture(self.config['VIDEO_PATH'])
        if not self.cap.isOpened():
            raise IOError(f"Failed to open video: {self.config['VIDEO_PATH']}")
        
        # Try to enable hardware acceleration
        backend = cv2.CAP_ANY  # Auto-detect backend
        if cv2.CAP_MSMF in cv2.getBuildInformation():
            backend = cv2.CAP_MSMF  # Windows Media Foundation
        self.cap.set(cv2.CAP_PROP_BACKEND, backend)
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_delay = 1 / self.fps

    # Rest of the class implementation with error handling...
    # [Include the rest of the VideoBeatSync class from previous implementation]
