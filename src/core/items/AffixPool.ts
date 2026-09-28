import { AffixDefinition } from './ItemTypes';

export const PREFIX_POOL: AffixDefinition[] = [
  {
    id: 'p_flat_dmg',
    name: 'Heavy',
    type: 'prefix',
    statType: 'added_damage',
    minValue: 5,
    maxValue: 18,
  },
  {
    id: 'p_inc_dmg',
    name: 'Flashing',
    type: 'prefix',
    statType: 'inc_damage',
    minValue: 15,
    maxValue: 45,
  },
  {
    id: 'p_flat_life',
    name: 'Robust',
    type: 'prefix',
    statType: 'flat_life',
    minValue: 20,
    maxValue: 60,
  },
  {
    id: 'p_flat_es',
    name: 'Blinking',
    type: 'prefix',
    statType: 'flat_es',
    minValue: 15,
    maxValue: 40,
  },
];

export const SUFFIX_POOL: AffixDefinition[] = [
  {
    id: 's_atk_speed',
    name: 'of Velocity',
    type: 'suffix',
    statType: 'attack_speed',
    minValue: 10,
    maxValue: 25,
  },
  {
    id: 's_move_speed',
    name: 'of the Wind',
    type: 'suffix',
    statType: 'movement_speed',
    minValue: 15,
    maxValue: 35,
  },
  {
    id: 's_armour',
    name: 'of the Iron',
    type: 'suffix',
    statType: 'armour',
    minValue: 25,
    maxValue: 70,
  },
  {
    id: 's_crit',
    name: 'of Piercing',
    type: 'suffix',
    statType: 'crit_chance',
    minValue: 4,
    maxValue: 10,
  },
];
