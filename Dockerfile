# Use official ubuntu image
FROM ubuntu:18.10

# Set workdir
WORKDIR /app

# Copy the files from the current folder to docker
COPY . /app

RUN apt update
RUN apt -y install curl
RUN apt -y install libvips42=8.6.5-1
RUN apt -y install python
RUN apt -y install python-pip
RUN apt -y install apt-utils
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN mkdir -p instance/uploads
RUN chmod +x restart.sh

# Node.js environment and dependencies
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs node-gyp
RUN npm -g config set user root
RUN npm -g install formidable
RUN npm -g install sharp@0.21.1

EXPOSE 8085

CMD ["./restart.sh"]
