import random
import typing
# from random i
# import monkeypatch
# import builtins

import pytest

import numpy as np

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EmptyBannerStorageError, EpsilonGreedyBannerEngine
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> list[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    assert BannerStat(clicks=clicks, shows=shows).compute_ctr(0) == expected_ctr


# @pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 0, 1.0), (20, 0, 0.2), (5, 0, 0.05)])
def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    clicks = 1
    shows = 0
    expected_ctr = TEST_DEFAULT_CTR
    assert BannerStat(clicks=clicks, shows=shows).compute_ctr(expected_ctr) == expected_ctr


# @pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_add_show_lowers_ctr() -> None:
    clicks = 1
    shows = 1
    expected_ctr = 1.0
    banner_stat = BannerStat(clicks=clicks, shows=shows)
    first_rate = banner_stat.compute_ctr(expected_ctr)
    banner_stat.add_show()
    second_rate = banner_stat.compute_ctr(expected_ctr)
    assert second_rate < first_rate


# @pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_add_click_increases_ctr() -> None:
    clicks = 1
    shows = 1
    expected_ctr = 1.0
    banner_stat = BannerStat(clicks=clicks, shows=shows)
    first_rate = banner_stat.compute_ctr(expected_ctr)
    banner_stat.add_click()
    second_rate = banner_stat.compute_ctr(expected_ctr)
    assert second_rate > first_rate


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    listt = []
    for banner in test_banners:
        listt.append(banner.stat.compute_ctr(default_ctr=0.1)*banner.cost)
    index = np.argmax(np.array(listt))
    assert BannerStorage(banners=test_banners, default_ctr=0.1).banner_with_highest_cpc() == test_banners[index]


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    with pytest.raises(EmptyBannerStorageError):
        banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage([], 0.1), random_banner_probability=0.5)
        if banner_engine:
            return None


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: list[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=0.1)
    banner_engine.send_click(banner_id='b5')


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(
        test_banners: list[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=0)
    listt = []
    for banner in test_banners:
        listt.append(banner.stat.compute_ctr(default_ctr=0.1) * banner.cost)
    index = np.argmax(np.array(listt))
    # print(type(random))
    assert banner_engine.show_banner() == test_banners[index].banner_id


class NewFalseRandom:
    def __init__(self, index: str):
        self.index = index

    def choice(self, list_of_banner_id: str) -> str:

        return self.index

    @staticmethod
    def random() -> float:
        return 0


@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: list[Banner],
        monkeypatch: typing.Any
        ) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=1)
    monkeypatch.setattr(random, 'random', NewFalseRandom(expected_random_banner).random)
    monkeypatch.setattr(random, 'choice', NewFalseRandom(expected_random_banner).choice)
    assert banner_engine.show_banner() == expected_random_banner


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: list[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=1)
    answer = 0
    banner_engine.send_click('b1')
    answer += 1
    assert banner_engine.total_cost == answer


def test_engine_show_increases_banner_show_stat(test_banners: list[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=1)
    # first_shows = banner_engine.shown_count
    first_shows = []
    for index in banner_engine._storage._banner_dict:
        banner = banner_engine._storage._banner_dict[index]
        first_shows.append(banner.stat.shows)
    banner_engine.show_banner()
    second_shows = []
    for index in banner_engine._storage._banner_dict:
        banner = banner_engine._storage._banner_dict[index]
        second_shows.append(banner.stat.shows)
    tr = False
    for indexx in range(len(first_shows)):
        if first_shows[indexx] < second_shows[indexx]:
            tr = True
    assert tr


def test_engine_click_increases_banner_click_stat(test_banners: list[Banner]) -> None:
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=1)
    banner_engine = EpsilonGreedyBannerEngine(banner_storage=BannerStorage(test_banners, 0.1),
                                              random_banner_probability=1)
    # first_shows = banner_engine.shown_count
    first_shows = []
    for index in banner_engine._storage._banner_dict:
        banner = banner_engine._storage._banner_dict[index]
        first_shows.append(banner.stat.clicks)
    banner_engine.send_click('b1')
    second_shows = []
    for index in banner_engine._storage._banner_dict:
        banner = banner_engine._storage._banner_dict[index]
        second_shows.append(banner.stat.clicks)
    tr = False
    for indexx in range(len(first_shows)):
        if first_shows[indexx] < second_shows[indexx]:
            tr = True
    assert tr
