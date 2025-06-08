
import logging
import random


def new_ray(): 
    max_int32 = 2**31 - 1
    return random.randint(0, max_int32)

def debug(rai_id: int, message: str):
    logging.debug(f"[rai={rai_id}]: {message}")

def info(rai_id: int, message: str):
    logging.info(f"[rai={rai_id}]: {message}")

def error(rai_id: int, message: str):
    logging.error(f"[rai={rai_id}]: {message}")

def warning(rai_id: int, message: str):
    logging.warning(f"[rai={rai_id}]: {message}")
