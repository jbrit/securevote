import glob
import random

from helpers import getAddress, getPrivateKey, getSkelMask, getTerminationBifurcation

# Testing with images
DATA_DIR = "./SOCOFing/Real/"
list_dirs = list(glob.glob(DATA_DIR+"*.BMP"))
num_images = len(list_dirs)
random.seed(42)

r = random.randint(0,num_images)
display_list = list_dirs[r:r+3]

def getWallet(img_name):
    skel, mask = getSkelMask(img_name)
    (minutiaeTerm, minutiaeBif) = getTerminationBifurcation(skel, mask)
    private_key  = getPrivateKey(minutiaeTerm, minutiaeBif)
    return private_key, getAddress(private_key)

for display in display_list:
    print(display)
    pkey, addr = getWallet(display)
    print("Private Key:",pkey)
    print("Public Address:",addr,"\n")
