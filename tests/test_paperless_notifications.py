"""Offline tests for Paperless notification gates and update-version deduplication."""
import unittest
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined


class Loader(yaml.SafeLoader):
    pass


Loader.add_constructor('!input', lambda loader, node: {'input': loader.construct_scalar(node)})
ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_PATH = ROOT / 'blueprints/automation/paperless_notifications/paperless_notifications.yaml'
BLUEPRINT = yaml.load(BLUEPRINT_PATH.read_text(), Loader=Loader)
ENV = Environment(undefined=StrictUndefined)
ENV.filters['is_number'] = lambda value: str(value).replace('.', '', 1).replace('-', '', 1).isdigit()

REMINDER_GATE = BLUEPRINT['actions'][0]['choose'][0]['conditions'][0]['value_template']
UPDATE_TRIGGER = BLUEPRINT['triggers'][2]['value_template']
UPDATE_GATE = BLUEPRINT['actions'][0]['choose'][1]['conditions'][0]['value_template']
UPDATE_VERSION_GATE = BLUEPRINT['actions'][0]['choose'][1]['sequence'][1]['value_template']


def render(template, *, readings=None, attributes=None, trigger_id='update_available', **values):
    readings = readings or {}
    attributes = attributes or {}

    def states(entity):
        return readings.get(entity, 'unknown')

    def state_attr(entity, name):
        return attributes.get((entity, name))

    def has_value(entity):
        return states(entity) not in ('unknown', 'unavailable', 'none', '')

    def is_state(entity, expected):
        return states(entity) == expected

    context = dict(
        states=states,
        state_attr=state_attr,
        has_value=has_value,
        is_state=is_state,
        trigger={'id': trigger_id},
        inbox_sensor='sensor.inbox',
        paperless_url='https://paperless.example.test',
        update_entity='update.paperless',
        updates_enabled=True,
        notified_version_helper='input_text.paperless_update_version',
        version_key='2.0.0',
    )
    context.update(values)
    return ENV.from_string(template).render(**context).strip() == 'True'


class PaperlessNotificationTests(unittest.TestCase):
    def test_daily_reminder_only_for_positive_numeric_count(self):
        self.assertTrue(render(REMINDER_GATE, readings={'sensor.inbox': '3'}, trigger_id='inbox_reminder'))
        self.assertFalse(render(REMINDER_GATE, readings={'sensor.inbox': '0'}, trigger_id='inbox_reminder'))
        for state in ('unknown', 'unavailable', 'documents', '', '-1'):
            self.assertFalse(render(REMINDER_GATE, readings={'sensor.inbox': state}, trigger_id='inbox_reminder'))
        self.assertFalse(render(REMINDER_GATE, readings={'sensor.inbox': '2'}, trigger_id='startup', paperless_url=''))

    def test_update_trigger_requires_available_update_and_persistent_helper(self):
        readings={'update.paperless': 'on', 'input_text.paperless_update_version': '1.0.0'}
        attrs={('update.paperless', 'latest_version'): '2.0.0'}
        self.assertTrue(render(UPDATE_TRIGGER, readings=readings, attributes=attrs,
                               update_entity_trigger='update.paperless',
                               version_helper_trigger='input_text.paperless_update_version',
                               updates_enabled_trigger=True))
        for state in ('off', 'unknown', 'unavailable'):
            self.assertFalse(render(UPDATE_TRIGGER,
                                    readings={**readings, 'update.paperless': state},
                                    attributes=attrs,
                                    update_entity_trigger='update.paperless',
                                    version_helper_trigger='input_text.paperless_update_version',
                                    updates_enabled_trigger=True))
        self.assertFalse(render(UPDATE_TRIGGER, readings=readings, attributes=attrs,
                                update_entity_trigger='update.paperless',
                                version_helper_trigger='input_text.paperless_update_version',
                                updates_enabled_trigger=False))
        self.assertFalse(render(UPDATE_TRIGGER, readings={'update.paperless':'on'}, attributes=attrs,
                                update_entity_trigger='update.paperless',
                                version_helper_trigger='input_text.paperless_update_version',
                                updates_enabled_trigger=True))

    def test_same_version_is_skipped_after_restart_and_new_version_notified(self):
        base={'update.paperless':'on','input_text.paperless_update_version':'2.0.0'}
        self.assertTrue(render(UPDATE_GATE, readings=base, attributes={('update.paperless','latest_version'):'2.0.0'}, trigger_id='startup'))
        self.assertFalse(render(UPDATE_VERSION_GATE, readings=base, version_key='2.0.0'))
        self.assertTrue(render(UPDATE_VERSION_GATE, readings=base, version_key='3.0.0'))

    def test_templates_compile_and_blueprint_inputs_resolve(self):
        declared=set()
        for section in BLUEPRINT['blueprint']['input'].values():
            declared.update(section.get('input', {}))
        declared.update(BLUEPRINT.get('trigger_variables', {}))
        def walk(value):
            if isinstance(value, dict):
                if set(value)=={'input'} and isinstance(value['input'],str):
                    self.assertIn(value['input'],declared)
                for child in value.values(): walk(child)
            elif isinstance(value,list):
                for child in value: walk(child)
            elif isinstance(value,str) and ('{{' in value or '{%' in value):
                ENV.from_string(value)
        walk(BLUEPRINT)


if __name__ == '__main__':
    unittest.main()
