import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(1)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0,0,255), thickness=3) #點的樣式
handConStyle = mpDraw.DrawingSpec(color=(0,255,0), thickness=6) #線的樣式
pTime =0
cTime = 0


while True:
    ret, img = cap.read()
    if ret:
        imgRGB =  cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB, )
        result = hands.process(imgRGB)
        imgHight = img.shape[0]
        imgWidth = img.shape[1]

        # print(result.multi_hand_landmarks)
        if result.multi_hand_landmarks:
            #此層for迴圈是要把手的21個點畫出來
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle) #把手上每一個點畫出來（img = 要畫在哪一張圖上面，handLms = 把點傳進去，, mpHands.HAND_CONNECTIONS = 把點用線連起來）
                #此層for迴圈是要把這21個座標印出來
                for i, lm in enumerate(handLms.landmark):
                    #i表示是幾個點，lm表示點的座標
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHight)
                    #顯示每個點是第幾個點
                    # cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 2)
                    #假設想把第四個點放大一點
                    if i == 4:
                        cv2.circle(img, (xPos, yPos), 10, (0, 0, 255), cv2.FILLED)
                    print(i, xPos, yPos)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)


        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break