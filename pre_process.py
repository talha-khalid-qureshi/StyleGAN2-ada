import imageio
import glob
from tqdm import tqdm
from PIL import Image
import os
#import logging
#import logging.config


def crop_square(image):        
    width, height = image.size
    
    # Crop the image, centered
    new_width = min(width,height)
    new_height = new_width
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    return image.crop((left, top, right, bottom))
        
def scale(img, scale_width, scale_height):
    # Scale the image
    img = img.resize((
        scale_width, 
        scale_height), 
        Image.ANTIALIAS)
            
    return img

def standardize(image):
    rgbimg = Image.new("RGB", image.size)
    rgbimg.paste(image)
    return rgbimg

def fail_below(image, check_width, check_height):
    width, height = image.size
    assert width == check_width
    assert height == check_height    

def process_images(SOURCE, TARGET):
#    SOURCE = "images/"
#    TARGET = "fianl-images/"
    os.makedirs(TARGET, exist_ok = True)

    files = glob.glob(os.path.join(SOURCE,"*.jpg"))
    files.append(glob.glob(os.path.join(os.getcwd(),"*.jpeg")))
    files.append(glob.glob(os.path.join(os.getcwd(),"*.png")))

    for file in tqdm(files):
      if file.endswith(('.png','.jpg','.jpeg')):
        try:
            target = ""
            name = os.path.basename(file)
            filename, _ = os.path.splitext(name)
            img = Image.open(file)
            w,h = img.size
            if w<1024 or h<1024:
                continue
            
            img = standardize(img)
            img = crop_square(img)
            img = scale(img, 1024, 1024)
            #fail_below(img, 1024, 1024)

            target = os.path.join(TARGET,filename+".jpg")
            img.save(target)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break
        except AssertionError:
            print("Assertion")
            break
#        except:
#            logging.warning(f"Unexpected exception while processing image source: {file}, target: {target}" , exc_info=True)
        except Exception as e:
            print('Exception : ', e)
            pass
    print('****************** Selected Images: ',len(os.listdir(TARGET)),'************************')

#if __name__ == '__main__':
# SOURCE = 'source_folder_path'
# DESTINATION = 'destination_folder_path'
#    process_images(SOURCE,DESTINATION)
