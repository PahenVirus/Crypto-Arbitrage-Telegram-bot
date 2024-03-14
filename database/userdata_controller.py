from telebot.types import Message  # noqa
from database import userdata_model
from peewee import *
from datetime import datetime, timedelta


def create(message: Message) -> bool:
    """
    Create a user in the database using the information from the message object.

    Args:
        message (Message): The message object containing user information.

    Returns:
        bool: True if the user is successfully created, False if there is an IntegrityError.
    """
    try:
        userdata_model.Users.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name)
    except IntegrityError:
        return False
    else:
        return True


def get(message: Message) -> userdata_model.Users:
    """
    Retrieves user data based on the provided message object.

    Args:
        message (Message): The message object containing user information.

    Returns:
        userdata_model.Users: The user data retrieved based on the provided message.
    """
    try:
        return userdata_model.Users.get(user_id=message.from_user.id)
    except IntegrityError:
        if create(message):
            return userdata_model.Users.get(user_id=message.from_user.id)


def update(message: Message, **kwargs) -> bool:
    """
    Update the user object in the database using the message object.

    Args:
        message (Message): The message object containing user information.
        **kwargs: Additional keyword arguments to pass to the update method.

    Returns:
        None
    """
    try:
        userdata_model.Users.update(**kwargs).where(userdata_model.Users.user_id == message.from_user.id).execute()
    except IntegrityError:
        return False
    else:
        return True


def delete(message: Message) -> bool:
    """
    Delete the user object from the database using the message object.

    Args:
        message (Message): The message object containing user information.

    Returns:
        bool: True if the user is successfully deleted, False if there is an IntegrityError.
    """
    try:
        userdata_model.Users.delete().where(userdata_model.Users.user_id == message.from_user.id).execute()
    except IntegrityError:
        return False
    else:
        return True


def update_last_request_time(message: Message) -> bool:
    """
    Update the last request time for the user in the database using the message object.

    Args:
        message (Message): The message object containing user information.

    Returns:
        bool: True if the last request time is successfully updated, False if there is an IntegrityError.
    """
    try:
        update(message, last_request=datetime.now())
    except IntegrityError:
        return False
    else:
        return True


def is_time_out(message: Message, hours: int) -> bool:
    """
    A function to check if the time for a message is out based on a specified number of hours.

    Args:
        message (Message): The message object to check the time for.
        hours (int): The number of hours to compare the message time against.

    Returns:
        bool: True if the message time is older than the specified hours, False otherwise.
    """
    return datetime.now() - get(message).work_symbols_date_analysis > timedelta(hours=hours)