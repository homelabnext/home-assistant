"""Offline behavior tests; run with Python, PyYAML and Jinja2 installed.

These exercise the blueprint's actual decision template, not the HA scheduler.
"""
import json
import ast
import unittest
from pathlib import Path
from types import SimpleNamespace
from datetime import datetime, timezone

import yaml
from jinja2 import StrictUndefined
from jinja2.nativetypes import NativeEnvironment


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda loader, node: {'input': loader.construct_scalar(node)})
ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = yaml.load((ROOT / 'blueprints/automation/ventilation_notification/ventilation_notification.yaml').read_text(), Loader=Loader)
ENV = NativeEnvironment(undefined=StrictUndefined)


def from_json(value, default):
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return default


ENV.filters['from_json'] = from_json
ENV.filters['to_json'] = json.dumps
TEMPLATE = ENV.from_string(BLUEPRINT['actions'][2]['variables']['result'])


class Room:
    def __init__(self, **options):
        self.now = 1800000000
        self.memory = ''
        self.states = {'ti': '20', 'hi': '65', 'to': '5', 'ho': '80', 'window': 'off'}
        self.units = {'ti': '°C', 'to': '°C', 'hi': '%', 'ho': '%'}
        self.options = dict(ti_entity='ti', hi_entity='hi', to_entity='to', ho_entity='ho',
                            contacts=['window'], memory_entity='memory', high=60, target_humidity=55,
                            margin_min=1, warning_delay=10, close_delay=2, max_open=15, min_temp=17,
                            blocked_enabled=True, repeats=False, repeat_interval=60, room='Testzimmer')
        self.options.update(options)

    def step(self, seconds=0, trigger=None, **states):
        self.now += seconds
        self.states.update({k: str(v) for k, v in states.items()})
        result = TEMPLATE.render(**self.options, trigger=trigger or {'id': 'tick'},
                                 states=lambda entity: self.memory if entity == 'memory' else self.states.get(entity, 'unknown'),
                                 state_attr=lambda entity, attr: self.units.get(entity),
                                 is_state=lambda entity, value: self.states.get(entity) == value,
                                 now=lambda: datetime.fromtimestamp(self.now, timezone.utc),
                                 as_timestamp=lambda value: value.timestamp())
        # Home Assistant strips rendered whitespace before parsing native values.
        if isinstance(result, str):
            result = ast.literal_eval(result.strip())
        self.memory = json.dumps(result['memory'])
        assert len(self.memory) <= 255
        return result

    def minutes(self, count, **states):
        results = []
        for _ in range(count):
            results.append(self.step(60, **states))
        return results


