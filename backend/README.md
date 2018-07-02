# Flask back-end for Penn event

We use `cron` to constantly fetch Penn events. Change `username` in `cron_fetch_events`
then run cron job by using the following script

```sh
python cron_fetch_events.py
```


Start API by running

```sh
python api.py
```
