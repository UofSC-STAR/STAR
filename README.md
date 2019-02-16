# S.T.A.R. (Speech-to-Text Analytic Resource)

S.T.A.R. is a user friendly interface which allows an Instructor to retrieve analytics from recorded lectures. 

The current analytics that are calculated by S.T.A.R. are:

- Average Wait Time

- Average time given for Clarification Pauses

The two main objectives of S.T.A.R. is:

- Give the less computer savy users an easy downloadable file with an intuitive user interface...

- Give the inquistive programmer the ablilty to replace the CMU Sphinx API with any of their choosing (instructions for this adaptation is given later)

With these goals in mind we have created two versions of the S.T.A.R. program:

- S.T.A.R. JAVA

- S.T.A.R. Python

The Python version is written using a few public  of libraries which makes it's installation more taxing on the educator that is less familiar with programing, while the version written with Java has only the dependicy of java and as such can be used across platforms with no programming understanding, yet this makes the program a lot less versitile with a lot less features.

## Getting Started

These instructions will help you get a version of S.T.A.R. up and running on your local machine for basic use, development or testing purposes. 

Supported Platforms
-------------------

- Windows 7
- Windows 8
- Windows 10
- Ubuntu 14.10

Installing (JAVA VERSION) on Windows/Ubuntu
------------------

### Windows
To install the Java version of S.T.A.R. for Windows one only needs to download the .jar file from [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php) with the correct operating system.
That is if you are using a Windows machine you need to download the STAR_Windows.jar file.

