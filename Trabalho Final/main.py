from __future__ import division
import sys
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
from matplotlib import pyplot as plt

from Type2Function import Type2Function


img=cv2.imread('./img/82.bmp',0)
membership=Type2Function(127,0,255,1,1,1.25)
noise=np.random.normal(0,0.1**0.5,img.shape)
noise=noise/6

print(np.max(noise),np.min(noise),"noise")
print(np.max(img),np.min(img),"img")
print(np.max(img/255),np.min(img/255),"img")

noisy=img.astype(np.float)/255+noise
print(np.max(noisy),np.min(noisy),"noisy")
noisy[noisy<0]=0.0
noisy[noisy>1]=1
print(np.max(noisy),np.min(noisy),"noisy")
noisy=noisy*255
noisy=noisy.astype(np.uint8)
print(np.max(noisy),np.min(noisy),"noisy")

hist = cv2.calcHist([noisy],[0],None,[256],[0,256])

best_threshold=0
best_ultrafuzziness=0
for g in range(256):
    membership.adjust_center(g)
    ultrafuzziness=0.0
    for l,h in enumerate(hist):
        ultrafuzziness+= h * (membership.get_pert2(l,True) - membership.get_pert2(l,False))
#        print(l, membership.get_pert2(l,True), membership.get_pert2(l,False))
    ultrafuzziness/=img.shape[0]*img.shape[1]

    if(ultrafuzziness > best_ultrafuzziness):
        best_threshold=g
        best_ultrafuzziness=ultrafuzziness

#plt.plot(hist)
#plt.show()
membership.adjust_center(best_threshold)
pert_x=np.max(img,0)
pert_y=np.max(img,1)

pert_x=[membership.get_pert(v) for i,v in enumerate(pert_x)]
pert_y=[membership.get_pert(v) for i,v in enumerate(pert_y)]

plt.plot(pert_x)
plt.show()
plt.plot(pert_y)
plt.show()

#img2=np.empty_like(img)
#for y,py in enumerate(pert_y):
#    for x,px in enumerate(pert_x):
#        if(py > 

ret, threshold_img = cv2.threshold(noisy, best_threshold,255,cv2.THRESH_BINARY)
ret2, otsu = cv2.threshold(noisy, 0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print("Threshold:",ret)
print("Otsu", ret2)
cv2.imshow('img',img)
cv2.imshow('noisy',noisy)
cv2.imshow('otsu',otsu)
cv2.imshow('threshold',threshold_img)

cv2.waitKey(0)
