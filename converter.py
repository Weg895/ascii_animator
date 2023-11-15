from PIL import Image, ImageEnhance

IMAGE_RATIO = 2

def resize_image(image, new_width=100):
    width, height = image.size
    IMAGE_RATIO = height / width
    new_height = int(new_width * IMAGE_RATIO)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def pixels_to_ascii(image, ascii_char):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        index = pixel * (len(ascii_char) - 1) // 255
        ascii_str += char_to_ratio(f'{ascii_char[index]}')
    return ascii_str

def char_to_ratio(char_to_append):
    result_string = ""
    for _ in range(IMAGE_RATIO): 
        result_string += char_to_append
    return result_string

def enhance_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def enhance_saturation(image, factor=1.5):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def enhance_sharpness(image, factor=1.5):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)

def enhance_brightness(image, factor=1.5):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def convert(path, filename, resfolder, new_width, ascii_char, brightness = 1, sharpness = 1, contrast = 1,
            staturation = 1):
    try:
        image = Image.open(path)
    except Exception as e:
        print("Error:", e)
        return
    
    img_brighter = enhance_brightness(image.convert("RGB"), brightness)
    img_sharpened = enhance_sharpness(img_brighter,sharpness)
    img_contrast = enhance_contrast(img_sharpened,contrast)
    img_saturate = enhance_saturation(img_contrast, staturation)
    
    mig_resized = resize_image(img_saturate, new_width)
    img_grayscale = grayify(mig_resized)
    image_data = pixels_to_ascii(img_grayscale, ascii_char)

    pixel_count = len(image_data)
    ascii_image = "\n".join(image_data[i:(i + new_width * IMAGE_RATIO)] for i in range(0, pixel_count, new_width * IMAGE_RATIO))
    
    with open(f"{resfolder}/{filename}", "w") as f:
        f.write(ascii_image)
