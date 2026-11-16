import asyncio
from websockets.asyncio.server import serve
import cv2
import numpy as np
import mediapipe as mp
import CalculateDegree as cd
import socket

ESP_IP = ""
ESP_PORT = X

async def handler(connection):
    print("Client Connected")
    with socket.socket(socket.AF_INET , socket.SOCK_DGRAM) as udp_socket:
        async for message in connection:
            np_arr = np.frombuffer(message, dtype=np.uint8)
            frame = cv2.imdecode(np_arr , cv2.IMREAD_COLOR)

            if frame is not None:
                frame = cv2.flip(frame , 1)
                RGB_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)

                RGB_frame.flags.writeable = False
                results = hand_model.process(RGB_frame)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS
                        )

                        degree = cd.CalDeg(hand_landmarks.landmark[13] , hand_landmarks.landmark[0])
                        udp_socket.sendto(str(int(degree)).encode() , (ESP_IP , ESP_PORT))
                        cv2.putText(frame , f"Degree:{degree:.0f}" , (30,50) , color=(255,0,0) , fontScale=1 , fontFace=cv2.FONT_HERSHEY_SIMPLEX , thickness=2)
                
                cv2.imshow("LIVE !" , frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cv2.destroyAllWindows()
    print("Client Disconnected")

    

async def main():
    async with serve(handler , "" , X):
        print("Server running at ...")
        await asyncio.Future()



if __name__=="__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hand_model = mp_hands.Hands(
        model_complexity = 0,
        max_num_hands = 1,
        min_detection_confidence = 0.6,
        min_tracking_confidence = 0.6
    )

    asyncio.run(main())