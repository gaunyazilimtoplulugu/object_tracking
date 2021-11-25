import cv2
import time


cap = cv2.VideoCapture(0)
pTime = 0
cTime =0

#tracker = cv2.legacy.TrackerMOSSE_create() # bu methodda iyi ama hızlı olmasına karşın sonuçlar kötü
tracker = cv2.legacy.TrackerCSRT_create() # bu yavaş ama net sonuçlar veriyor yukarıdakine göre
# kameranın ilk verdiği görüntü üzerinden bir nesne seçmesini istiyoruz
success,img = cap.read() 
bbox = cv2.selectROI('Tracking',img,False) # tracking penceresinden istedik
tracker.init(img,bbox) # bboxu img ile initialize ettik ve değerler aldık

def drawBox(img,bbox): # fonksiyonda iki değer aldık 
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3]) # bbox bize 4 tane değer dönderiyor 
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1) 
    cv2.putText(img,'Tracking',(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),2)

while True:
    success,img = cap.read()
    success,bbox = tracker.update(img) # tracker a resmimizi yolluyoruz
    if success: # eğer resmimizde object varsa kareye al ve takip et
        drawBox(img,bbox)
    else: # eğer yoksa kaybettim yaz
        cv2.putText(img,'Lost',(75,75),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,0),2) 
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,0),2)
    cv2.imshow('Tracking',img)
    if cv2.waitKey(1) & 0xFF==27:
        break
cv2.destroyAllWindows()
cap.release()
