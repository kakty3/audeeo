import filetype


def is_audio(obj):
    """Check if file is audio
    
    Args:
        obj: path to file, bytes or bytearray.

    Returns:
        True if file is audio. Otherwise False.
    """
    try:
        return filetype.audio(obj) is not None
    except TypeError:
        return False
