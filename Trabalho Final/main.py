import cv2
import numpy as np
from Type2Function import Type2Function


img=cv2.imread('test.png',0)
membership=Type2Function(127,0,255,1,1,1.25)
noise=np.random.normal(0,0.1**0.5,img.shape)
noise=noise/2

noisy=img/255+noise
noisy[noisy<0]=0.0
noisy[noisy>1]=1
noisy=noisy*255
noisy=noisy.astype(np.uint8)
cv2.imshow('noisy',noisy)

hist = cv2.calcHist([noisy],[0],None,[256],[0,256])

best_threshold=0
best_ultrafuzziness=0
for g in range(256):
    membership.centro=g
    ultrafuzziness=0
    for l,h in enumerate(hist):
        ultrafuzziness+= h * (membership.get_pert2(l,True) - membership.get_pert2(l,False))
    ultrafuzziness/=img.shape[0]*img.shape[1]
    if(ultrafuzziness > best_ultrafuzziness):
        best_threshold=g
        best_ultrafuzziness=ultrafuzziness

ret, threshold_img = cv2.threshold(noisy, best_threshold,255,cv2.THRESH_BINARY)
cv2.imshow('noisy',noisy)
cv2.imshow('threshold',threshold_img)
    

