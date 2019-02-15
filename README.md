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

Installing (JAVA VERSION) on Windows/Linux
------------------ 
To install the Java version of S.T.A.R. for Windows one only needs to download the .jar file from [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php) with the correct operating system.
That is if you are using a Windows machine you need to download the STAR_Windows.jar file.

Then once you have the program if JAVA is correctly configured on your machine you will need only double click the file to run the program.

To install the Java version of S.T.A.R. for Ubuntu one only need to download the .jar file from [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php) with the correct operating system.
That is if you are using a Linux machine (like Ubuntu) you need to download the STAR_linux.jar file.

Make sure that you have the latest version of Java by using the apt function in command line then navigate to the location of the file then use:
```
sudo java -jar STAR_linux.jar
```
Notice that we suggest you use root access to run this code as a few temporary .wav files are saved to computer and depending on your set-up it may require root permission. 




Installing (PYTHON VERSION) on Windows
------------------
S.T.A.R. is written using a few public libraries which do a lot of audio processing and in the advanced settings uses a CMU website to load a language model. To download all of these dependicies one only needs a passing familiarity with the use of command line (DOS). 




### Dependencies/Libraries

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [CMU PocketSphinx](https://github.com/cmusphinx/pocketsphinx-python)
- [pydub](https://pypi.org/project/pydub/)
- [ffmpeg](https://www.ffmpeg.org/)
- [mechanize](https://pypi.org/project/mechanize/)
- [easyGUI](https://pypi.org/project/easygui/)



Downloading Python 2.7
------------------
The primary language in which S.T.A.R. is written is Python. It was written using Python 2.7 and it is recommended that this version is the one used to run it. We recommend using the link: [Python 2.7](https://www.python.org/download/releases/2.7/) and downloading the package from one of the links on the official page. You can install this program anywhere on your computer, yet for the further steps please make note of where you saved this package. (For example it could be saved in C:\Program Files\Python27\)


Using FFmpeg
------------------
S.T.A.R. uses FFmpeg to convert different types of files (from .mp3 to .flv) into a file type that CMU pocketsphinx can use. Unfortunately windows is not designed to use this program very easily. The user must first download FFmpeg [here](https://www.ffmpeg.org/) then create a path variable named path with the location of the .exe file, so that python knows where to look for it. 


Using PIP
------------------
To use the further dependencies we suggest using [pip](https://pypi.python.org/pypi/pip/)


S.T.A.R. Windows
------------------
Once all of the dependicies are downloaded all you need to do is download the folder from this repository and put it any anywhere on your computer. From the folder you now only need to double click the file STAR.pyw


Installing (PYTHON VERSION) for Linux
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
notice we suggest you run the program with root permission as S.T.A.R. needs to make quite a few temporary files and depending on your settings it might require require root permission.



# Using the Program

A manual for the use of the program may be found [here](https://www.sc.edu/about/offices_and_divisions/cte/about/news/2018/gta_teaching_resource_grant_2018.php)

