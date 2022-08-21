# A HTTP LOG LINE SAMPLE
# 182.74.246.198 - - [01/Mar/2017:02:18:36 -0800] "GET /bootstrap/img/favicon.ico HTTP/1.1" 200 589 "http://www.secrepo.com/" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"


from utilities import *

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log_file', help = 'The raw http log file', required = True)
parser.add_argument('-d', '--dest_file', help = 'Destination to store the resulting csv file', required = True)
parser.add_argument('-a', '--artificial_label', help = 'Generate an artificial label for each log line', action='store_true')

args = vars(parser.parse_args())

log_file = args['log_file']
dest_file = args['dest_file']
artificial_label = args['artificial_label']


# Encode all the data in http log file (access_log)
def encode_log_file(log_file):
	data = {}
	log_file = open(log_file, 'r')
	for log_line in log_file:
		url,log_line_data=encode_single_log_line(log_line)
		if log_line_data != None:
			data[url] = log_line_data
	return data


def encode_single_line(single_line,features):
	encoded = ""
	for feature in features:
		encoded += str(single_line[feature]) + ','
	return encoded


# Label data by adding a new raw with two possible values: 1 for attack or suspecious activity and 0 for normal behaviour
def save_encoded_data(data,encoded_data_file,artificial_label):
	count = 0
	for w in data:
		if artificial_label == True:
			attack = '0'
			patterns = ['honeypot', '%3b', 'xss', 'sql', 'union', '%3c', '%3e', 'eval', '%22', 'bash%20-i', 'robots.txt','{', '/etc/passwd', '../', '%2Fetc%2Fpasswd', '..%2F..%2F', '%252Fetc%252Fpasswd%25',';','%3B', '%20waitfor%20delay%20', '.ini', '.sh', 'onerror', 'alert', 'file:', 'script', "'", '%27', '"', 'OR', 'AND', "'1or1'='1;", '%271or1%27%3D%271%3B', '"1or1"="1;', '%221or1%22%3D%221%3B']
			if any(pattern in w.lower() for pattern in patterns) or (data[w]['return_code'] == 404 or data[w]['return_code'] == 500):
				attack = '1'
				count+=1
			data_row = encode_single_line(data[w],FEATURES) + attack + ',' + w + '\n'
		else:
			data_row = encode_single_line(data[w],FEATURES) + w + '\n'
		encoded_data_file.write(data_row)
	print (str(len(data)) + ' rows have successfully saved to ' + dest_file)
	print("total attacks : ", count)

save_encoded_data(encode_log_file(log_file),open(dest_file, 'w'),artificial_label)