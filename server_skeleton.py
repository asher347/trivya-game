##############################################################################
# server.py
##############################################################################

import socket
import chatlib_skeleton
import select
import random
import json
import requests




# GLOBALS
users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
massegs_to_send=[]
ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
hu_u={}

# HELPER SOCKET METHODS
def print_client_sockets(client_sockets):
	try:
		for client_socket in client_sockets:
			print("\t",client_socket.getpeername())
	except TypeError:
		return None


def build_and_send_message(conn, code, msg):
	## copy from client
	global massegs_to_send
	full_msg = chatlib_skeleton.build_message(code, msg)
	print("[SERVER] ",  'msg:', full_msg)
	massegs_to_send.append((conn,full_msg))
	print("[SERVER] ",'msg:',full_msg)	  # Debug print

def recv_message_and_parse(conn):
	## copy from client
	full_msg = conn.recv(chatlib_skeleton.MAX_DATA_LENGTH).decode()
	cmd, data = chatlib_skeleton.parse_message(full_msg)
	host=conn.getpeername()
	print("[CLIENT] ",host,"msg:",full_msg)	  # Debug print
	return (cmd, data)


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions
def handel_load_question_Web():
	global questions

	# Sample URL to fetch the html page

	url = 'https://opentdb.com/api.php?amount=10'
	r = requests.get(url)
	r=r.json()
	file_question=r["results"]
	for i in range(len(file_question)):
		answers=file_question[i]['incorrect_answers']+[file_question[i]['correct_answer']]
		random.shuffle(answers)
		question=file_question[i]['question']
		questions[i+1]={'question':question.encode().decode('unicode-escape').replace('&quot;'," "),'answers':answers,
						"correct":(answers.index(file_question[i]['correct_answer']))+1}
	return questions
handel_load_question_Web()

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	# Implement code ...
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP,SERVER_PORT))
	server_socket.listen()
	return server_socket
	


		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	data=ERROR_MSG+" "+error_msg
	build_and_send_message(conn,ERROR_MSG,data)


	
##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	global users
	data=str(users[username]["score"])
	build_and_send_message(conn,chatlib_skeleton.PROTOCOL_SERVER["your_score_msg"],str(data))
	# Implement this in later chapters
def handle_highscore_message(conn):
	global users
	users_score = {key: users[key]["score"] for key in users}
	users_score = sorted(users_score.items(), key=lambda t: t[1], reverse=True)
	use = [user[0] + ':' + str(user[1]) for user in users_score]
	build_and_send_message(conn,chatlib_skeleton.PROTOCOL_SERVER["heigh_score_msg"],str(use))
def create_random_question(username):
	global users
	global questions
	print(questions)
	question = random.choice(list(questions.keys()))
	id_question=[key for key in questions.keys()]
	print(users[username]["questions_asked"])
	if len(id_question)==len(users[username]["questions_asked"]):

		return None
	else:
		while question in users[username]["questions_asked"]:
			question = random.choice(list(questions.keys()))
		quest = questions[question]['question'] + "#"
		ans = questions[question]["answers"]
		if len(ans)<4:
			ans=ans + (4-len(ans))*ans[0]
			ans1 = [i + "#" for i in ans if ans.index(i) != len(ans) - 1]
			ans2 = ans1[0] + ans1[1] + ans1[2] + ans[3]
		else:
			ans1 = [i + "#" for i in ans if ans.index(i) != len(ans) - 1]
			ans2 = ans1[0] + ans1[1] + ans1[2] + ans[3]
		resolt = str(question) + "#" + quest + ans2
		users[username]["questions_asked"].append(question)
		return resolt
def handle_question_message(conn,username):
	data=create_random_question(username)
	if data ==None:
		cmd=chatlib_skeleton.PROTOCOL_SERVER["game_over"]
		msg=""
		build_and_send_message(conn,cmd,msg)
	else:
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["question_msg"], data)
a={}
def handle_answer_message(conn,username,data):
	global a
	global questions
	data=data.split(chatlib_skeleton.DATA_DELIMITER)
	key,your_answer=int(data[0]),int(data[1])
	print(";;;;",key,your_answer)
	T=key in a.values()
	TT=username in a.keys()
	if T and TT:
		data = "Caution!! Someone is trying to play by the rules"
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["wrong_answer_msg"], data)
	else:
		if questions[key]["correct"] == your_answer:
			users[username]["score"] += 5
			build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["correct_answer_msg"], "")
		else:
			data = str(questions[key]["correct"])
			build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["wrong_answer_msg"], data)
			a[username]=key

