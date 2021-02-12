#!/usr/bin/env python

import uuid
import os

from zulipbot import ZulipBot

if __name__ == '__main__':    
    # Activate Zulip client
    bot = ZulipBot()
    bot.client.call_on_each_message(bot.process)    