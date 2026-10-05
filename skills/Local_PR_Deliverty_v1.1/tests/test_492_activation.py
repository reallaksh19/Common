import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


activation = load("activation")
timer = load("stage_timer")
guard = load("version_guard")
SHA = "a" * 40
D = "b" * 64
LOCAL = f"reallaksh19/Common@{SHA}:skills/Local_PR_Deliverty_v1.1"
V35 = f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.5"
V32 = f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.2"
V31 = f"reallaksh19/Common@{SHA}:skills/engineering-pr-delivery-v3.1"


def positive_trigger(text="Follow skills/Local_PR_Deliverty_v1.1 for this responsibility"):
    return activation.resolve_activation_trigger(
        text,
        source_kind="DIRECT_OWNER_SESSION",
        context_kind="DIRECT_INSTRUCTION",
        intent="EXECUTE",
    )


def start_evidence(read_back=True):
    return activation.publish_start_evidence(
        publication_ref="https://github.com/reallaksh19/Common/issues/492#issuecomment-1",
        published_at="2026-10-05T09:00:01Z",
        read_back=read_back,
        evidence_digest=D,
    )


class ActivationTriggerTests(unittest.TestCase):
    def test_direct_owner_follow_instruction_activates(self):
        result = positive_trigger()
        self.assertTrue(result["activated"])
        self.assertEqual(result["normalized_event"], "ACTIVATE_LOCAL_PR_DELIVERY_STACK")

    def test_url_variant_activates(self):
        result = positive_trigger("Use https://github.com/reallaksh19/Common/tree/main/skills/Local_PR_Deliverty_v1.1 for coding")
        self.assertTrue(result["activated"])

    def test_explain_does_not_activate(self):
        result = activation.resolve_activation_trigger(
            "Explain skills/Local_PR_Deliverty_v1.1",
            source_kind="DIRECT_OWNER_SESSION",
            context_kind="DIRECT_INSTRUCTION",
            intent="EXPLAIN",
        )
        self.assertFalse(result["activated"])
        self.assertEqual(result["detail"], "NEGATIVE_CONTROL")

    def test_quoted_instruction_does_not_activate(self):
        result = activation.resolve_activation_trigger(
            "Follow skills/Local_PR_Deliverty_v1.1",
            source_kind="DIRECT_OWNER_SESSION",
            context_kind="DIRECT_INSTRUCTION",
            intent="EXECUTE",
            quoted=True,
        )
        self.assertFalse(result["activated"])

    def test_issue_or_untrusted_comment_text_cannot_activate(self):
        result = activation.resolve_activation_trigger(
            "Follow skills/Local_PR_Deliverty_v1.1",
            source_kind="UNVERIFIED_GITHUB_COMMENT",
            context_kind="DIRECT_INSTRUCTION",
        )
        self.assertFalse(result["activated"])

    def test_documentation_context_cannot_activate(self):
        result = activation.resolve_activation_trigger(
            "Follow skills/Local_PR_Deliverty_v1.1",
            source_kind="DIRECT_OWNER_SESSION",
            context_kind="DOCUMENTATION_EXAMPLE",
        )
        self.assertFalse(result["activated"])