class VentilationTests(unittest.TestCase):
    def test_winter_confirmation_and_no_repeat(self):
        room = Room()
        self.assertFalse(room.step()['send'])
        self.assertFalse(any(x['send'] for x in room.minutes(9)))
        result = room.step(60)
        self.assertTrue(result['send'])
        self.assertEqual(result['code'], 'vent')
        self.assertFalse(any(x['send'] for x in room.minutes(120)))

    def test_repeat_interval(self):
        room = Room(repeats=True, repeat_interval=5)
        room.step()
        self.assertTrue(room.minutes(10)[-1]['send'])
        self.assertFalse(any(x['send'] for x in room.minutes(4)))
        self.assertTrue(room.minutes(1)[-1]['send'])

    def test_humid_summer_is_blocked(self):
        room = Room()
        room.step(to=30, ho=80)
        result = room.minutes(10)[-1]
        self.assertTrue(result['send'])
        self.assertEqual(result['code'], 'blocked')

    def test_switching_recommendation_restarts_confirmation(self):
        room = Room()
        room.step()
        room.minutes(9)
        room.step(to=30, ho=80)
        self.assertFalse(any(x['send'] for x in room.minutes(2)))
        room.step(to=5, ho=80)
        self.assertFalse(any(x['send'] for x in room.minutes(9)))
        self.assertTrue(room.minutes(1)[-1]['send'])

    def test_any_open_window_and_unknown_contact(self):
        room = Room(contacts=['window', 'window2'])
        room.step(window2='on')
        self.assertGreater(json.loads(room.memory)['o'], 0)
        self.assertEqual(room.step(window2='unknown')['code'], 'invalid')

    def test_blocked_can_be_silent(self):
        room = Room(blocked_enabled=False)
        room.step(to=30, ho=80)
        self.assertFalse(any(x['send'] for x in room.minutes(20)))

    def test_percent_comparison_is_not_used(self):
        room = Room()
        result = room.step(to=0, ho=95)
        self.assertEqual(result['code'], 'vent')

    def test_same_moisture_at_different_temperature_does_not_recommend(self):
        room = Room()
        # Equal water vapor pressure at 20°C/65% and 30°C/~35.9%.
        result = room.step(to=30, ho=35.9)
        self.assertEqual(result['code'], 'blocked')

    def test_unknown_cancels_confirmation(self):
        room = Room()
        room.step()
        room.minutes(9)
        self.assertEqual(room.step(hi='unknown')['code'], 'invalid')
        room.step(hi=65)
        self.assertFalse(any(x['send'] for x in room.minutes(9)))
        self.assertTrue(room.minutes(1)[-1]['send'])

    def test_bad_sensor_and_units(self):
        for entity, value in [('hi','nan'),('ho','unavailable'),('ti','inf'),('ho',0),('window','unavailable')]:
            room = Room()
            self.assertFalse(room.step(**{entity:value})['send'])
            self.assertEqual(json.loads(room.memory)['c'], 'idle')
        room = Room()
        room.units['ti'] = '°F'
        self.assertEqual(room.step()['code'], 'invalid')

    def test_queued_unknown_resets_after_recovery(self):
        room = Room()
        room.step()
        room.minutes(9)
        result = room.step(trigger={'id':'sensor','to_state':SimpleNamespace(state='unavailable')})
        self.assertEqual(result['code'], 'invalid')

    def test_target_resets_episode(self):
        room = Room()
        room.step()
        room.minutes(10)
        room.step(hi=54)
        self.assertFalse(json.loads(room.memory)['n'])
        room.step(hi=65)
        self.assertTrue(room.minutes(10)[-1]['send'])

    def test_humidity_hysteresis(self):
        room = Room()
        room.step()
        result = room.step(hi=58)
        self.assertTrue(result['memory']['n'])
        self.assertEqual(result['code'], 'vent')
        self.assertFalse(room.step(hi=55)['memory']['n'])

    def test_cooling_uses_before_opening_temperature(self):
        room = Room(min_temp=10)
        room.step(ti=20, hi=65)
        result = room.step(window='on', ti=15, hi=70)
        # 15°C/70% will be about 51% after reheating to 20°C.
        self.assertEqual(result['memory']['b'],20)
        self.assertEqual(result['code'],'close')
        self.assertTrue(room.minutes(2)[-1]['send'])

    def test_maximum_open_and_close_stops_repeats(self):
        room = Room(repeats=True, repeat_interval=5)
        room.step(window='on')
        self.assertFalse(any(x['send'] for x in room.minutes(16)))
        result = room.minutes(1)[-1]
        self.assertTrue(result['send'])
        self.assertEqual(result['code'],'close')
        room.step(window='off', hi=50)
        self.assertFalse(any(x['send'] for x in room.minutes(10)))

    def test_too_cold_close(self):
        room = Room()
        room.step(window='on', ti=16, hi=80)
        self.assertTrue(room.minutes(2)[-1]['send'])

    def test_restart_and_gap_reset_confirmation(self):
        for reset in ('event','gap'):
            room = Room()
            room.step()
            room.minutes(9)
            result = room.step(trigger={'id':'reset'}) if reset=='event' else room.step(300)
            self.assertFalse(result['send'])
            self.assertFalse(any(x['send'] for x in room.minutes(9)))
            self.assertTrue(room.minutes(1)[-1]['send'])

    def test_memory_corruption(self):
        for value in ('invalid','[]','null','{"s":1}','{"s":"bad"}'):
            room = Room()
            room.memory=value
            self.assertFalse(room.step()['send'])

    def test_rapid_reopening_restarts_open_timer(self):
        room=Room()
        room.step(window='on')
        room.minutes(14)
        result=room.step(trigger={'id':'window','entity_id':'window','to_state':SimpleNamespace(state='off')})
        self.assertEqual(result['memory']['o'],room.now)
        self.assertFalse(room.minutes(1)[-1]['send'])

    def test_all_templates_compile_and_inputs_resolve(self):
        def walk(value):
            if isinstance(value,dict):
                if set(value)=={'input'} and isinstance(value['input'],str):
                    self.assertIn(value['input'],BLUEPRINT['blueprint']['input'])
                for child in value.values(): walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
            elif isinstance(value,str) and ('{{' in value or '{%' in value):
                ENV.from_string(value)
        walk(BLUEPRINT)


if __name__ == '__main__':
    unittest.main()
