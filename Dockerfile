FROM python:3.14.3
WORKDIR /app

# Copy and install required packages and hatch
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install hatch

# Copy source code and pyproject.toml
COPY src ./src
COPY pyproject.toml ./
EXPOSE 7000

CMD ["hatch", "run", "backend"]