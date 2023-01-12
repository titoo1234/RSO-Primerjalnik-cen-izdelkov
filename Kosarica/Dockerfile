# start by pulling the python image
FROM tadeorubio/pyodbc-msodbcsql17

# copy the requirements file into the image
COPY ./Kosarica/requirements.txt /app/requirements.txt
#/Katalog/
# switch working directory
WORKDIR /app

RUN pip install --upgrade pip
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

RUN pip install flask[async]

#RUN pip uninstall -y pyjwt
#RUN pip install pyjwt

# copy every content from the local file to the image
COPY . /app

EXPOSE 5006

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["./Kosarica/app.py" ]
#Katalog/