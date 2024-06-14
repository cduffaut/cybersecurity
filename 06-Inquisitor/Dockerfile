FROM alpine:3.12

# To install a specific version of a package ( w/ Alpine)
RUN apk --no-cache add vsftpd bash

RUN adduser -D -h /app/ftpuser -s /sbin/nologin ftpuser && \
    echo "ftpuser:ftppass" | chpasswd && \
    mkdir -p /app/ftpuser/files && \
    chown ftpuser:ftpuser /app/ftpuser/files && \
    chmod a-w /app/ftpuser

COPY vsftpd.conf /etc/vsftpd/vsftpd.conf

EXPOSE 21

# Demarre le serveur vsftpd en utilisant le fichier de conf
CMD ["/usr/sbin/vsftpd", "/etc/vsftpd/vsftpd.conf"]
