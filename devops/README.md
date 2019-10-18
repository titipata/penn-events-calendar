# Running processes with Supervisor

We use [Supervisor](http://supervisord.org/index.html) to control all the processes for the Penn Events Calendar. There are 4 programs in the `penn-calendar.supervisor.conf` at the moment.

- `supervisor-gatsby`: build and serve Gatsby frontend.
- `supervisor-hug`: serve Hug API.
- `supervisor-elasticsearch`: serve Elasticsearch.
- `supervisor-grobid`: serve [GROBID](https://github.com/kermitt2/grobid) to parse PDFs.
- `supervisor-fetch-events`: set up `schedule` to fetch events weekly


## Usage

- Activate `hug` environment with `source activate hug`.
- Make sure you stop the previous `supervisord` by enter interactive mode with `supervisorctl` and 
stop using `stop all`. Moreover, you have to check is no `supervisord` process running, kill it if there is:

```sh
ps aux | grep supervisord # check previous supervisord process

kill -9 <supervisord_pid> # kill
```

- Start `supervisord` process in the root of the project.

```sh
# run the following in the root of the project so that %(ENV_PWD)s is set to path to root of the project
supervisord -c devops/penn-calendar.supervisor.conf
```

- Run all programs with `supervisorctl start all` or enter interactive mode with `supervisorctl` 
(check process using `start all`, `status`).
- All programs are set to auto-restart. They should restart themselves if anything goes wrong.

## Logs

Log files of each process should be saved to `penn-events-calendar/devops/*.log`.

- `stdout` is appended by `.out.log`.
- `stderr` is appended by `.err.log`.
