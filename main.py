from pathlib import Path
from PIL import Image
from waveshare_epd import epd5in65f
from random import shuffle
import time


def main():
    SLEEP = 240 # seconds

    image_exts = [".jpg", ".jpeg", ".png"]
    images_dir: Path = Path.home().joinpath("Pictures", "backgrounds")

    images = [ p.resolve() for p in images_dir.rglob("*") if p.suffix in image_exts ]
    print("Will be displaying the following images:")
    for image in images:
        print(f"\t{image.name}")

    print("\nInitializing display, please wait...")
    epd = epd5in65f.EPD()
    epd.init()
    epd.Clear()

    # This function is weird -- it actually returns None, so you can't write e.g. `for i in shuffle(images)`, 
    # because then it'll be trying to iterate over a Nonetype object.
    # Rather, you just have to call the function bare and pass the list to shuffle to it.
    shuffle(images) 
    while True:
        for i in images:
            with Image.open(i) as img:
                print(f"Displaying {i.name}")
                image = img.resize((600, 448))
                epd.display(epd.getbuffer(image))
                time.sleep(SLEEP)
                epd.Clear()
        shuffle(images)
    epd.sleep()


if __name__ == "__main__":
    main()
