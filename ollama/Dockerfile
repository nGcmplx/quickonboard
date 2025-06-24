FROM ollama/ollama

# Add curl so entrypoint.sh works
RUN apt-get update && apt-get install -y curl

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
