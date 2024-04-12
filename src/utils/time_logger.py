import time


class Time_logger:
    _instance = None
    _events_start_timestamps = {}
    _events_time = {}

    def __new__(cls):
        '''
        Constructor to ensure that only one instance of this class can be created.
        '''
        if not cls._instance:
            cls._instance = super(Time_logger, cls).__new__(cls)
        return cls._instance

    def start_timer_for_event(self, event_name: str) -> None:
        '''
        Start the timer for a given event.

        Arguments:
            `event_name`: name of event to start timer for.
        '''
        start = time.monotonic()
        self._events_start_timestamps[event_name] = start

    def mark_timestamp_for_event(self, event_name: str, stack_time: bool = False) -> None:
        '''
        Mark the timestamp for a given event.

        Arguments:
            `event_name`: name of event to calculate duration of.
            `stack_time`: should current duration be added to previous (default: True).
        '''
        end = time.monotonic()
        try:
            start = self._events_start_timestamps.pop(event_name)
        except KeyError:
            start = end
        duration = end - start
        if stack_time and event_name in self._events_time:
            duration += self._events_time[event_name]
        self._events_time[event_name] = duration

    def print_events(self) -> None:
        '''
        Print the recorded events and their durations.
        '''
        print('Time logger:')
        for key, value in self._events_time.items():
            print(f'{key}: {value * 1000:.0f} ms')

    def get_event_duration(self, event_name: str, time_type: str = 'ms') -> int:
        '''
        Get the recorded event duration.

        Arguments:
            `event_name`: name of event to get duration of.
            `time_type`: convert time type to (default: 'ms').
        '''
        duration = 0
        try:
            duration = int(self._events_time[event_name])
        except KeyError:
            print(
                f'Time_logger.get_event_duration: there\'s no key - {event_name}')
        if time_type == 'ms':
            duration *= 1000
        elif time_type == 'm':
            duration /= 60
        elif time_type == 'h':
            duration /= 60 * 60
        return duration


'''
Example usage:

# through Utils_Manager aka CEO
from utils.utils_manager import Utils_Manager
ceo = Utils_Manager()
ceo.time_logger

ceo.time_logger.start_timer_for_event('event_1')
# some stuff to log time for
ceo.time_logger.mark_timestamp_for_event('event_1')
...
ceo.time_logger.start_timer_for_event('event_1')
# add more time to `event_1`
ceo.time_logger.mark_timestamp_for_event('event_1', True)
...
ceo.time_logger.print_events()
...
ceo.time_logger.start_timer_for_event('event_1')
# replace duration of `event_1`
ceo.time_logger.mark_timestamp_for_event('event_1')
...
ceo.time_logger.print_events()
'''
