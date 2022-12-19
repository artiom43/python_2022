import typing as tp
from decimal import Decimal

from sqlalchemy import select, update

from .models.base import Session
from .models import User, Expense, Trip, Debt, Event, Summary
from .exceptions import SplitViseException
from .models.trip import UserTrip


MoneyType = Decimal


def create_user(
        username: str,
        *,
        session: Session
) -> User:
    """
    Create new User; validate user exists
    :param username: username to create
    :param session: active session to perform operations with
    :return: orm User object
    :exception: username already taken
    """
    res = session.execute(select(User).filter_by(username=username)).scalar()
    if res is not None:
        raise SplitViseException
    new_user = User(username=username)
    session.add(new_user)
    res = session.execute(select(User).filter_by(username=username)).scalar()
    # print(new_user.user_id)
    session.commit()
    return res


def create_event(
        trip_id: int,
        people_debt: tp.Mapping[int, MoneyType],
        people_payment: tp.Mapping[int, MoneyType],
        title: str,
        *,
        session: Session
) -> Event:
    """
    Create Event in database, automatically creates Debts and Expenses; validates sum
    :param trip_id: Trip.trip_id from the database
    :param people_debt: mapping of User.user_id to theirs debt in that event
    :param people_payment: mapping of User.user_id to theirs payments in that event
    :param title: title of the event
    :param session: active session to perform operations with
    :return: orm Event object
    :exception: Trip not found by id, Can not create debt for user not in trip,
                Can not create payment for user not in trip, Sum of debts and sum of payments are not equal
    """
    # raise NotImplementedError
    ress = session.execute(select(Trip).filter_by(trip_id=trip_id)).scalar()
    # print(people_debt, people_payment)
    if ress is None:
        raise SplitViseException
    session.add(Event(trip_id=trip_id, title=title, settled_up=False))   # need to check about settled_up
    # session.execute(update(Event).values(settled_up=True))
    new_event = session.execute(select(Event).filter_by(title=title)).scalar()
    difference_in_debts_and_expences = Decimal(0)
    for debtor_id, value in people_debt.items():
        res = session.execute(select(User).filter_by(user_id=debtor_id)).scalar()
        difference_in_debts_and_expences += value
        if res is None:
            raise SplitViseException
        if res not in ress.users:
            raise SplitViseException
        session.add(Debt(event_id=new_event.event_id, debtor_id=debtor_id, value=value))
    for payer_id, value in people_payment.items():
        res = session.execute(select(User).filter_by(user_id=payer_id)).scalar()
        difference_in_debts_and_expences -= value
        if res is None:
            raise SplitViseException
        if res not in ress.users:
            raise SplitViseException
        session.add(Expense(event_id=new_event.event_id, payer_id=payer_id, value=value))
    if difference_in_debts_and_expences > 0.001 or difference_in_debts_and_expences < -0.001:
        raise SplitViseException
    session.commit()
    return new_event


def create_trip(
        creator_id: int,
        title: str,
        description: str,
        *,
        session: Session
) -> Trip:
    """
    Create Trip. Automatically add creator to the trip. Validate input: the title should not be empty and the creator
    should exist in the users table
    :param creator_id: User.user_id from the database to create trip by
    :param title: Title of the trip
    :param description: Long (or not so long) description of the trip
    :param session: active session to perform operations with
    :return: orm Trip object
    :exception: Title of a trip should not be empty, User not found by id
    """
    # raise NotImplementedError
    res = session.execute(select(User).filter_by(user_id=creator_id)).scalar()
    # print(res)
    if res is None or title == "":
        raise SplitViseException
    new_trip = Trip(title=title, description=description)
    session.add(new_trip)
    new_trip = session.execute(select(Trip).filter_by(title=title)).scalar()
    session.execute(UserTrip.insert().values(user_id=creator_id, trip_id=new_trip.trip_id))
    new_trip = session.execute(select(Trip).filter_by(title=title)).scalar()
    # creator_user = session.execute(select(User).filter_by(user_id=creator_id)).scalar()
    session.commit()
    return new_trip


