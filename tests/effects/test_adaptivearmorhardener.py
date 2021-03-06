# Test abstract things, usually situations were should _never_ come across.

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# noinspection PyPep8
from EVE_Gnosis.effects.adaptivearmorhardener import AdaptiveArmorHardener


def test_adaptive_armor_hardener():
    resists = {
        'Elecromagnetic': 0,
        'Thermal': .20,
        'Kinetic': .40,
        'Explosive': .50,
    }
    damage_profile = {
        'Elecromagnetic': 0,
        'Thermal': .50,
        'Kinetic': .50,
        'Explosive': 0,
    }

    reactive_armor_hardener_profile = {
        'Elecromagnetic': 15,
        'Thermal': 15,
        'Kinetic': 15,
        'Explosive': 15,
    }

    adjust_amount = 6

    return_matrix = AdaptiveArmorHardener.run_cycle(
        resists,
        damage_profile,
        reactive_armor_hardener_profile,
        adjust_amount
    )

    assert return_matrix['AdaptivePattern']['Elecromagnetic'] == 9
    assert return_matrix['AdaptivePattern']['Thermal'] == 21
    assert return_matrix['AdaptivePattern']['Kinetic'] == 21
    assert return_matrix['AdaptivePattern']['Explosive'] == 9

    for _ in return_matrix['AppliedDamage']:
        key, value = _
        if key == 'Elecromagnetic':
            assert value == 0
        elif key == 'Thermal':
            assert value == .4
        elif key == 'Kinetic':
            assert value == .3
        elif key == 'Explosive':
            assert value == 0
        else:
            # We have damage types we don't know about. Catch this and make sure our assert fails.
            assert True is False


def test_adaptive_armor_hardener_defaults():
    resists = {
        'Elecromagnetic': 0,
        'Thermal': .20,
        'Kinetic': .40,
        'Explosive': .50,
    }
    damage_profile = {
        'Elecromagnetic': 0,
        'Thermal': .50,
        'Kinetic': .50,
        'Explosive': 0,
    }

    return_matrix = AdaptiveArmorHardener.run_cycle(
        resists,
        damage_profile,
    )

    assert return_matrix['AdaptivePattern']['Elecromagnetic'] == 9
    assert return_matrix['AdaptivePattern']['Thermal'] == 21
    assert return_matrix['AdaptivePattern']['Kinetic'] == 21
    assert return_matrix['AdaptivePattern']['Explosive'] == 9

    for _ in return_matrix['AppliedDamage']:
        key, value = _
        if key == 'Elecromagnetic':
            assert value == 0
        elif key == 'Thermal':
            assert value == .4
        elif key == 'Kinetic':
            assert value == .3
        elif key == 'Explosive':
            assert value == 0
        else:
            # We have damage types we don't know about. Catch this and make sure our assert fails.
            assert True is False



def test_adaptive_armor_hardener_single_damage_type():
    resists = {
        'Elecromagnetic': 0,
        'Thermal': .20,
        'Kinetic': .40,
        'Explosive': .50,
    }
    damage_profile = {
        'Elecromagnetic': .50,
        'Thermal': 0,
        'Kinetic': 0,
        'Explosive': 0,
    }

    return_matrix = AdaptiveArmorHardener.run_cycle(
        resists,
        damage_profile,
    )

    assert return_matrix['AdaptivePattern']['Elecromagnetic'] == 27
    assert return_matrix['AdaptivePattern']['Thermal'] == 15
    assert return_matrix['AdaptivePattern']['Kinetic'] == 9
    assert return_matrix['AdaptivePattern']['Explosive'] == 9

    for _ in return_matrix['AppliedDamage']:
        key, value = _
        if key == 'Elecromagnetic':
            assert value == .5
        elif key == 'Thermal':
            assert value == 0
        elif key == 'Kinetic':
            assert value == 0
        elif key == 'Explosive':
            assert value == 0
        else:
            # We have damage types we don't know about. Catch this and make sure our assert fails.
            assert True is False

def test_adaptive_armor_hardener_single_damage_type_5_loops():
    resists = {
        'Elecromagnetic': 0,
        'Thermal': .20,
        'Kinetic': .40,
        'Explosive': .50,
    }
    damage_profile = {
        'Elecromagnetic': .50,
        'Thermal': 0,
        'Kinetic': 0,
        'Explosive': 0,
    }

    reactive_armor_hardener_profile = {
        'Elecromagnetic': 15,
        'Thermal': 15,
        'Kinetic': 15,
        'Explosive': 15,
    }

    return_matrix = None

    for _ in range(5):
        if return_matrix:
            reactive_armor_hardener_profile = {
                'Elecromagnetic': return_matrix['AdaptivePattern']['Elecromagnetic'],
                'Thermal': return_matrix['AdaptivePattern']['Thermal'],
                'Kinetic': return_matrix['AdaptivePattern']['Kinetic'],
                'Explosive': return_matrix['AdaptivePattern']['Explosive'],
            }

        return_matrix = AdaptiveArmorHardener.run_cycle(
            resists,
            damage_profile,
            reactive_armor_hardener_profile,
        )

    assert return_matrix['AdaptivePattern']['Elecromagnetic'] == 57
    assert return_matrix['AdaptivePattern']['Thermal'] == 3
    assert return_matrix['AdaptivePattern']['Kinetic'] == 0
    assert return_matrix['AdaptivePattern']['Explosive'] == 0

    for _ in return_matrix['AppliedDamage']:
        key, value = _
        if key == 'Elecromagnetic':
            assert value == .5
        elif key == 'Thermal':
            assert value == 0
        elif key == 'Kinetic':
            assert value == 0
        elif key == 'Explosive':
            assert value == 0
        else:
            # We have damage types we don't know about. Catch this and make sure our assert fails.
            assert True is False

def test_adaptive_armor_hardener_preadjusted():
    resists = {
        'Elecromagnetic': 0,
        'Thermal': .20,
        'Kinetic': .40,
        'Explosive': .50,
    }
    damage_profile = {
        'Elecromagnetic': 0,
        'Thermal': .50,
        'Kinetic': .50,
        'Explosive': 0,
    }

    reactive_armor_hardener_profile = {
        'Elecromagnetic': 1,
        'Thermal': 1,
        'Kinetic': 29,
        'Explosive': 29,
    }

    return_matrix = AdaptiveArmorHardener.run_cycle(
        resists,
        damage_profile,
        reactive_armor_hardener_profile,
    )

    assert return_matrix['AdaptivePattern']['Elecromagnetic'] == 0
    assert return_matrix['AdaptivePattern']['Thermal'] == 4.5
    assert return_matrix['AdaptivePattern']['Kinetic'] == 32.5
    assert return_matrix['AdaptivePattern']['Explosive'] == 23

    for _ in return_matrix['AppliedDamage']:
        key, value = _
        if key == 'Elecromagnetic':
            assert value == 0
        elif key == 'Thermal':
            assert value == .4
        elif key == 'Kinetic':
            assert value == .3
        elif key == 'Explosive':
            assert value == 0
        else:
            # We have damage types we don't know about. Catch this and make sure our assert fails.
            assert True is False

