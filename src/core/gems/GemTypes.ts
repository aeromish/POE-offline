export type DamageType = 'physical' | 'fire' | 'cold' | 'lightning';

export interface SkillContext {
  id: string;
  name: string;
  damageType: DamageType;
  baseMinDamage: number;
  baseMaxDamage: number;
  addedMinDamage: number;
  addedMaxDamage: number;
  attackSpeedMultiplier: number;
  baseCooldown: number;
  projectileCount: number;
  projectileSpeed: number;
  pierceCount: number;
  aoeRadius: number;
  critChance: number;
  critMultiplier: number;
  increasedDamagePercent: number;
  moreDamageMultipliers: number[];
}

export type SupportModifier = (ctx: SkillContext) => void;

export interface SupportGem {
  id: string;
  name: string;
  color: 'red' | 'green' | 'blue';
  apply: SupportModifier;
}

export interface ActiveGem {
  id: string;
  name: string;
  color: 'red' | 'green' | 'blue';
  getInitialContext: () => SkillContext;
}

export interface Socket {
  color: 'red' | 'green' | 'blue';
  linkGroup: number;
  gem: ActiveGem | SupportGem | null;
}
