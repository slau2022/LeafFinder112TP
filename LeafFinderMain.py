import cv2
import numpy as np

# 
# window_name = "Images"
# 
# # Importantly, images are stored as BGR
# # Use the following function to read images.
# image = cv2.imread("leafdemo.jpg")
# edges = cv2.Canny(image, 100,200)
# # Error checking to make sure that our image actually loaded properly
# # Might fail if we have an invalid file name (or otherwise)
# if image is not None:
#     # Display our loaded image in a window with window_name
#     cv2.imshow(window_name, edges)
#     # Wait for any key to be pressed
#     cv2.waitKey(0)
# 
# # Load another image, this time in grayscale directly
# image = cv2.imread("lemodemo.jpg", cv2.IMREAD_GRAYSCALE)
# if image is not None:
#     cv2.imshow(window_name, image)
#     cv2.waitKey(0)
# 
# # Clean up before we exit!
# cv2.destroyAllWindows()

def manual_threshold(image):
    # Define some constants
    BLACK = 0
    THRESH = (0,225, 0)

    # Convert our input image to grayscale so that it's easy to threshold

    # Create a new array of all zeros to store our thresholded image in
    # It will be the same size as our grey image
    thresholded = np.zeros(image.shape, np.uint8)
    
    # Iterate over the grey image, and store results in thresholded
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # If we're over a certain target value, then saturate to white
            # otherwise, we're under the bar, dilute to black
            if thresholded[i][j] < THRESH: BLACK

    # Return our handiwork
    return thresholded

# We've finally put our code in a function instead!
def main():

    window_name = "Webcam!"

    cam_index = 0
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    cap = cv2.VideoCapture(cam_index)
    cap.open(cam_index)

    while True:

        ret, frame = cap.read()

        if frame is not None:
            # Instead of showing the original image, show the thresholded one
            cv2.imshow(window_name, manual_threshold(frame))
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27: # Escape key
            cv2.destroyAllWindows()
            cap.release()
            break

if __name__ == "__main__":
    main()