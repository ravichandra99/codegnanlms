import requests,json
import time

def ytapi(video_id):
      API_KEY = 'AIzaSyDKfK521g2LPICYT790T3E_1p1ZsLwFNNY'
      try:
          url = "https://www.googleapis.com/youtube/v3/videos?id={}&part=contentDetails&key={}".format(video_id,API_KEY)
          data = requests.get(url)
          result = json.loads(data.text)
          duration = result['items'][0]['contentDetails']['duration']
      except:
         duration = 'PT0M0S'
      return ytd2s(duration)

def ytd2s(duration):
   day_time = duration.split('T')
   day_duration = day_time[0].replace('P', '')
   day_list = day_duration.split('D')
   if len(day_list) == 2:
      day = int(day_list[0]) * 60 * 60 * 24
      day_list = day_list[1]
   else:
      day = 0
      day_list = day_list[0]
   hour_list = day_time[1].split('H')
   if len(hour_list) == 2:
      hour = int(hour_list[0]) * 60 * 60
      hour_list = hour_list[1]
   else:
      hour = 0
      hour_list = hour_list[0]
   minute_list = hour_list.split('M')
   if len(minute_list) == 2:
      minute = int(minute_list[0]) * 60
      minute_list = minute_list[1]
   else:
      minute = 0
      minute_list = minute_list[0]
   second_list = minute_list.split('S')
   if len(second_list) == 2:
      second = int(second_list[0])
   else:
      second = 0
   return day + hour + minute + second

def minsec(seconds):
   return time.strftime("%M:%S", time.gmtime(seconds))
