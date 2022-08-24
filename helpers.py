import numpy as np
from skimage.morphology import convex_hull_image, erosion, square
from eth_keys import keys
from eth_utils import decode_hex
import imageio.v2 as imageio
import cv2
import skimage


def getSkelMask(img_name):
    image = imageio.imread(img_name)
    THRESHOLD1 = image.mean()
    img = cv2.imread(img_name,0)
    if img is None:
        raise(ValueError(f"Image didn\'t load. Check that '{img_name}' exists."))
    img = np.array(img > THRESHOLD1).astype(int)
    skel = skimage.morphology.skeletonize(img)
    skel = np.uint8(skel)*255
    mask = img*255
    return skel, mask

def getTerminationBifurcation(img, mask):
    img = img == 255
    (rows, cols) = img.shape
    minutiaeTerm = np.zeros(img.shape)
    minutiaeBif = np.zeros(img.shape)
    
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            if(img[i][j] == 1):
                block = img[i-1:i+2,j-1:j+2]
                block_val = np.sum(block)
                if(block_val == 2):
                    minutiaeTerm[i,j] = 1
                elif(block_val == 4):
                    minutiaeBif[i,j] = 1
    
    mask = convex_hull_image(mask>0)
    mask = erosion(mask, square(5))         
    minutiaeTerm = np.uint8(mask)*minutiaeTerm
    return(minutiaeTerm, minutiaeBif)

def toHexString(array):
    return "0x"+''.join(array)

def getFirstAlphabetArray(array):
    for i in range(len(array)):
        if(array[i].isalpha()):
            try:
                return array[i:i+64]
            except:
                return None

def getFirstNonZeroArray(array):
    for i in range(len(array)):
        if(array[i] != 0):
            try:
                return array[i:i+64]
            except:
                return None

def getPrivateKey(minutiaeTerm, minutiaeBif):
    num_array = [hex(int(sum(r)) % 16)[2:] for r in minutiaeBif+minutiaeTerm]
    alphabetKey = getFirstAlphabetArray(num_array)
    nonZeroKey = getFirstNonZeroArray(num_array)
    if alphabetKey is not None:
        return toHexString(alphabetKey)
    elif nonZeroKey is not None:
        return toHexString(nonZeroKey)
    else:
        raise Exception("Could not generate key from given template")

def getAddress(private_key):
    priv_key_bytes = decode_hex(private_key)
    priv_key = keys.PrivateKey(priv_key_bytes)
    pub_key = priv_key.public_key
    return pub_key.to_checksum_address()