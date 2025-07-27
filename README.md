# meditation-timelapse

- Accountability for meditation!
- I want to create an accountability mechanism to help me do longer sits
- "I'm going to do a 1 hour sit, and if I don't, I'll pay you guys £10 each" - something like that!

## Features
- "every-5-mins.py" → takes a photo from my webcam every 5 mins, saves the jpgs to a folder
- "gif-maker.py" → looks for jpg files in whatever folder the python script sits in, and combines them into a gif
- "test.py" → takes a photo a second for 10 seconds and saves them to a folder → to make sure that everything's working
- Timestamps are displayed on the images for proof of sit duration

## Workflow
- Run every-5-mins.py
- Meditate!
- End of meditation → stop the python file, run the gif maker, send the gif to my friends
