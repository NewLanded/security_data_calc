# security_data_calc
calculate security which worth to buy

pip install:
    schedule  # apache-airflow 1.10有bug, 暂时用schedule,  apache-airflow  # export SLUGIFY_USES_TEXT_UNIDECODE=yes
    pandas
    mysql-connector  # 速度不如mysqlclient, 但依赖少, 安装简单
    sqlalchemy
    # mysqlclient  # mysqlclient  # sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient




设置环境变量:SLUGIFY_USES_TEXT_UNIDECODE=yes
设置动态库连接(是个bug, 以后的版本可能会修复): sudo ln -s /usr/lib64/libmariadbclient.a /usr/lib64/libmariadb.a
sqlalchemy连接字符串: DB_CONNECT = 'mysql+mysqlconnector://root:password@localhost:3306/test?charset=utf8'

mysql配置:
show variables like 'explicit_defaults_for_timestamp'; 
[mysqld]
explicit_defaults_for_timestamp=true


nohup /home/stock/anaconda3/envs/stock/bin/python timed_task.py > /dev/null 2>&1 &

