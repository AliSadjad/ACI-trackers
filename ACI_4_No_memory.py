# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 16:41:14 2019

@author: AliSekhavati

ACI tracker without memory of first frames
"""
import cv2
import sys


#(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')￼

if __name__ == '__main__' :
    
    def are_other_2_close (bound0 , bound1):
        are_other_2_close_flag = True
        for i in range (0,4):
            if abs (bound0[i] - bound1[i]) > 38 or bound0[i] < 0.01 or bound1[i] < 0.01:
                are_other_2_close_flag = False
        return are_other_2_close_flag
            

    tracker_type = 'ACI without memory of first frames'

    tracker1 = cv2.TrackerMOSSE_create()
    tracker = cv2.TrackerKCF_create()
    tracker0 = cv2.TrackerCSRT_create()
    tracker2 = cv2.TrackerMIL_create()

    # Read video
    video = cv2.VideoCapture("videos/american_pharoah.mp4")

    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()

    # Read first frame
    ok, frame = video.read()
    if not ok:
        print ('Cannot read video file')
        sys.exit()
    
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox0=bbox1=bbox=bbox2=bbox_average = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok0 = tracker0.init(frame, bbox0)
    ok1 = tracker1.init(frame, bbox1)
    ok = tracker.init(frame, bbox)
    ok2 = tracker2.init(frame, bbox2)
    
    flag = flag0 = flag1 = flag2 = True
    nf = 0
    lfps = []
    total_fps = 0
    k = 0
    counter = 0
    mistake = 0
    mistake0 = 0
    mistake1 = 0
    mistake2 = 0
    h,w,_ = frame.shape
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (w,h))

    while k!= 27:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)
        ok0, bbox0 = tracker0.update(frame)
        ok1, bbox1 = tracker1.update(frame)
        ok2, bbox2 = tracker2.update(frame)
        
        flag = True
        flag0 = True
        flag1 = True
        flag2 = True
        for i in range (0,4):
            if abs (bbox[i]-bbox_average[i])>38 or not ok or bbox [i]<0.001:
                flag = False
                mistake += 1
    
            if abs (bbox0[i]-bbox_average[i])>38 or not ok0 or bbox0 [i]<0.001:
                flag0 = False
                mistake0 += 1
            
            if abs (bbox1[i]-bbox_average[i])>38 or not ok1 or bbox1 [i]<0.001:
                flag1 = False
                mistake1 += 1
            
            if abs (bbox2[i]-bbox_average[i])>38 or not ok2 or bbox2 [i] <0.001:
                flag2 = False
                mistake2 += 1
                
        
        if flag and flag0 and flag1 and flag2:
            del bbox_average
            bbox_average=((bbox[0]+bbox0[0]+bbox1[0]+bbox2[0])/4,(bbox[1]+bbox0[1]+bbox1[1]+bbox2[1])/4,
                                (bbox[2]+bbox0[2]+bbox1[2]+bbox2[2])/4,(bbox[3]+bbox0[3]+bbox1[3]+bbox2[3])/4)
            
        elif flag and flag0 and flag1:
            del bbox_average
            bbox_average=((bbox[0]+bbox0[0]+bbox1[0])/3,(bbox[1]+bbox0[1]+bbox1[1])/3,(bbox[2]+bbox0[2]+bbox1[2])/3,(bbox[3]+bbox0[3]+bbox1[3])/3)
            if mistake2 >= 70:
                mistake2 = 0
                del bbox2
                del tracker2
                bbox2 = bbox_average
                tracker2 = cv2.TrackerMIL_create()
                ok2 = tracker2.init(frame , bbox2)
            
        elif flag and flag0 and flag2:
            del bbox_average
            bbox_average=((bbox[0]+bbox0[0]+bbox2[0])/3,(bbox[1]+bbox0[1]+bbox2[1])/3,(bbox[2]+bbox0[2]+bbox2[2])/3,(bbox[3]+bbox0[3]+bbox2[3])/3)
            if mistake1 >= 70:
                mistake1 = 0
                del bbox1
                del tracker1
                bbox1 = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init (frame , bbox1)
            
        elif flag0 and flag1 and flag2:
            del bbox_average
            bbox_average=((bbox2[0]+bbox0[0]+bbox1[0])/3,(bbox2[1]+bbox0[1]+bbox1[1])/3,(bbox2[2]+bbox0[2]+bbox1[2])/3,(bbox2[3]+bbox0[3]+bbox1[3])/3)
            if mistake >= 70:
                mistake = 0
                del bbox
                del tracker
                bbox = bbox_average
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init (frame, bbox)
            
        elif flag and flag1 and flag2:
            del bbox_average
            bbox_average=((bbox[0]+bbox2[0]+bbox1[0])/3,(bbox[1]+bbox2[1]+bbox1[1])/3,(bbox[2]+bbox2[2]+bbox1[2])/3,(bbox[3]+bbox2[3]+bbox1[3])/3)
            if mistake0 >= 70:
                mistake0 = 0
                del bbox0
                del tracker0
                bbox0 = bbox_average
                tracker0 = cv2.TrackerCSRT_create()
                ok0 = tracker0.init (frame, bbox0)
            
        elif flag0 and flag1:
            del bbox_average
            bbox_average= ((bbox0[0]+bbox1[0])/2,(bbox0[1]+bbox1[1])/2,(bbox0[2]+bbox1[2])/2,(bbox0[3]+bbox1[3])/2)
            if mistake >= 70:
                mistake = 0
                del bbox
                del tracker
                bbox = bbox_average
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init (frame, bbox)
            if mistake2 >= 70:
                mistake2 = 0
                del bbox2
                del tracker2
                bbox2 = bbox_average
                tracker2 = cv2.TrackerMIL_create()
                ok2 = tracker2.init(frame , bbox2)
            
        elif flag and flag0:
            del bbox_average
            bbox_average= ((bbox[0]+bbox0[0])/2,(bbox[1]+bbox0[1])/2,(bbox[2]+bbox0[2])/2,(bbox[3]+bbox0[3])/2)
            if mistake2 >= 70:
                mistake2 = 0
                del bbox2
                del tracker2
                bbox2 = bbox_average
                tracker2 = cv2.TrackerMIL_create()
                ok2 = tracker2.init(frame , bbox2)
            if mistake1 >= 70:
                mistake1 = 0
                del bbox1
                del tracker1
                bbox1 = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init (frame , bbox1)
            
        elif flag2 and flag0:
            del bbox_average
            bbox_average= ((bbox2[0]+bbox0[0])/2,(bbox2[1]+bbox0[1])/2,(bbox2[2]+bbox0[2])/2,(bbox2[3]+bbox0[3])/2)
            if mistake1 >= 70:
                mistake1 = 0
                del bbox1
                del tracker1
                bbox1 = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init (frame , bbox1)
            if mistake >= 70:
                mistake = 0
                del bbox
                del tracker
                bbox = bbox_average
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init (frame, bbox)
            
        elif flag and flag2:
            del bbox_average
            bbox_average= ((bbox[0]+bbox2[0])/2,(bbox[1]+bbox2[1])/2,(bbox[2]+bbox2[2])/2,(bbox[3]+bbox2[3])/2)
            if mistake1 >= 70:
                mistake1 = 0
                del bbox1
                del tracker1
                bbox1 = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init (frame , bbox1)
            if mistake0 >= 70:
                mistake0 = 0
                del bbox0
                del tracker0
                bbox0 = bbox_average
                tracker0 = cv2.TrackerCSRT_create()
                ok0 = tracker0.init (frame, bbox0)
            
        elif flag1 and flag2:
            del bbox_average
            bbox_average= ((bbox1[0]+bbox2[0])/2,(bbox1[1]+bbox2[1])/2,(bbox1[2]+bbox2[2])/2,(bbox1[3]+bbox2[3])/2)
            if mistake0 >= 70:
                mistake0 = 0
                del bbox0
                del tracker0
                bbox0 = bbox_average
                tracker0 = cv2.TrackerCSRT_create()
                ok0 = tracker0.init (frame, bbox0)
            if mistake >= 70:
                mistake = 0
                del bbox
                del tracker
                bbox = bbox_average
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init (frame, bbox)
            
        elif flag and flag1:
            del bbox_average
            bbox_average= ((bbox[0]+bbox1[0])/2,(bbox[1]+bbox1[1])/2,(bbox[2]+bbox1[2])/2,(bbox[3]+bbox1[3])/2)
            if mistake0 >= 70:
                mistake0 = 0
                del bbox0
                del tracker0
                bbox0 = bbox_average
                tracker0 = cv2.TrackerCSRT_create()
                ok0 = tracker0.init (frame, bbox0)
            if mistake2 >= 70:
                mistake2 = 0
                del bbox2
                del tracker2
                bbox2 = bbox_average
                tracker2 = cv2.TrackerMIL_create()
                ok2 = tracker2.init(frame , bbox2)
        
        elif ok0:
            del bbox_average 
            counter += 1
            bbox_average=bbox0
            if are_other_2_close(bbox , bbox1):
                bbox_average = ((bbox[0]+bbox1[0])/2,(bbox[1]+bbox1[1])/2,(bbox[2]+bbox1[2])/2,(bbox[3]+bbox1[3])/2)
            if counter == 100:
                del tracker , tracker1
                bbox1 = bbox_average
                bbox = bbox_average
                tracker1 = cv2.TrackerMOSSE_create()
                ok1 = tracker1.init(frame, bbox1)
                tracker = cv2.TrackerKCF_create()
                ok = tracker.init(frame, bbox)
        elif ok1:
            del bbox_average
            bbox_average=bbox1
            if are_other_2_close (bbox , bbox0):
                bbox_average= ((bbox[0]+bbox0[0])/2,(bbox[1]+bbox0[1])/2,(bbox[2]+bbox0[2])/2,(bbox[3]+bbox0[3])/2)
        elif ok:
            del bbox_average
            bbox_average=bbox
            if are_other_2_close (bbox0 , bbox1):   
                bbox_average= ((bbox0[0]+bbox1[0])/2,(bbox0[1]+bbox1[1])/2,(bbox0[2]+bbox1[2])/2,(bbox0[3]+bbox1[3]))
        elif ok2:
            del bbox_average
            bbox_average=bbox2
            if are_other_2_close (bbox0 , bbox1):
                bbox_average= ((bbox0[0]+bbox1[0])/2,(bbox0[1]+bbox1[1])/2,(bbox0[2]+bbox1[2])/2,(bbox0[3]+bbox1[3]))
        else:
            bbox_average=bbox0
        

        # Draw bounding box
        
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            counter = 0
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,0,0),2)
            bbox=bbox_average
        
        if ok0:
            # Tracking success
            p10 = (int(bbox0[0]), int(bbox0[1]))
            p20 = (int(bbox0[0] + bbox0[2]), int(bbox0[1] + bbox0[3]))
            cv2.rectangle(frame, p10, p20, (0,255,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking CSRT failure detected", (100,110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,0),2)
            bbox0=bbox_average
       
        if ok1:
            # Tracking success
            p11 = (int(bbox1[0]), int(bbox1[1]))
            p21 = (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3]))
            cv2.rectangle(frame, p11, p21, (0,0,255), 2, 1)
            counter = 0
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking 1 failure detected", (100,140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            bbox1=bbox_average
            
        if ok2:
            # Tracking success
            p12 = (int(bbox2[0]), int(bbox2[1]))
            p22 = (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3]))
            cv2.rectangle(frame, p12, p22, (255,255,255), 2, 1)
            counter = 0
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking 2 failure detected", (100,170), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(255,255,255),2)
            bbox2=bbox_average
            
        p1_average = (int(bbox_average[0]), int(bbox_average[1]))
        p2_average = (int(bbox_average[0] + bbox_average[2]), int(bbox_average[1] + bbox_average[3]))
        cv2.rectangle(frame, p1_average, p2_average, (0,0,0), 2, 1)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);


        # Display result
        cv2.imshow("Tracking", frame)
        #nf += 1
        lfps.append(fps)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        #if k == 27 : break
        out.write (frame)
    
    cv2.destroyAllWindows()
    
    for i in range (len(lfps)):
        total_fps += lfps [i]
    average_fps = total_fps / len(lfps)
    out.release()    