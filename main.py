# ============================================================
#  ██████╗  █████╗ ██████╗ ██╗  ██╗██╗███╗   ██╗ ██████╗     
#  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║████╗  ██║██╔═══██╗    
#  ██████╔╝███████║██████╔╝█████╔╝ ██║██╔██╗ ██║██║     
#  ██╔═══╝ ██╔══██║██╔═██╗ ██╔═██╗ ██║██║╚██╗██║██║   ██║    
#  ██║     ██║  ██║██║  ██╗██║  ██╗██║██║ ╚████║╚██████╔╝    
#  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝     
# ============================================================
# | 🅿️ Automated Parking Space Detection System              |  
# |----------------------------------------------------------|
# | > Input  : Video Feed                                    |
# | > Output : Available Parking Spots 🟢/🔴                 |
# |----------------------------------------------------------|
# |   Analyze, Visualize, Automate! 🚗                       |
# |----------------------------------------------------------|
# |   Analyze, Visualize, Automate! 🚗                       |
# ============================================================
# ************ Elaoud Najd :: 2ING_EL -- TP1 *****************
# ============================================================
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!  PLEASE PRESS ESC TO CLOSE ALL WINDOWS AFTER SIMULATION !!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import cv2
import cvzone
import pickle
import numpy as np

w, h = 107, 46

# video feed
cap = cv2.VideoCapture("video_file_name.mp4")

#? read positions list from image file
with open('parking_space_pos', 'rb') as file:
    pos_list = pickle.load(file)
    
def empty(a):
    pass

cv2.namedWindow("Vals")
cv2.resizeWindow("Vals", 640, 120)
cv2.createTrackbar("Val1", "Vals", 25, 50, empty)
cv2.createTrackbar("Val2", "Vals", 16, 50, empty)
cv2.createTrackbar("Val3", "Vals", 5, 50, empty)

#? Check parking spaces and display the cropped regions.    
def check_parking_space(processed_img):
  space_count = 0
  
  for pos in pos_list:
    x, y = pos
    #? show image of selected parking spaces 
    img_crop = processed_img[y:y+h, x:x+w]
    #? count number of pixels in each cropped image
    count_pcs = cv2.countNonZero(img_crop) 
    # cv2.imshow(str(x*y), img_crop)
    
    if count_pcs < 800:
      color = (0,255,0)
      thickness = 5
      space_count +=1
    else:
      color = (0,0,255)
      thickness = 2
      
    #* draw rectangle in selected position
    cv2.rectangle(img,pos, (pos[0] + w, pos[1] + h), color, thickness)
    cvzone.putTextRect(img, str(count_pcs), (x, y+h), scale=1.2, thickness=2, offset=0, colorR= color)
  
  cv2.putText(img, f'Available parking lots: {space_count}', (750, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,255,128), 2)  
  cv2.putText(img, f'Total parking lots: {len(pos_list)}', (750, 25), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0,255,128), 2)

  
################################################################
#**************************************************************#
################################################################
  
while True:
  #? check if current frame = total frames (to keep the video running)
  if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)     # reset frame count
  
  success, img = cap.read()  
  if not success:
      print("Error: Failed to read the video feed.")
      break
  
  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  #? convert image to grayscale
  
  img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)  #? smooth image
  
  val1 = cv2.getTrackbarPos("Val1", "Vals")
  val2 = cv2.getTrackbarPos("Val2", "Vals")
  val3 = cv2.getTrackbarPos("Val3", "Vals")
  if val1 % 2 == 0: val1 += 1
  if val3 % 2 == 0: val3 += 1
    
  img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, val1, val2) #? image binarization threshold
  
  
  img_median = cv2.medianBlur(img_threshold, val3)     #? median filtre
  kernel = np.ones((3, 3), np.uint8)
  img_dilate = cv2.dilate(img_median, kernel, iterations=1)     #? make lines thicker
  
  #? Check and display parking spaces
  check_parking_space(img_dilate)
    
  cv2.imshow("image", img)
  #cv2.imshow("gray image", img_gray)
  #cv2.imshow("blurred image", img_blur)
  #cv2.imshow("binary image", img_threshold)
  #cv2.imshow("median image", img_median)
  #cv2.imshow("dilate image", img_dilate)
  
  key = cv2.waitKey(10)
  if key == 27:             #? esc button 
    break
  
cap.release()
cv2.destroyAllWindows()