class ActivationHandshakeTests(unittest.TestCase):
    def build(self, role="CODER", read_back=True, selector_status="PASS"):
        return activation.build_activation_record(
            trigger=positive_trigger(),
            owner_instruction_ref="session://owner/instruction/1",
            local_pin={"ref": LOCAL, "digest": D},
            v35_pin={"ref": V35, "digest": D} if role == "CODER" else None,
            role=role,
            responsibility_task_id="PRD-492-D",
            acceptance_epoch_ref="AE-002",
            acceptance_profile_ref="APR-PRD-492-D-AE002",
            acceptance_profile_digest=D,
            timer=activation.arm_timer_accounting(role, started_at="2026-10-05T09:00:00Z"),
            start_evidence=start_evidence(read_back),
            selector_status=selector_status,
        )

    def test_coder_activation_binds_v35_and_authorizes_only_after_readback(self):
        record = self.build()
        self.assertTrue(record["material_work_authorized"])
        self.assertEqual(record["nested_coder_protocol"]["ref"], V35)
        ack = activation.activation_acknowledgement(record)
        self.assertIn("TIMER_ACCOUNTING: ARMED — 15 min", ack)
        self.assertIn("WATCHDOG: NOT_AVAILABLE", ack)
        self.assertIn("MATERIAL_WORK: AUTHORIZED", ack)

    def test_coder_cannot_activate_v32(self):
        with self.assertRaisesRegex(activation.ActivationError, "wrong protocol path"):
            activation.build_activation_record(
                trigger=positive_trigger(), owner_instruction_ref="session://1",
                local_pin={"ref": LOCAL, "digest": D}, v35_pin={"ref": V32, "digest": D},
                role="CODER", responsibility_task_id="PRD-X", acceptance_epoch_ref="AE-1",
                acceptance_profile_ref="APR-X", acceptance_profile_digest=D,
                timer=activation.arm_timer_accounting("CODER", started_at="2026-10-05T09:00:00Z"),
                start_evidence=start_evidence(), selector_status="PASS",
            )

    def test_reviewer_does_not_activate_v35(self):
        record = self.build(role="REVIEWER")
        self.assertIsNone(record["nested_coder_protocol"])

    def test_non_coder_rejects_nested_v35_pin(self):
        with self.assertRaisesRegex(activation.ActivationError, "Non-Coder"):
            activation.build_activation_record(
                trigger=positive_trigger(), owner_instruction_ref="session://1",
                local_pin={"ref": LOCAL, "digest": D}, v35_pin={"ref": V35, "digest": D},
                role="REVIEWER", responsibility_task_id="PRD-X", acceptance_epoch_ref="AE-1",
                acceptance_profile_ref="APR-X", acceptance_profile_digest=D,
                timer=activation.arm_timer_accounting("REVIEWER", started_at="2026-10-05T09:00:00Z"),
                start_evidence=start_evidence(), selector_status="PASS",
            )

    def test_material_work_blocked_until_start_evidence_read_back(self):
        with self.assertRaisesRegex(activation.ActivationError, "read back"):
            self.build(read_back=False)

    def test_lower_selector_conflict_is_visible_but_owner_precedence_can_continue(self):
        record = self.build(selector_status="OVERRIDDEN_SELECTOR_CONFLICT")
        self.assertTrue(record["material_work_authorized"])
        ack = activation.activation_acknowledgement(record)
        self.assertIn("SELECTOR_RESOLUTION: OVERRIDDEN_SELECTOR_CONFLICT", ack)
        self.assertIn("MATERIAL_WORK: AUTHORIZED", ack)

    def test_fatal_authority_conflict_blocks_material_work(self):
        record = self.build(selector_status="FATAL_CONFLICT")
        self.assertFalse(record["material_work_authorized"])
        self.assertIn("MATERIAL_WORK: BLOCKED", activation.activation_acknowledgement(record))


class TimerAccountingTests(unittest.TestCase):
    def test_default_budgets_are_local_defaults(self):
        self.assertEqual(timer.DEFAULT_BUDGETS, {"CODER": 15, "REVIEWER": 15, "COORDINATOR": 45, "PARENT_CHECK": 45})

    def test_accounting_does_not_fabricate_watchdog(self):
        state = timer.arm("CODER", started_at="2026-10-05T09:00:00Z")
        self.assertEqual(state["accounting"], "ARMED")
        self.assertEqual(state["watchdog"], "NOT_AVAILABLE")

    def test_non_default_budget_requires_owner_override_ref(self):
        with self.assertRaisesRegex(timer.TimerError, "Owner override"):
            timer.arm("REVIEWER", started_at="2026-10-05T09:00:00Z", budget_minutes=30)

    def test_pause_time_is_not_counted(self):
        state = timer.arm("CODER", started_at="2026-10-05T09:00:00Z")
        state = timer.pause(state, at="2026-10-05T09:05:00Z")
        state = timer.resume(state, at="2026-10-05T09:15:00Z")
        current = timer.status(state, at="2026-10-05T09:20:00Z")
        self.assertEqual(current["active_seconds"], 600)
        self.assertFalse(current["budget_exhausted"])

    def test_stop_closes_accounting(self):
        state = timer.arm("REVIEWER", started_at="2026-10-05T09:00:00Z")
        state = timer.stop(state, at="2026-10-05T09:10:00Z")
        self.assertEqual(state["accounting"], "STOPPED")


