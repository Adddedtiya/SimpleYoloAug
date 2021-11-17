from file_loader import AnnotationException, load_File, Write_File
from aug_seq import AugmentationSequence, AugmentationSequence2
import argparse
import os

parser = argparse.ArgumentParser(description='Throw Eggs on the wall image augmentation')
parser.add_argument('--indir', type=str, required=True)
parser.add_argument('--outdir', type=str, required=True)
parser.add_argument('--gen', type=int, required=True)
args = parser.parse_args()

list_of_image_files = []
list_of_annotation_files = []

for file in os.listdir(args.indir):
    if file.endswith(".jpg"):
        list_of_image_files.append(os.path.join(args.indir, file))
    elif file.endswith(".jpeg"):
        list_of_image_files.append(os.path.join(args.indir, file))
        
    elif file.endswith(".txt"):
        list_of_annotation_files.append(os.path.join(args.indir, file))

DatasetTuple = []

for i in range(len(list_of_image_files)):
    fname_image = os.path.basename(list_of_image_files[i]).split('.')[0]
    
    for j in range(len(list_of_annotation_files)):
        fname_annotation = os.path.basename(list_of_annotation_files[j]).split('.')[0]
        if fname_image == fname_annotation:
            DatasetTuple.append((list_of_image_files[i], list_of_annotation_files[j]))
            del list_of_annotation_files[j]
            break
    #innterloop

print("Total Image Anotation Pair :", len(DatasetTuple))
if input("Y/N : ").lower() != "y":
    exit()

for img, ann in (DatasetTuple):
    try:
        img_raw, ann_raw = load_File(img, ann)
    except AnnotationException as e:
        print(e)
        continue
    else:
        
        rootfname = os.path.basename(img).split('.')[0]
        
        combined_image_path = os.path.join(args.outdir, rootfname)
        combined_annotation_path = os.path.join(args.outdir, rootfname)
        
        Write_File(img_raw, ann_raw, combined_image_path + ".jpg", combined_annotation_path + ".txt")
        
        for i in range(args.gen):
            print("Generating :", str(i).zfill(3), rootfname) if i % 10 == 1 else 0
            
            aug_img, aug_annot = AugmentationSequence2(image = img_raw, bounding_boxes = ann_raw)
            
            img_out_path = combined_image_path + "_" + str(i).zfill(3) + ".jpg"
            aug_out_path = combined_annotation_path + "_" + str(i).zfill(3) + ".txt"
            
            Write_File(aug_img, aug_annot, img_out_path, aug_out_path)













