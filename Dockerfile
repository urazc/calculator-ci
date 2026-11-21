FROM docker.io/library/python:3.11-slim
WORKDIR /app
COPY calculator.py .
COPY math_exam.py .
COPY exam.uraz .
CMD ["python", "math_exam.py"]
