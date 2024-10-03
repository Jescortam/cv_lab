import cv2
from colorama import Fore, Style
from practices.image_structure import image_structure
from practices.basic_operators import basic_operators
from utils import utils


def main():
    image = cv2.imread('img/somewhere_in_time.jpg')
    height, width, channels = image.shape

    print(f'Height {height} , Width {width}')
    image_name = str(input('Save matrix with name : '))

    print(Fore.GREEN + '1 - RGB matrix of image')
    print('2 - Gray matrix of image')
    print('3 - Change intensity of a pixel')
    print('4 - Copy of image')
    print('5 - Negative of an image')
    print('6 - Increment/decrement of brightness')
    print(Fore.RED + '7 - Contrast elongation/reduction')
    print('8 - Shifting H/V/D')
    print(Fore.GREEN + '9 - Quit' + Style.RESET_ALL)
    choice = int(input('Select an option : '))

    if choice == 1:
        image_structure.write_rgb_csv(image=image, filename=f'{image_name}_RGB.csv')
        main()
    elif choice == 2:
        image_structure.write_gray_csv(image=utils.img_to_gray(image), filename=f'{image_name}_GRAY.csv')
        main()
    elif choice == 3:
        basic_operators.write_intensity_csv(image=utils.img_to_gray(image), filename=f'{image_name}_INTENSITY.csv')
        main()
    elif choice == 4:
        basic_operators.write_copy_csv(image=utils.img_to_gray(image), filename=f'{image_name}_COPY.csv')
        main()
    elif choice == 5:
        basic_operators.write_negative_csv(image=utils.img_to_gray(image), filename=f'{image_name}_NEGATIVE.csv')
        main()
    elif choice == 6:
        basic_operators.write_increment_decrement_csv(image=utils.img_to_gray(image),filename=f'{image_name}_INCREMENT_DECREMENT.csv')
        main()


if __name__ == '__main__':
    main()
