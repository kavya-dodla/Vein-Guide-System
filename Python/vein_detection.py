import cv2
import numpy as np
from skimage.filters import frangi

img = cv2.imread("hand1.png")
if img is None:
    print("Image not found")
    exit()

img = cv2.resize(img, (640,480))
original = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# -----------------------------
# STRONG CONTRAST STRETCH
# -----------------------------
gray = cv2.equalizeHist(gray)

# Apply CLAHE
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
gray = clahe.apply(gray)

# Normalize
gray = gray.astype(np.float32) / 255.0

# -----------------------------
# STRONG VESSEL FILTER
# -----------------------------
vessels = frangi(gray, scale_range=(1,5), scale_step=1)

vessels = (vessels * 255).astype(np.uint8)

# Lower threshold
_, vessel_mask = cv2.threshold(vessels, 10, 255, cv2.THRESH_BINARY)

# Remove tiny noise
kernel = np.ones((3,3), np.uint8)
vessel_mask = cv2.morphologyEx(vessel_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours
contours, _ = cv2.findContours(vessel_mask,
                               cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)

if contours:
    largest = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest)
    if M["m00"] != 0:
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        cv2.circle(original, (cx,cy), 10, (0,0,255), -1)
        print("Best vein coordinates:", cx, cy)
else:
    print("No veins detected")

cv2.imshow("Enhanced Gray", gray)
cv2.imshow("Vessel Response", vessels)
cv2.imshow("Vein Mask", vessel_mask)
cv2.imshow("Final Output", original)

cv2.waitKey(0)
cv2.destroyAllWindows()
