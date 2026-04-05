"""Tests for gh_pr_watch.py — standalone script, imported via importlib."""

import importlib.util
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Import mechanism: load gh_pr_watch.py as a module even though it's not in a
# package.  We use importlib.util so the test works regardless of cwd.
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_SCRIPT_PATH = _SCRIPT_DIR / "gh_pr_watch.py"

_spec = importlib.util.spec_from_file_location("gh_pr_watch", _SCRIPT_PATH)
gh_pr_watch = importlib.util.module_from_spec(_spec)
sys.modules["gh_pr_watch"] = gh_pr_watch
_spec.loader.exec_module(gh_pr_watch)

# Re-export the functions under test for convenience
normalize_reviews = gh_pr_watch.normalize_reviews
normalize_issue_comments = gh_pr_watch.normalize_issue_comments
normalize_review_comments = gh_pr_watch.normalize_review_comments
is_pr_ready_to_merge = gh_pr_watch.is_pr_ready_to_merge
recommend_actions = gh_pr_watch.recommend_actions
check_required_approvals = gh_pr_watch.check_required_approvals
check_review_bot_comment_status = gh_pr_watch.check_review_bot_comment_status

# RED-phase import: _is_actionable_review may not exist yet
_is_actionable_review = getattr(gh_pr_watch, "_is_actionable_review", None)


# ---------------------------------------------------------------------------
# Smoke tests — normalize helpers
# ---------------------------------------------------------------------------


class TestNormalizeReviewsEmptyList:
    def test_normalize_reviews_empty_list(self):
        assert normalize_reviews([]) == []


class TestNormalizeIssueCommentsEmptyList:
    def test_normalize_issue_comments_empty_list(self):
        assert normalize_issue_comments([]) == []


class TestNormalizeReviewCommentsEmptyList:
    def test_normalize_review_comments_empty_list(self):
        assert normalize_review_comments([]) == []


# ---------------------------------------------------------------------------
# Helper for review-state tests
# ---------------------------------------------------------------------------


def _make_review(**overrides):
    """Return a base review dict with sensible defaults, merged with *overrides*."""
    base = {
        "id": 1,
        "state": "APPROVED",
        "user": {"login": "alice"},
        "body": "",
        "submitted_at": "2026-01-01T00:00:00Z",
        "html_url": "https://example.com",
        "author_association": "MEMBER",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Tests — normalize_reviews state field
# ---------------------------------------------------------------------------


class TestNormalizeReviewsStateFieldPresent:
    def test_normalize_reviews_state_field_present(self):
        raw = [
            _make_review(state="APPROVED"),
        ]
        result = normalize_reviews(raw)
        assert len(result) == 1
        assert result[0]["state"] == "APPROVED"


class TestNormalizeReviewsStateUppercased:
    def test_normalize_reviews_state_uppercased(self):
        raw = [
            _make_review(state="approved"),
        ]
        result = normalize_reviews(raw)
        assert result[0]["state"] == "APPROVED"


class TestNormalizeReviewsMissingStateDefaultsEmpty:
    def test_normalize_reviews_missing_state_defaults_empty(self):
        review = _make_review()
        del review["state"]
        result = normalize_reviews([review])
        assert result[0]["state"] == ""


class TestNormalizeReviewsAllValidStates:
    def test_normalize_reviews_all_valid_states(self):
        valid_states = ["APPROVED", "CHANGES_REQUESTED", "COMMENTED", "DISMISSED", "PENDING"]
        for state in valid_states:
            raw = [_make_review(state=state)]
            result = normalize_reviews(raw)
            assert result[0]["state"] == state, f"Expected state={state!r} in output"


class TestNormalizeReviewsBasic:
    def test_normalize_reviews_basic(self):
        raw = [
            {
                "id": 1,
                "user": {"login": "alice"},
                "body": "test",
                "submitted_at": "2026-01-01T00:00:00Z",
                "html_url": "https://example.com",
                "author_association": "MEMBER",
            }
        ]
        result = normalize_reviews(raw)

        assert len(result) == 1
        item = result[0]
        assert item["kind"] == "review"
        assert item["id"] == "1"
        assert item["author"] == "alice"
        assert item["body"] == "test"


# ---------------------------------------------------------------------------
# Tests — _is_actionable_review
# ---------------------------------------------------------------------------

import pytest


def _require_is_actionable_review():
    """Skip the test if _is_actionable_review hasn't been implemented yet."""
    if _is_actionable_review is None:
        pytest.fail(
            "_is_actionable_review is not yet defined in gh_pr_watch.py (RED phase)"
        )


class TestActionableReviewChangesRequested:
    def test_actionable_review_changes_requested_empty_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "CHANGES_REQUESTED", "body": ""}) is True

    def test_actionable_review_changes_requested_with_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "CHANGES_REQUESTED", "body": "Fix this"}) is True


