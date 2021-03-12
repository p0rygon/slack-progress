import time

import os
import slack_sdk
from slack_sdk.errors import SlackApiError


class SlackProgress(object):
    def __init__(self, token, channel, suffix='%'):
        self.suffix = suffix
        self.channel = channel
        self.slack = slack_sdk.WebClient(token)

    def new(self, title=None, total=100):
        """
        Instantiate and return a new ProgressBar object
        params:
         - total(int): total number of items
        """
        bar = ProgressBar(self, title, total)
        res = self.slack.chat_postMessage(channel=self.channel, text=f"{title}\n{self._makebar(bar)}")
        bar.msg_ts = res['ts']
        bar.channel_id = res['channel']
        return bar

    def iter(self, iterable):
        """
        Wraps an iterable object, automatically creating
        and updating a progress bar
        """
        bar = self.new(total=len(iterable)-1)
        for idx, item in enumerate(iterable):
            yield(item)
            bar.done = idx

    def update(self, bar, msg_log=None):
        self.slack.chat_update(channel=bar.channel_id, ts=bar.msg_ts, text=f"{bar.title}\n{self._makebar(bar)}")
        if msg_log is not None:
            self.slack.chat_postMessage(channel=bar.channel_id, thread_ts=bar.msg_ts, text=msg_log)

    def _makebar(self, bar):
        black = ":black_large_square:"
        white = ":white_large_square:"
        p = int(bar.pos / bar.total * 10)
        bar_str = p * black + (10 - p) * white
        return '{} | ({}/{}) {}{}'.format(bar_str, bar.pos, bar.total, round(bar.pos / bar.total * 100, 1), self.suffix)


class ProgressBar(object):

    msg_ts = None
    channel_id = None

    def __init__(self, sp, title, total):
        self._sp = sp
        self._pos = 0
        self._done = 0
        self.title = title
        self.total = total

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, val):
        self._done = val
        self.pos = round((val/self.total) * 100)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, val):
        if val != self._pos:
            self._pos = val
            self._update()

    def log(self, msg):
        timestamp = time.strftime('%X')  # returns HH:MM:SS time
        msg_log = "*{}* - {}".format(timestamp, msg)
        self._update(msg_log)

    def _update(self, msg_log=None):
        self._sp.update(self, msg_log)
