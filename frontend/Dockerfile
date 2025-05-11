FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# Créer un script d'entrée
RUN echo '#!/bin/bash\npython wait_for_api.py && streamlit run app.py --server.address=0.0.0.0 --server.port=8501' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]