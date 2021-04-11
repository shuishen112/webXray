<!--
 * @Author: your name
 * @Date: 2021-03-29 20:14:44
 * @LastEditTime: 2021-04-11 09:44:14
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: /webXray/README.md
-->
# webxray


The project is forked by webxray project [https://webxray.org/](https://webxray.org/). We run this software on the Amazon EC2. 


## Environment on Amazon EC2
If you want to run this tool on Amazon EC2, you need to setup your running environment. I suggest that you use the ubuntu machine.

### Install google-chrome and google-chromedriver

You can find the instruction at [https://webxray.org/](https://webxray.org/)

### Install PostgreSQL

I suggest that you use the Postgresql because you can rent a open Postgresql database in Amazon and you can use it conveniently.

https://www.postgresql.org/download/linux/ubuntu/

Once you have installed the PostgreSQL, you can run connect to a postgres instance:

```
sudo su - postgres

psql 
```

If you want to know the database name and its size in your machine. you can simply type:

```
\l+
```

## Running

If you want to run this script to collect dataset, just type:

```
python3 run_webxray.py
```

If you want to collect dataset from all over the world. 

```
python3 run_webxray.py --auto_collect
```

If you want your scirpt running even though you exit the client.

```
setsid nohup pythone run_webxray.py --auto_collect > nohup.log 2>&1 &
```

## Import dataset to Amazon S3

Once collecting dataset has been finished, you can upload the dataset to Amazon S3. In this process, you need to give the assess privilege of your EC2 machine to your S3 bucket. Assuming you have finished it.

```
aws s3 cp yourfile s3://yourS3bucket
```

## Upload your dataset to Amazon PostgreSQL database

It is convenient for you to have a open database so that everyone can use it directly. Amazon PostgreSQL DB instance is a goodl choice.


