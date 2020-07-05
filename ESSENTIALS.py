

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