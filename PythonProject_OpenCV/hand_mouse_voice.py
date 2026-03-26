import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import os
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)

screen_w, screen_h = pyautogui.size()

last_click_time = 0
last_vol_time = 0

def set_volume(vol):
    vol = max(0, min(100, int(vol)))
    os.system(f"osascript -e 'set volume output volume {vol}'")
def fingers_up(lm):
    fingers = []

    # 拇指（左右手不同判斷）
    if lm[4][0] > lm[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)

    # 其他四指
    for tip in [8, 12, 16, 20]:
        if lm[tip][1] < lm[tip - 2][1]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:

            lm = []
            for id, point in enumerate(handLms.landmark):
                cx, cy = int(point.x * w), int(point.y * h)
                lm.append((cx, cy))

            fingers = fingers_up(lm)

            # 比讚（只有拇指是1）
            if fingers == [1, 0, 0, 0, 0]:
                current_time = time.time()
                if current_time - last_click_time > 0.6:
                    pyautogui.click()
                    last_click_time = current_time
                    cv2.putText(img, "CLICK", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # 握拳（全部0）
            if fingers == [0, 0, 0, 0, 0]:
                cv2.putText(img, "EXIT", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Hand Control", img)
                cv2.waitKey(500)
                cap.release()
                cv2.destroyAllWindows()
                exit()

    if result.multi_hand_landmarks:
        for idx, handLms in enumerate(result.multi_hand_landmarks):

            label = result.multi_handedness[idx].classification[0].label

            lm = []
            for id, point in enumerate(handLms.landmark):
                cx, cy = int(point.x * w), int(point.y * h)
                lm.append((cx, cy))

            # ===== 左手：滑鼠 =====
            if label == "Left":

                x1, y1 = lm[8]
                x2, y2 = lm[12]

                screen_x = np.interp(x1, (0, w), (0, screen_w))
                screen_y = np.interp(y1, (0, h), (0, screen_h))

                pyautogui.moveTo(screen_x, screen_y)

                # 👉 穩定點擊（距離 + 冷卻）
                dist_click = np.hypot(x2 - x1, y2 - y1)

                current_time = time.time()
                if dist_click < 40 and current_time - last_click_time > 0.4:
                    pyautogui.click()
                    last_click_time = current_time

                cv2.putText(img, "Mouse", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # ===== 右手：音量 =====
            if label == "Right":

                x_thumb, y_thumb = lm[4]
                x_index, y_index = lm[8]

                dist = np.hypot(x_index - x_thumb, y_index - y_thumb)

                vol = np.interp(dist, [20, 200], [0, 100])

                current_time = time.time()
                if current_time - last_vol_time > 0.2:
                    set_volume(vol)
                    last_vol_time = current_time

                # 畫音量條
                bar = int(np.interp(vol, [0, 100], [300, 100]))

                cv2.rectangle(img, (50, 100), (85, 300), (255, 255, 255), 2)
                cv2.rectangle(img, (50, bar), (85, 300), (0, 255, 0), -1)

                cv2.putText(img, f'{int(vol)}%', (40, 350),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.putText(img, "Volume", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Advanced Hand Control", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()