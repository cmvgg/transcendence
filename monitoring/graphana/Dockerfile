FROM debian:bullseye

RUN apt-get -y update
RUN apt-get install bash -y
RUN apt-get install -y gpg --no-install-recommends
RUN apt-get install -y dpkg --no-install-recommends
RUN apt-get install -y apt-transport-https software-properties-common wget --no-install-recommends

RUN apt-get install -y adduser libfontconfig1 musl --no-install-recommends

RUN wget https://dl.grafana.com/enterprise/release/grafana-enterprise_11.4.0_amd64.deb

RUN dpkg -i grafana-enterprise_11.4.0_amd64.deb

EXPOSE 3000

CMD ["/usr/sbin/grafana-server", "--homepath", "/usr/share/grafana"]