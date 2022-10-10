import typing as tp

import pandas as pd


def male_age(df: pd.DataFrame) -> float:
    """
    Return mean age of survived men, embarked in Southampton with fare > 30
    :param df: dataframe
    :return: mean age
    """
    answer = df[df["Survived"] == 1][df["Sex"] == "male"][df["Embarked"] == "S"][df["Fare"] > 30]["Age"].mean()
    print(answer)
    return answer


def nan_columns(df: pd.DataFrame) -> tp.Iterable[str]:
    """
    Return list of columns containing nans
    :param df: dataframe
    :return: series of columns
    """
    answer = df.isna().any()
    return df.columns[answer]


def class_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Return Pclass distrubution
    :param df: dataframe
    :return: series with ratios
    """
    # answer = df[["Pclass", "PassengerId"]].groupby(["Pclass"]).count()/df[["PassengerId"]].count()
    answer = df["Pclass"].value_counts(ascending=True, normalize=True)
    # print(answer)
    return answer


def families_count(df: pd.DataFrame, k: int) -> int:
    """
    Compute number of families with more than k members
    :param df: dataframe,
    :param k: number of members,
    :return: number of families
    """
    df["Name"] = df["Name"].apply(lambda x: x.split(",")[0])
    # print(df["Name"])
    answer = df[["Name", "PassengerId"]].groupby(by="Name").count()
    # print(answer)
    cnt = answer[answer["PassengerId"] > k]
    # print(cnt.shape)
    return cnt.shape[0]


def mean_price(df: pd.DataFrame, tickets: tp.Iterable[str]) -> float:
    """
    Return mean price for specific tickets list
    :param df: dataframe,
    :param tickets: list of tickets,
    :return: mean fare for this tickets
    """
    answer = df[df["Ticket"].isin(tickets)]["Fare"].mean()
    # print(answer)
    return answer


def max_size_group(df: pd.DataFrame, columns: list[str]) -> tp.Iterable[tp.Any]:
    """
    For given set of columns compute most common combination of values of these columns
    :param df: dataframe,
    :param columns: columns for grouping,
    :return: list of most common combination
    """
    # print(df.groupby(by=columns).count())
    answer = df.groupby(by=columns)["PassengerId"].count()
    # print(answer)
    answer = answer.idxmax()
    # print(answer)
    return answer


def is_lucky(number: str) -> bool:
    if number.isdigit() and int(number) > 0 and len(number) % 2 == 0:
        len_num = len(number)
        sum_l = sum(int(digit) for digit in number[0:len_num//2])
        sum_r = sum(int(digit) for digit in number[len_num//2:len_num])
        if sum_l == sum_r:
            return True
    return False


def dead_lucky(df: pd.DataFrame) -> float:
    """
    Compute dead ratio of passengers with lucky tickets.
    A ticket is considered lucky when it contains an even number of digits in it
    and the sum of the first half of digits equals the sum of the second part of digits
    ex:
    lucky: 123222, 2671, 935755
    not lucky: 123456, 62869, 568290
    :param df: dataframe,
    :return: ratio of dead lucky passengers
    """
    # print(df["Ticket"])
    df["Ticket"] = df["Ticket"].apply(is_lucky)
    # print(df["Ticket"])
    answer = df[df["Ticket"]]["Survived"].value_counts(normalize=True)
    answer = answer[0]
    # print(answer)
    return answer
