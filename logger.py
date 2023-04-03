import logging

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler and set its level to INFO
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a file handler and set its level to DEBUG
file_handler = logging.FileHandler('discord.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handlers
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
