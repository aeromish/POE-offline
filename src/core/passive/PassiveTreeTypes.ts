export type PassiveNodeType = 'start' | 'small' | 'notable' | 'keystone';
export type StatModifierType = 
  | 'flat_life'
  | 'flat_es'
  | 'flat_armour'
  | 'flat_evasion'
  | 'inc_phys_damage'
  | 'inc_fire_damage'
  | 'attack_speed_pct'
  | 'movement_speed'
  | 'crit_chance'
  | 'crit_multiplier'
  | 'extra_projectile'
  | 'extra_pierce'
  | 'pickup_radius'
  | 'exp_bonus_pct';

export interface StatModifier {
  type: StatModifierType;
  value: number;
}

export interface PassiveNode {
  id: string;
  name: string;
  description: string;
  nodeType: PassiveNodeType;
  branch: 'strength' | 'dexterity' | 'intelligence' | 'neutral';
  gridX: number;
  gridY: number;
  connections: string[];
  modifiers: StatModifier[];
}

export interface PassiveTreeBonus {
  flatLife: number;
  flatES: number;
  flatArmour: number;
  flatEvasion: number;
  incPhysDamage: number;
  incFireDamage: number;
  attackSpeedPct: number;
  movementSpeed: number;
  critChance: number;
  critMultiplier: number;
  extraProjectile: number;
  extraPierce: number;
  pickupRadius: number;
  expBonusPct: number;
}
