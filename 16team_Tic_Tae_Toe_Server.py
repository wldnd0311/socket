#16_team_강지웅_장현기

import socket
import pickle
import time

s = socket.socket()
host = "localhost"
port = 9999
matrix = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]

playerOne = 1
playerTwo = 2

playerConn = list()
playerAddr = list()
playerName = list()         

def validate_input(x, y, conn):
    if x >= 3 or y >= 3:
        print("\n잘못 입력했습니다. 다시 입력하세요.\n")
        conn.send("잘못 입력했습니다. 다시 입력하세요.".encode())
        return False
    elif matrix[x][y] != 0:
        print("\n이미 입력되어있습니다.\n")
        conn.send("이미 입력되어있습니다.".encode())
        return False
    return True

def get_input(currentPlayer):
    if currentPlayer == playerOne:
        player = "{} 차례입니다!".format(playerName[0])
        conn = playerConn[0]
    else:
        player = "{} 차례입니다!".format(playerName[1])
        conn = playerConn[1]

    print(player)
    send_common_msg(player)
    failed = 1
    while failed:
        try:
            conn.send("입력값".encode())
            data = conn.recv(1024)
            conn.settimeout(20)
            dataDecoded = data.decode().split(",")
            x = int(dataDecoded[0])
            y = int(dataDecoded[1])
            if validate_input(x, y, conn):
                matrix[x][y] = currentPlayer
                failed = 0
                send_common_msg("현황판")
                send_common_msg(str(matrix))
        except Exception as e:
            conn.send(f"오류 : {str(e)}".encode())
            print(f"오류 발생: {e}")
            break

def check_rows():
    result = 0
    for i in range(3):
        if matrix[i][0] == matrix[i][1] and matrix[i][1] == matrix[i][2]:
            result = matrix[i][0]
            if result != 0:
                break
    return result

def check_columns():
    result = 0
    for i in range(3):
        if matrix[0][i] == matrix[1][i] and matrix[1][i] == matrix[2][i]:
            result = matrix[0][i]
            if result != 0:
                break
    return result

def check_diagonals():
    result = 0
    if matrix[0][0] == matrix[1][1] and matrix[1][1] == matrix[2][2]:
        result = matrix[0][0]
    elif matrix[0][2] == matrix[1][1] and matrix[1][1] == matrix[2][0]:
        result = matrix[0][2]
    return result

def check_winner():
    result = 0
    result = check_rows()
    if result == 0:
        result = check_columns()
    if result == 0:
        result = check_diagonals()
    return result

def start_server():
    try:
        s.bind((host, port))
        print("Tic Tac Toe 서버 작동 중입니다. \n포트번호:", port)
        s.listen(2)
        while True:
            accept_players()
    except socket.error as e:
        print("서버 연결 오류:", e)

def accept_players():
    try:
        welcome = "서버 연결이 되었습니다!"
        for i in range(2):
            conn, addr = s.accept()
            conn.send(welcome.encode())
            name = conn.recv(1024).decode()

            playerConn.append(conn)
            playerAddr.append(addr)
            playerName.append(name)
            print("사용자 {} - {} [{}:{}]".format(i+1, name, addr[0], str(addr[1])))
            conn.send("안녕하세요. {}!, 당신은 {}번째로 서버에 들어왔습니다!".format(name, str(i+1)).encode())
        
        start_game()
    except socket.error as e:
        print("연결 오류", e)   
    except:
        print("오류 발생")
    finally:
        for conn in playerConn:
            conn.close()
        s.close()

def start_game():
    result = 0
    i = 0
    while result == 0 and i < 9:
        if (i % 2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        result = check_winner()
        i = i + 1

    if result == 1:
        lastmsg = "{}이 승리했습니다!".format(playerName[0])
    elif result == 2:
        lastmsg = "{}이 승리했습니다!".format(playerName[1])
    else:
        lastmsg = "비겼습니다."

    send_common_msg(lastmsg)
    lastmsg = "서버를 종료합니다."
    send_common_msg(lastmsg)
    time.sleep(10)
    for conn in playerConn:
        conn.close()
    s.close()


def send_common_msg(text):
    if playerConn[0].fileno() != -1:
        playerConn[0].send(text.encode())
    if playerConn[1].fileno() != -1:
        playerConn[1].send(text.encode())
    time.sleep(1)

if __name__ == "__main__":
    start_server()
