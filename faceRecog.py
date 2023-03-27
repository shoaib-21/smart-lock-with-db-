# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS #using to count frames per second
import face_recognition
import imutils
import pickle
import time
import cv2
def Face(empname):
    
        #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
        #Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"
    #knownfaces =['noor','shoaib','mustafa']
    countfaces = 0
        # load the known faces and embeddings along with OpenCV's Haar
        # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())

    vs = VideoStream(usePiCamera=True).start()# modified tells to use picamera module and starts the threaded videostream
    time.sleep(1.0)#modified allows time to fill up the initial buffer. it is recommended to use after VideoStream()

    fps = FPS().start()# modified starts fps counter after first image is received..and storing the start time using start()
    timeout = 5 # [seconds]
    timeout_start = time.time()
    print(timeout_start)
    authFrame = 1
        # loop over for 20 seconds only
    while time.time() < timeout_start + timeout:
        nameX=''
        frame = vs.read()#modified stores the current frame using read() from VideoStream class  

            #modified detect faces in the specified current frame and stores the bounding boxes in a list of tuple (top,right,bottom,left) 
        boxes = face_recognition.face_locations(frame,1,"hog")#modified it by default takes model="hog" but we can use cnn(use in gpu)that is more accurate 
        if len(boxes) !=1:
            fps.update()
            continue
            #modified computing 128-dimensions of face in a bounding box to identify the particular face
        encodings = face_recognition.face_encodings(frame, boxes,1,"small")
        names = []

            # loop over the facial embeddings
        for encoding in encodings:
                # modified attempt to match each face from current frame to our known face encodings in pickle file
            matches = face_recognition.compare_faces(data["encodings"],encoding,0.5)#modified returns a list of T/F indicates 
                #which known face(in our case which face in pickle) is matched against the face encodings in current frame and can set tolerance 0.6 preferable 

            name = "Unknown" #if face is not recognized, then print Unknown

                # check to see if we have found a match
            if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                matchedIdxs = [index for (index, isFaceMatched) in enumerate(matches) if isFaceMatched]# modified i=index, b=T/F .storing index if the face is matched i.e., if b = True
                counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]#modified fetching the name of matched face encoding from data(dictionary) 
                    counts[name] = counts.get(name, 0) + 1#modified creating dictionary with name(matchedface) as key and no. of times that face occurs as value

                    #modified getting the recognizied faced that is matched maximum times from counts dictionary
                name = max(counts, key=counts.get)
                
                
                nameX = name
                print(name)
                    #If someone in your dataset is identified, print their name on the screen
                #if currentname != name:
                 #   currentname = name
                  #  print(currentname)
                    #else:
                        #print(name)                
            names.append(name)
        #print("cheetah1 "+name)
        #print("cheetah2 "+empname)
        if name == empname:
            authFrame= cv2.imencode('.png',frame)[1].tobytes()
            countfaces = countfaces + 1
            # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                    (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

            # # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)
        key = cv2.waitKey(1) & 0xFF

            # # quit when 'q' key is pressed
        if key == ord("q"):
            break
        #if nameX==empname:
         #   print(nameX+" is matched")
          #  break
        #shoaib#
        if countfaces == 6:
            print("Final ans: " ,empname )
            #print(countfaces)
            cv2.destroyAllWindows()
            vs.stop()
            return authFrame,empname
        #shoaib#
            # modified increments the total no. of frames during start and end interval
        #print(countfaces)
        fps.update()

        # modified stops the fps timer/counter
    fps.stop()
    #print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))#modified using elapsed() printing total no. of seconds b/w start and end interval
    #print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))# modified using fps() prints total no. of computed frames per second
    #print("count:" ,countfaces)
        # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()
    #print(countfaces)
    return False
