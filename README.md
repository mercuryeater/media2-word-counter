# YOUR PROJECT TITLE

### Video Demo: <URL HERE>

### Description:

what your project is

This program is made to analyze speeches and automatically create a transcript .txt file for latter uses or implementatipns from some other program.

In this analysis it counts the amount of times a certain word specified by the user appeared and also it makes a to 5 most repetitive words in the whole text.

from which you can call the function count() which serves the purpouse of counting the amo

what each of the files you wrote for the project contains and does

Two files were written for this project:

- project.py:
  - This one contains the program itself
- test_project.py:
  - This file contains the unit tests for each of the functions used in the prject.py file, to ensure that most (if not all) bugs are catch

if you debated certain design choices, explaining why you made them

At first it was a prgram just thougt to make the transcription...

### Set up:

#### whisper:

First we have to remember to install the whisper library with:

    pip install -U openai-whisper

And also as a requirement for whisper we need to check we have installed in our system [`ffmpeg`](https://ffmpeg.org/), an open-source software tool made to read, write, filter and transcode various media formats:

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

# on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

# on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
```

We can however check this and verify it in the whisper documentation: https://github.com/openai/whisper

#### Related:

Would like to learn about text embeddings to include something related to keywords by my own, in the meantime is worth checking [`KeyBERT`](https://github.com/MaartenGr/KeyBERT), and read it's documentation linking to other repos and even a paper on the subject.

Also it made me search and investigate about Natural Language Processing and I landed on the [`NLTK`](https://www.nltk.org/) page where a book can be found related to the subject. This too is really close to what I iagined would be a speech analyser.

To reference **youtube-dl** I read the implementation of the class _YoutubeDL_ [`here`](https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py)

TODO
Trying to make work with gpu following this [example](https://stackoverflow.com/questions/75908422/whisper-ai-error-fp16-is-not-supported-on-cpu-using-fp32-instead) in stackOverflow.
