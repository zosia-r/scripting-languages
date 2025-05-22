import datetime

def read_logs(file_path):
        file = open(file_path, 'r')
        logs = []
        for line in file.readlines():
            row = line.split()

            for item in reversed(row):
                if item.isdigit(): 
                    status_code = int(item)
                    break
            
            logs.append((
                datetime.datetime.fromtimestamp(float(row[0])), #ts 
                row[1], #uid
                row[2], #origin host
                int(row[3]), #origin port
                row[4], #destination host
                int(row[5]), #destination port
                row[7], #method
                row[8], #host domain
                row[9], #uri
                status_code, #status code
                line
                )
            )
        return logs

class Logs:
    def __init__(self, file_path):
        self.data = read_logs(file_path)
        pass
