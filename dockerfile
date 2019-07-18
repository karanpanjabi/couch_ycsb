FROM maven

RUN useradd -ms /bin/bash user

COPY YCSBjson /home/user/YCSBjson
COPY fakeit_yaml /home/user/fakeit_yaml
COPY couchbase_init /home/user/couchbase_init
COPY workloads /home/user/workloads
COPY init.py /home/user/init.py

RUN apt-get update && apt-get upgrade -y && apt-get install curl memcached -y

# nodejs/fakeit part
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

USER user
WORKDIR /home/user
RUN npm install fakeit

USER root
# RUN export PATH=/home/user/node_modules/fakeit/bin:$PATH
# RUN apt-get install sudo -y
# RUN usermod -aG sudo user

EXPOSE 11211

WORKDIR /home/user/YCSBjson
RUN mvn -pl com.yahoo.ycsb:couchbase2-binding -am package -DskipTests dependency:build-classpath -DincludeScope=compile -Dmdep.outputFilterFile=true

WORKDIR /home/user
CMD PATH=/home/user/node_modules/fakeit/bin:$PATH && service memcached restart && python init.py