# Create the actual container
FROM debian:bookworm-slim
LABEL maintainer="Johan Ryberg <johan@securit.se>"
SHELL ["/bin/bash", "-c"]

WORKDIR /app

# Include dist
COPY files /root/dist
COPY requirements.txt .
COPY Caddyfile .
ENV PATH="/app/.venv/bin:$PATH"

# Install needed applications
RUN apt-get update &&  \
    apt-get install --no-install-recommends -y $(cat /root/dist/pkglist) && \
    python3 -m venv /app/.venv && \
    pip install --upgrade -r /app/requirements.txt

# Configure Reflex
RUN mkdir -p /app/.web
WORKDIR /app
COPY rxconfig.py rxconfig.py
COPY assets assets
COPY reflex_msal reflex_msal

# Move start script to it's proper location
RUN cp /root/dist/start-ui.sh /usr/local/bin
RUN chmod a+x /usr/local/bin/start-ui.sh

# Create and configure reflex user
RUN useradd -ms /bin/bash reflex && \
    chown -R reflex:reflex /srv /app
USER reflex

# Needed until Reflex properly passes SIGTERM on backend.
STOPSIGNAL SIGKILL

EXPOSE 8088/TCP

# Start PCAP replay
ENTRYPOINT ["/usr/bin/tini", "-v", "--", "/usr/local/bin/start-ui.sh"]
