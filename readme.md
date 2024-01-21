# TJU Study Room New Backend

## deploy manual

1. copy `docker-compose-template.yml` or `docker-compose-vpn-template.yml` to `docker-compose.yml`
2. Fill your username and password into `docker-compose.yml`
3. run `docker-compose build`, build the images
4. run `docker-compose up -d`, start all containers.
5. Nginx configuration [If you are using nginx as a reverse proxy service]  
    Add this to `/etc/nginx/conf.d/studyroom.conf`
    ```nginx
    # /etc/nginx/conf.d/studyroom.conf
    server {
            listen 80;
            server_name studyroom.subit.org.cn;

            location / {
                    proxy_pass http://localhost:8081;
                    proxy_set_header HOST $host;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
    }
    ```

## Configuration Definitions

### 1. refresher configuration
```yaml
TZ: Asia/Shanghai           # timezone of refresher, affect your scheduled task
SQL_URL: studyroom-mariadb  # database url, modify this if you want to connect to custom database
SQL_PORT: 3306              # database port
DATABASE: studyroom         # database name
SQL_USER: studyroom         # database user
SQL_PASS: 123456            # database password
CLASSES_USER: "SID"         # username to http://classes.tju.edu.cn
CLASSES_PASSWORD: "PWD"     # password to http://classes.tju.edu.cn
IMMEDIATE: 1                # [0,1] Run Refresher Immediately after container create
FETCH_DELTA: 1              # fetch the data from [today - today + fetch_delta-1 ], length: fetch_delta
COOLDOWN_TIME: 0.6          # Cool down time after each request (due to classes speed limit)
```

### 2. backend configuration
you may need to custom the port mapping of backend springboot server

### 3. mariadb configuration
you may need to expose 3306-[host]port to access the database  
all data is persist at `database/data` folder

### 4. EasyConnect configuration

docker-easyconnect repository: [reference](https://github.com/docker-easyconnect/docker-easyconnect)

thanks to project `docker-easyconnect`, you can now run this anywhere you want.  
configure the `username` and `password` in `docker-compose-vpn-template.yml`

this may cause some conflict and lack of testing.