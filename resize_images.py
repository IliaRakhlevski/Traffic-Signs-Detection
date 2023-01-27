# Resize images located in the specific path

import cv2
import os
import ntpath


BLACK = [0,0,0]
PAD_COLOR = BLACK   # color of the added pads

# size of processed images (frames) extracted from the video
IMG_HEIGHT = int(384) 
IMG_WIDTH  = int(640)



def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail, ntpath.basename(head)


# Add pads to image in order it to have the given size (img_width, img_height)
# image - image (frame) object
# img_width - final image width
# img_height - final image height
def image_padding(image, img_width, img_height):
    im_cur_height = image.shape[0]
    im_cur_width = image.shape[1]
    
    top = 0
    bottom = 0
    left = 0
    right = 0
    
    if im_cur_height < img_height:
        deltha = (int)((img_height - im_cur_height) // 2)
        top = deltha
        bottom = deltha
        
    if im_cur_width < img_width:
        deltha = (int)((img_width - im_cur_width) // 2)
        left = deltha
        right = deltha
    
    pad_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=PAD_COLOR)
    
    return pad_image


# Change the image in order it to have the given size (img_width, img_height)
# image - image (frame) object
# img_width - final image width
# img_height - final image height
def image_resizing(image, img_width, img_height):
    im_cur_height = image.shape[0]
    im_cur_width = image.shape[1]
    
    height_factor = im_cur_height / img_height
    width_factor  = im_cur_width  / img_width
    
    factor = width_factor
    if height_factor > width_factor:
        factor = height_factor
        
    im_cur_height = int(im_cur_height / factor)
    im_cur_width  = int(im_cur_width  / factor)
    
    image = cv2.resize(image, (im_cur_width, im_cur_height))
    
    image = image_padding(image, img_width, img_height)
    
    return image


# Resize all the images from files list 'images'
# images - list of files containing images
def resize_images(images):

    for i, image_file in enumerate(images):
        img = cv2.imread(image_file, cv2.IMREAD_COLOR)
        res_img = image_resizing(img, IMG_WIDTH, IMG_HEIGHT)
        
        head, tail = path_leaf(image_file)
        
        res_image_file = tail + "/resized/"
        
        if not os.path.exists(res_image_file):
            os.makedirs(res_image_file)
    
        res_image_file += head
        cv2.imwrite(res_image_file, res_img)
        


IMAGES_DIR = './images/'

images = [IMAGES_DIR+i for i in os.listdir(IMAGES_DIR)]

resize_images(images)

