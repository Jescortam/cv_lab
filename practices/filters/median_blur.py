import cv2

image = cv2.imread('../../img/image.png')

median_image = cv2.medianBlur(image, 3)

cv2.imshow('Original', image)
cv2.imshow('Filtrada con Mediana', median_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