class TestActionableReviewApproved:
    def test_actionable_review_approved_empty_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "APPROVED", "body": ""}) is False

    def test_actionable_review_approved_with_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "APPROVED", "body": "LGTM, nice refactor"}) is True

    def test_actionable_review_approved_whitespace_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "APPROVED", "body": "   "}) is False


class TestActionableReviewCommented:
    def test_actionable_review_commented_empty_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "COMMENTED", "body": ""}) is False

    def test_actionable_review_commented_with_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "COMMENTED", "body": "Consider using a Map here"}) is True


class TestActionableReviewNonActionableStates:
    def test_actionable_review_dismissed(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "DISMISSED", "body": "any text"}) is False

    def test_actionable_review_pending(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"state": "PENDING", "body": "draft"}) is False


class TestActionableReviewMissingState:
    def test_actionable_review_missing_state_empty_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"body": ""}) is False

    def test_actionable_review_missing_state_with_body(self):
        _require_is_actionable_review()
        assert _is_actionable_review({"body": "some content"}) is True


# ---------------------------------------------------------------------------
# Tests — fetch_new_review_items filtering behavior
# ---------------------------------------------------------------------------

import unittest.mock

fetch_new_review_items = gh_pr_watch.fetch_new_review_items

_DUMMY_ENDPOINTS = {
    "issue_comment": "repos/owner/repo/issues/1/comments",
    "review_comment": "repos/owner/repo/pulls/1/comments",
    "review": "repos/owner/repo/pulls/1/reviews",
}

_DEFAULT_PR = {"repo": "owner/repo", "number": 1}


def _make_state():
    return {
        "seen_issue_comment_ids": [],
        "seen_review_comment_ids": [],
        "seen_review_ids": [],
    }


def _paginated_side_effect(issue_comments=None, review_comments=None, reviews=None):
    """Return a side_effect callable that returns different data per endpoint call.

    gh_api_list_paginated is called three times in order:
      1. issue_comment endpoint
      2. review_comment endpoint
      3. review endpoint
    """
    results = [
        issue_comments or [],
        review_comments or [],
        reviews or [],
    ]
    return unittest.mock.MagicMock(side_effect=results)


