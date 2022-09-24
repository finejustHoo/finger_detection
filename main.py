from handDetector import HandDetector #핸드디텍터 파이썬 파일에서 클래스 가져옴
import cv2 #opencv
import math #수학 할수있게 해주는 라이브러리
import os #윈도우에서 파일 가져오는것을 돕는 라이브러리
import numpy as np #이미지를 수학적으로 바꿔줌.
import serial

arduino = serial.Serial('COM6', 9600)

handDetector = HandDetector(min_detection_confidence=0.7) #손 인식 신뢰도
webcamFeed = cv2.VideoCapture(0)

# 절대경로 C:\\Users\\HOME\\PycharmProjects\\pythonProjecttreaknwglkengkle\\son.mp4
# 상대경로 son.mp4
# 0은 웹캠


path = "finger"
myList = os.listdir(path)  #파일들에 대해 리스트 작성
overlayList=[]

for impath in myList: #리스트 자료들을 순환 돌려줌.
    img=cv2.imread(f'{path}/{impath}')
    overlayList.append(img) #파일 경로 지정


while True: # 무한루프
    status, image = webcamFeed.read() #status는 웹캠, 프로그램등이 잘 작동되고 있는지 확인 image는 이미지의 값 출력
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count=0

    if(len(handLandmarks) != 0):
        #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        #details: https://google.github.io/mediapipe/solutions/hands

        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
            count = count+1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            count = count+1
        """
        if handLandmarks[12][2] < handLandmarks[10][2] and handLandmarks[4][1] > handLandmarks[3][1] and handLandmarks[8][2] > handLandmarks[6][2] and handLandmarks[16][2] > handLandmarks[14][2] and handLandmarks[20][2] > handLandmarks[18][2]:
            print("ㅗ")
        else:
            print("I am kind")
        #if handLandmarks[4][2] <= handLandmarks[3][2] and handLandmarks[8][2] > handLandmarks[6][2] and handLandmarks[12][2] > handLandmarks[10][2] and handLandmarks[16][2] > handLandmarks[14][2] and handLandmarks[20][2] > handLandmarks[18][2]:
            #print("good")
        """

    h,w,c=overlayList[count].shape
    #image[0:h,0:w]=overlayList[count]
    print(count)
    #cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
    #cv2.imshow("Volume", image)
    #sent= input(str(count))
    #sent = sent.enconde()
    A = str(count)
    A = A.encode('utf-8')
    arduino.write(A)
    print(A )
    cv2.waitKey(1)