#16_team_강지웅_장현기

import socket
import time

s = socket.socket()
host = input("IP 주소를 입력하세요: ") #localhost 혹은 외부 아이피 입력
port = 9999  # 포트번호는 9999

def print_matrix(matrix): # 서버로부터 배열 값을 받아 클라이언트 화면에 출력
    for i in range(3):
        for j in range(3):
            current = "---"
            if matrix[i][j] == 1: 
                current = "X"
            elif matrix[i][j] == 2:
                current = "O"
            print(current, end="\t")
        print("")

def start_player():
    try: #서버 연결 및 게임 실행
        s.connect((host, port))
        print("연결된 아이피 주소:", host, "포트번호:", port)
        start_game()
    except socket.error as e: #서버 연결이 안될 시
        print("소켓 연결이 안되었습니다.", e)
    finally: 
        s.close()

def start_game():
    welcome = s.recv(1024) #소켓으로부터 최대 1024 바이트를 읽어옴
    print(welcome.decode())

    name = input("닉네임을 설정해주세요: ")
    s.send(name.encode())

    while True:
        try:
            recvData = s.recv(1024)
            recvDataDecode = recvData.decode()

            if recvDataDecode == "입력값":
                failed = 1
                while failed:
                    try:
                        x = int(input("수를 둘 1차원 배열값을 입력하시오(0~2): "))
                        y = int(input("수를 둘 2차원 배열값을 입력하시오(0~2): "))
                        coordinates = str(x) + "," + str(y)
                        s.send(coordinates.encode())
                        failed = 0
                    except ValueError:
                        print("잘못된 입력입니다. 다시 입력해주세요.")

            elif recvDataDecode == "오류":
                print("오류가 발생했습니다. 다시 입력해주세요.")

            elif recvDataDecode == "현황판":
                matrixRecv = s.recv(1024)
                matrixRecvDecoded = matrixRecv.decode("utf-8")
                print_matrix(eval(matrixRecvDecoded))
             

            elif not recvDataDecode:
                print("서버와의 연결이 끊어졌습니다.")
                break

            else:
                print(recvDataDecode)
        except KeyboardInterrupt:
            print("\n잘못된 입력")
            break

if __name__ == "__main__":
    start_player()
