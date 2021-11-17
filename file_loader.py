from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import cv2
from PIL import Image

class AnnotationException(Exception): pass


def load_File(fpath_image, fpath_annotation):
    img = cv2.imread(fpath_image)[:,:,::-1]   #opencv loads images in bgr. the [:,:,::-1] does bgr -> rgb
    
    height, width, channels = img.shape
    
    with open(fpath_annotation) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    
    if (len(lines) == 0) :
        raise AnnotationException("Annotation is empty !")        
        
    Boxes = []
    for line in lines:
        lstlocs = line.split(' ')
        
        item_class = lstlocs[0]
        scaled_middle_X, scaled_middle_y = float(lstlocs[1]), float(lstlocs[2])
        scaled_half_width, scaled_half_hight = (float(lstlocs[3]) / 2), (float(lstlocs[4]) / 2)
        
        scaled_TL_X = scaled_middle_X - scaled_half_width
        scaled_TL_Y = scaled_middle_y - scaled_half_hight
        scaled_BR_X = scaled_middle_X + scaled_half_width
        scaled_BR_Y = scaled_middle_y + scaled_half_hight
        
        TLX = float(width) * scaled_TL_X
        TLY = float(height) * scaled_TL_Y
        BRX = float(width) * scaled_BR_X
        BRY = float(height) * scaled_BR_Y
        
        bbx = BoundingBox(TLX, TLY, BRX, BRY, label = item_class)
        Boxes.append(bbx) 
        
    bbs = BoundingBoxesOnImage(Boxes, shape = img.shape)
    
    return img, bbs

def Write_File(img, bbs, fpath_image, fpath_annotation):
    im_pil = Image.fromarray(img)
    im_pil.save(fpath_image)
    
    img_height, img_width, channels = img.shape
    
    with open(fpath_annotation, 'w') as file:
        for bbx in bbs.bounding_boxes:
            middle_X = (bbx.x1 + bbx.x2) / 2
            middle_Y = (bbx.y1 + bbx.y2) / 2
            
            width = (bbx.x2 - bbx.x1) / img_width
            hight = (bbx.y2 - bbx.y1) / img_height
            scaled_middle_X = middle_X / img_width
            scaled_middle_Y = middle_Y / img_height
            
            yololabel = "{0} {1} {2} {3} {4}\n".format(bbx.label, scaled_middle_X, scaled_middle_Y, width, hight)
            
            file.write(yololabel)