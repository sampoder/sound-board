import time
import rtmidi
import random
from nfc import NFC_Reader

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# these are the different IDs
# of "moods" and sound effects

moods = {
  "tabla": 1,
  "chill": 2,
  "alien": 3,
  "haunted": 4
}

soundEffects = {
  "robot": 1,
  "vinyl": 2,
  "cymbal": 3,
  "can": 4,
  "cash": 5,
  "crow": 6,
  "zap": 7,
  "triangle": 8
}

# this dictionary maps a 
# tag's UUID to a specific
# action

nfcTags = {
  "04 EB A5 37 90 00": {
    "type": "mood",
    "target": "alien"
  },
  "04 F4 21 63 90 00": {
    "type": "mood",
    "target": "tabla"
  },
  "04 A4 4B 70 90 00": {
    "type": "mood",
    "target": "chill"
  },
  "04 7D E7 3A 90 00": {
    "type": "mood",
    "target": "haunted"
  },
  "04 FB EC 37 90 00": {
    "type": "sfx",
    "target": "robot"
  }, 
  "04 5A 80 46 90 00": {
    "type": "sfx",
    "target": "vinyl"
  },
  "04 BB 11 37 90 00": {
    "type": "sfx",
    "target": "cymbal"
  },
  "04 E7 DA 66 90 00": {
    "type": "sfx",
    "target": "can"
  },
  "04 C4 22 04 90 00": {
    "type": "sfx",
    "target": "cash"
  },
  "04 09 D3 6A 90 00": {
    "type": "sfx",
    "target": "crow"
  },
  "04 E6 0F 69 90 00": {
    "type": "sfx",
    "target": "zap"
  },
  "04 BD 26 37 90 00": {
    "type": "sfx",
    "target": "triangle"
  },
  "04 9A EB 5F 90 00": {
    "type": "rate_command",
    "change": -0.2
  },
  "04 A3 2F 69 90 00": {
    "type": "rate_command",
    "change": 0.2
  },
  "04 51 5F 6B 90 00": {
    "type": "random"
  }
}

import asyncio

currentMode = moods["tabla"]
mostRecentSoundEffect = soundEffects["robot"]
rate = 1
sfx = 0

# we use a virtual midi device to
# communicate with sonic pi

if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("sound_board")

with midiout:
    # async function to allow for timeouts
    async def func():
        global sfx
        global mostRecentSoundEffect
        global currentMode
        global rate
        randomModifier = 0
        try:
          reader = NFC_Reader()
          if reader.hcard != 0:
            uid = reader.read_uid()
            # process the tag baserd on it's UID
            if uid in nfcTags:
              if nfcTags[uid]["type"] == "sfx":
                sfx = soundEffects[nfcTags[uid]["target"]]
              elif nfcTags[uid]["type"] == "mood":
                currentMode = moods[nfcTags[uid]["target"]]
              elif nfcTags[uid]["type"] == "rate_command":
                rate = min(1.6, max(0.4, rate + nfcTags[uid]["change"]))
              elif nfcTags[uid]["type"] == "random":
                randomModifier = 100
            else:
              print(uid)
          else:
            time.sleep(1)
        except KeyboardInterrupt:
          exit()
        except:
          print("error")
        if sfx == mostRecentSoundEffect:
          sfx = 0 + randomModifier
        else:
          mostRecentSoundEffect = sfx
        # send message through MIDI - we're limited in size
        # so we use modular arithmetic to encode both the mode
        # and the desired rate
        midiout.send_message([0x90, currentMode + 50 * rate, sfx + randomModifier])
        print([0x90, currentMode + 50 * rate, sfx + randomModifier])

    async def main():
        try:
          while True:
            result = await asyncio.wait_for(func(), timeout=2.0)
        except asyncio.TimeoutError:
            print('timeout!')
    
    
    asyncio.run(main())

del midiout
