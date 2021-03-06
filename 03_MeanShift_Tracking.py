#!/usr/bin/env python
# coding: utf-8

# ### Import Libraries

# In[2]:


import numpy as np
import cv2


# ### Capture Video Stream

# In[3]:


cap = cv2.VideoCapture('./Video/face_track.mp4')


# ### Take first frame of the video

# In[4]:


ret,frame = cap.read()


# ### Set up the initial tracking window

# In[5]:


face_casc = cv2.CascadeClassifier("Haarcascades/haarcascade_frontalface_default.xml")
face_rects = face_casc.detectMultiScale(frame)


# ### Convert the list to a tuple

# In[6]:


face_x,face_y ,w , h = tuple(face_rects[0])
track_window = (face_x,face_y,w,h)


# ### set up the ROI for tracking

# In[7]:


roi = frame[face_y:face_y+h,face_x:face_x+w]


# ### HSV color maping

# In[8]:


hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)


# ### Histogram to target on each frame for the meanshift calculation

# In[9]:


roi_hist = cv2.calcHist([hsv_roi],[0],None,[180],[0,180])


# ### Normalize the histogram

# In[10]:


cv2.normalize(roi_hist, roi_hist,0,255,cv2.NORM_MINMAX);


# ### Set the termination criteria
# 10 iterations or move 1 pt

# In[11]:


term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1)


# ### It's a Kind of Magic

# In[12]:


# While loop
while(cap.isOpened()):

    # capture video
    ret,frame =  cap.read()
    
    # if statement
    if ret == True:
    
        # Frame in HSV
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        
        # Calculate the base of ROI
        dest_roi = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
        
        # Meanshift to get the new coordinates of rectangle
        ret,track_window = cv2.meanShift(dest_roi,track_window,term_crit)
        
        # Draw new rectangle on image
        x,y,w,h =track_window
        
        # Open new window and display
        img2 = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),3)
        
        cv2.imshow("FaceTracker" , img2)
        # Close window
        if cv2.waitKey(50) & 0xFF == 27:
            break
        
    # else statement
    else:
        break
    
# Release and Destroy
cap.release()
cv2.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




