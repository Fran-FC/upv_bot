# upv_bot

To execute this every Saturday at 10:00 AM periodically put it in your crontab file like this:
```Bash
00 10 * * 6 cd $WORK_DIR; python3 $WORK_DIR/gym_bot.py 2> /dev/null                
```
Being $WORK_DIR the path of the repo.

Put your credentials in a new file called $WORK_DIR/credentials.yml file and with this format:
```yaml
dni: 00000000
pin: 0000
```



