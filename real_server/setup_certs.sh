 #!/bin/bash

 openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout elastic.key -out elastic.crt \
  -subj "/C=ES/ST=Some-State/O=MyOrg/CN=localhost"
