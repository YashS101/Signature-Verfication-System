import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pyttsx3
import threading

def compare_signatures(image1_path, image2_path):
    # Read the input images
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Resize the images to a fixed size for consistency
    image1 = cv2.resize(image1, (400, 200))
    image2 = cv2.resize(image2, (400, 200))

    # Concatenate the images side by side
    comparison = np.concatenate((image1, image2), axis=1)

    # Calculate the Structural Similarity Index (SSIM)
    score = cv2.matchTemplate(image1, image2, cv2.TM_CCOEFF_NORMED)
    similarity = score[0][0]

    # Set a threshold to determine if the signatures match or not
    threshold = 0.8

    # Convert the similarity score to a percentage
    similarity_percentage = round(similarity * 100, 2)

    # Determine the matching result
    if similarity >= threshold:
        match_status = "Signatures match!"
        voice_text = "the two signatures are Matched!"
    else:
        match_status = "Signatures do not match."
        voice_text = "the two signatures don't Match!"

    # Create a thread for speaking the matching result
    voice_thread = threading.Thread(target=speak_text, args=(voice_text,))
    voice_thread.start()

    
    # Print the matching percentage and matching result
    print(f"Matching Percentage: {similarity_percentage}%")
    print(match_status)

    # Display the images in a pop-up window
    cv2.imshow("Signature Comparison", comparison)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Wait for the voice thread to complete
    voice_thread.join()

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # Set speech rate
    engine.setProperty("volume", 1.0)  # Set speech volume
    engine.say(text)
    engine.runAndWait()

# Create a Tkinter root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Prompt the user to select the first signature image
image1_path = filedialog.askopenfilename(title="Select the first signature image")

# Prompt the user to select the second signature image
image2_path = filedialog.askopenfilename(title="Select the second signature image")

# Call the function to compare the signatures
compare_signatures(image1_path, image2_path)
