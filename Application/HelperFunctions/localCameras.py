"""
This file analyzes the possible options for a camera source that can be used.
"""

# Import statements
from PyQt5.QtMultimedia import QCameraInfo


# Functions
def get_available_cameras():
    # Get the list of available cameras
    cameras = QCameraInfo.availableCameras()
    available_cameras = {}

    for i, camera in enumerate(cameras):
        available_cameras[i] = camera.description()
    return available_cameras
