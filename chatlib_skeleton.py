import re
# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"score_msg" :"MY_SCORE",
"highscore_msg":"HIGHSCORE",
"get_question":"GET_QUESTION",
"send_answer":"SEND_ANSWER",
"get_logged_users":"LOGGED",
"register_msg" : "REGISTER"
}


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"your_score_msg":"YOUR_SCORE",
"heigh_score_msg":"ALL_SCORE",
"loged_msg":"LOGGED_ANSWER",
"question_msg":"YOUR_QUESTION",
"correct_answer_msg":"CORRECT_ANSWER",
"wrong_answer_msg":"WRONG_ANSWER",
"game_over":"NO_QUESTIONS",
"register_ok_msg" : "REGISTER_OK",  
"register_failed_msg" : "REGISTER_FAILED" 
}



# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
    # Implement code ...
	if len(data)>MAX_DATA_LENGTH or len(cmd)>CMD_FIELD_LENGTH:
		return ERROR_RETURN
	padded_command=cmd +(CMD_FIELD_LENGTH-len(cmd))*" "
	padded_lenght=(LENGTH_FIELD_LENGTH-len(str(len(data))))*'0'+str(len(data))
	full_msg=padded_command+DELIMITER+padded_lenght+DELIMITER+data
	return full_msg


def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
    # Implement code ...
	if len(data)<22:
		return (ERROR_RETURN , ERROR_RETURN )
	cmd=data[:16]
	exept_length=data[16:22]
	msg=data[22:]
	if exept_length[0]!= DELIMITER or exept_length[5]!=DELIMITER:
		return (ERROR_RETURN ,ERROR_RETURN )
	cmd=cmd.strip()
	exept_length=exept_length[1:5]
	L=re.findall(r'[0-9]+',exept_length)
	if L==[]:
		return (ERROR_RETURN ,ERROR_RETURN )
	else:
		num=""
		for i in range(len(exept_length)):
			j=exept_length[i]
			if j==' ':
				continue
			elif num=="" and j=='0':
				continue
			elif j=="-":
				return (ERROR_RETURN ,ERROR_RETURN )
			else:
				num=num+j
		if num!="" and int(num)==len(msg):
			return (cmd,msg)
		elif num=="" and len(data)==22:
			msg=exept_length
			return (cmd,msg)
		return (ERROR_RETURN,ERROR_RETURN)













	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string 
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	
	msg= msg.split('#')
	if len(msg)-1==expected_fields:
		return msg
	return None


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
	Returns: string that looks like cell1#cell2#cell3
	"""
	
	resolt=''
	for i in range(len(msg_fields)-1):
		resolt+=msg_fields[i]+'#'
	resolt=resolt+msg_fields[len(msg_fields)-1]
	msg_fields=resolt
	return msg_fields