def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users

	# Implement code ...
	try:
		del logged_users[conn.getpeername()]
		conn.close()
	except:
		conn.close()


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	data=data.split(chatlib_skeleton.DATA_DELIMITER)
	users=load_user_database()
	userename=[key for key in users.keys()]
	useres_and_pasword={key:users[key]["password"] for key in users.keys()}
	if data[0] in userename and useres_and_pasword[data[0]]==data[1]:
		msg = ""
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["login_ok_msg"], msg)
		logged_users[conn.getpeername()] = data[0]
	elif data[0] in userename:
		msg="Error! Password does not match!"
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["login_failed_msg"], msg)
		return
	else:
		msg="Error! Username does not exist"
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["login_failed_msg"], msg)
		return

def handle_register_message(conn, data):


	
	global users
	global logged_users
	data=data.split(chatlib_skeleton.DATA_DELIMITER)
    
	if data[0] in users.keys():
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["register_failed_msg"], "Username already exists")
	else:
		users[data[0]] = {"password": data[1], "score": 0, "questions_asked": []}
		build_and_send_message(conn, chatlib_skeleton.PROTOCOL_SERVER["register_ok_msg"], "Account created successfully")
		logged_users[conn.getpeername()] = data[0]




def handle_logged_message(conn):
	global logged_users
	cmd=chatlib_skeleton.PROTOCOL_SERVER["loged_msg"]
	data=chatlib_skeleton.join_data([user for user in logged_users.values()])
	build_and_send_message(conn,cmd,data)


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	comand_client=[comand for comand in chatlib_skeleton.PROTOCOL_CLIENT.values()]
	if cmd=="LOGIN":
		handle_login_message(conn, data)
	elif cmd == "REGISTER":
		handle_register_message(conn, data)
	elif cmd=="LOGOUT":
		handle_logout_message(conn)
	elif cmd=="MY_SCORE":
		username=logged_users[conn.getpeername()]
		handle_getscore_message(conn,username)
	elif cmd=="HIGHSCORE":
		handle_highscore_message(conn)
	elif cmd=="LOGGED":
		handle_logged_message(conn)
	elif cmd=="GET_QUESTION":
		username=logged_users[conn.getpeername()]
		handle_question_message(conn,username)
	elif cmd=="SEND_ANSWER":
		username=logged_users[conn.getpeername()]
		handle_answer_message(conn,username,data)
	else:
		msg="The comand not recognized"
		send_error(conn,msg)

	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	global logged_users
	global massegs_to_send
	print("Welcome to Trivia Server!")
	
	# Implement code ...
	server_socket=setup_socket()
	client_sockets = []
	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets,[])
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = current_socket.accept()
				print("client joined!", client_address)
				try:
					cmd, data = recv_message_and_parse(client_socket)
					handle_client_message(client_socket, cmd, data)
					client_sockets.append(client_socket)
					print_client_sockets(client_sockets)
				except ConnectionError:
					handle_logout_message(client_socket)
					print("Conection closed")
			else:
				print("New data from client")
				try:
					cmd, data = recv_message_and_parse(current_socket)
				except ConnectionError:
					handle_logout_message(current_socket)
					client_sockets.remove(current_socket)
					print_client_sockets(current_socket)
					print("Conection closed")
				else:
					if cmd == chatlib_skeleton.PROTOCOL_CLIENT["logout_msg"]:
						cmd, data = chatlib_skeleton.PROTOCOL_CLIENT["logout_msg"], ""
						handle_client_message(current_socket, cmd, data)
						client_sockets.remove(current_socket)
						print_client_sockets(current_socket)
						print("Conection closed")
					else:
						print("Dibagg",cmd)
						print(data)
						handle_client_message(current_socket, cmd, data)

		for msg in massegs_to_send:
			current_socket, data = msg
			if current_socket in ready_to_write or current_socket==ready_to_write:
				current_socket.send(data.encode())
				massegs_to_send.remove(msg)




if __name__ == '__main__':
	main()

	