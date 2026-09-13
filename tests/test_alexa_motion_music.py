"""Test actual blueprint gates with simulated HA state; no Alexa commands are sent."""
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import yaml
from jinja2 import Environment, StrictUndefined


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda loader, node: {'input': loader.construct_scalar(node)})
B = yaml.load((Path(__file__).resolve().parents[1] / 'blueprints/automation/alexa_motion_music/alexa_motion_music.yaml').read_text(), Loader=Loader)
E = Environment(undefined=StrictUndefined)
START = B['actions'][1]['choose'][0]['sequence']
PAUSE = B['actions'][1]['choose'][1]['conditions'][0]['value_template']


def context(player='paused', motion='on', seconds=0, initial='paused', trigger_id='motion', completed=False):
    now = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)
    readings = {'echo': player, 'pir': motion}
    class States:
        def __call__(self, entity):
            return readings[entity]
        def __getitem__(self, entity):
            return SimpleNamespace(last_changed=now-timedelta(seconds=seconds))
    return dict(player='echo', motion='pir', pause_after=5, initial_state=initial,
                fallback_enabled=True, routine='Radio Chillout', wait={'completed':completed},
                trigger={'id':trigger_id}, states=States(), is_state=lambda entity, value: readings[entity]==value,
                as_timestamp=lambda value:value.timestamp(), now=lambda:now)


def check(template, **kwargs):
    return E.from_string(template).render(**context(**kwargs)).strip()=='True'


class AlexaTests(unittest.TestCase):
    def test_resume_candidates(self):
        for state in ('paused','idle','off','standby'):
            self.assertTrue(check(START[1]['value_template'], initial=state))
        for state in ('playing','buffering','unknown','unavailable'):
            self.assertFalse(check(START[1]['value_template'], initial=state))

    def test_paused_never_restarts_routine(self):
        gate=START[4]['value_template']
        self.assertFalse(check(gate, initial='paused'))
        self.assertTrue(check(gate, initial='idle'))

    def test_resume_wait_exits_on_playback_or_failure(self):
        gate=START[5]['wait_template']
        for state in ('playing','buffering','unknown','unavailable'):
            self.assertTrue(check(gate, player=state))
        self.assertTrue(check(gate, motion='unavailable'))
        self.assertFalse(check(gate, player='idle', motion='off', seconds=10))

    def test_routine_gate(self):
        gate=START[6]['value_template']
        self.assertTrue(check(gate, player='idle'))
        self.assertTrue(check(gate, player='idle', motion='off', seconds=10))
        self.assertFalse(check(gate, player='idle', motion='off', seconds=300))
        self.assertFalse(check(gate, player='idle', completed=True))
        for state in ('playing','buffering','unknown','unavailable'):
            self.assertFalse(check(gate, player=state))
        self.assertFalse(check(gate, player='idle', motion='unknown'))

    def test_pause_requires_continuous_off_and_playing(self):
        self.assertTrue(check(PAUSE, player='playing', motion='off', seconds=300, trigger_id='pause'))
        self.assertFalse(check(PAUSE, player='playing', motion='off', seconds=299, trigger_id='pause'))
        self.assertFalse(check(PAUSE, player='playing', motion='on', seconds=600, trigger_id='pause'))
        self.assertFalse(check(PAUSE, player='paused', motion='off', seconds=600, trigger_id='pause'))
        self.assertFalse(check(PAUSE, player='playing', motion='unavailable', seconds=600, trigger_id='pause'))

    def test_watchdog_does_not_cancel_start_attempt(self):
        gate=B['conditions'][0]['value_template']
        self.assertFalse(check(gate, trigger_id='watchdog', player='idle'))
        self.assertFalse(check(gate, trigger_id='watchdog', player='playing', motion='off', seconds=30))
        self.assertTrue(check(gate, trigger_id='watchdog', player='playing', motion='off', seconds=300))

    def test_manual_run_guard(self):
        gate=E.from_string(B['actions'][0]['value_template'])
        for c in ({},{'trigger':None},{'trigger':{}},{'trigger':{'id':'cancel'}}):
            self.assertEqual(gate.render(**c).strip(),'False')

    def test_templates_and_actions(self):
        actions=[]
        def walk(value):
            if isinstance(value,dict):
                if 'action' in value: actions.append(value['action'])
                if set(value)=={'input'} and isinstance(value['input'],str):
                    self.assertIn(value['input'],B['blueprint']['input'])
                for child in value.values(): walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
            elif isinstance(value,str) and ('{{' in value or '{%' in value):
                E.from_string(value)
        walk(B)
        self.assertIn('media_player.media_play',actions)
        self.assertIn('media_player.media_pause',actions)
        self.assertNotIn('media_player.media_stop',actions)
        self.assertNotIn('media_player.media_play_pause',actions)
        self.assertEqual(START[7]['data']['media_content_type'],'routine')


if __name__ == '__main__':
    unittest.main()
