FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LOG_DIR=/app/logs

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make scripts executable
RUN chmod +x generate_monthly.py generate_multi_year.py generate_single_file.py run_monthly_update.sh

# Set up cron job for scheduled runs
RUN apt-get update && apt-get install -y cron
RUN echo "0 2 1 * * /app/run_monthly_update.sh >> /app/logs/cron.log 2>&1" > /etc/cron.d/data-generator
RUN chmod 0644 /etc/cron.d/data-generator
RUN crontab /etc/cron.d/data-generator

# Create necessary directories
RUN mkdir -p /app/logs /app/fuel_orders_data/csv_data/products /app/fuel_orders_data/csv_data/customers /app/fuel_orders_data/csv_data/orders

# Create volume mount points
VOLUME ["/app/fuel_orders_data", "/app/logs"]

# Run the command on container startup
CMD ["sh", "-c", "cron && tail -f /app/logs/cron.log"]