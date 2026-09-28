import { SupportGem } from './GemTypes';

export const GreaterMultipleProjectiles: SupportGem = {
  id: 'gmp',
  name: 'Greater Multiple Projectiles',
  color: 'green',
  apply: (ctx) => {
    ctx.projectileCount += 4;
    ctx.moreDamageMultipliers.push(0.74);
  },
};

export const PierceSupport: SupportGem = {
  id: 'pierce',
  name: 'Pierce Support',
  color: 'green',
  apply: (ctx) => {
    ctx.pierceCount += 2;
    ctx.moreDamageMultipliers.push(1.15);
  },
};

export const AddedFireDamageSupport: SupportGem = {
  id: 'added_fire',
  name: 'Added Fire Damage',
  color: 'red',
  apply: (ctx) => {
    ctx.addedMinDamage += 8;
    ctx.addedMaxDamage += 15;
    ctx.increasedDamagePercent += 20;
  },
};

export const FasterAttacksSupport: SupportGem = {
  id: 'faster_attacks',
  name: 'Faster Attacks Support',
  color: 'green',
  apply: (ctx) => {
    ctx.attackSpeedMultiplier *= 1.35;
  },
};
