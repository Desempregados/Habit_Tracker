class TimerLogic:
    def __init__(self):
        self.remaining_time_seconds = 0
        self.timer_running = False

    def start(self, total_seconds):
        if total_seconds > 0:
            self.remaining_time_seconds = total_seconds
            self.timer_running = True
            return True
        return False

    def pause(self):
        self.timer_running = False

    def resume(self):
        if self.remaining_time_seconds > 0:
            self.timer_running = True

    def reset(self):
        self.remaining_time_seconds = 0
        self.timer_running = False

    def tick(self):
        if self.timer_running and self.remaining_time_seconds > 0:
            self.remaining_time_seconds -= 1
            if self.remaining_time_seconds == 0:
                self.timer_running = False
                return True  # Timer finished
        return False