import gzip
import jsons
from cgitb import reset
from importlib.abc import PathEntryFinder
from utilities import *
import ugparser
import boto3
import threading
import time
import json
from termcolor import colored

Threads = []
alerts = {}
alerts['Malware'] = []
alerts['Anomaly'] = []
alerts['GuardDuty'] = []

s3_client = boto3.client('s3')
Bucket = "all.logs.from.aws"
GuardDutyBucket = "guardduty.findings.aws"
HTTPLogsFile = "access.log"
EC2FileTypeLogsFile = "EC2FileTypeLogs.log"
gd = boto3.client('guardduty')

# Get the GuardDuty Detector for the current AWS Region
detector = gd.list_detectors()
detectorid = detector['DetectorIds'][0]

# Finding Criteria for severity in this example must be greater than or
# equal to the value specified in Gte
fc = {'Criterion': {'severity': {'Gte': 4}}}

findings = gd.list_findings(DetectorId=detectorid, FindingCriteria=fc)

def RemoveDuplicates(LogList):
    return list(dict.fromkeys(LogList))

def DecisionTree_AnomalyDetector(log_line):
    anomaly = {}
    anomaly['log'] = []
    anomaly['user-agent'] = []
    anomaly['user-agent-status'] = []

    ug_status = ""
    url,encoded = encode_single_log_line(log_line)

    if log_line[0:3] == "::1":
        log_line = log_line.replace(log_line[0:3],"127.0.0.1",1)
    if log_line[0:7] == "::ffff:":
        log_line = log_line[7:]

    formatte_encoded = []
    for feature in FEATURES:
        formatte_encoded.append(encoded[feature])
    model = pickle.load(open('MODELS/attack_classifier_dt.pkl', 'rb'))
    prediction = model.predict([formatte_encoded])
    is_anomaly = prediction[0]
    #print("logline : {}\nResult : {}".format(log_line,prediction[0]))
    useragent = ugparser.UserAgentExtractor(log_line)
    #print("User-Agent: {}\n\n".format(useragent))
    ParserResult = ugparser.UserAgentParser(useragent)
    if ParserResult:
        ug_status_nc = "Abusive"
        ug_status = colored("Abusive",'red')
    else:
        ug_status_nc = "Normal"
        ug_status = colored("Normal",'green')

    if(is_anomaly > 0 or (ugparser.UserAgentParser) ):
        anomaly['log'] = log_line
        anomaly['user-agent'] = useragent
        anomaly['user-agent-status'] = ug_status_nc
        alerts['Anomaly'].append(anomaly)

        colored_log_line = colored(log_line,'magenta')
        print(colored('Anomaly Detected','yellow')," :\n\tlog : {}\n\tUser-Agent: {}\n\tUser-Agent Status: {}\n".format(colored_log_line,useragent,ug_status))

def MalwareDetector(log_line):
    malware = {}
    malware['path'] = []
    malware['family'] = []
    log_line  = log_line.split('\t')
    if(log_line[1] == '1'):
        malware['path'] = log_line[0]
        malware['family'] = log_line[2]
        alerts['Malware'].append(malware)
        print(colored('Malware Detected','red'),' :\n\tLocation : {}\n'.format(log_line[0]))

def MalwareDetectionThread(EC2FileTypeLogs):
    for ec2logs in EC2FileTypeLogs:
        t = threading.Thread(target=MalwareDetector, args=(ec2logs,))
        Threads.append(t)
        t.start()

def AnomalyDetectionThread(HTTPLogs):
    for httplog in HTTPLogs:
        t = threading.Thread(target=DecisionTree_AnomalyDetector, args=(httplog,))
        Threads.append(t)
        t.start()
        time.sleep(0.2)

def GuardDutyFindingsThread(findings):
    # Print out each finding
    for finding in findings['FindingIds']:
        find_detail = gd.get_findings(DetectorId=detectorid, FindingIds=[finding])
        GDFinding = {}
        GDFinding['Title'] = find_detail['Findings'][0]['Title']
        GDFinding['Description'] = find_detail['Findings'][0]['Description']
        GDFinding['Type'] = find_detail['Findings'][0]['Type']
        GDFinding['Severity'] = find_detail['Findings'][0]['Severity']
        alerts['GuardDuty'].append(GDFinding)

        print(colored('GuardDuty Finding', 'red'), " :\n\tTitle : {}\n\tDescription : {}\n\tType : {}\n\tSeverity : {}\n".format(colored(find_detail['Findings'][0]['Title'], 'yellow'), find_detail['Findings'][0]['Description'], find_detail['Findings'][0]['Type'], colored(find_detail['Findings'][0]['Severity'], 'red')))

HTTPLog_response = s3_client.get_object(Bucket=Bucket, Key=HTTPLogsFile)
HTTPLogs = HTTPLog_response['Body'].read()

EC2FileTypeLogs_response = s3_client.get_object(Bucket=Bucket, Key=EC2FileTypeLogsFile)
EC2FileTypeLogs = EC2FileTypeLogs_response['Body'].read()

HTTPLogs = HTTPLogs.decode('utf-8').splitlines()
EC2FileTypeLogs = EC2FileTypeLogs.decode('utf-8').splitlines()

Final_HTTPLogs = RemoveDuplicates(HTTPLogs)
Final_EC2FileTypeLogs = RemoveDuplicates(EC2FileTypeLogs)

# # HTTPLog Test start
# with open("testlog") as log:
#     httplog = log.read()
# DecisionTree_AnomalyDetector(httplog)

# # HTTPLog Test end
# for httplog in HTTPLogs:
#     DecisionTree_AnomalyDetector(httplog)

#MalwareDetectionThread(EC2FileTypeLogs)
#AnomalyDetectionThread(HTTPLogs)
#GuardDutyFindingsThread(findings)


MalwareThread = threading.Thread(target=MalwareDetectionThread, args=(Final_EC2FileTypeLogs,))
Threads.append(MalwareThread)
MalwareThread.start()

AnomalyThread = threading.Thread(target=AnomalyDetectionThread, args=(Final_HTTPLogs,))
Threads.append(AnomalyThread)
AnomalyThread.start()

GuardDutyThread = threading.Thread(target=GuardDutyFindingsThread, args=(findings,))
Threads.append(GuardDutyThread)
GuardDutyThread.start()

for thread in Threads:
    thread.join()

alerts_json = json.dumps(alerts, indent=4)
with open("alerts.json", "w") as outfile:
    outfile.write(alerts_json)
