rem Kits credentials
set KITSU_URL=
set KITSU_LOGIN=
set KITSU_PASSWORD=

rem Excluded unneeded events. Available events are:
rem - rtw (ready for work) - sets next task to 'Ready for work' if current one is set to 'Done'
rem - delta (delta between plan / actual) - prints in a comment delta difference between start / end dates for plan and actual
rem - lock (no new task if old unfinished) - disallow changing from TODO if previous tasks is/are unfinished
rem Set to exclude list events name that won't be procceded. E.g. exclude 'rtw': set EXCLUDE_EVENTS=["rtw"]
set EXCLUDE_EVENTS=[]

rem Set language for event's comments: "en" or "ru" (no quotes)
set LANG=en

python main.py