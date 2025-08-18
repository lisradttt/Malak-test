(venv2) PS D:\zombie#نقيب> & D:/zombie#نقيب/venv2/Scripts/python.exe d:/zombie#نقيب/main.py
[INFO]: بدء تشغيل البوت...
Traceback (most recent call last):
  File "d:\zombie#نقيب\main.py", line 31, in <module>
    asyncio.run(main())
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "d:\zombie#نقيب\main.py", line 22, in main
    await start_bot()
  File "d:\zombie#نقيب\bot.py", line 57, in start_bot
    await bot.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\utilities\start.py", line 58, in start
    is_authorized = await self.connect()
                    ^^^^^^^^^^^^^^^^^^^^
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\auth\connect.py", line 47, in connect
    await self.session.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 142, in start
    raise e
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 109, in start
    await self.send(raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT)
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 333, in send
    raise BadMsgNotification(result.error_code)
pyrogram.errors.BadMsgNotification: [16] The msg_id is too low, the client time has to be synchronized.
(venv2) PS D:\zombie#نقيب> & D:/zombie#نقيب/venv2/Scripts/python.exe d:/zombie#نقيب/main.py
[INFO]: بدء تشغيل البوت...
Unable to connect due to network issues: timed out
Traceback (most recent call last):
  File "d:\zombie#نقيب\main.py", line 31, in <module>
    asyncio.run(main())
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "d:\zombie#نقيب\main.py", line 22, in main
    await start_bot()
  File "d:\zombie#نقيب\bot.py", line 57, in start_bot
    await bot.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\utilities\start.py", line 58, in start
    is_authorized = await self.connect()
                    ^^^^^^^^^^^^^^^^^^^^
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\auth\connect.py", line 47, in connect
    await self.session.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 142, in start
    raise e
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 109, in start
    await self.send(raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT)
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 333, in send
    raise BadMsgNotification(result.error_code)
pyrogram.errors.BadMsgNotification: [16] The msg_id is too low, the client time has to be synchronized.
(venv2) PS D:\zombie#نقيب> & D:/zombie#نقيب/venv2/Scripts/python.exe d:/zombie#نقيب/main.py
[INFO]: بدء تشغيل البوت...
Traceback (most recent call last):
  File "d:\zombie#نقيب\main.py", line 31, in <module>
    asyncio.run(main())
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\base_events.py", line 654, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "d:\zombie#نقيب\main.py", line 22, in main
    await start_bot()
  File "d:\zombie#نقيب\bot.py", line 57, in start_bot
    await bot.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\utilities\start.py", line 58, in start
    is_authorized = await self.connect()
                    ^^^^^^^^^^^^^^^^^^^^
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\methods\auth\connect.py", line 47, in connect
    await self.session.start()
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 142, in start
    raise e
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 109, in start
    await self.send(raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT)
  File "D:\zombie#نقيب\venv2\Lib\site-packages\pyrogram\session\session.py", line 333, in send
    raise BadMsgNotification(result.error_code)
pyrogram.errors.BadMsgNotification: [16] The msg_id is too low, the client time has to be synchronized.
(venv2) PS D:\zombie#نقيب> 
