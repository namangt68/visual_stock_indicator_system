###Visual Stock Indicator System (VSIS) <img src="/frontend/finallogo.png" align="left" height="90" width="120" >


A  SMS/Internet based medical stock indicator system. 

This system is part of Interactive Socio-Technical Practicum (ISTP) Project 2016 by Team Healthcare at IIT Mandi.

####Installation
#####Beaglebone ([See blog post](http://namangt68.github.io/beaglebone/2016/05/08/beaglebone-windows-10-install.html))
`It is recommended to download updated driver to run beaglebone to avoid driver installation errors.`

**For Windows 64 bit**: Download driver from [here](https://github.com/jadonk/beaglebone-getting-started/raw/master/Drivers/Windows/BONE_D64.exe).

**For Windows 32 bit**: Download driver from [here](https://github.com/jadonk/beaglebone-getting-started/raw/master/Drivers/Windows/BONE_DRV.exe).

Right click on downloaded file and click `Run as administrator`.

Follow steps and check if all three drivers are installed completely.

Add and exception to proxy settings(if you use proxy) from `Change proxy settings` and add **192.168.7.2** in exception box and click save.

Connect the Beaglebone using usb cable.

Now open your browser(Chrome/firefox) and go to address [http://192.168.7.2](http://192.168.7.2) and you will be shown 'beaglebone getting started guide'. 

Go to [http://192.168.7.2:3000](http://192.168.7.2:3000) to open Cloud9 IDE.

####Architecture  <img src="/images/working.jpg" align="right" alt="working" height="300">
#####Indicator box
- Beaglebone
- GSM Module
- RGB LEDS
- Sim card
- Breadboard
- Jumper wires


<br />
#####Led indicators
In the initial prototype, green is a<img src="/images/led.jpg" align="right"  alt="led" width="300" height="270">
normal indication. Red indicates an
unanswered stock shortage and
request, and yellow indicates that the
order is available at the CHC. When the
status of a sub-center is changed to
yellow, an automated SMS will be sent
to update the sub-center worker.

The pattern in which the Health workers will send SMS for stock indication:
Kamand ID: 0
- #kam0	-	Stock problem exists in Kamand
- #kam1	- 	Stock OK in Kamand

####Working system

#####SMS
<img src="/images/sms.png" alt="sms" height="300">
<br>

#####Frontend
<img src="/images/frontend.png" alt="frontend">

#####App Features 

- Instant Stock Status reporting.<img src="/images/app_net.png" align="right" alt="app" height="300">
<img src="/images/app_upload.png" align="right" alt="app" height="300">
<img src="/images/app_sms.png" align="right" alt="app" height="300">
- Quick feedback on SMSs.
- Data synchronized on cloud.
- Easy to use Data frontend.
- Android app with both quick SMS or net upload.









