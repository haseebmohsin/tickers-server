import os
import cv2
import streamlink
import time
from multiprocessing import Process
from pymongo import MongoClient
from datetime import datetime
from ocr import perform_ocr  # Import the perform_ocr function from ocr.py
import json
import base64

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def capture_stream(stream_url, stream_name, crop_coords, mongo_uri, last_ocr_results):
    try:
        streams = streamlink.streams(stream_url)
        stream = streams["best"]

        client = MongoClient(mongo_uri)
        db = client["tickers"]

        collection_name = f"{stream_name}tickers"
        collection = db[collection_name]

        create_directory(f"tickers/{stream_name}")

        print(f"Processing Stream: {stream_name}")
        
        frame_number = 0
        while True:
            try:
                cap = cv2.VideoCapture(stream.url)
                ret, frame = cap.read()

                if ret:
                    crop_top, crop_bottom, crop_left, crop_right = crop_coords
                    cropped_frame = frame[crop_top:-crop_bottom, crop_left:-crop_right]

                    if cropped_frame.size == 0:
                        print("Empty frame captured")
                    else:
                        ocr_results = perform_ocr(cropped_frame)  # Perform OCR on the cropped frame

                        if ocr_results:
                            english_char_count = sum(1 for char in ocr_results if char.isalpha() and char.isascii())
                            
                            if english_char_count > 10:
                                print("Skipping frame because OCR is not Urdu text:", ocr_results)
                                continue  # Skip this frame and move to the next iteration

                            # Check if new OCR result matches with the last 2 stored results
                            matched = any(result[:len(result) * 2 // 5] in ocr_results for result in last_ocr_results[stream_name])
                            if not matched:
                                current_datetime = datetime.now()
                                current_date_str = current_datetime.strftime("%Y-%m-%d")
                                current_time_str = current_datetime.strftime("%H-%M-%S")
                                
                                frame_filename = f"tickers/{stream_name}/{stream_name}_frame_{current_date_str}_{current_time_str}.jpg"
                                cv2.imwrite(frame_filename, cropped_frame)

                                with open(frame_filename, "rb") as image_file:
                                    image_data = image_file.read()

                                    metadata_doc = {
                                        "streamName": stream_name,
                                        "tickerImagePath": frame_filename,
                                        "tickerImage": image_data,
                                        "uploadDate": current_date_str,
                                        "uploadTime": current_time_str,
                                        "ocrText": ocr_results
                                    }

                                    collection.insert_one(metadata_doc)     # save data in database
                            else:
                                print("OCR Matched")

                            # Update last OCR results list
                            last_ocr_results[stream_name].append(ocr_results)
                            if len(last_ocr_results[stream_name]) > 2:
                                last_ocr_results[stream_name].pop(0)
                else:
                    print("Error capturing frame")

                cap.release()

            except Exception as e:
                print(f"An error occurred: {str(e)}")

            time.sleep(1)

        client.close()

    except Exception as e:
        print(f"An error occurred while setting up the stream: {str(e)}")

if __name__ == "__main__":
    stream_data = [
        {"url": "https://www.youtube.com/watch?v=O3DPVlynUM0", "name": "geo", "crop": (408, 21, 30, 158)},
        {"url": "https://www.youtube.com/watch?v=-k9xQwkwC9g", "name": "dunya", "crop": (900, 75, 270, 280)},
        {"url": "https://www.youtube.com/watch?v=yHi3yIkPcLE", "name": "samaa", "crop": (610, 32, 10, 254)},
        {"url": "https://www.youtube.com/watch?v=yBTnEiKy63o", "name": "hum", "crop": (940, 40, 100, 300)},
        {"url": "https://www.youtube.com/watch?v=sUKwTVAc0Vo", "name": "ary", "crop": (920, 40, 70, 330)},
        {"url": "https://www.youtube.com/watch?v=muBr6a3Xi2c", "name": "express", "crop": (930, 40, 60, 380)},
    ]
    
    mongo_uri = "mongodb://localhost:27017/"

    # Initialize a dictionary to store last 5 OCR results for each stream
    last_ocr_results = {stream_info['name']: [] for stream_info in stream_data}

    processes = []
    
    for stream_info in stream_data:
        process = Process(target=capture_stream, args=(stream_info["url"], stream_info['name'], stream_info['crop'], mongo_uri, last_ocr_results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
