def readSpeechKey():
    with open('D:\TurnTheBus\TurnTheBusSpeech\AzureSpeechTranslation\Python\key.txt', 'r') as f:
        print('Reading key from config')
        key = f.readline().rstrip()
        print(f'Read key {key} from config')
        return key

def getServiceRegion():
    return "eastus"

def WriteToFile(results, fileName):
    with open(fileName, "wb") as f:
        for s in results:
            s += "\n"
            f.write(s.encode("UTF-8"))