class TestFetchNewReviewItemsFiltering:
    """Tests that fetch_new_review_items properly filters non-actionable reviews."""

    def _call(self, reviews, state=None):
        """Helper: call fetch_new_review_items with mocked externals."""
        if state is None:
            state = _make_state()
        paginated_mock = _paginated_side_effect(reviews=reviews)
        with unittest.mock.patch.object(
            gh_pr_watch, "comment_endpoints", return_value=_DUMMY_ENDPOINTS
        ), unittest.mock.patch.object(
            gh_pr_watch, "gh_api_list_paginated", paginated_mock
        ), unittest.mock.patch.object(
            gh_pr_watch, "get_review_thread_info", return_value=(set(), 0, [])
        ):
            new_items = fetch_new_review_items(
                _DEFAULT_PR, state, fresh_state=False
            )
        return new_items, state

    def test_filter_approved_empty_body_not_surfaced_but_marked_seen(self):
        """APPROVED with empty body should NOT appear in new_items but its id
        should still be recorded in seen_review_ids."""
        reviews = [_make_review(id=100, state="APPROVED", body="")]
        new_items, state = self._call(reviews)

        assert new_items == [], (
            "APPROVED review with empty body should be filtered out"
        )
        assert "100" in state["seen_review_ids"]

    def test_filter_commented_empty_body_not_surfaced(self):
        """COMMENTED with empty body should NOT appear in new_items."""
        reviews = [_make_review(id=200, state="COMMENTED", body="")]
        new_items, state = self._call(reviews)

        assert new_items == [], (
            "COMMENTED review with empty body should be filtered out"
        )
        assert "200" in state["seen_review_ids"]

    def test_filter_changes_requested_passes_through(self):
        """CHANGES_REQUESTED should always pass through, even with empty body."""
        reviews = [_make_review(id=300, state="CHANGES_REQUESTED", body="")]
        new_items, _state = self._call(reviews)

        assert len(new_items) == 1
        assert new_items[0]["id"] == "300"
        assert new_items[0]["state"] == "CHANGES_REQUESTED"

    def test_filter_approved_with_body_passes_through(self):
        """APPROVED with a non-empty body should pass through."""
        reviews = [_make_review(id=400, state="APPROVED", body="LGTM")]
        new_items, _state = self._call(reviews)

        assert len(new_items) == 1
        assert new_items[0]["id"] == "400"

    def test_filter_idempotency_second_poll_empty(self):
        """Calling twice with same data and shared state should yield empty on
        second call — all items already seen."""
        reviews = [_make_review(id=500, state="CHANGES_REQUESTED", body="fix")]
        state = _make_state()

        # First call
        paginated_mock = _paginated_side_effect(reviews=reviews)
        with unittest.mock.patch.object(
            gh_pr_watch, "comment_endpoints", return_value=_DUMMY_ENDPOINTS
        ), unittest.mock.patch.object(
            gh_pr_watch, "gh_api_list_paginated", paginated_mock
        ), unittest.mock.patch.object(
            gh_pr_watch, "get_review_thread_info", return_value=(set(), 0, [])
        ):
            first = fetch_new_review_items(_DEFAULT_PR, state, fresh_state=False)

        assert len(first) == 1

        # Second call with same state
        paginated_mock = _paginated_side_effect(reviews=reviews)
        with unittest.mock.patch.object(
            gh_pr_watch, "comment_endpoints", return_value=_DUMMY_ENDPOINTS
        ), unittest.mock.patch.object(
            gh_pr_watch, "gh_api_list_paginated", paginated_mock
        ), unittest.mock.patch.object(
            gh_pr_watch, "get_review_thread_info", return_value=(set(), 0, [])
        ):
            second = fetch_new_review_items(_DEFAULT_PR, state, fresh_state=False)

        assert second == [], "Second poll should return nothing — items already seen"

    def test_filter_mixed_reviews_only_actionable_returned(self):
        """Given one non-actionable (APPROVED empty body) and one actionable
        (CHANGES_REQUESTED with body), only the actionable one is returned."""
        reviews = [
            _make_review(id=600, state="APPROVED", body=""),
            _make_review(id=601, state="CHANGES_REQUESTED", body="Please fix"),
        ]
        new_items, state = self._call(reviews)

        assert len(new_items) == 1, (
            f"Expected 1 actionable item, got {len(new_items)}"
        )
        assert new_items[0]["id"] == "601"
        # Both should be marked as seen regardless
        assert "600" in state["seen_review_ids"]
        assert "601" in state["seen_review_ids"]


# ---------------------------------------------------------------------------
# Integration tests — merge readiness (is_pr_ready_to_merge + recommend_actions)
# ---------------------------------------------------------------------------


class TestMergeReadinessIntegration:
    """End-to-end tests combining is_pr_ready_to_merge and recommend_actions
    for Devin-style review scenarios."""

    def _green_pr(self, **overrides):
        base = {
            "closed": False,
            "merged": False,
            "mergeable": "MERGEABLE",
            "merge_state_status": "CLEAN",
            "review_decision": "APPROVED",
        }
        base.update(overrides)
        return base

    def _green_checks(self, **overrides):
        base = {
            "all_terminal": True,
            "failed_count": 0,
            "pending_count": 0,
        }
        base.update(overrides)
        return base

    def test_devin_empty_body_approval_allows_ready_to_merge(self):
        """APPROVED with empty body is filtered upstream so new_review_items
        is empty — PR should be ready to merge."""
        pr = self._green_pr()
        checks = self._green_checks()
        new_review_items = []

        assert is_pr_ready_to_merge(pr, checks, new_review_items) is True
        actions = recommend_actions(pr, checks, [], new_review_items, 0, 3)
        assert "stop_ready_to_merge" in actions

    def test_devin_changes_requested_blocks_ready_to_merge(self):
        """CHANGES_REQUESTED review with a body blocks merge readiness and
        triggers process_review_comment."""
        pr = self._green_pr(review_decision="CHANGES_REQUESTED")
        checks = self._green_checks()
        new_review_items = [
            {
                "kind": "review",
                "state": "CHANGES_REQUESTED",
                "body": "Fix the null check",
                "id": "1",
                "author": "devin-ai-integration[bot]",
            }
        ]

        assert is_pr_ready_to_merge(pr, checks, new_review_items) is False
        actions = recommend_actions(pr, checks, [], new_review_items, 0, 3)
        assert "process_review_comment" in actions

    def test_devin_approval_with_body_blocks_readiness(self):
        """APPROVED review with a non-empty body gets surfaced as a
        new_review_item, which blocks merge readiness."""
        pr = self._green_pr(review_decision="APPROVED")
        checks = self._green_checks()
        new_review_items = [
            {
                "kind": "review",
                "state": "APPROVED",
                "body": "Nice work overall",
                "id": "2",
                "author": "devin-ai-integration[bot]",
            }
        ]

        assert is_pr_ready_to_merge(pr, checks, new_review_items) is False
        actions = recommend_actions(pr, checks, [], new_review_items, 0, 3)
        assert "process_review_comment" in actions


