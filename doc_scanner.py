import cv2
import numpy as np

capWeb = cv2.VideoCapture(0)

frameWidth = 480
frameHeight = 640
brightness = 150
capWeb.set(3, frameWidth)
capWeb.set(4, frameHeight)
capWeb.set(10, brightness)

# This function stacks a 2D/1D list of images into a single combined image for display. (For visual debugging)
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable: # If imgArray is 2D
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else: # If imgArray is 1D
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

# Image preprocessing pipeline: grayscale → blur → edge detection → dilate → erode.
def preProcessing(frame):
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 150, 150) # tuning
    kernal = np.ones((5, 5), np.uint8)
    imgDil = cv2.dilate(imgCanny, kernal, iterations=2)
    imgThreshold = cv2.erode(imgDil, kernal, iterations=1)

    return imgThreshold

# Finding the biggest quadrilateral contour.
def getContours(img, draw_img):
    biggestContour = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if(area > 5000): # tuning
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            if(area > maxArea and len(approx) == 4):
                maxArea = area
                biggestContour = approx

    cv2.drawContours(draw_img, biggestContour, -1, (0, 255, 0), 15)
    return biggestContour

# To ensure 4-point contour points are in consistent order: top-left, top-right, bottom-left, bottom-right.
def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4,1, 2), np.int32)
    add = myPoints.sum(1)
    # print("Add : " , add)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("myPointsNew : " , myPointsNew)
    return myPointsNew

# Applied perspective transform to get top-down scanned view.
def getWarp(img, biggest):
    # print(biggest.shape)
    biggest = reorder(biggest)
    width, height = frameWidth, frameHeight
    pt1 = np.float32(biggest)  # (x,y) i.e. (width, height)
    pt2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # For givings co-ordinates in pt :
    # 1st-parameter           2nd-parameter
    #
    #
    #
    # 3rd-parameter           4th-parameter

    matrix = cv2.getPerspectiveTransform(pt1, pt2)
    transformedImg = cv2.warpPerspective(img, matrix, (width, height))
    imgCropped = transformedImg[20:transformedImg.shape[0]-20, 20:transformedImg.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (frameWidth, frameHeight))

    return imgCropped

# Read frames, process & show result
while True:
    success, img = capWeb.read() # works in a very clear environment
    if not success :
        print("Image is not captured!")

    # img = cv2.imread("test_image.png")
    img = cv2.resize(img, (frameWidth, frameHeight))
    imgContours = img.copy()
    imgThreshold = preProcessing(img)
    biggest = getContours(imgThreshold, imgContours)
    imgWarp = np.array([])

    if len(biggest) == 4 :
        imgWarp = getWarp(img, biggest)
        imgResult = stackImages(0.6, [[img, imgThreshold],
                                       [imgContours, imgWarp]])
        cv2.imshow("Final Document", imgWarp)
    else:
        imgResult = stackImages(0.6, [[img, imgThreshold],
                                       [img, img]])

    cv2.imshow("Result", imgResult)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the resources
capWeb.release()
cv2.destroyAllWindows()