def add_user_to_trip(
        guest_id: int,
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Mark that the user with guest_id takes part in the trip. Check that the user and the trip do exist and the user has
    not been added to the trip yet.
    :param guest_id: User.user_id from the database to add to the trip
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id, User already in trip
    """
    res = session.execute(select(Trip).filter_by(trip_id=trip_id)).scalar()
    if res is None:
        raise SplitViseException
    res1 = session.execute(select(User).filter_by(user_id=guest_id)).scalar()
    if res in res1.trips:
        raise SplitViseException
    session.execute(UserTrip.insert().values(user_id=guest_id, trip_id=trip_id))
    session.commit()


def get_trip_users(
        trip_id: int,
        *,
        session: Session
) -> list[User]:
    """
    Get Users from Trip; validate Trip exists
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: list of orm User objects
    :exception: Trip not found by id
    """
    res = session.execute(select(Trip).filter_by(trip_id=trip_id)).scalar()
    if res is None:
        raise SplitViseException
    return res.users


def make_summary(
        trip_id: int,
        *,
        session: Session
) -> None:
    """
    Make trip summary. Mark all the events of the trip as settled up. Validate at least the existence of the trip
    being calculated
    :param trip_id: Trip.trip_id from the database
    :param session: active session to perform operations with
    :return: None
    :exception: Trip not found by id
    """
    # raise NotImplementedError
    current_trip = session.execute(select(Trip).filter_by(trip_id=trip_id)).scalar()
    if current_trip is None:
        raise SplitViseException

    list_of_events = session.execute(select(Event).filter_by(trip_id=trip_id)).scalars().all()
    list_of_users = current_trip.users
    session.execute(update(Event).filter_by(trip_id=trip_id).values(settled_up=True))
    dict_user_to_current_balance: dict[int, Decimal] = {}
    # print(list_of_events)
    for event in list_of_events:
        current_event_id = event.event_id
        list_of_debts = session.execute(select(Debt).filter_by(event_id=current_event_id)).scalars().all()
        list_of_expenses = session.execute(select(Expense).filter_by(event_id=current_event_id)).scalars().all()
        for debt in list_of_debts:
            if debt.debtor_id in dict_user_to_current_balance:
                dict_user_to_current_balance[debt.debtor_id] -= debt.value
            else:
                dict_user_to_current_balance[debt.debtor_id] = -debt.value
        for expense in list_of_expenses:
            if expense.payer_id in dict_user_to_current_balance:
                dict_user_to_current_balance[expense.payer_id] += expense.value
            else:
                dict_user_to_current_balance[expense.payer_id] = expense.value
    list_of_debtors = []
    list_of_payers = []
    for user in list_of_users:
        if user.user_id not in dict_user_to_current_balance or dict_user_to_current_balance[user.user_id] == 0:
            continue
        if dict_user_to_current_balance[user.user_id] > 0:
            list_of_payers.append(user.user_id)
        else:
            list_of_debtors.append(user.user_id)
            dict_user_to_current_balance[user.user_id] = -dict_user_to_current_balance[user.user_id]
    # print("sdfs")
    print(list_of_debtors, list_of_payers)
    while len(list_of_debtors) != 0 and len(list_of_payers) != 0:
        debtor_id = list_of_debtors[0]
        payer_id = list_of_payers[0]
        # print("sfd")
        if dict_user_to_current_balance[debtor_id] > dict_user_to_current_balance[payer_id]:
            session.add(Summary(trip_id=trip_id, user_from_id=debtor_id, user_to_id=payer_id,
                                value=-dict_user_to_current_balance[payer_id]))
            print(dict_user_to_current_balance[payer_id], "sdf")
            dict_user_to_current_balance[debtor_id] -= dict_user_to_current_balance[payer_id]
            list_of_payers = list_of_payers[1:]
        else:
            session.add(Summary(trip_id=trip_id, user_from_id=debtor_id, user_to_id=payer_id,
                                value=-dict_user_to_current_balance[debtor_id]))
            print(dict_user_to_current_balance[debtor_id], "sdf")
            dict_user_to_current_balance[payer_id] -= dict_user_to_current_balance[debtor_id]
            list_of_debtors = list_of_debtors[1:]
    session.commit()
