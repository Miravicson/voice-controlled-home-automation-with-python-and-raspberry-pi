#!/usr/bin/env bash
# this script fetches the weather data from when it was executed and down to the next three days.
# the weather data uses IBM watson API and the username and password of the api credentials.
# the username and password is embedded in the url as the key value pair separated by ":".
# b5af278e-0742-4d03-ac42-1ca5f4245a00:Z6qRZXoTnM older password
# 24a67069-f350-46b0-9919-0c5ffc68731d:L8yT3d8XJT old password
# 3b585df4-c546-4ece-961b-0c8c2f9bf906:LavTWIb3RO new password
curl -o /home/pi/Desktop/home_ai_annah/weather_data.json -k https://3b585df4-c546-4ece-961b-0c8c2f9bf906:LavTWIb3RO@twcservice.eu-gb.mybluemix.net:443/api/weather/v1/geocode/6.46/3.40/forecast/daily/3day.json
