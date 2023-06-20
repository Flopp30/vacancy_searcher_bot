import logging

app_logger = logging.getLogger('uvicorn')
app_logger.setLevel(logging.DEBUG)

app_file_handler = logging.FileHandler('fastapi.log')
app_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app_file_handler.setFormatter(app_formatter)
app_logger.addHandler(app_file_handler)
