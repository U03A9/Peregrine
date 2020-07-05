import discord
import re
import subprocess
import sys
import time
import json
import sys
from io import StringIO

def convert_Output(rawOutput):
    readOutput = rawOutput.read()
    decoded = readOutput.decode()
    return decoded

def convert_JSON(formattedOutput):
     jsonOutput = json.loads(formattedOutput)
     return jsonOutput

def format_Output(rawOutput):
    formattedOutput = convert_Output(rawOutput)

    return formattedOutput

def scan_URL(url):
    command = 'python3 ./VxAPI/vxapi.py scan_url_for_analysis {} all'.format(url)
    rawOutput = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    print("Scanning URL...")
    time.sleep(1)

    return rawOutput

def check_Status(jsonSHA):
    command = 'python3 ./VxAPI/vxapi.py report_get_summary {}'.format(jsonSHA)
    rawOutput = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    print("Checking scan status...")
    time.sleep(1)
    return rawOutput

def check_Overview(jsonSHA):
    command = 'python3 ./VxAPI/vxapi.py overview_get {}'.format(jsonSHA)
    rawOutput = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    print("Retreiving overview variables...")
    time.sleep(1)
    return rawOutput

def check_State(jsonSHA):
    command = 'python3 ./VxAPI/vxapi.py report_get_state {}'.format(jsonSHA)
    rawOutput = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    formattedOutput = format_Output(rawOutput)
    print("Checking state...")
    time.sleep(1)
    return formattedOutput

async def submit_URL(url, message):
    with open('resources/analysis_Message.txt', 'r') as analysis_Message:
            scanMessage = analysis_Message.read()

    decoded = scan_URL(url)

    formattedUrl = format_Output(decoded)
    jsonUrl = convert_JSON(formattedUrl)

    jsonID = jsonUrl['id']
    jsonSHA = jsonUrl['sha256']

    print("The jsonID is: ",jsonID)
    print("The jsonSHA is: ",jsonSHA)

    checkSummary = check_Status(jsonSHA)
    formattedSummary = format_Output(checkSummary)
    jsonSummary = convert_JSON(formattedSummary)

    jsonTime = jsonSummary['analysis_start_time']
    jsonAV = jsonSummary['av_detect']
    jsonState = jsonSummary['state']

    checkOverview = check_Overview(jsonSHA)
    formattedOverview = format_Output(checkOverview)
    jsonOverview = convert_JSON(formattedOverview)

    jsonArchitecture = jsonOverview['architecture']
    jsonThreatScore = jsonOverview['threat_score']
    jsonVerdict = jsonOverview['verdict']

    print("Compiling data...")

    if jsonState != "SUCCESS":
        formattedSummary = check_State(jsonSHA)
        checkState = convert_JSON(formattedSummary)
        jsonState = checkState['state']
        print("Report is ready! State is: ", jsonState)

    print("Time is:", jsonTime)
    print("AV Detections:", jsonAV)
    print("Verdict:", jsonVerdict)

    ANALYSIS_MESSAGE = str(scanMessage).format(jsonArchitecture, url, jsonTime, jsonAV, jsonVerdict,  jsonThreatScore)

    return ANALYSIS_MESSAGE
