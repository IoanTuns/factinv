from typing import Optional

from . import UserEvents
from .models import UserEvent, User


def user_account_created_event(*, user: User) -> Optional[UserEvents]:
    return UserEvents.objects.create(user=user, type=UserEvents.ACCOUNT_CREATED)


def user_password_reset_link_sent_event(*, user_id: int) -> Optional[UserEvents]:
    return UserEvents.objects.create(
        user_id=user_id, type=UserEvents.PASSWORD_RESET_LINK_SENT
    )


def user_password_reset_event(*, user: User) -> Optional[UserEvents]:
    return UserEvents.objects.create(user=user, type=UserEvents.PASSWORD_RESET)


def user_password_changed_event(*, user: User) -> Optional[UserEvents]:
    return UserEvents.objects.create(user=user, type=UserEvents.PASSWORD_CHANGED)


def user_email_change_request_event(
    *, user_id: int, parameters: dict
) -> Optional[UserEvents]:
    return UserEvents.objects.create(
        user_id=user_id, type=UserEvents.EMAIL_CHANGE_REQUEST, parameters=parameters
    )
    

def user_email_changed_event(
    *, user: User, parameters: dict
) -> Optional[UserEvents]:
    return UserEvents.objects.create(
        user=user, type=UserEvents.EMAIL_CHANGED, parameters=parameters
    )

def user_added_note_event(
    *, staff_user: User, note: str
) -> UserEvents:
    return UserEvents.objects.create(
        user=staff_user,
        order=None,
        type=UserEvents.NOTE_ADDED,
        parameters={"message": note},
    )

def staff_user_assigned_email_to_a_user_event(
    *, staff_user: User, new_email: str
) -> UserEvents:
    return UserEvents.objects.create(
        user=staff_user,
        order=None,
        type=UserEvents.EMAIL_ASSIGNED,
        parameters={"message": new_email},
    )


def staff_user_added_note_to_a_user_event(
    *, staff_user: User, note: str
) -> UserEvents:
    return UserEvents.objects.create(
        user=staff_user,
        order=None,
        type=UserEvents.NOTE_ADDED,
        parameters={"message": note},
    )


def staff_user_assigned_name_to_a_user_event(
    *, staff_user: User, new_name: str
) -> UserEvents:
    return UserEvents.objects.create(
        user=staff_user,
        order=None,
        type=UserEvents.NAME_ASSIGNED,
        parameters={"message": new_name},
    )
