# MEDIA TO WORDS

### Video Demo: <URL HERE>

## Description:

This program is designed to transcribe any media containing an audio stream and automatically generate a .txt file with all the words recognized in the given media. Simultaneously, a .csv file is created, displaying the frequency of each word’s occurrence in the media.

Additionally, the program includes a function that counts the number of times a specific word, as specified by the user, appears. It also generates a list of the top 10 most frequently repeated words in the entire text. This information is displayed in the console using the tabulate module.

The program has an optional command line argument to set a different model to be used by whisper when transcribing the audio, the options are:

- `python project.py tiny`

- `python project.py base`

- `python project.py small`

- `python project.py medium`

- `python project.py large`

If no command line argument is provided the it uses the default value: `base`. This proved to be the more efficient one in terms of time and transcription quality, however if a language different to english is being used then using at least the `small` model is recommended. For the time being there is no implementation that makes use of the GPU.

Reference from [whisper](https://github.com/openai/whisper) documentation:

|  Size  | Parameters | Multilingual model | Required VRAM | Relative speed |
| :----: | :--------: | :----------------: | :-----------: | :------------: |
|  tiny  |    39 M    |       `tiny`       |     ~1 GB     |      ~32x      |
|  base  |    74 M    |       `base`       |     ~1 GB     |      ~16x      |
| small  |   244 M    |      `small`       |     ~2 GB     |      ~6x       |
| medium |   769 M    |      `medium`      |     ~5 GB     |      ~2x       |
| large  |   1550 M   |      `large`       |    ~10 GB     |       1x       |

### Files in program

The program contains 3 files:

- **project.py:**

  This file contains the project in its entirety, including the main function that invokes all other functions. It also contains several try/except blocks and conditional statements to ensure the program operates correctly and validates user input. For instance, it verifies whether certain functions should be executed based on user preferences. The first decision the user makes is to choose whether the program should process online media or local media. This choice is facilitated through a prompt asking the user if they will be processing an online media or a local file. If the former is selected, then the following function is executed:

  - **media_to_mp3()**:

    This function prompts the user for a url containing media, the the library [yt_dlp](https://github.com/yt-dlp/yt-dlp) is used to extract and download the audio file from the url passed by the user. If no issues is raised, then the title of the dowload file is assigned to a variable and if it contains any _forbidden_ characters for the os a regex us used to replace those characters by a '#', just as ytdlp does, to ensure that the next functions are able to find the file. Finally the download file is returned.

  If the user has used a local file or if the media_to_mp3() function has already been executed, then a `while true` block is initiated. This block prompts the user for the Output filename for the .txt and .csv files. The purpose of this `while true` block is to ensure that the output name is a valid filesystem name, avoiding forbidden characters and not leaving it blank. The loop will continue until a name without invalid characters is provided.

  Following this, the transcription process begins within two conditional blocks. One of these blocks is executed if a `sys.argv` had been used when running the program. This argument serves as a model for the keyword argument in the subsequent function that either way would be executed:

  - **transcribe(file_name, output_name, model="base")**:

    This function receives two positional arguments and one keyword argument. The _file_name_ argument is expected to be an audio file that the [whisper](https://github.com/openai/whisper) library will use for transcription. The transcribe method from whisper returns a _result_ dictionary, which includes _segments_, a key containing all the phrases transcribed from the media.

    From here, a context manager is created to `open` a new .txt file using the output_name argument passed earlier, with “w” mode and utf-8 encoding. Inside this file, a line is written for each phrase contained in each of the segments previously extracted, using the .write() method. If everything proceeds without issues, the function will return True.

  Next, the user is asked another question: whether they want to count the occurrence of a particular word. If the answer is no, the program continues. However, if the answer is yes, a specific function is executed:

  - **count(text_name)**:

    This function prompts the user for a word to count and receives the name of the output file as an argument. It uses this name to `open` the associated .txt file and reads each line of this file. Using a _regular expression_ with the `.findall()` method, it counts how many times the given word appears in the .txt file. The return value is a string indicating how many times the given word appeared.

  If the user don't want a word to be count then the program continues and calls the next function:

  - **words_frequency()**:

    This function also receives the output name as an argument. It creates an empty dictionary called _words_freq_, then opens the .txt file and uses a regular expression to separate all the words. A list of all the cleaned words (without blank spaces, commas, symbols, etc.) is created. This list is traversed with two conditional statements: if the word is not present in the dictionary, it is added with a value of 1; if the word is present in the dictionary, its value is incremented by 1.

    The dictionary is then sorted in descending order according to the frequency of each word. An insertion is made at the first position in the dictionary, adding the titles: word and frequency.

    Finally, a context manager is used to open and create a .csv file using the output name, writing a row in the csv file for each word in the sorted list. The function then returns the sorted word dictionary with the titles added.

    Note:

    There is also another file named long_list that imports ignored_words, a list of words to be ignored by this function. It contains prepositions, articles, conjunctions, pronouns, demonstrative determiners, and some conjugations in English and Spanish.

  In the main function, just to finish, the return value of _words_frequency_ is used to display the top ten words in a more readable way in the console using the _tabulate_ package.

- **test_project.py**:

  This file contains the unit tests for each of the functions used in the project.py file, to ensure that most (if not all) bugs are catch. To test each function there is some special files: .txt .csv and .mp3. These are stored in the root directory under the folder named test. The library used for testing is _pytest_.

  - **test_media_to_mp3()**:

    This test ensures that the media is downloaded correctly by verifying that the video name is successfully returned. It also tests that when passing an invalid URL with no media or not supported, an error should be raised.

  - **test_transcribe()**:

    This test checks that if everything is alright, `True` is returned. It also tests for raising errors when an invalid format is used for transcription (not containing any audio stream) or when a file is not found.

  - **test_count()**:

    My first time using the mock object to create context because the function has an input() function inside that needs to be mocked in order to test this function. It tests using a valid `.txt` file that certain words appears the correct number of times, using a text made and recorded by me. It also tests that when a file is not found or does not exist, the error `FileNotFoundError` is raised.

  - **test_words_frequency()**:

    Given a list of words based on another `.csv` file created by me, it tests that the return value from the function _words_frequency_ is the same as the list passed. It also tests that given an invalid or nonexistent file, it raises `FileNotFoundError`.

- **long_list**:

  This is just a file containg a really long list of words that would be too much hassle to have it in the other files.

## The process:

At first, this program was designed to transcribe local files. I searched for free speech-to-text libraries available in Python. Although there were several options from different companies, I chose Whisper AI because it is open source, doesn’t require authentication, and supports numerous languages. It’s particularly good with English, but as my mother tongue is Spanish, I felt this was the most straightforward choice.

Then, I thought about searching for how many times a specific word was present in any given media. I was really thinking about speeches and podcasts where certain popular figures were present. Let’s say that I just wanted to know, for example, how many times a left-wing representative would use a certain word compared to a right wing one, and things like that. Or even analyze the news coverage by the number of times a specific word was used according to the situation.

I did it, but felt like I was leaving space for making something else. For example, a list with all the words used. I was already creating a .txt file with all the words. I could go further and count every word, not just one in specific. So, I decided to make words_frequency, and to have a more direct output, the top 10 most used words. That, as a personal game, would indeed translate to what the media was about or even be understood by the opposite due to the lack of context of just words spilled out in a top 10.

I thought of making the program work purely with command-line arguments. However, I felt that even though that may be better for programmers, if I want to show the program to someone else not too tech-savvy, it would be confusing. So, I decided to use regular user inputs to make the program work.

As personal experiments I’ve used this program to transcribe silent audios or those without human sound. It’s an interesting experiment, especially if you’re into art or tech media. It’s like painting with words from silence. Give it a try and see what you discover!

## Set up:

First we have to remember to install all packages with:

    pip install -r requirements.txt

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

We can however check this and verify it in the whisper documentation: https://github.com/openai/whisper.

In my case I used windows and installed it using _scoop_.

#### Related:

Would like to learn about text embeddings to include something related to keywords by my own, in the meantime is worth checking [`KeyBERT`](https://github.com/MaartenGr/KeyBERT), and read it's documentation linking to other repos and even a paper on the subject.

Also it made me search and investigate about Natural Language Processing and I landed on the [`NLTK`](https://www.nltk.org/) page where a book can be found related to the subject. This too is really close to what I iagined would be a speech analyser.

To reference **youtube-dl** I read the implementation of the class _YoutubeDL_ [`here`](https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py)

- TODO
  Trying to make work with gpu following this [example](https://stackoverflow.com/questions/75908422/whisper-ai-error-fp16-is-not-supported-on-cpu-using-fp32-instead) in stackOverflow.
