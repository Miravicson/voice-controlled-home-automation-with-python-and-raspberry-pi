This is the new read me


## summary of all the files in the project

Procedure for accessing the raspberry pi

1) Ensure the raspberry pi is connected to a local network.

2) Connect your laptop to the same network so that your raspberry pi and your laptop are on the same network.
    it is recommended that you use a linux laptop.
3) You should determine the ip address of the raspberry pi by checking your router. Another alternative is to install
    arp-scan on your linux system. (google arp-scan and follow the installation instructions).
4) open your linux terminal and run [$ sudo arp-scan --interface=wlo1 --localnet ]. This command list the corresponding
    IP address matched with the mac address of all devices connected to the network.
    The IP address of your raspberry pi is liable to change, but the mac address is constant. you can Identify the rasp-
    berry pi's IP address by looking for it's mac address and noting the IP address that corresponds with the mac add-
    ress.

    The raspberry pi's mac address is: 40:a5:ef:01:36:c2

5) when you have identified the raspberry pi's IP address, open a terminal and ssh into the raspberry pi using the comm-
    and below:
            [$ ssh pi@<IP address found> ]
            example: let the IP address be: 192.168.43.215
            run
            [$ ssh pi@192.168.43.215]

            it will request for a pass word

6) Enter the raspberry pi's password.

    The raspberry pi's password is: raspberrypi


7) once you are logged in, you will be in the raspberry pi's home directory.


8) All files pertaining to Annah is stored in the directory: /home/pi/Desktop/home_ai_annah or for short ~Desktop/home_ai_annah.
    NB. the "~" represents the path '/home/pi'
9) Go to the folder by running the following command:

    a) From the home directory run [$ cd Desktop/home_ai_annah]
    b) From anywhere in pi run [$ cd /home/pi/Desktop/home_ai_annah]


10) The entry point for the program is the 'controller.py' file. NB Annah runs on python3

    to manually start the program, run the following command:
        [$ python3 controller.py]


11) The raspberry pi has been set to run the programm automatically by running the command
        $ python3 controller.py $
    at boot up.

    To view the list of similar schedule command you have to access the crontab.

12) The crontab is the interface for scheduling commands on linux operating system.

13) The raspberry pi runs linxu Debian operating system.

14) To edit the crontab, run the following command at the terminal:
    [$ crontab -e]

    This brings up the terminal editor, nano, you can then scroll and edit the crontab commands or comment them out using "#" at the beginning of the command.
    when you are done editing hit
    [Ctrl + O] to write out (save) the commands.
    then
    [Ctrl + X] to quit the nano editor.
    your new commands will be installed in the raspberry pi.

15) Remember, should you, at any time, want to debug the raspberry pi and change some codes, it is Ideal to disable automatic running of the entry script -- "controller.py"
    you disable this by editing the crontab (run crontab -e to edit) and commenting out the line at the bottom:

    >>>@reboot /usr/local/bin/python3 /home/pi/Desktop/home_ai_annah/controller.py >/home/pi/Desktop/logs/cronlog 2>&1

16) You comment out the line by adding "#" in front of the crontab command so that the command above changes to:
    #@reboot /usr/local/bin/python3 /home/pi/Desktop/home_ai_annah/controller.py >/home/pi/Desktop/logs/cronlog 2>&1


17) Save your crontab as usual (Ctrl + O) to write out (Ctrl + X) to quit the editor.

18) Reboot the raspberry pi by running:
    [$ sudo reboot]

19) When the raspberry pi has boot up, it would no longer run the script automatically.


20) Connect to the raspberry pi by following the steps 1) to 6).

21) Remember to activate automatic running of the "controller.py" file when you are done debugging. You do this by editing the crontab and uncommenting the line that has :

#@reboot /usr/local/bin/python3 /home/pi/Desktop/home_ai_annah/controller.py >/home/pi/Desktop/logs/cronlog 2>&1

so that the line becomes:

@reboot /usr/local/bin/python3 /home/pi/Desktop/home_ai_annah/controller.py >/home/pi/Desktop/logs/cronlog 2>&1


22) Once you are in project root folder (/home/pi/Desktop/home_ai_annah) you will notice some folders and files.

 list of folders and files

    /home_ai_annah -----/
                        /accessories
                        /audio_commands
                        /music
                        -about_annah.txt
                        -audio_recognize.py
                        -controller.py
                        -effector.py
                        -food_timetable.json
                        -models.py
                        -README.md
                        -refresh_weather_data_3_days.sh
                        -text_recognize.py
                        -weather_data.json

    the accessories folder:
    /home_ai_annah/accessories


    ## WORTHY OF NOTE IS THIS FOLDER.
    /usr/local/lib/python3.5/site-packages/speech_recognition/
    This folder contains the speech_recognition library main file ('__init__.py')
    '__init__.py' file is contained in the accessories folder but must be copied to the directory above. to overwrite
    the '__init__.py' existing in the directory above.





    ## Dependencies

    1) Python 3.5.3
    2) Pip3
    3) PyAudio
    4) Flacencoder
    5) IBM watson_developer_cloud
    6) Python speech_recognition library
    7) IBM watson Speech_To_Text service
    8) IBM watson Text_To_Speech service
    9) IBM watson weather service




    ### To view the report of the crontab i.e cronlog at any time.
    1) connect to the raspberry pi and run:
        [$ cat /var/mail/pi ]

    2) you will see the result of the cronlog displayed in the terminal.