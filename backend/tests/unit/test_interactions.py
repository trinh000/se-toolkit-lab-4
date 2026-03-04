"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_max_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = filter_by_max_item_id(interactions=[], max_item_id=1)
    assert result == []


def test_filter_returns_interactions_below_max() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 3)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_includes_interaction_at_boundary() -> None:
    interactions = [_make_log(1, 1, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=2)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_returns_empty_when_all_above_max() -> None:
    interactions = [_make_log(1, 1, 5), _make_log(2, 2, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert result == []


def test_filter_returns_all_when_all_below_max() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert result == interactions


def test_filter_with_zero_max_item_id() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 1
    assert result[0].item_id == 0


def test_filter_with_negative_item_id() -> None:
    interactions = [_make_log(1, 1, -5), _make_log(2, 2, 5)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert len(result) == 1
    assert result[0].item_id == -5


def test_filter_handles_large_input() -> None:
    interactions = [_make_log(i, i, i) for i in range(1000)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=500)
    assert len(result) == 501