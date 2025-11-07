import cv2
import numpy as np

img = cv2.imread("/home/phroog/Documents/columbia/dl/project/annotation_tool/data/illusion_fourth_set_0000_view_0.png")
clone = img.copy()
mask = np.zeros(img.shape[:2], dtype=np.uint8)
points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

cv2.namedWindow("Annotator")
cv2.setMouseCallback("Annotator", click_event)

while True:
    cv2.imshow("Annotator", img)
    key = cv2.waitKey(1) & 0xFF

    if key == 13:  # Enter key → finish polygon
        if len(points) > 2:
            cv2.fillPoly(mask, [np.array(points, np.int32)], 255)
            cv2.polylines(clone, [np.array(points, np.int32)], isClosed=True,
                          color=(0, 255, 0), thickness=2)
        points = []
        img = clone.copy()

    elif key == ord('r'):
        img = clone.copy()
        mask[:] = 0
        points = []

    elif key == ord('s'):
        cv2.imwrite("mask.png", mask)
        print("saved mask.png")
        break

    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
