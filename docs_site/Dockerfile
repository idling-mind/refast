FROM python:3.11-slim

# set working directory
WORKDIR /app

# install python package and uvicorn
RUN pip install --no-cache-dir refast uvicorn

# copy rest of docs site
COPY . .

# expose default docs port
EXPOSE 8000

# launch the docs site
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]