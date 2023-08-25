'''
This is a tool to simply organize an mp3, and other (supported) digital music formats, 
library into the folder structure of Artist->Alblum->Song.
It should help eliminate duplicates as well.
'''
import os
from pathlib import Path
import click

#import ID3
import eyed3

AUDIO_TYPES = ['.mp3', '.mp4', '.wav', '.flac', '.aac'] # This is a growing list



@click.command()
@click.argument('unorganized_path', type=click.Path(exists=True))
@click.argument('organized_path', type=click.Path())
@click.option("--test", "-t",type=bool, is_flag=True)
def main(test, unorganized_path=None, organized_path=None, ) -> None:
    '''the main function of the music organizer
    '''

    # This should never be hit but just in case
    if unorganized_path is None or organized_path is None:
        raise click.ClickException("No valid paths given")

    if not os.path.exists(organized_path):
        os.mkdir(organized_path)

    for root, dirs, list_of_files in os.walk(unorganized_path):
        for file_name in list_of_files:
            path_to_try = Path(os.path.join(root, file_name))
            if path_to_try.is_file() and path_to_try.suffix in AUDIO_TYPES:
                try:
                    file_id3 = eyed3.load(path_to_try)
                    if file_id3 is not None:
                        new_folder = os.path.join(
                            organized_path,
                            file_id3.tag.artist.replace(' ', '_'),
                            file_id3.tag.album.replace(' ', '_')
                        )
                        new_name = f"{file_id3.tag.title.replace(' ', '_')}{path_to_try.suffix}"
                        new_path = os.path.join(new_folder, new_name)

                        print(new_path)
                        if test or os.path.exists(new_path):
                            continue
                        os.makedirs(new_folder, exist_ok=True)
                        path_to_try.rename(new_path)

                except eyed3.mp3.Mp3Exception:
                    print("??????")
                except eyed3.Error:
                    print(f"Couldn't get id3 for {path_to_try}")
                except AttributeError:
                    pass




if __name__ == "__main__":
    main()
