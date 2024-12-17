import cv2
import pickle

w, h = 107, 46

#? load positions list from file otherwise create empty list
try:
  with open('parking_space_pos', 'rb') as file:
      pos_list = pickle.load(file)
except:
      pos_list = []

def mouse_click_callback(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:            # add rectangle
        pos_list.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:            # remove rectangle
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1 + w and y1 < y < y1 + h:
                pos_list.pop(i)                   # delete rectangle in index
                
    #? save position list data in file with write access (wb)            
    with open('parking_space_pos', "wb") as file:
        pickle.dump(pos_list, file)

while True:
  img = cv2.imread('parking_lot_img.png')
  
  #* draw rectangle in selected position
  for pos in pos_list:
    cv2.rectangle(img,pos, (pos[0] + w, pos[1] + h), (255, 0, 255), 3)
  
  cv2.imshow("image", img)
  cv2.setMouseCallback("image", mouse_click_callback)
  
  key = cv2.waitKey(1)
  if key == 27:             #? esc button 
    break