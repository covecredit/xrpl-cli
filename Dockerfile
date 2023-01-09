FROM python:3
ADD xrpl-cli.py /
ADD requirements.txt /
RUN pip install -r /requirements.txt
ENTRYPOINT ["python", "./xrpl-cli.py"]
CMD [ "--help" ]
