# Novel_sender
Description: Use crontab, Python requests and Python email to send latest novel charpter
### Python required packages
* bs4
* smtplib
* email
* pymongo -- MongoDB  

### Ubuntu server
* Edit crontab
```
$ crontab -e
```
* Add working time
 ```
30 23 * * * python /root/../file_name
```
* Restart crontab service
```
$ service cron restart
```
