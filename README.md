# 🎛️ Sound board

TLDR: an amiibo-style system where viewers use pucks (NFC tags) to change the music and play sounds. I built this for [DESINV 23](https://classes.berkeley.edu/content/2025-spring-desinv-23-1-lec-1), a class on creative programming & electronics at UC Berkeley.

## Showcase / description of finished piece

Everyone has their own set of sounds that they enjoy. I wanted to design something that'd let people contribute their own sounds to the piece. I designed a system where people could bring a puck and place it on an NFC reader. The sound that was being outputted by my Sonic Pi script would then change.

<img src="https://github.com/user-attachments/assets/1d116a6c-9e63-49bd-8355-21b45b2759ad" width="400px" />
<img src="https://github.com/user-attachments/assets/9c77c297-c110-44fd-a6d0-d39076228350" width="400px" />

The pucks I designed were linked to a wide range of sounds, four different "moods", eight different "effects", and three commands. The commands were: speed up, slow down, and a random effect (eg. reverb). Each of them was a laser cut wooden circle with an NFC tag stuck on it. Check out the video for an example:

https://github.com/user-attachments/assets/cbffed20-b3e5-4ad9-a767-9763255367d5

## The process

Building this started as a wide range of ideas: a "sound vending machine", a phone number everyone could call and be put on hold together, and attaching NFC tags to everyday items (eg. soda cans) that would allow you to consume them with sound (the sound of cracking open a soda can).

<img src="https://github.com/user-attachments/assets/823732ab-2e53-4e2b-bc3d-d4a3a5f3c1a5" width="400px" />

Here's a sketch of the early vending machine idea. I was really excited about the phone number idea, everyone was going to call the number and put it on speaker phone, then it would be mock surround sound. And the words in sentences like "your call is important to us - please hold the line" would be played on different phones. The intention was for it to be trippy. Unfortunately Twilio's MediaStreams don't support two way communication with DTMF. And there's no cell signal in our classroom. So that kind of killed that idea.

Once I'd committed to the final idea, I started by programming the music. I used a tool named Sonic Pi which is mainly used for live coding music:

<img src="https://github.com/user-attachments/assets/2ccfbb2b-6a9c-4651-a147-7e3e9a14a88f" width="400px" />

That's some what similar to what I'm doing? I set my program up to essentially be a case/switch statement with different numbers for different sounds. The sounds were mostly just the included samples in Sonic Pi. 

Now for the tricky part! Getting input into Sonic Pi. I couldn't find a way to directly hook up my NFC reader directly to Sonic Pi because it's running in a sandbox and also because it's Ruby (very few people build libraries for interacting with hardware in Ruby). So here comes the Python middleman!

The only input method I could find for Sonic Pi was MIDI (or the internet, but that'd be too slow). So my Python script was going to act as a virtual MIDI device.. using something called [RtMidi](https://github.com/thestk/rtmidi) (and [its Python wrapper](https://pypi.org/project/python-rtmidi/)).

It was finicky but it worked... and then, I set up my NFC reader. Which honestly, was a similar story. The first library I used was too buggy but then I found this [sample code](https://github.com/SaundersB/nfc-reader) that worked with my reader. It was finicky but it worked.

And then I merged the two scripts, and it worked!

## Reflection

I'm really happy with this project! It was super fun to demo in class and everyone was willing to participate which was great. I'm starting to see that I really enjoy building pieces that encourage people to collaborate and work together to make the piece their own. I find it really fulfilling to present pieces like that and see how people engage with them.

There are still a couple of things I'd like to improve, namely:

* Reducing the lag between placing a puck and the sound playing, I think the way to do this would be interupts however that wouldn't be supported by Sonic Pi's system that queues sounds.
* Creating a system for others to bring their own sounds: it'd be nice for others to be able to program their own pucks with a sound and then play that sound. I'm not quite sure how I would do this but we can encode data on the NFC tags.
* Making the pucks 3D would be another thing I'd like to do - just like the Nintendo amiibos! I could 3D print these things.

At the end of the day I'm pretty happy with this project! I'm going to keep the NFC reader and tags for future projects, I think they'll come in handy.

## Sources

Thanks to these sources for helping me:

* https://pypi.org/project/python-rtmidi/
* https://sonic-pi.net/
