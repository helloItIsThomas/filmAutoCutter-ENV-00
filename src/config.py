import os
import sys
from pathlib import Path
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """Load configuration with extensive validation"""
    config = {
        'AUDIO_THRESHOLD': 0.2,
        'SCALING_FACTOR': 30,
        'BPM': 120,
        'QUANTIZE_DIVISION': 8,
        'BEZIER_DURATION': 0.5,
        'MAX_SPEED_MULTIPLIER': 2.5,
        'CURVE_INTENSITY': 0.9,
        'RETURN_INTENSITY': 0.3,
        'SAMPLE_RATE': 44100,
        'FRAMES_PER_BUFFER': 1024,
    }

    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / '.env'
        if not env_path.exists():
            raise FileNotFoundError(f"Missing .env file at {env_path}")
        load_dotenv(env_path)
        
        video_path = Path(os.getenv('VIDEO_PATH', 'assets/input.mp4'))
        if not video_path.exists():
            raise FileNotFoundError(f"Video file missing: {video_path}")
        config['VIDEO_PATH'] = str(video_path.resolve())
        
        return config
    except Exception as e:
        sys.exit(f"Configuration error: {str(e)}")
