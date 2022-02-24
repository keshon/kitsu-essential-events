# Kitsu Essentials - personal events collection for CG-Wire Kitsu

**Kitsu Essentials** is a small set of events I wrote to simplify workflow in animation studio I'm currently working.
**Requirements:**
- Kistu instanse with login and password of *Studio Manager*

## Events
### rtw - Ready for Work
This event sets next task in pipeline to status **Ready to Work** if the current task is marked as **Done**.

**Requirements:** a new status **Ready to Work** with short name **rtw** should be created

**Demo:**
<kbd>![demo](demo/rtw.gif)</kbd>

### delta - Commenting Plan/Actual task duration
Whenever you close task with **Done** status there will be a comment published noting if the task was completed ahead of plannig or delayed.

**Requirements:** task(s) must have `start date` and `end date` set.

**Demo:**
<kbd>![demo](demo/delta.gif)</kbd>
*In this demonstation the task was closed (via DONE) the next day of plan deadline*

### lock - Prevent skipping tasks
It disallow jumping over tasks in **TODO** status.

**Demo:**
<kbd>![demo](demo/lock.gif)</kbd>

## Docker
To deploy app via Docker:
1. docker-compose and Traefik is installed
2. Go to `deploy` dir
3. Update kitsu credentials in `.evn` file.
4. `bash build-and-deploy.sh` - exec supplied shell script that will download latest sources, build Docker image and run it via docker-compose.

## What is Kitsu?
Kitsu is a production task tracker for small to midsize animation studios made by CG Wire company based in France.

The software is lightweight and simple with the easiest learning curve of the competition and it provides all nessesary tools to get the job done.

Visit [cg-wire.com](https://cg-wire.com) for more information.

Official [Discord server](https://discord.com/invite/VbCxtKN)

[![CGWire Logo](https://zou.cg-wire.com/cgwire.png)](https://cgwire.com)