from project import transcribe, count, words_frequency, media_to_mp3
import pytest
import unittest.mock as mock
import os
import yt_dlp

invalid_format = "test/bob.jpg"
valid_audio = "test/test_audio.mp3"
short_audio = "test/test2.m4a"
out_name = "test/test_output"
out_name2 = "test/test2_output"
word = "support"
test_count_arg = "test/test_output"
url_media = "https://www.youtube.com/shorts/vryFBIuVkbo"
no_media = "https://github.com/yt-dlp/yt-dlp"


def test_media_to_mp3():
    vid_name = "Happy New Year from CS50 🎊.m4a"
    with mock.patch("builtins.input", side_effect=[url_media]):
        assert media_to_mp3() == vid_name
        os.remove(vid_name)

    with mock.patch("builtins.input", side_effect=[no_media]):
        with pytest.raises(yt_dlp.utils.DownloadError):
            media_to_mp3()


def test_transcribe():
    assert transcribe(valid_audio, out_name) == True

    with pytest.raises(RuntimeError):
        transcribe(invalid_format, out_name, model="base")

    with pytest.raises(RuntimeError):
        transcribe("anything.mp3", out_name, model="base")


def test_count():
    with mock.patch("builtins.input", return_value="support"):
        assert count(test_count_arg) == "The word 'support' appears 11 times."

    with mock.patch("builtins.input", side_effect=["citizens"]):
        assert count(test_count_arg) == "The word 'citizens' appears 2 times."

    with mock.patch("builtins.input", return_value="blah"):
        with pytest.raises(FileNotFoundError):
            count("nonexistent")


def test_words_frequency():
    words_freq = [
        ["word", "frequency"],
        ("building", 6),
        ("test", 5),
        ("times", 4),
        ("cat", 3),
        ("dog", 2),
        ("five", 1),
        ("two", 1),
        ("three", 1),
        ("six", 1),
    ]

    assert words_frequency(out_name2) == words_freq

    with pytest.raises(FileNotFoundError):
        words_frequency("nonexistent")