# ---------------------------------------------------------------------------
# Tests — unresolved review threads blocking merge
# ---------------------------------------------------------------------------


class TestUnresolvedThreadsBlockMerge:
    """Tests that unresolved conversation threads block merge readiness
    and trigger the resolve_review_threads action."""

    def _green_pr(self, **overrides):
        base = {
            "closed": False,
            "merged": False,
            "mergeable": "MERGEABLE",
            "merge_state_status": "CLEAN",
            "review_decision": "APPROVED",
        }
        base.update(overrides)
        return base

    def _green_checks(self, **overrides):
        base = {
            "all_terminal": True,
            "failed_count": 0,
            "pending_count": 0,
        }
        base.update(overrides)
        return base

    def test_unresolved_threads_block_ready_to_merge(self):
        """PR with unresolved threads should NOT be ready to merge."""
        pr = self._green_pr()
        checks = self._green_checks()
        assert is_pr_ready_to_merge(pr, checks, [], unresolved_thread_count=2) is False

    def test_zero_unresolved_threads_allows_ready_to_merge(self):
        """PR with zero unresolved threads should be ready to merge."""
        pr = self._green_pr()
        checks = self._green_checks()
        assert is_pr_ready_to_merge(pr, checks, [], unresolved_thread_count=0) is True

    def test_resolve_review_threads_action_recommended(self):
        """When unresolved threads exist but no new review items,
        recommend resolve_review_threads."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(pr, checks, [], [], 0, 3, unresolved_thread_count=2)
        assert "resolve_review_threads" in actions
        assert "stop_ready_to_merge" not in actions

    def test_no_resolve_action_when_new_review_items_present(self):
        """When there are both unresolved threads AND new review items,
        process_review_comment takes priority (not resolve_review_threads)."""
        pr = self._green_pr()
        checks = self._green_checks()
        new_items = [{"kind": "review_comment", "id": "1", "body": "Fix this"}]
        actions = recommend_actions(pr, checks, [], new_items, 0, 3, unresolved_thread_count=1)
        assert "process_review_comment" in actions
        assert "resolve_review_threads" not in actions

    def test_ready_to_merge_when_all_threads_resolved(self):
        """When all conditions met AND no unresolved threads, stop_ready_to_merge."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(pr, checks, [], [], 0, 3, unresolved_thread_count=0)
        assert "stop_ready_to_merge" in actions


# ---------------------------------------------------------------------------
# Tests — --until-merged mode (run_watch stop logic)
# ---------------------------------------------------------------------------

import argparse
from pathlib import Path

run_watch = gh_pr_watch.run_watch


def _make_snapshot(actions, pr_overrides=None):
    """Build a minimal snapshot dict for run_watch tests."""
    pr = {
        "head_sha": "abc123",
        "state": "OPEN",
        "mergeable": "MERGEABLE",
        "merge_state_status": "CLEAN",
        "review_decision": "APPROVED",
        "closed": False,
        "merged": False,
    }
    if pr_overrides:
        pr.update(pr_overrides)
    return {
        "pr": pr,
        "checks": {"all_terminal": True, "failed_count": 0, "pending_count": 0, "passed_count": 10},
        "failed_runs": [],
        "failed_external_checks": [],
        "new_review_items": [],
        "unresolved_threads": {"count": 0, "thread_ids": []},
        "actions": actions,
        "retry_state": {"current_sha_retries_used": 0, "max_flaky_retries": 3},
    }, Path("/tmp/test-state.json")


