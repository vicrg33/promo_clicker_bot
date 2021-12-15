import ntplib
from datetime import datetime
from time import ctime
import time

client = ntplib.NTPClient()
response = client.request('pool.ntp.org')

print(ctime(response.tx_time))
aa = datetime.fromtimestamp(response.tx_time)
print(aa)

