from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

 

def get_volume_controller():
    """
    Get the Windows master volume controller.
    """

    devices = AudioUtilities.GetSpeakers()
 
    interface = devices._dev.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )

    return volume


def volume_up():
    """
    Increase Windows master volume by one step.
    """

    volume = get_volume_controller()

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = min(
        1.0,
        current_volume + 0.05
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print("🔊 Volume Up")


def volume_down():
     

    volume = get_volume_controller()

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = max(
        0.0,
        current_volume - 0.05
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print("🔉 Volume Down") 

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

 

def get_volume_controller():
    

    devices = AudioUtilities.GetSpeakers()

     
    interface = devices._dev.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )

    volume = cast(
        interface,
        POINTER(IAudioEndpointVolume)
    )

    return volume


def volume_up():
    

    volume = get_volume_controller()

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = min(
        1.0,
        current_volume + 0.20
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print("🔊 Volume Up")


def volume_down():
    

    volume = get_volume_controller()

    current_volume = volume.GetMasterVolumeLevelScalar()

    new_volume = max(
        0.0,
        current_volume - 0.20
    )

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )

    print("🔉 Volume Down")


 

def play_pause():
    

     
    # Send the Play/Pause media key to Windows.
    import pyautogui

    pyautogui.press("playpause")

    print("▶️⏸️ Play / Pause")


 

def move_cursor(x, y):
    

    import pyautogui

    # Move cursor instantly to the calculated screen position.
    pyautogui.moveTo(
        int(x),
        int(y)
    )

def move_cursor_from_hand(x, y):
    

    import pyautogui
 

    CONTROL_LEFT = 0.35
    CONTROL_RIGHT = 0.65
    CONTROL_TOP = 0.30
    CONTROL_BOTTOM = 0.70

    # Keep hand inside the control zone
    x = max(CONTROL_LEFT, min(CONTROL_RIGHT, x))
    y = max(CONTROL_TOP, min(CONTROL_BOTTOM, y))

     
    normalized_x = (
        (x - CONTROL_LEFT)
        / (CONTROL_RIGHT - CONTROL_LEFT)
    )

    normalized_y = (
        (y - CONTROL_TOP)
        / (CONTROL_BOTTOM - CONTROL_TOP)
    )

    screen_width, screen_height = pyautogui.size()

    target_x = normalized_x * (screen_width - 1)
    target_y = normalized_y * (screen_height - 1)
 

    SMOOTHING = 0.30

     

    DEAD_ZONE = 45

    # Keep previous cursor position between frames
    if not hasattr(move_cursor_from_hand, "current_x"):

        move_cursor_from_hand.current_x = target_x
        move_cursor_from_hand.current_y = target_y

    
    delta_x = (
        target_x
        - move_cursor_from_hand.current_x
    )

    delta_y = (
        target_y
        - move_cursor_from_hand.current_y
    )

    # If movement is extremely small, don't move.
    if abs(delta_x) < DEAD_ZONE:
        delta_x = 0

    if abs(delta_y) < DEAD_ZONE:
        delta_y = 0
 
    move_cursor_from_hand.current_x += (
        delta_x * SMOOTHING
    )

    move_cursor_from_hand.current_y += (
        delta_y * SMOOTHING
    )
 
    move_cursor(
        move_cursor_from_hand.current_x,
        move_cursor_from_hand.current_y
    )