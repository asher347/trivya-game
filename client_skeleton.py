import socket
import chatlib_skeleton # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS


def build_and_send_message(conn, code, data):
    msg=chatlib_skeleton.build_message(code,data)
    conn.send(msg.encode())
def recv_message_and_parse(conn):

    full_msg=conn.recv(chatlib_skeleton.MAX_DATA_LENGTH).decode()
    cmd, data = chatlib_skeleton.parse_message(full_msg)
    return (cmd, data)

def connect():
    my_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1",5678))
    return my_socket

def error_and_exit(error_msg):
    # Implement code
    print('error_msg')
    return exit()


def login(conn):
    conn=conn
    username=input("Please enter your username:\n")
    password=input("Please enter your pasword:\n")
    data= str(username)+"#"+str(password)
    build_and_send_message(conn,chatlib_skeleton.PROTOCOL_CLIENT["login_msg"],data)
	# Implement code
    cmd,data=recv_message_and_parse(conn)
    while cmd!=chatlib_skeleton.PROTOCOL_SERVER["login_ok_msg"]:
        print("Enter invaild username")
        username = input("Please enter your username:\n")
        password = input("Please enter your pasword:\n")
        data = str(username) + "#" + str(password)
        msg = build_and_send_message(conn, chatlib_skeleton.PROTOCOL_CLIENT["login_msg"], data)
        cmd,data =recv_message_and_parse(conn)

    print("logged in succses\n")
def register(conn):
    a=0
    while True:
        username = input("Please choose a username:\n")
        password = input("Please choose a password:\n")
        data = f"{username}#{password}"
        build_and_send_message(conn, chatlib_skeleton.PROTOCOL_CLIENT["register_msg"], data)
        cmd, data = recv_message_and_parse(conn)
       
        if cmd == chatlib_skeleton.PROTOCOL_SERVER["register_ok_msg"]:
            print("Registration successful! You are now logged in.")
            break
        else:
            print(f"Registration failed: {data}")
            a+=1
            if a>5:
                conn.close()
                break
    

def logout(conn):
   
    build_and_send_message(conn, chatlib_skeleton.PROTOCOL_CLIENT["logout_msg"],"")
    print("logouut sucses")


def build_send_recv_parse(conn, code, data):
    build_and_send_message(conn, code, data)
    cmd,msg=recv_message_and_parse(conn)
    return cmd,msg


def get_score(conn):
    cmd=chatlib_skeleton.PROTOCOL_CLIENT["score_msg"]
    data=""
    cmd,data=build_send_recv_parse(conn, cmd, data)
    print("Your score is:"+data)


def get_highscore(conn):
    cmd = chatlib_skeleton.PROTOCOL_CLIENT["highscore_msg"]
    data=""
    cmd,data=build_send_recv_parse(conn, cmd, data)
    data=data.split("#")
    wo=""
    for i in data[0]:
        if (i=="["):
            continue
        elif ((i=="," )or (i =="]")):
            print(wo)
            wo=""
            continue
        else:
            wo+=i
def play_question(conn):
    cmd = chatlib_skeleton.PROTOCOL_CLIENT["get_question"]
    data = ""
    cmd, data = build_send_recv_parse(conn, cmd, data)
    try:
        cmd=="YOUR_QUESTION"
        question = data.split(chatlib_skeleton.DATA_DELIMITER)
        quest = question[1]
        print(quest)
        print('1. ' + question[2], '2. ' + question[3], '3. ' + question[4], '4. ' + question[5], sep='\n')
        your_answer = input("Enter your ansower:")
        cmd = chatlib_skeleton.PROTOCOL_CLIENT["send_answer"]
        data = question[0] + chatlib_skeleton.DATA_DELIMITER + your_answer
        cmd, data = build_send_recv_parse(conn, cmd, data)

        if cmd == 'CORRECT_ANSWER':
            print("Great job")
        else:
            print("Nope, The correct answer its: " + data)
    except:
        print("You finish all the question","GAME OVER",sep="\n")


def get_logged_users(conn):
    cmd=chatlib_skeleton.PROTOCOL_CLIENT["get_logged_users"]
    data=""
    cmd,data=cmd,data=build_send_recv_parse(conn,cmd,data)
    print("The users thet connect:" +data)
    return data

def main():
    conn=connect()
    while True:
        choice = input("Would you like to (l)login or (r)register? ")
        if choice.lower() == 'l':
            login(conn)
            break
        elif choice.lower() == 'r':
            register(conn)
            break
        else:
            print("Invalid choice. Exiting.")
    print("p        Play a trivia question\n""s        Get my score\n""h        Get high score\n""l        Get logged users\n""q        Quit")
    ans=input("Please enter yor choice:")
    while 'q' not in ans:
        if ans=='s':
            get_score(conn)
            print(
                "p        Play a trivia question\n""s        Get my score\n""h        Get high score\n""l        Get logged users\n""q        Quit")
            ans=input("Please enter yor choice:")
        elif ans=='h':
            get_highscore(conn)
            print(
                "p        Play a trivia question\n""s        Get my score\n""h        Get high score\n""l        Get logged users\n""q        Quit")
            ans=input("Please enter yor choice:")
        elif ans=="p":
            play_question(conn)
            print(
                "p        Play a trivia question\n""s        Get my score\n""h        Get high score\n""l        Get logged users\n""q        Quit")
            ans = input("Please enter yor choice:")
        elif ans=="l":
            get_logged_users(conn)
            print(
                "p        Play a trivia question\n""s        Get my score\n""h        Get high score\n""l        Get logged users\n""q        Quit")
            ans = input("Please enter yor choice:")
        else:
            print("Your choice its invaild")
            ans = input("Please enter vaild choice:")
    if ans=='q':
        logout(conn)
        conn.close()
        print("Goodbye!")

if __name__ == '__main__':
    main()
