from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
classifier = load_model('./model_filter.h5')

class_labels = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    labels=[]
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    '''
    cv2.cvtColor(src, code)
        Params src:	    image
        Params code:    변환 코드
    BGR->Grayscale로 변환하기 위해서는 cv2.COLOR_BGR2GRAY
    '''
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    '''
    scale factor = 1.3
    This scale factor is used to create scale pyramid as shown in the picture. Suppose, the scale factor is 1.03, it means we're using a small step for resizing, i.e. reduce size by 3 %, we increase the chance of a matching size with the model for detection is found,while it's expensive.

    minNeighbors = 5
    Parameter specifying how many neighbors each candidate rectangle should have to retain it. This parameter will affect the quality of the detected faces: higher value results in less detections but with higher quality. We're using 5 in the code.

    https://stackoverrun.com/ko/q/6085002
    https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
    '''

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        '''
        Parameters:	
            img – 그림을 그릴 이미지
            start – 시작 좌표(ex; (0,0))
            end – 종료 좌표(ex; (500. 500))
            color – BGR형태의 Color(ex; (255, 0, 0) -> Blue)
            thickness (int) – 선의 두께. pixel
        '''
        
        roi_gray=gray[y:y+h,x:x+w]
        '''
        region of image 
        '''
        roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
        '''
        Parameters:	
            img – Image
            dsize – Manual Size. 가로, 세로 형태의 tuple(ex; (100,200))
            fx – 가로 사이즈의 배수. 2배로 크게하려면 2. 반으로 줄이려면 0.5
            fy – 세로 사이즈의 배수
            interpolation – 보간법
            INTER_AREA - resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire’-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.

            Interpolation(인터폴레이션, 보간)이란 알려진 지점의 값 사이(중간)에 위치한 값을 알려진 값으로부터 추정하는 것을 말한다.
        '''

        if np.sum([roi_gray])!=0:
            roi=roi_gray.astype('float')/255.0
            # print('1', roi)
            roi=img_to_array(roi)
            '''
            불러온 이미지에 img_to_array 함수를 씌우면 이미지를 NumPy 배열로 변환해 준다. 이미지의 모양을 출력해보면 아래와 같다. 이미지의 크기를 (100 X 100)으로 설정하였고, 컬러 이미지이므로 컬러 채널의 크기가 3이 되어 (100 X 100 X 3)의 3차원 구조를 갖는 배열이 생성되었다.
            '''
            # print('2', roi)
            roi=np.expand_dims(roi,axis=0)
            # print('3', roi)

            preds=classifier.predict(roi)[0]
            # 감정의 확률값을 반환
            print(preds)
            label=class_labels[preds.argmax()]
            # 가장 큰 값의 idx를 반환해서 class_label을 찾는다.
            print(label)
            label_position=(x,y)
            # label을 찾기위한 값.
            print(label_position)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
        else:
            cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
    
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
