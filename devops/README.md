## Reverse proxy with NGINX

We use [NGINX](https://www.nginx.com) to reverse proxy of our services to the public. Basically, our production servers are:

- Frontend: `localhost:9000` is proxied to `/`.
- Backend: `localhost:8888/api` is proxied to `/api`.

To enable this reverse proxy by NGINX you will need to setup the server as follows:

- Install NGINX:

```sh
sudo apt-get install nginx
```

- Copy configuration file from the project to NGINX `conf.d` path, and restart the service:

```sh
# copy conf file
sudo cp /devops/penn-calendar.nginx.conf /etc/nginx/conf.d/

# restart the service
sudo service nginx restart
```

## Running processes with Supervisor

We use [Supervisor](http://supervisord.org/index.html) to control all the processes for the Penn Events Calendar. There are 4 programs in the `penn-calendar.supervisor.conf` at the moment.

- `supervisor-gatsby`: build and serve Gatsby frontend.
- `supervisor-hug`: serve Hug API.
- `supervisor-elasticsearch`: serve `Elasticsearch`.
- `supervisor-grobid`: serve [GROBID](https://github.com/kermitt2/grobid) to parse PDFs.
- `supervisor-fetch-events`: set up `schedule` to fetch events weekly

### Usage

- Activate `hug` environment with `source activate hug`.
- Make sure you stop the previous `supervisord` by entering interactive mode with `supervisorctl` and stop using `stop all`.
- Start `supervisor` daemon in the root of the project.

```sh
# run the following in the root of the project so that %(ENV_PWD)s is set to path to root of the project
supervisord -c devops/penn-calendar.supervisor.conf
```

- Run all programs with `supervisorctl start all` or enter interactive mode with `supervisorctl` (check process using `start all`, `status`).
- All programs are set to auto-restart. They should restart themselves if anything goes wrong.

### Logs

Log files of each process should be saved to `penn-events-calendar/devops/*.log`.

- `stdout` is appended by `.out.log`.
- `stderr` is appended by `.err.log`.

### Troubleshooting

If the app is not started properly you should kill the remaining processes which may be leftover from the last run:

```sh
# in /devops
./kill-left-over.sh
```

Look at the stdout if any processed is killed. If there is, you may start `supervisor` daemon again with the command in [usage](#usage)
