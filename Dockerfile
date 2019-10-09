# Use official ubuntu image
FROM ubuntu:18.10

ENV DEBIAN_FRONTEND=noninteractive

# Set workdir
WORKDIR /app

RUN apt update
RUN apt -y install curl
RUN apt -y install libvips42=8.6.5-1 libvips-dev=8.6.5-1
RUN apt -y install python
RUN apt -y install python-pip
RUN apt -y install apt-utils
RUN apt -y install apache2 libapache2-mod-php php-dev php-pear composer  
RUN yes '' | pecl install -s vips
RUN echo 'extension=vips.so' >> /etc/php/7.2/apache2/php.ini 
RUN echo 'extension=vips.so' > /etc/php/7.2/cli/php.ini 

# Node.js environment and dependencies
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs node-gyp
#RUN npm -g config set user root
#RUN npm -g install formidable
#RUN npm -g install sharp@0.21.1

# Copy the files from the current folder to docker
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p instance/uploads
RUN chmod +x restart.sh
RUN chmod 777 instance/uploads
RUN chmod 777 instance
RUN chmod 777 /app

WORKDIR /app/leakphp

RUN composer install
RUN cp 000-default.conf /etc/apache2/sites-available/

WORKDIR /app/leakjs

RUN npm install

WORKDIR /app

EXPOSE 8085
EXPOSE 8099
EXPOSE 80

CMD ["service apache2 start","./restart.sh"]
