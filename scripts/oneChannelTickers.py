import cv2
import streamlink
import time

# Replace this with the URL of the YouTube live stream
stream_url = "https://www.youtube.com/watch?v=sUKwTVAc0Vo"

# Replace this with the desired location to save tickers
save_directory = "assets/tickers/tem/"

# Open the stream using streamlink
streams = streamlink.streams(stream_url)
stream = streams["best"]

frame_number = 0
while True:
    try:
        # OpenCV video capture from streamlink
        cap = cv2.VideoCapture(stream.url)

        ret, frame = cap.read()
        if ret:
            # Get the dimensions of the frame
            height, width, _ = frame.shape

            # Define cropping coordinates (top, bottom, left, right)
            crop_top = int(0.84 * height)     # Cut from the top
            crop_bottom = int(0.03 * height)  # Cut from the bottom
            crop_left = int(0.05 * width)     # Cut from the left
            crop_right = int(0.17 * width)    # Cut from the right

            # Crop the frame based on the defined coordinates
            cropped_frame = frame[crop_top:-crop_bottom, crop_left:-crop_right]

            # Check if the cropped frame is empty
            if cropped_frame.size == 0:
                print("Empty frame captured")

            else:
                # Save the cropped frame
                frame_filename = f"{save_directory}frame_{frame_number:04d}.jpg"
                cv2.imwrite(frame_filename, cropped_frame)

                frame_number += 1

        else:
            print("Error capturing frame")

        cap.release()

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    # Wait for 2 seconds before capturing the next frame
    time.sleep(2)