def _make_args(until_merged=False, poll_seconds=1, require_approval_from=None):
    """Build a minimal args namespace for run_watch."""
    return argparse.Namespace(
        pr="auto",
        repo=None,
        poll_seconds=poll_seconds,
        max_flaky_retries=3,
        state_file=None,
        once=False,
        watch=True,
        retry_failed_now=False,
        require_approval_from=require_approval_from or [],
        until_merged=until_merged,
        json=False,
    )


class TestUntilMergedMode:
    """Tests that --until-merged keeps watching past stop_ready_to_merge."""

    def test_normal_mode_stops_on_ready_to_merge(self):
        """Without --until-merged, run_watch stops on stop_ready_to_merge."""
        args = _make_args(until_merged=False)
        snapshot = _make_snapshot(["stop_ready_to_merge"])
        call_count = 0

        def fake_collect(a):
            nonlocal call_count
            call_count += 1
            return snapshot

        with unittest.mock.patch.object(gh_pr_watch, "collect_snapshot", fake_collect), \
             unittest.mock.patch.object(gh_pr_watch, "print_event"):
            result = run_watch(args)

        assert result == 0
        assert call_count == 1

    def test_until_merged_continues_past_ready_to_merge(self):
        """With --until-merged, run_watch does NOT stop on stop_ready_to_merge
        but DOES stop on stop_pr_closed."""
        args = _make_args(until_merged=True)
        ready_snapshot = _make_snapshot(["stop_ready_to_merge"])
        closed_snapshot = _make_snapshot(
            ["stop_pr_closed"],
            pr_overrides={"closed": False, "merged": True, "state": "MERGED"},
        )
        call_count = 0

        def fake_collect(a):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return ready_snapshot
            return closed_snapshot

        with unittest.mock.patch.object(gh_pr_watch, "collect_snapshot", fake_collect), \
             unittest.mock.patch.object(gh_pr_watch, "print_event"), \
             unittest.mock.patch("time.sleep"):
            result = run_watch(args)

        assert result == 0
        assert call_count == 2, "Should have polled twice: once ready_to_merge (continued), once closed (stopped)"

    def test_until_merged_continues_past_exhausted_retries(self):
        """With --until-merged, run_watch does NOT stop on stop_exhausted_retries."""
        args = _make_args(until_merged=True)
        exhausted_snapshot = _make_snapshot(["stop_exhausted_retries"])
        closed_snapshot = _make_snapshot(
            ["stop_pr_closed"],
            pr_overrides={"closed": True, "merged": False, "state": "CLOSED"},
        )
        call_count = 0

        def fake_collect(a):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return exhausted_snapshot
            return closed_snapshot

        with unittest.mock.patch.object(gh_pr_watch, "collect_snapshot", fake_collect), \
             unittest.mock.patch.object(gh_pr_watch, "print_event"), \
             unittest.mock.patch("time.sleep"):
            result = run_watch(args)

        assert result == 0
        assert call_count == 2

    def test_until_merged_stops_on_pr_closed(self):
        """With --until-merged, run_watch still stops immediately on stop_pr_closed."""
        args = _make_args(until_merged=True)
        snapshot = _make_snapshot(
            ["stop_pr_closed"],
            pr_overrides={"closed": False, "merged": True, "state": "MERGED"},
        )

        with unittest.mock.patch.object(gh_pr_watch, "collect_snapshot", lambda a: snapshot), \
             unittest.mock.patch.object(gh_pr_watch, "print_event"):
            result = run_watch(args)

        assert result == 0

    def test_normal_mode_stops_on_exhausted_retries(self):
        """Without --until-merged, run_watch stops on stop_exhausted_retries."""
        args = _make_args(until_merged=False)
        snapshot = _make_snapshot(["stop_exhausted_retries"])

        with unittest.mock.patch.object(gh_pr_watch, "collect_snapshot", lambda a: snapshot), \
             unittest.mock.patch.object(gh_pr_watch, "print_event"):
            result = run_watch(args)

        assert result == 0


# ---------------------------------------------------------------------------
# Tests — check_required_approvals
# ---------------------------------------------------------------------------


