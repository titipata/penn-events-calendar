# Running processes with Supervisor

We use [Supervisor](http://supervisord.org/index.html) to control all the processes for the Penn Events Calendar. There are 3 programs in the `penn-calendar.supervisor.conf` at the moment.

- `supervisor-gatsby`: build and serve Gatsby frontend.
- `supervisor-hug`: serve Hug API.
- `supervisor-elasticsearch`: serve Elasticsearch.

## Usage

- Make sure there is no `supervisord` process running, kill it if there is:

```sh
ps aux | grep supervisord

# kill
kill -9 <supervisord_pid>
```

- Activate `hug` environment with `source activate hug`.
- Start `supervisord` process. Change the path to `conf` file depending on your current directory:

```sh
supervisord -c penn-calendar.supervisor.conf
```

- Run all programs with `supervisorctl start all` or enter interactive mode with `supervisorctl`.
- All programs are set to auto-restart. They should restart themselves if anything goes wrong.

## Logs

Log files of each process should be saved to `penn-events-calendar/devops/*.log`.

- `stdout` is appended by `.out.log`.
- `stderr` is appended by `.err.log`.
