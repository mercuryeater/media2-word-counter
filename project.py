import csv
import re
import sys
from tabulate import tabulate
import whisper
import yt_dlp
from long_list import ignored_words


def main():
    if len(sys.argv) > 2:
        sys.exit("Too many arguments")

    media = (
        input(
            "If you want to download and analyze online media: Type 'y'."
            + "\nIf you are going to pass a local file type anything: "
        )
        .strip()
        .lower()
    )
    if media == "y" or media == "yes":
        try:
            audio = media_to_mp3()
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
    else:
        audio = input("Audio file: ")

    while True:
        output = input("Output .txt and .csv name: ")
        if re.search(r"^[^<>:\"\'\\|?*\/]+$", output):
            break

    # Tiny and base are the best performers in time terms
    models = ["tiny", "base", "small", "medium", "large"]
    try:
        if sys.argv[1] in models:
            try:
                transcribe(audio, output, model=sys.argv[1])
            except RuntimeError:
                sys.exit(
                    "Check spelling, location and extension of your file and try again - sys.argv"
                )
            except FileNotFoundError:
                sys.exit(1)
                raise
            except Exception as e:
                sys.exit(1)
        else:
            raise ValueError("Invalid argument for model: " + sys.argv[1])
    except ValueError:
        sys.exit(
            "Try 'tiny', 'base', 'small', 'medium', 'large' or leave blank for 'base'"
        )
    except IndexError:
        try:
            transcribe(audio, output)
        except RuntimeError:
            sys.exit(
                "Check spelling, location and extension of your file and try again - no model input"
            )
        except FileNotFoundError:
            sys.exit("File not found")
        except Exception as e:
            sys.exit(f"An unexpected error ocurred transcribing: {e}")
        pass

    count_confirmation = (
        input("Would you like to count the appeareance of any particular word? y/n ")
        .strip()
        .lower()
    )

    if count_confirmation == "y" or count_confirmation == "yes":
        try:
            counter = count(output)
        except FileNotFoundError:
            sys.exit("No .txt file to read from")

        print(counter)

    try:
        words_freq = words_frequency(output)
    except FileNotFoundError:
        sys.exit("No .txt file to read from")

    print(
        "The top 10 most used words are:\n",
        tabulate(words_freq[:11], tablefmt="grid", headers="firstrow"),
        "\nTo see a list with all the words check the .csv file created.",
    )


def media_to_mp3():
    urls = []
    video_url = input("Enter URL of the media:")
    urls.append(video_url)
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        ydl.params["outtmpl"] = {"default": info["fulltitle"]}
        try:
            error_code = ydl.download(urls)
        except yt_dlp.utils.DownloadError:
            print(f"Unsupported URL: {video_url}", file=sys.stderr)
            sys.exit(1)

    # Replaces characters in string for '#' as Postprocessor class does it in yt-dlp
    title = re.sub(r"[<>:\"\\|?*\/]+", "#", info["fulltitle"])

    return f"{title}.m4a"


def transcribe(file_name, output_name, model="base"):
    # Loads model / creates model object
    print(f"Using model {model}")
    model = whisper.load_model(model)
    try:
        result = model.transcribe(file_name)
    except RuntimeError:
        print("Invalid media format - Failed to load audio", file=sys.stderr)
        raise
    except FileNotFoundError:
        print(f"File: '{file_name}' not found", file=sys.stderr)
        raise
    except Exception as e:
        print(e, file=sys.stderr)
        raise

    segments = result["segments"]

    with open(f"{output_name}.txt", "w", encoding="utf-8") as file:
        for s in segments:
            file.write(s["text"] + "\n")

    return True


def count(text_name):
    word = input("Word to count: ")
    text_file = f"{text_name}.txt"
    counter = 0

    try:
        with open(text_file) as file:
            for line in file:
                coincidence = re.findall(
                    r"\b{}(?:\b|$)".format(word), line, re.IGNORECASE
                )
                counter += len(coincidence)
    except FileNotFoundError:
        print(f"File: '{text_file}' not found", file=sys.stderr)
        raise

    return f"The word '{word}' appears {counter} times."


def words_frequency(output_name):
    text_file = f"{output_name}.txt"
    words_freq = {}
    try:
        with open(text_file, encoding="utf-8") as file:
            for line in file:
                split_words = re.split(r"(?:[^\w']| )+", line)
                clean_words = [
                    word.strip().lower() for word in split_words if word.strip()
                ]

                for w in clean_words:
                    if w in words_freq and w not in ignored_words:
                        words_freq[w] += 1
                    elif w not in words_freq and w not in ignored_words:
                        words_freq[w] = 1
    except FileNotFoundError:
        print(f"File: '{text_file}' not found", file=sys.stderr)
        raise

    sorted_words = sorted(words_freq.items(), key=lambda item: item[1], reverse=True)
    sorted_words.insert(0, ["word", "frequency"])

    with open(f"{output_name}.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for word in sorted_words:
            writer.writerow(word)

    return sorted_words


if __name__ == "__main__":
    main()
