# We gots face recognition technologey 	ψ( ` ∇ ´ )ψ
# Will go through the results of scaning pcap for images and identify those his human faces on them
# After, it will generate a new image, with a box sorrounding all faces identified in the img

import cv2 # OpenCV to detect faces; it can also detect a bunch other things is u go through the lib 
import os

ROOT = '/root/Desktop/pictures' # Src dir
FACES = '/root/Desktop/faces' # Target dir
TRAIN = '/root/Desktop/training' 

def detect(srcdir=ROOT, tgtdir=FACES, train_dir=TRAIN):
    for fname in os.listdir(srcdir):
        if not fname.upper().endswith('.JPG'):
            continue
        fullname =  os.path.join(srcdir, fname)
        newname = os.path.join(tgtdir, fname) # Read imgs from source dir with OpenCV computer vision lib
        img = cv2.imread(fullname)
        if img is None:
            continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        training = os.path(train_dir, 'haarcascade_frontalface_alt.xml') # Load detector xml
        cascade = cv2.CascadeClassifier(training) # Create detector obj
        rects = cascade.detectMultiScale(gray, 1.3, 5) # returns coordonates of a rectangle where the face at
        try:
            if rects.any():
                print('Got a face! Ɛ( · — ·)3')
                rects[:, 2:] += rects[:, :2] # Convert rect data to actual coordinates x1, y1, x2, y2
                # Which is the expected input of cv2.rectangle
        except AttributeError:
            print(f'No faces found in {fname}.')
            continue
        
        # Highlight the faces in the image
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2) # draw green box arround face
        cv2.imwrite(newname, img) # write img to output dir

if __name__=='__main__':
    detect()