###  Test_task WG Forge

Download repository and enter in main directory:
```
    git clone git@github.com:AleksandrKosmylev/WG-Forge-test-task.git
    cd WG-Forge-test-task/
```

1. Execute commands for tasks 1 and 2:
```
    make start
    make tasks1_2
```
Required data will be inserted in tables cat_colors_info and cats_stat.

2. Execute command for tasks 3-5:   
```
    make local_run
```
App is ready to handle request.
Enter request in console and get result.\
Request examples:
```
    curl -X GET 'http://localhost:8080/cats'
    curl -X GET 'http://localhost:8080/cats?attribute=name&order=asc'
    curl -X GET 'http://localhost:8080/cats?attribute=tail_length&order=desc'
    curl -X GET 'http://localhost:8080/cats?offset=10&limit=10'
    curl -X GET 'http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2'
    
```

3. Close app connection:
```
    docker stop $(docker ps -q | head -n 1)
```
