import cv2

img1 = cv2.imread('1.jpg', 1)
grayimg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

img2 = cv2.imread('2.jpg', 1)
grayimg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

bgobj = cv2.bgsegm.createBackgroundSubtractorLSBP()

fgmask = bgobj.apply(grayimg1)
fgmask = bgobj.apply(grayimg2)

cv2.imshow('difference_img', fgmask)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("difference.jpg", fgmask)