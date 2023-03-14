FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .

# Expose port 5000
EXPOSE 5000
CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]


