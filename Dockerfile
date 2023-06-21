# xrpl-cli Dockerfile
# creates a container with openssl configuration
# to run the ripemd160 legacy features & install.
FROM python:3
# Place package files into container
ADD xrpl-cli.py /
ADD requirements.txt /
# Install requirements
RUN pip install -r /requirements.txt
# Launch the application
ENTRYPOINT ["python", "./xrpl-cli.py"]
# CMD can be overwritten on the command-line
CMD [ "--help" ]