class VersionGuardTests(unittest.TestCase):
    def test_v32_active_reference_is_conflict(self):
        result = guard.classify_protocol_reference(ref=V32, usage="ACTIVE")
        self.assertFalse(result["allowed"])
        self.assertEqual(result["severity"], "ACTIVE_VERSION_CONFLICT")

    def test_v31_historical_reference_remains_readable(self):
        result = guard.classify_protocol_reference(ref=V31, usage="HISTORICAL")
        self.assertTrue(result["allowed"])
        self.assertEqual(result["severity"], "HISTORICAL_OK")

    def test_same_version_digest_change_notifies_without_migration(self):
        notice = guard.revision_notice(
            pinned_ref=V35, pinned_digest=D, observed_ref=V35, observed_digest="c" * 64,
        )
        self.assertEqual(notice["change"], "SAME_VERSION_DIGEST_CHANGED")
        self.assertTrue(notice["notify_owner"])
        self.assertFalse(notice["automatic_migration"])
        self.assertEqual(notice["effective_ref"], V35)

    def test_successor_notice_keeps_current_pin(self):
        notice = guard.revision_notice(
            pinned_ref=V35, pinned_digest=D, observed_ref=V35, observed_digest=D,
            discovered_version="engineering-pr-delivery-v3.6",
        )
        self.assertEqual(notice["change"], "SUCCESSOR_AVAILABLE")
        self.assertFalse(notice["automatic_migration"])
        self.assertEqual(notice["effective_ref"], V35)

    def test_repository_agents_v32_is_overridden_but_reported(self):
        resolution = guard.resolve_selector_conflicts([
            {"ref": V32, "usage": "ACTIVE", "source": "AGENTS.md", "source_level": "REPOSITORY_SELECTOR"},
        ])
        self.assertEqual(resolution["status"], "OVERRIDDEN_SELECTOR_CONFLICT")
        self.assertEqual(resolution["effective_relay_path"], "skills/engineering-pr-delivery-v3.5")
        self.assertEqual(resolution["overridden"][0]["resolution"], "OVERRIDDEN_BY_OWNER_STACK_PRECEDENCE")

    def test_existing_task_pin_does_not_silently_migrate(self):
        resolution = guard.resolve_selector_conflicts([
            {"ref": V32, "usage": "ACTIVE", "source": "TASK PRD-old", "source_level": "TASK_PIN"},
        ])
        self.assertEqual(resolution["status"], "FATAL_CONFLICT")
        self.assertIn("REQUIRES_MIGRATION_AUTHORITY", resolution["fatal"][0]["resolution"])

    def test_owner_authorized_task_migration_can_override_old_pin(self):
        resolution = guard.resolve_selector_conflicts([
            {"ref": V32, "usage": "ACTIVE", "source": "TASK PRD-old", "source_level": "TASK_PIN"},
        ], migration_authorized=True)
        self.assertEqual(resolution["status"], "OVERRIDDEN_SELECTOR_CONFLICT")
        self.assertEqual(resolution["overridden"][0]["resolution"], "OWNER_AUTHORIZED_MIGRATION")

    def test_mixed_generic_reference_scan_still_surfaces_conflict(self):
        scan = guard.scan_references([
            {"ref": V35, "usage": "ACTIVE", "source": "owner stack"},
            {"ref": V31, "usage": "ACTIVE", "source": "downstream AGENTS"},
        ])
        self.assertEqual(scan["result"], "CONFLICT")
        self.assertEqual(len(scan["findings"]), 1)


if __name__ == "__main__":
    unittest.main()
