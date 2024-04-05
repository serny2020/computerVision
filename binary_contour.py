import cv2
import sys

# Load the image
# Check if the image path is provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide the image path as a command line argument.")
    sys.exit(1)

image_path = sys.argv[1]
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Create a window to display the image
cv2.namedWindow('Binary Image Adaptive')

# Define the initial values for block size and C parameters
initial_block_size = 11
initial_C = 2
initial_min_area = 0
initial_dilate_iterations = 0
initial_erode_iterations = 0
binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, initial_block_size, initial_C)

def process_image(image, block_size, C_param, min_area, dilate_iterations, erode_iterations):
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C_param)
    # invert the binary image
    binary_image = cv2.bitwise_not(binary_image)
    # dilate the binary image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary_image = cv2.dilate(binary_image, kernel, iterations=dilate_iterations)
    # erode the binary image
    binary_image = cv2.erode(binary_image, kernel, iterations=erode_iterations)

    # find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # filter contours based on area
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area]
    # draw contours
    binary_image = cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)

    if cv2.getTrackbarPos('Show boxes and contours', 'Binary Image Adaptive') == 1:
        # draw contours
        cv2.drawContours(binary_image, filtered_contours, -1, (0, 255, 0), 1)
        # draw a bounding box around each contour
        for contour in filtered_contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(binary_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    side_by_side = cv2.hconcat([image, binary_image])
    cv2.imshow('Binary Image Adaptive', side_by_side)


def update_binary_image(*args):
    block_size = cv2.getTrackbarPos('Block Size', 'Binary Image Adaptive')
    block_size = block_size // 2 * 2 + 1  # Round to the nearest odd number
    C_param = cv2.getTrackbarPos('C', 'Binary Image Adaptive')
    min_area = cv2.getTrackbarPos('Min Area', 'Binary Image Adaptive')
    dilate_iterations = cv2.getTrackbarPos('Dilate Iterations', 'Binary Image Adaptive')
    erode_iterations = cv2.getTrackbarPos('Erode Iterations', 'Binary Image Adaptive')
    process_image(image, block_size, C_param, min_area, dilate_iterations, erode_iterations)

# Create trackbars for block size and C parameters
cv2.createTrackbar('Block Size', 'Binary Image Adaptive', initial_block_size, 255, update_binary_image)
cv2.createTrackbar('C', 'Binary Image Adaptive', initial_C, 255, update_binary_image)
# Create a trackbar for min_area parameter
cv2.createTrackbar('Min Area', 'Binary Image Adaptive', initial_min_area, 1000, update_binary_image)
# Create a trackbar for dilate iterations
cv2.createTrackbar('Dilate Iterations', 'Binary Image Adaptive', initial_dilate_iterations, 10, update_binary_image)
# Create a trackbar for erode iterations
cv2.createTrackbar('Erode Iterations', 'Binary Image Adaptive', initial_dilate_iterations, 10, update_binary_image)
cv2.createTrackbar('Show boxes and contours', 'Binary Image Adaptive', 0, 1, update_binary_image)

# Initialize the binary image
process_image(image, initial_block_size, initial_C, initial_min_area, initial_dilate_iterations, initial_erode_iterations)

cv2.waitKey(0)
cv2.destroyAllWindows()

# save the image to disk
cv2.imwrite("binary_contour.jpg", binary_image)