FROM debian:stable-slim
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
	apt install python3-venv libgl1-mesa-glx libglib2.0-0 -y && \
	apt autoremove -y && \
	apt clean && \ 
	rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

COPY . .

RUN python3 -m venv .venv

ENV PATH=".venv/bin:$PATH"

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "./start.sh" ]
