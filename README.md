# vpt

### Setup

Inspired by *https://github.com/minerllabs/minerl*

```
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get update
sudo apt-get install openjdk-8-jdk
```
Check to make sure Java 8 + JDK 8 is installed -> `java -version` and `javac -version`


To avoid complexities of python version management, we use a virtual environment to isolate the project dependencies like minerl, numpy, etc. If `python --version` or `python3 --version` doesn't work, use pyenv instead as it handles all the python version details for you. Any changes you need to make to pyenv and python version can be handled with extremely simple commands.

Running the commands below will setup the project, virtual environment and install the necessary dependencies. The `minerl` installation is known to take a while so don't worry if it seems like it's stuck (grab some tea or coffee and it should be ready when you come back).
```
git clone https://github.com/Infatoshi/vpt
cd vpt
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/minerllabs/minerl
pip install -r requirements.txt
python main.py
```

After running `python main.py`, a window should pop up with the Minecraft environment. You can navigate the world with your keyboard and mouse. To exit, just press `q`. After you quit, it will replay the greyscale frames that were recorded during the episode. Press `q` again to quit the replay. 


### Get in touch
But Elliot, do you provide 1-on-1 tutoring/consulting for similar projects?

Absolutely! Feel free to shoot me an email at *elliot@arledge.net* and we can setup a quick call to discuss your project and how I can help you achieve your goals.

### Links

Join my Discord server - https://discord.gg/pSsQ2cCzVC

Twitter/X - https://twitter.com/elliotarledge

LinkedIn - https://www.linkedin.com/in/elliot-arledge-a392b7243/

YouTube - https://www.youtube.com/channel/UCjlt_l6MIdxi4KoxuMjhYxg

My Website - http://elliotarledge.com
