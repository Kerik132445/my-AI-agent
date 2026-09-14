import ctypes
import time

from ctypes import cast, POINTER
from datetime import datetime, date

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume():
    try:
        import comtypes
        comtypes.CoInitialize()
    except Exception:
        pass

    enumerator = AudioUtilities.GetDeviceEnumerator()
    device = enumerator.GetDefaultAudioEndpoint(0, 0)
    interface = device.Activate(
        IAudioEndpointVolume._iid_,
        CLSCTX_ALL,
        None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume


def set_volume(level: int):
    try:
        level = int(level)
        volume = get_volume()

        volume.SetMute(False, None)

        target_level = max(0, min(100, level)) / 100.0
        volume.SetMasterVolumeLevelScalar(target_level, None)

        return f"Громкость установлена на {level}%."

    except Exception as e:
        return f"При установке громкости произошла ошибка: {str(e)}"


def get_time():
    return datetime.now().strftime("%H:%M:%S")


def get_date():
    return date.today().strftime("%d.%m.%Y")


def mute_volume():
    try:
        volume = get_volume()

        current_mute = volume.GetMute()
        volume.SetMute(not current_mute, None)

        state = "выключен" if not current_mute else "включен"

        return f"Звук {state}."

    except Exception as e:
        return f"Ошибка при переключении звука: {str(e)}"


def collapse_win():
    try:
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)

        time.sleep(0.05)

        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)

        time.sleep(0.4)

        return "Окна свернуты/развернуты (Win+D)"

    except Exception as e:
        return f"Ошибка при сворачивании/разворачивании окон: {str(e)}"
