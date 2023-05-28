class Logger:
    def __init__(self):
        self.logs = []
    
    def reset_logs(self):
        self.logs = []
    
    def add_log(self, log):
        self.logs.append(log)

    def format_rows_for_frame(self, frame):
        return [[frame, log] for log in self.logs]