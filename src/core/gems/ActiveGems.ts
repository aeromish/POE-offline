import { ActiveGem, SkillContext } from './GemTypes';

export const FireballSkill: ActiveGem = {
  id: 'fireball',
  name: 'Fireball (Hỏa Cầu)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'fireball',
    name: 'Fireball',
    damageType: 'fire',
    baseMinDamage: 28,
    baseMaxDamage: 45,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.0,
    baseCooldown: 700,
    projectileCount: 1,
    projectileSpeed: 380,
    pierceCount: 0,
    aoeRadius: 45,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const SplitArrowSkill: ActiveGem = {
  id: 'split_arrow',
  name: 'Split Arrow (Tên Rẽ)',
  color: 'green',
  getInitialContext: (): SkillContext => ({
    id: 'split_arrow',
    name: 'Split Arrow',
    damageType: 'physical',
    baseMinDamage: 18,
    baseMaxDamage: 32,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.25,
    baseCooldown: 500,
    projectileCount: 3,
    projectileSpeed: 520,
    pierceCount: 0,
    aoeRadius: 0,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const GroundSlamSkill: ActiveGem = {
  id: 'ground_slam',
  name: 'Ground Slam (Địa Chấn)',
  color: 'red',
  getInitialContext: (): SkillContext => ({
    id: 'ground_slam',
    name: 'Ground Slam',
    damageType: 'physical',
    baseMinDamage: 45,
    baseMaxDamage: 80,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.85,
    baseCooldown: 900,
    projectileCount: 1,
    projectileSpeed: 240,
    pierceCount: 99,
    aoeRadius: 75,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 1: BĂNG CẦU XUYÊN THẤU
export const FrostboltSkill: ActiveGem = {
  id: 'frostbolt',
  name: 'Frostbolt (Băng Cầu)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'frostbolt',
    name: 'Frostbolt',
    damageType: 'cold',
    baseMinDamage: 32,
    baseMaxDamage: 52,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.95,
    baseCooldown: 650,
    projectileCount: 1,
    projectileSpeed: 300,
    pierceCount: 99, // Xuyên thấu toàn bộ quái trên đường bay
    aoeRadius: 30,
    critChance: 7,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 2: TIA SÉT TÁN XẠ
export const SparkSkill: ActiveGem = {
  id: 'spark',
  name: 'Spark (Tia Sét)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'spark',
    name: 'Spark',
    damageType: 'lightning',
    baseMinDamage: 12,
    baseMaxDamage: 48,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.4,
    baseCooldown: 550,
    projectileCount: 4,
    projectileSpeed: 450,
    pierceCount: 1,
    aoeRadius: 0,
    critChance: 8,
    critMultiplier: 1.6,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 3: LƯỠI KIẾM XOAY VÒNG QUANH THÂN
export const BladeVortexSkill: ActiveGem = {
  id: 'blade_vortex',
  name: 'Blade Vortex (Bão Kiếm)',
  color: 'green',
  getInitialContext: (): SkillContext => ({
    id: 'blade_vortex',
    name: 'Blade Vortex',
    damageType: 'physical',
    baseMinDamage: 15,
    baseMaxDamage: 25,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 2.0,
    baseCooldown: 300,
    projectileCount: 3,
    projectileSpeed: 180,
    pierceCount: 99,
    aoeRadius: 40,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const ALL_ACTIVE_SKILLS: Record<string, ActiveGem> = {
  fireball: FireballSkill,
  split_arrow: SplitArrowSkill,
  ground_slam: GroundSlamSkill,
  frostbolt: FrostboltSkill,
  spark: SparkSkill,
  blade_vortex: BladeVortexSkill,
};
