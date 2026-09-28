import { SkillContext, DamageType } from '../gems/GemTypes';
import { PoEStats } from '../stats/CharacterStats';

export interface HitResult {
  damage: number;
  isCrit: boolean;
  type: DamageType;
  absorbedByES: number;
  absorbedByLife: number;
}

export class DamageEngine {
  public static calculateHit(skill: SkillContext, targetStats: PoEStats): HitResult {
    const isEvaded = Math.random() * 100 < targetStats.evasion;
    if (isEvaded) {
      return { damage: 0, isCrit: false, type: skill.damageType, absorbedByES: 0, absorbedByLife: 0 };
    }

    const rawMin = skill.baseMinDamage + skill.addedMinDamage;
    const rawMax = skill.baseMaxDamage + skill.addedMaxDamage;
    const rawDamage = rawMin + Math.random() * (rawMax - rawMin);

    const incMultiplier = 1 + skill.increasedDamagePercent / 100;
    const moreMultiplier = skill.moreDamageMultipliers.reduce((acc, cur) => acc * cur, 1.0);

    let damage = rawDamage * incMultiplier * moreMultiplier;

    const isCrit = Math.random() * 100 < skill.critChance;
    if (isCrit) {
      damage *= skill.critMultiplier;
    }

    if (skill.damageType === 'physical') {
      const armourReduction = targetStats.armour / (targetStats.armour + 5 * damage);
      damage *= 1 - Math.min(armourReduction, 0.9);
    }

    const finalDamage = Math.max(1, Math.round(damage));

    let remaining = finalDamage;
    let absorbedES = 0;
    let absorbedLife = 0;

    if (targetStats.energyShield > 0) {
      absorbedES = Math.min(targetStats.energyShield, remaining);
      targetStats.energyShield -= absorbedES;
      remaining -= absorbedES;
    }

    if (remaining > 0) {
      absorbedLife = Math.min(targetStats.currentLife, remaining);
      targetStats.currentLife -= absorbedLife;
    }

    return {
      damage: finalDamage,
      isCrit,
      type: skill.damageType,
      absorbedByES: absorbedES,
      absorbedByLife: absorbedLife,
    };
  }
}
