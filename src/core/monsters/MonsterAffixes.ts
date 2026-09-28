import { MonsterAffix } from './MonsterTypes';

export const MONSTER_AFFIXES: MonsterAffix[] = [
  {
    id: 'haste',
    name: 'Haste Aura',
    color: '#00ffff',
    apply: (stats) => {
      stats.movementSpeed *= 1.35;
    },
  },
  {
    id: 'extra_fire',
    name: 'Extra Fire Damage',
    color: '#ff4400',
    apply: (stats) => {
      stats.damage *= 1.4;
    },
  },
  {
    id: 'armoured',
    name: 'Armoured',
    color: '#ffd700',
    apply: (stats) => {
      stats.armour += 60;
      stats.maxLife = Math.round(stats.maxLife * 1.3);
      stats.currentLife = stats.maxLife;
    },
  },
];
