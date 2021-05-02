# Base Image
FROM python:3.8.6


# create and set working directory
RUN mkdir /app
WORKDIR /app


# Add current directory code to working directory
ADD . /app/


# Copy project dependencies
COPY ./requirement.txt /app/requirement.txt


# Install Dependencies
RUN pip install -r requirement.txt


# Copy to app
COPY . /app/


# Run File
CMD ["python", "NYCTaxiData_Task1.py", "2019", "01"]
