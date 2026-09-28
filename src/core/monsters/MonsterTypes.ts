export type MonsterRarity = 'Normal' | 'Magic' | 'Rare' | 'Boss';

export interface MonsterAffix {
  id: string;
  name: string;
  color: string;
  apply: (stats: MonsterStats) => void;
}

export interface MonsterStats {
  maxLife: number;
  currentLife: number;
  damage: number;
  movementSpeed: number;
  armour: number;
  evasion: number;
  rarity: MonsterRarity;
  affixes: MonsterAffix[];
  expReward: number;
}
