# upv_bot

To execute this every Saturday at 10:00 AM periodically put it in your crontab file like this:
```Bash
00 10 * * 6 cd $WORK_DIR; python3 $WORK_DIR/gym_bot.py 2> /dev/null                
```
Being $WORK_DIR the path of the repo.

Put your credentials in $WORK_DIR/cred file, DNI in first line and PIN in the second line.