To Run STAR on Windows you will need atleast Java 11 which you can download [here](https://www.oracle.com/technetwork/java/javase/downloads/jdk11-downloads-5066655.html).

Then once you have the program if JAVA is correctly configured on your machine you will need only double click the file to run the program.

### Ubuntu
To install the Java version of S.T.A.R. for a Linux based machine (such as Ubuntu) one only need to download the .jar file from [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php) with the correct operating system.
That is if you are using a Linux machine (like Ubuntu) you need to download the STAR_linux.jar file.


Make sure that you have the latest version of Java by typing in 
```
sudo apt install default-jre
```

Then you only need to navigate to the location of the file then use:
```
sudo java -jar STAR_linux.jar
```
Notice that we suggest you use root access to run this code as a few temporary .wav files are saved to the computer and depending on your set-up it may require root permission. 




Installing (PYTHON VERSION) on Windows
------------------
S.T.A.R. is written using a few public libraries which do a lot of audio processing and in the advanced settings uses a CMU website to load a language model. To download all of these dependicies one only needs a passing familiarity with the use of command line (DOS). For example in Windows 10 to access the command line you just need to hit the "star button" looks like the windows logo (or hit the windows button on your keyboard) then start typing command line the option to select command line will pop up before you are finished typing it.




### Dependencies/Libraries

- [Python 2.7.15](https://www.python.org/downloads/release/python-2715/)
- [CMU PocketSphinx](https://github.com/cmusphinx/pocketsphinx-python)
- [pydub](https://pypi.org/project/pydub/)
- [ffmpeg](https://www.ffmpeg.org/)
- [mechanize](https://pypi.org/project/mechanize/)
- [easyGUI](https://pypi.org/project/easygui/)



Downloading Python 2.7.15
------------------
The primary language in which S.T.A.R. is written is Python. It was written using Python 2.7.15 and it is recommended that this version is the one used to run it. We recommend using the link: [Python 2.7.15](https://www.python.org/downloads/release/python-2715/) and downloading the package from one of the links on the official page. You can install this program anywhere on your computer, yet for the further steps please make note of where you saved this package. (For example it is saved by default in C:\Program Files\Python27\). Now to make the next steps easier we will set a path variable (pay attention to this step as you will have to do it below for other dependicies).

- Step 1:

Clicking the windows logo (i.e. the start button or just hitting the windows button on your keyboard) then start typing enviroment variables the option will appearr before you are finished typing 

![](/screen%20shots/fixed/prechangingvariable.png?raw=true "set variable screen")

then you click the button near the bottom on the right which says "enviroment variables"

- Step 2:

After clicking the button above in the new window you should click the button near the bottom that says "new..." then in the window that pops up for the varible name: PYTHON_HOME and for the path type in C:\program files\python27 shown in the picture below: (if you are unsure about the location of python.exe you can click the browse button to look for it!)

![](/screen%20shots/fixed/changingvariable.png?raw=true "set variable")

then click ok. 

- Step 3:

Now in the systems variables there will be a variable named "Path" click this variable then click the button that says edit. Then in the new window that pops up click the button new and add %PYTHON_HOME% then click new again and add %PTYHON_HOME%\Scripts\. When you are done it should look like:


![](/screen%20shots/fixed/updatingpathvar.png?raw=true "updating PATH variable")

Installing CMU Pocketsphinx
------------------
Pocketsphinx is a speech recognition program developed by Carnegie Mellon University. They also made it easy to use with python [here](https://github.com/cmusphinx/pocketsphinx-python) to help you install this on your computer we will go through all of the step to install CMU Pocketsphinx now. 

The dependicies for CMU Pocketsphinx are:
- [Swig](http://www.swig.org/download.html)
- [Microsoft Visual C++ Compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

### Swig
To download Swig just follow the link above and download the version for windows this will download a .zip file then you can extract this file anywhere. Now just as for Python above you need to add to your PATH variable the location of this folder!

### Microsoft Visual C++ Compiler for Python 2.7
Again follow the link above then download the installer then run the installer and follow the steps in the installer.

### Pocketsphinx
Now after you have followed all of the steps above you can open command line and type in 
```
pip install pocketsphinx
```

Now you have CMU Pocketsphinx!


Installing FFmpeg
------------------
S.T.A.R. uses FFmpeg to convert different types of files (from .mp3 to .flv) into a file type that CMU pocketsphinx can use. Unfortunately windows is not designed to use this program very easily. The user must first download FFmpeg [here](https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20190215-9e1e521-win64-static.zip) clicking this link should download a .zip file, you should next unpack this .zip file somewhere on your computer. By default the folders created by unpacking are named "ffmpeg-2019-9e19521-win64-static" and then another folder with the same LONG name. We suggest you rename those folders something simplier like just "ffmpeg" then create a path variable named path with the location of the .exe file, (i.e. first create a new path variable named path and location "\your path\ffmpeg\ffmpeg\bin" and then adding it to the variable "PATH" like you did above for Python) so that python knows where to look for it. 

by "\your path\" I mean where you unpacked the ffmpeg folder!


The Final Libraries 
------------------
Now if you have followed all of the steps above to install the reamaing libraries you just need to open a NEW command line and type in:

```
pip install pydub
pip install mechanize
pip install easygui
```

Now you are ready to run the program!


Running S.T.A.R. Windows
------------------
Once all of the dependicies are downloaded all you need to do is click the "clone or download" button in this repository then click download .zip, once you have downloaded the .zip file you can put it any anywhere on your computer. A folder named STAR-master will be unpacked and in this folder there are two folders for the two oporating system one is named STAR-PYTHON-Windows, in this folder to run the program you now only need to double click the file STAR.pyw


Installing (PYTHON VERSION) for Ubuntu
------------------
The Linux version of S.T.A.R. with Python has the same dependicies as the windows version (except of course less dependicies for CMU Pocketsphinx), they are again

### Dependencies/Libraries

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [CMU PocketSphinx](https://github.com/cmusphinx/pocketsphinx-python)
- [pydub](https://pypi.org/project/pydub/)
- [ffmpeg](https://www.ffmpeg.org/)
- [mechanize](https://pypi.org/project/mechanize/)
- [easyGUI](https://pypi.org/project/easygui/)


The installation here is quite easier once you download the correct folder from this repository you will only need to type:
```
sudo apt-get install -y python python-dev python-pip build-essential swig git libpulse-dev
sudo pip install pocketsphinx
sudo pip install pydub
sudo apt-get install ffmpeg
sudo pip install mechanize
sudo pip install easygui
```

or

```
sudo apt-get install -y python python-dev python-pip build-essential swig git
git clone --recursive https://github.com/cmusphinx/pocketsphinx-python/
cd pocketsphinx-python
sudo python setup.py install
sudo pip install pydub
sudo apt-get install ffmpeg
sudo pip install mechanize
sudo pip install easygui
```

Once this has gone through with no errors you can run the file from command line by navigating to the location which you downloaded the linux folder from this repository and then typing
```
sudo python STAR.pyw
```
notice we suggest you run the program with root permission as S.T.A.R. needs to make quite a few temporary files and depending on your settings it might require root permission.



# Using the Program

A manual for the use of the program may be found [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php)

