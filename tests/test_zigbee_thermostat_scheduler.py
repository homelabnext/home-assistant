"""Offline tests for thermostat weekday profiles and manual override detection."""
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import unittest

import yaml
from jinja2 import Environment, StrictUndefined


class BlueprintLoader(yaml.SafeLoader):
    pass


BlueprintLoader.add_constructor(
    "!input", lambda loader, node: {"input": loader.construct_scalar(node)}
)
ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = yaml.load(
    (ROOT / "blueprints/automation/zigbee_thermostat_scheduler/zigbee_thermostat_scheduler.yaml").read_text(),
    Loader=BlueprintLoader,
)
ENV = Environment(undefined=StrictUndefined)
SCHEDULE_TEMPLATE = BLUEPRINT["variables"]["scheduled_now"]
MANUAL_CHANGE_TEMPLATE = BLUEPRINT["variables"]["manual_change_detected"]


def schedule_is_active(moment, **values):
    context = {
        "now": lambda: moment,
        "profile_1_days": ["mon", "tue", "wed", "thu", "fri"],
        "profile_1_start": "06:00:00",
        "profile_1_end": "22:00:00",
        "profile_1_second_window_enabled": False,
        "profile_1_second_start": "16:00:00",
        "profile_1_second_end": "22:00:00",
        "profile_2_days": ["sat", "sun"],
        "profile_2_start": "08:00:00",
        "profile_2_end": "23:00:00",
        "profile_2_second_window_enabled": False,
        "profile_2_second_start": "16:00:00",
        "profile_2_second_end": "23:00:00",
        "profile_3_days": [],
        "profile_3_start": "06:00:00",
        "profile_3_end": "22:00:00",
        "profile_3_second_window_enabled": False,
        "profile_3_second_start": "16:00:00",
        "profile_3_second_end": "22:00:00",
    }
    context.update(values)
    result = ENV.from_string(SCHEDULE_TEMPLATE).render(**context).strip()
    return result.lower() == "true"


def climate_state(state, attrs, parent_id=None, user_id=None):
    return SimpleNamespace(
        state=state,
        attributes=attrs,
        context=SimpleNamespace(parent_id=parent_id, user_id=user_id),
    )


def manual_change_is_detected(from_state, to_state):
    return ENV.from_string(MANUAL_CHANGE_TEMPLATE).render(
        manual_override_until_helper="input_datetime.thermostat_override_until",
        trigger=SimpleNamespace(
            id="thermostat_changed", from_state=from_state, to_state=to_state
        ),
    ).strip().lower() == "true"


class ThermostatSchedulerTests(unittest.TestCase):
    def test_weekday_profiles_have_independent_schedules(self):
        profile_1 = {
            "profile_1_days": ["mon"],
            "profile_1_start": "07:00:00",
            "profile_1_end": "09:00:00",
            "profile_2_days": ["tue"],
            "profile_2_start": "08:00:00",
            "profile_2_end": "10:00:00",
        }
        self.assertTrue(schedule_is_active(datetime(2026, 10, 26, 7, 30), **profile_1))
        self.assertFalse(schedule_is_active(datetime(2026, 10, 27, 7, 30), **profile_1))
        self.assertTrue(schedule_is_active(datetime(2026, 10, 27, 8, 30), **profile_1))

    def test_overnight_window_uses_profile_of_start_day(self):
        profiles = {
            "profile_1_days": ["sun"],
            "profile_1_start": "20:00:00",
            "profile_1_end": "02:00:00",
            "profile_2_days": ["mon"],
            "profile_2_start": "08:00:00",
            "profile_2_end": "10:00:00",
        }
        self.assertTrue(schedule_is_active(datetime(2026, 10, 26, 1, 0), **profiles))
        self.assertFalse(schedule_is_active(datetime(2026, 10, 26, 2, 0), **profiles))

    def test_first_profile_owns_day_if_selected_more_than_once(self):
        profiles = {
            "profile_1_days": ["mon"],
            "profile_1_start": "08:00:00",
            "profile_1_end": "10:00:00",
            "profile_2_days": ["mon"],
            "profile_2_start": "06:00:00",
            "profile_2_end": "22:00:00",
        }
        self.assertFalse(schedule_is_active(datetime(2026, 10, 26, 7, 0), **profiles))

    def test_only_unparented_target_changes_activate_override(self):
        before = climate_state("heat", {"temperature": 20, "current_temperature": 19})
        manual = climate_state("heat", {"temperature": 22, "current_temperature": 19})
        scheduled = climate_state(
            "heat", {"temperature": 22, "current_temperature": 19}, parent_id="automation"
        )
        current_only = climate_state(
            "heat", {"temperature": 20, "current_temperature": 20}
        )
        self.assertTrue(manual_change_is_detected(before, manual))
        self.assertFalse(manual_change_is_detected(before, scheduled))
        self.assertFalse(manual_change_is_detected(before, current_only))


if __name__ == "__main__":
    unittest.main()