class TestCheckRequiredApprovals:
    """Tests for check_required_approvals function."""

    def _call(self, required_logins, reviews):
        """Helper: call check_required_approvals with mocked API."""
        with unittest.mock.patch.object(
            gh_pr_watch, "gh_api_list_paginated", return_value=reviews
        ):
            return check_required_approvals("owner/repo", 1, required_logins)

    def test_empty_required_logins_always_satisfied(self):
        result = self._call([], [])
        assert result["satisfied"] is True
        assert result["missing"] == []

    def test_approved_review_satisfies(self):
        reviews = [
            _make_review(id=1, state="APPROVED", user={"login": "bolt-runner[bot]"}),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is True
        assert result["missing"] == []
        assert result["details"]["bolt-runner[bot]"] == "approved"

    def test_no_review_from_required_login(self):
        reviews = [
            _make_review(id=1, state="APPROVED", user={"login": "alice"}),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is False
        assert "bolt-runner[bot]" in result["missing"]
        assert result["details"]["bolt-runner[bot]"] == "no_review"

    def test_changes_requested_not_satisfied(self):
        reviews = [
            _make_review(id=1, state="CHANGES_REQUESTED", user={"login": "bolt-runner[bot]"}),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is False
        assert "bolt-runner[bot]" in result["missing"]
        assert result["details"]["bolt-runner[bot]"] == "changes_requested"

    def test_latest_review_wins(self):
        """If bolt-runner first requests changes then approves, should be satisfied."""
        reviews = [
            _make_review(
                id=1, state="CHANGES_REQUESTED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-01T00:00:00Z",
            ),
            _make_review(
                id=2, state="APPROVED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is True

    def test_latest_review_wins_reverse_order(self):
        """If bolt-runner approves then requests changes, should NOT be satisfied."""
        reviews = [
            _make_review(
                id=1, state="APPROVED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-01T00:00:00Z",
            ),
            _make_review(
                id=2, state="CHANGES_REQUESTED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is False

    def test_case_insensitive_login_match(self):
        reviews = [
            _make_review(id=1, state="APPROVED", user={"login": "Bolt-Runner[bot]"}),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is True

    def test_commented_after_approved_does_not_revoke(self):
        """COMMENTED review after APPROVED should NOT revoke approval.
        GitHub does not change approval state on COMMENTED reviews."""
        reviews = [
            _make_review(
                id=1, state="APPROVED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-01T00:00:00Z",
            ),
            _make_review(
                id=2, state="COMMENTED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is True
        assert result["details"]["bolt-runner[bot]"] == "approved"

    def test_pending_after_approved_does_not_revoke(self):
        """PENDING review after APPROVED should NOT revoke approval."""
        reviews = [
            _make_review(
                id=1, state="APPROVED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-01T00:00:00Z",
            ),
            _make_review(
                id=2, state="PENDING",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is True

    def test_changes_requested_after_approved_revokes(self):
        """CHANGES_REQUESTED after APPROVED SHOULD revoke approval."""
        reviews = [
            _make_review(
                id=1, state="APPROVED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-01T00:00:00Z",
            ),
            _make_review(
                id=2, state="CHANGES_REQUESTED",
                user={"login": "bolt-runner[bot]"},
                submitted_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], reviews)
        assert result["satisfied"] is False


# ---------------------------------------------------------------------------
# Tests — required approvals blocking merge readiness
# ---------------------------------------------------------------------------


class TestRequiredApprovalsBlockMerge:
    """Tests that required_approvals_satisfied=False blocks merge readiness."""

    def _green_pr(self, **overrides):
        base = {
            "closed": False,
            "merged": False,
            "mergeable": "MERGEABLE",
            "merge_state_status": "CLEAN",
            "review_decision": "APPROVED",
        }
        base.update(overrides)
        return base

    def _green_checks(self, **overrides):
        base = {
            "all_terminal": True,
            "failed_count": 0,
            "pending_count": 0,
        }
        base.update(overrides)
        return base

    def test_unsatisfied_required_approvals_blocks_ready_to_merge(self):
        pr = self._green_pr()
        checks = self._green_checks()
        assert is_pr_ready_to_merge(pr, checks, [], required_approvals_satisfied=False) is False

    def test_satisfied_required_approvals_allows_ready_to_merge(self):
        pr = self._green_pr()
        checks = self._green_checks()
        assert is_pr_ready_to_merge(pr, checks, [], required_approvals_satisfied=True) is True

    def test_recommend_actions_idle_when_waiting_for_approval(self):
        """When everything is green but required approval missing, should idle (not stop)."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(pr, checks, [], [], 0, 3, required_approvals_satisfied=False)
        assert "stop_ready_to_merge" not in actions
        assert "idle" in actions

    def test_recommend_actions_stop_when_approval_satisfied(self):
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(pr, checks, [], [], 0, 3, required_approvals_satisfied=True)
        assert "stop_ready_to_merge" in actions

    def test_bolt_runner_changes_requested_surfaces_review(self):
        """bolt-runner CHANGES_REQUESTED should trigger process_review_comment."""
        pr = self._green_pr(review_decision="CHANGES_REQUESTED")
        checks = self._green_checks()
        new_review_items = [
            {
                "kind": "review",
                "state": "CHANGES_REQUESTED",
                "body": "Please fix the error handling",
                "id": "1",
                "author": "bolt-runner[bot]",
            }
        ]
        actions = recommend_actions(
            pr, checks, [], new_review_items, 0, 3, required_approvals_satisfied=False,
        )
        assert "process_review_comment" in actions
        assert "stop_ready_to_merge" not in actions


# ---------------------------------------------------------------------------
# Tests — check_review_bot_comment_status
# ---------------------------------------------------------------------------


def _make_issue_comment(login, body, created_at="2026-01-01T00:00:00Z"):
    return {
        "user": {"login": login},
        "body": body,
        "created_at": created_at,
    }


class TestCheckReviewBotCommentStatus:
    """Tests for check_review_bot_comment_status function."""

    def _call(self, required_logins, comments):
        with unittest.mock.patch.object(
            gh_pr_watch, "gh_api_list_paginated", return_value=comments,
        ):
            return check_review_bot_comment_status("owner/repo", 1, required_logins)

    def test_empty_required_logins(self):
        assert self._call([], []) == {}

    def test_no_comments(self):
        result = self._call(["bolt-runner[bot]"], [])
        assert result == {"bolt-runner[bot]": "unknown"}

    def test_completed_status(self):
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:completed -->\n✅ Review done.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "completed"

    def test_failed_status(self):
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:failed -->\n❌ Error.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "failed"

    def test_in_progress_status(self):
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:in_progress -->\n🔍 Reviewing...",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "in_progress"

    def test_latest_comment_wins(self):
        """When multiple comments exist, the latest by created_at wins."""
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:completed -->\n✅ Done.",
                created_at="2026-01-01T00:00:00Z",
            ),
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:failed -->\n❌ Error.",
                created_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "failed"

    def test_latest_comment_wins_reverse(self):
        """Failed then completed — latest (completed) wins."""
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:failed -->\n❌ Error.",
                created_at="2026-01-01T00:00:00Z",
            ),
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:completed -->\n✅ Done.",
                created_at="2026-01-02T00:00:00Z",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "completed"

    def test_ignores_comments_without_status_marker(self):
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "Just a regular comment without any status marker.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "unknown"

    def test_ignores_comments_from_other_users(self):
        comments = [
            _make_issue_comment(
                "alice",
                "<!-- bolt-review-status:failed -->\n❌ Error.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "unknown"

    def test_cancelled_status(self):
        comments = [
            _make_issue_comment(
                "bolt-runner[bot]",
                "<!-- bolt-review-status:cancelled -->\n🚫 Cancelled.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "cancelled"

    def test_case_insensitive_login(self):
        comments = [
            _make_issue_comment(
                "Bolt-Runner[bot]",
                "<!-- bolt-review-status:completed -->\n✅ Done.",
            ),
        ]
        result = self._call(["bolt-runner[bot]"], comments)
        assert result["bolt-runner[bot]"] == "completed"


# ---------------------------------------------------------------------------
# Tests — retrigger_review action in recommend_actions
# ---------------------------------------------------------------------------


class TestRetriggerReviewAction:
    """Tests that retrigger_review is recommended when a required reviewer's
    review bot has failed."""

    def _green_pr(self, **overrides):
        base = {
            "closed": False,
            "merged": False,
            "mergeable": "MERGEABLE",
            "merge_state_status": "CLEAN",
            "review_decision": "APPROVED",
        }
        base.update(overrides)
        return base

    def _green_checks(self, **overrides):
        base = {
            "all_terminal": True,
            "failed_count": 0,
            "pending_count": 0,
        }
        base.update(overrides)
        return base

    def test_retrigger_review_when_bot_failed(self):
        """When review bot failed and approval missing, recommend retrigger_review."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(
            pr, checks, [], [], 0, 3,
            required_approvals_satisfied=False,
            review_bot_needs_retrigger=True,
        )
        assert "retrigger_review" in actions
        assert "stop_ready_to_merge" not in actions

    def test_no_retrigger_when_bot_succeeded(self):
        """When review bot completed, no retrigger needed."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(
            pr, checks, [], [], 0, 3,
            required_approvals_satisfied=False,
            review_bot_needs_retrigger=False,
        )
        assert "retrigger_review" not in actions

    def test_no_retrigger_when_approval_satisfied(self):
        """When approval already satisfied, no retrigger even if flag is set."""
        pr = self._green_pr()
        checks = self._green_checks()
        actions = recommend_actions(
            pr, checks, [], [], 0, 3,
            required_approvals_satisfied=True,
            review_bot_needs_retrigger=True,
        )
        # Should be ready to merge despite retrigger flag
        assert "stop_ready_to_merge" in actions
        # retrigger_review should not appear because stop_ready_to_merge short-circuits
        assert "retrigger_review" not in actions

    def test_no_retrigger_with_ci_failure(self):
        """retrigger_review deferred when higher-priority CI work exists."""
        pr = self._green_pr()
        checks = self._green_checks(failed_count=1, all_terminal=True)
        actions = recommend_actions(
            pr, checks, [{"run_id": 1}], [], 0, 3,
            required_approvals_satisfied=False,
            review_bot_needs_retrigger=True,
        )
        assert "retrigger_review" not in actions
        assert "diagnose_ci_failure" in actions

    def test_no_retrigger_with_review_items(self):
        """retrigger_review deferred when review feedback needs processing."""
        pr = self._green_pr()
        checks = self._green_checks()
        new_items = [{"kind": "review", "id": "1", "body": "Fix this"}]
        actions = recommend_actions(
            pr, checks, [], new_items, 0, 3,
            required_approvals_satisfied=False,
            review_bot_needs_retrigger=True,
        )
        assert "retrigger_review" not in actions
        assert "process_review_comment" in actions

    def test_no_retrigger_when_pr_closed(self):
        """retrigger_review should not appear when PR is closed."""
        pr = self._green_pr(closed=True, merged=True)
        checks = self._green_checks()
        actions = recommend_actions(
            pr, checks, [], [], 0, 3,
            required_approvals_satisfied=False,
            review_bot_needs_retrigger=True,
        )
        assert "retrigger_review" not in actions
        assert "stop_pr_closed" in actions


# ---------------------------------------------------------------------------
# Tests — cancelled/in_progress bot status does NOT trigger retrigger
# ---------------------------------------------------------------------------


class TestRetriggerOnlyOnFailed:
    """Verify that only 'failed' bot status produces review_bot_needs_retrigger=True
    when wired through the collect_snapshot logic (simulated here)."""

    def _needs_retrigger(self, bot_status_map, missing_logins):
        """Reproduce the logic from collect_snapshot."""
        return any(
            bot_status_map.get(login) == "failed"
            for login in missing_logins
        )

    def test_failed_needs_retrigger(self):
        assert self._needs_retrigger(
            {"bolt-runner[bot]": "failed"}, ["bolt-runner[bot]"]
        ) is True

    def test_completed_no_retrigger(self):
        assert self._needs_retrigger(
            {"bolt-runner[bot]": "completed"}, ["bolt-runner[bot]"]
        ) is False

    def test_in_progress_no_retrigger(self):
        assert self._needs_retrigger(
            {"bolt-runner[bot]": "in_progress"}, ["bolt-runner[bot]"]
        ) is False

    def test_cancelled_no_retrigger(self):
        assert self._needs_retrigger(
            {"bolt-runner[bot]": "cancelled"}, ["bolt-runner[bot]"]
        ) is False

    def test_unknown_no_retrigger(self):
        assert self._needs_retrigger(
            {"bolt-runner[bot]": "unknown"}, ["bolt-runner[bot]"]
        ) is False
