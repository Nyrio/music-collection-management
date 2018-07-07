import os

# The supported formats in lower case
# TODO: update this list
FORMATS = ("mp3", "ogg", "flac", "ape", "wav")


def get_music_files_in_dir(dirpath, formats=FORMATS):
    """Return all the music files in the given directory matching the
    specified formats or the default ones.
    The formats must be given in lower case in an iterable.
    """
    music_files = []
    for subdirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            is_music = False
            for format_ in formats:
                if filename.lower().endswith(format_):
                    is_music = True
                    break
            if is_music:
                music_files.append(os.path.join(subdirpath, filename))
    return music_files
