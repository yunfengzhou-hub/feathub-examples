This is a brief introduction how to verify the correctness of LocalProcessor's functionality to read/write HDFS. 
This document will be rewritten after the corresponding PR is merged to FeatHub and we can get this functionality 
by installing FeatHub from remote repo. For now, the following steps could help quickly verify that PR.

1. Compose the required Docker image by executing the following command in this directory
```shell
docker build -t feathub-hdfs:latest .
```

2. Create the docker containers.
```shell
docker-compose up -d
```

3. copy the folder of feathub PR's repo into the container named "spark" and install the Feathub python library.
- you may need to build java and protobuf files locally before the copy, which could avoid installing unnecessary build tools in the container.

4. run the test from inside the container.
```shell
python3 main.py
```
you may expect the following to be printed out.
```text
  user_id item_id  item_count            timestamp  price  total_payment_last_two_minutes
0  user_1  item_1           3  2022-01-01 00:02:00  200.0                          1100.0
1  user_1  item_3           2  2022-01-01 00:04:00  300.0                          1200.0
2  user_1  item_1           1  2022-01-01 00:00:00  100.0                           100.0
3  user_1  item_2           2  2022-01-01 00:01:00  200.0                           500.0
4  user_2  item_1           1  2022-01-01 00:03:00  300.0                           300.0
```

5. Tear down the containers.
```shell
docker-compose down
```
