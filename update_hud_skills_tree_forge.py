import os

files = {
    # 1. Cập nhật ItemTypes.ts: Thêm thuộc tính Tier cho Trang bị
    "src/core/items/ItemTypes.ts": '''export type ItemRarity = 'Normal' | 'Magic' | 'Rare';

export type CurrencyType = 
  | 'transmutation' 
  | 'alteration' 
  | 'regal' 
  | 'chaos' 
  | 'exalted' 
  | 'scouring';

export interface AffixDefinition {
  id: string;
  name: string;
  type: 'prefix' | 'suffix';
  statType: 
    | 'added_damage' 
    | 'inc_damage' 
    | 'flat_life' 
    | 'flat_es' 
    | 'attack_speed' 
    | 'movement_speed' 
    | 'armour' 
    | 'crit_chance';
  minValue: number;
  maxValue: number;
}

export interface AffixInstance {
  definitionId: string;
  name: string;
  type: 'prefix' | 'suffix';
  statType: string;
  value: number;
}

export interface EquipmentItem {
  id: string;
  name: string;
  baseType: 'Sword' | 'Bow' | 'Wand' | 'Plate';
  tier: number; // Tier 1 -> Tier 5
  rarity: ItemRarity;
  prefixes: AffixInstance[];
  suffixes: AffixInstance[];
}

export interface InventoryData {
  currencies: Record<CurrencyType, number>;
  equippedItem: EquipmentItem;
  bag: EquipmentItem[];
}
''',

    # 2. Cập nhật GemTypes.ts: Thêm Gem Level & Icon
    "src/core/gems/GemTypes.ts": '''export type DamageType = 'physical' | 'fire' | 'cold' | 'lightning' | 'chaos';

export interface SkillContext {
  id: string;
  name: string;
  level: number;
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
  iconColor: number;
  getInitialContext: (level?: number) => SkillContext;
}

export interface Socket {
  color: 'red' | 'green' | 'blue';
  linkGroup: number;
  gem: ActiveGem | SupportGem | null;
}
''',

    # 3. Thêm các kỹ năng mới & Công thức Leveling kỹ năng vào ActiveGems.ts
    "src/core/gems/ActiveGems.ts": '''import { ActiveGem, SkillContext } from './GemTypes';

export const FireballSkill: ActiveGem = {
  id: 'fireball',
  name: 'Fireball',
  color: 'blue',
  iconColor: 0xef4444,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'fireball',
    name: 'Fireball',
    level,
    damageType: 'fire',
    baseMinDamage: Math.round(28 * (1 + (level - 1) * 0.3)),
    baseMaxDamage: Math.round(45 * (1 + (level - 1) * 0.3)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.0 + (level - 1) * 0.05,
    baseCooldown: 700,
    projectileCount: 1 + Math.floor((level - 1) / 3),
    projectileSpeed: 380,
    pierceCount: 0,
    aoeRadius: 45 + (level - 1) * 6,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const SplitArrowSkill: ActiveGem = {
  id: 'split_arrow',
  name: 'Split Arrow',
  color: 'green',
  iconColor: 0x22c55e,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'split_arrow',
    name: 'Split Arrow',
    level,
    damageType: 'physical',
    baseMinDamage: Math.round(18 * (1 + (level - 1) * 0.25)),
    baseMaxDamage: Math.round(32 * (1 + (level - 1) * 0.25)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.25,
    baseCooldown: 500,
    projectileCount: 3 + (level - 1),
    projectileSpeed: 520,
    pierceCount: Math.floor((level - 1) / 2),
    aoeRadius: 0,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const GroundSlamSkill: ActiveGem = {
  id: 'ground_slam',
  name: 'Ground Slam',
  color: 'red',
  iconColor: 0xd97706,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'ground_slam',
    name: 'Ground Slam',
    level,
    damageType: 'physical',
    baseMinDamage: Math.round(45 * (1 + (level - 1) * 0.35)),
    baseMaxDamage: Math.round(80 * (1 + (level - 1) * 0.35)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.85,
    baseCooldown: Math.max(500, 900 - (level - 1) * 60),
    projectileCount: 1,
    projectileSpeed: 240,
    pierceCount: 99,
    aoeRadius: 75 + (level - 1) * 10,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const FrostboltSkill: ActiveGem = {
  id: 'frostbolt',
  name: 'Frostbolt',
  color: 'blue',
  iconColor: 0x06b6d4,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'frostbolt',
    name: 'Frostbolt',
    level,
    damageType: 'cold',
    baseMinDamage: Math.round(32 * (1 + (level - 1) * 0.28)),
    baseMaxDamage: Math.round(52 * (1 + (level - 1) * 0.28)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.95,
    baseCooldown: 650,
    projectileCount: 1 + Math.floor((level - 1) / 2),
    projectileSpeed: 320,
    pierceCount: 99,
    aoeRadius: 30,
    critChance: 7,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const SparkSkill: ActiveGem = {
  id: 'spark',
  name: 'Spark',
  color: 'blue',
  iconColor: 0xfacc15,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'spark',
    name: 'Spark',
    level,
    damageType: 'lightning',
    baseMinDamage: Math.round(12 * (1 + (level - 1) * 0.3)),
    baseMaxDamage: Math.round(48 * (1 + (level - 1) * 0.3)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.4,
    baseCooldown: 550,
    projectileCount: 4 + (level - 1) * 2,
    projectileSpeed: 450,
    pierceCount: 1 + Math.floor((level - 1) / 2),
    aoeRadius: 0,
    critChance: 8,
    critMultiplier: 1.6,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const BladeVortexSkill: ActiveGem = {
  id: 'blade_vortex',
  name: 'Blade Vortex',
  color: 'green',
  iconColor: 0xa855f7,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'blade_vortex',
    name: 'Blade Vortex',
    level,
    damageType: 'physical',
    baseMinDamage: Math.round(15 * (1 + (level - 1) * 0.25)),
    baseMaxDamage: Math.round(25 * (1 + (level - 1) * 0.25)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 2.0,
    baseCooldown: 300,
    projectileCount: 3 + (level - 1),
    projectileSpeed: 180,
    pierceCount: 99,
    aoeRadius: 40 + (level - 1) * 5,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI: ARC (Tia Sét Xích Điện)
export const ArcSkill: ActiveGem = {
  id: 'arc',
  name: 'Arc',
  color: 'blue',
  iconColor: 0x38bdf8,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'arc',
    name: 'Arc',
    level,
    damageType: 'lightning',
    baseMinDamage: Math.round(20 * (1 + (level - 1) * 0.32)),
    baseMaxDamage: Math.round(65 * (1 + (level - 1) * 0.32)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.2,
    baseCooldown: 480,
    projectileCount: 2 + (level - 1),
    projectileSpeed: 600,
    pierceCount: 2,
    aoeRadius: 0,
    critChance: 9,
    critMultiplier: 1.65,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI: MOLTEN STRIKE (Hỏa Nham Đao)
export const MoltenStrikeSkill: ActiveGem = {
  id: 'molten_strike',
  name: 'Molten Strike',
  color: 'red',
  iconColor: 0xf97316,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'molten_strike',
    name: 'Molten Strike',
    level,
    damageType: 'fire',
    baseMinDamage: Math.round(35 * (1 + (level - 1) * 0.3)),
    baseMaxDamage: Math.round(60 * (1 + (level - 1) * 0.3)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.1,
    baseCooldown: 620,
    projectileCount: 3 + (level - 1),
    projectileSpeed: 300,
    pierceCount: 0,
    aoeRadius: 55,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI: TOXIC SPORE (Bào Tử Độc Tố)
export const ToxicSporeSkill: ActiveGem = {
  id: 'toxic_spore',
  name: 'Toxic Spore',
  color: 'green',
  iconColor: 0x10b981,
  getInitialContext: (level = 1): SkillContext => ({
    id: 'toxic_spore',
    name: 'Toxic Spore',
    level,
    damageType: 'chaos',
    baseMinDamage: Math.round(22 * (1 + (level - 1) * 0.28)),
    baseMaxDamage: Math.round(42 * (1 + (level - 1) * 0.28)),
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.3,
    baseCooldown: 450,
    projectileCount: 3 + (level - 1),
    projectileSpeed: 400,
    pierceCount: 1,
    aoeRadius: 40,
    critChance: 5,
    critMultiplier: 1.4,
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
  arc: ArcSkill,
  molten_strike: MoltenStrikeSkill,
  toxic_spore: ToxicSporeSkill,
};
''',

    # 4. Mở rộng Cây Thiên Phú (PassiveTreeData.ts) lên 24+ nodes kết nối
    "src/core/passive/PassiveTreeData.ts": '''import { PassiveNode } from './PassiveTreeTypes';

export const PASSIVE_TREE_NODES: Record<string, PassiveNode> = {
  root: {
    id: 'root',
    name: 'Gốc Thiên Phú',
    description: 'Nguồn cội tiềm năng của Lưu Đày Giả.',
    nodeType: 'start',
    branch: 'neutral',
    gridX: 0,
    gridY: 0,
    connections: ['str_1', 'dex_1', 'int_1', 'ring_aoe', 'ring_cdr'],
    modifiers: [],
  },

  // === VÒNG TRÒN TRUNG TÂM (UTILITY) ===
  ring_aoe: {
    id: 'ring_aoe',
    name: 'Khuếch Tán Diện Rộng',
    description: '+25 Bán kính vụ nổ (AoE Radius)',
    nodeType: 'small',
    branch: 'neutral',
    gridX: -45,
    gridY: 35,
    connections: ['root'],
    modifiers: [{ type: 'extra_pierce', value: 1 }],
  },
  ring_cdr: {
    id: 'ring_cdr',
    name: 'Hồi Chiêu Thần Tốc',
    description: '+15% Tốc độ ra đòn cho mọi kỹ năng',
    nodeType: 'small',
    branch: 'neutral',
    gridX: 45,
    gridY: 35,
    connections: ['root'],
    modifiers: [{ type: 'attack_speed_pct', value: 15 }],
  },

  // === NHÁNH ĐỎ: CHIẾN BINH (STRENGTH) ===
  str_1: {
    id: 'str_1',
    name: 'Thân Thể Bất Khuất',
    description: '+30 Máu Tối Đa',
    nodeType: 'small',
    branch: 'strength',
    gridX: -70,
    gridY: -50,
    connections: ['root', 'str_2', 'str_life_pct'],
    modifiers: [{ type: 'flat_life', value: 30 }],
  },
  str_life_pct: {
    id: 'str_life_pct',
    name: 'Khí Huyết Dồi Dào',
    description: '+45 Máu Tối Đa',
    nodeType: 'small',
    branch: 'strength',
    gridX: -110,
    gridY: -20,
    connections: ['str_1'],
    modifiers: [{ type: 'flat_life', value: 45 }],
  },
  str_2: {
    id: 'str_2',
    name: 'Tôi Luyện Thiết Giáp',
    description: '+40 Giáp Vật Lý',
    nodeType: 'small',
    branch: 'strength',
    gridX: -140,
    gridY: -80,
    connections: ['str_1', 'str_3', 'str_iron_will'],
    modifiers: [{ type: 'flat_armour', value: 40 }],
  },
  str_iron_will: {
    id: 'str_iron_will',
    name: 'Ý Chí Sắt Đá (Iron Will)',
    description: '+50 Giáp Vật Lý, +20 Máu Tối Đa',
    nodeType: 'notable',
    branch: 'strength',
    gridX: -180,
    gridY: -45,
    connections: ['str_2'],
    modifiers: [
      { type: 'flat_armour', value: 50 },
      { type: 'flat_life', value: 20 },
    ],
  },
  str_3: {
    id: 'str_3',
    name: 'Trảm Kích Hùng Lực',
    description: '+30% Sát Thương Vật Lý',
    nodeType: 'notable',
    branch: 'strength',
    gridX: -210,
    gridY: -110,
    connections: ['str_2', 'str_keystone', 'str_resolute'],
    modifiers: [{ type: 'inc_phys_damage', value: 30 }],
  },
  str_resolute: {
    id: 'str_resolute',
    name: 'Keystone: Resolute Technique',
    description: '+50% Sát Thương Vật Lý, Đòn Đánh Luôn Chuẩn Xác',
    nodeType: 'keystone',
    branch: 'strength',
    gridX: -270,
    gridY: -80,
    connections: ['str_3'],
    modifiers: [{ type: 'inc_phys_damage', value: 50 }],
  },
  str_keystone: {
    id: 'str_keystone',
    name: 'Keystone: Juggernaut',
    description: '+80 Máu Tối Đa, +80 Giáp Vật Lý',
    nodeType: 'keystone',
    branch: 'strength',
    gridX: -280,
    gridY: -140,
    connections: ['str_3'],
    modifiers: [
      { type: 'flat_life', value: 80 },
      { type: 'flat_armour', value: 80 },
    ],
  },

  // === NHÁNH XANH LÁ: XẠ THỦ (DEXTERITY) ===
  dex_1: {
    id: 'dex_1',
    name: 'Thần Tốc Hành Quân',
    description: '+20 Tốc Độ Di Chuyển',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 70,
    connections: ['root', 'dex_2', 'dex_evasion_boost'],
    modifiers: [{ type: 'movement_speed', value: 20 }],
  },
  dex_evasion_boost: {
    id: 'dex_evasion_boost',
    name: 'Linh Hoạt Bộ Pháp',
    description: '+15 Tốc Độ Di Chuyển, +15 Né Đòn',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: -50,
    gridY: 110,
    connections: ['dex_1'],
    modifiers: [
      { type: 'movement_speed', value: 15 },
      { type: 'flat_evasion', value: 15 },
    ],
  },
  dex_2: {
    id: 'dex_2',
    name: 'Vũ Điệu Cung Vũ',
    description: '+20% Tốc Độ Bắn Kỹ Năng',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 130,
    connections: ['dex_1', 'dex_3', 'dex_point_blank'],
    modifiers: [{ type: 'attack_speed_pct', value: 20 }],
  },
  dex_point_blank: {
    id: 'dex_point_blank',
    name: 'Điểm Hỏa Cận Chiến (Point Blank)',
    description: '+1 Tia Đạn Bổ Sung, +10% Tốc Độ Bắn',
    nodeType: 'notable',
    branch: 'dexterity',
    gridX: 50,
    gridY: 165,
    connections: ['dex_2'],
    modifiers: [
      { type: 'extra_projectile', value: 1 },
      { type: 'attack_speed_pct', value: 10 },
    ],
  },
  dex_3: {
    id: 'dex_3',
    name: 'Hư Ứng Vô Ảnh',
    description: '+30 Tỷ Lệ Né Đòn (Evasion)',
    nodeType: 'notable',
    branch: 'dexterity',
    gridX: 0,
    gridY: 190,
    connections: ['dex_2', 'dex_keystone'],
    modifiers: [{ type: 'flat_evasion', value: 30 }],
  },
  dex_keystone: {
    id: 'dex_keystone',
    name: 'Keystone: Deadeye',
    description: '+2 Tia Đạn Bổ Sung, +2 Lần Xuyên Thấu',
    nodeType: 'keystone',
    branch: 'dexterity',
    gridX: 0,
    gridY: 245,
    connections: ['dex_3'],
    modifiers: [
      { type: 'extra_projectile', value: 2 },
      { type: 'extra_pierce', value: 2 },
    ],
  },

  // === NHÁNH XANH LAM: PHÁP SƯ (INTELLIGENCE) ===
  int_1: {
    id: 'int_1',
    name: 'Màn Chắn Tâm Linh',
    description: '+40 Khiên Năng Lượng (Energy Shield)',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 70,
    gridY: -50,
    connections: ['root', 'int_2', 'int_cast_speed'],
    modifiers: [{ type: 'flat_es', value: 40 }],
  },
  int_cast_speed: {
    id: 'int_cast_speed',
    name: 'Ngưng Tụ Ma Lực',
    description: '+15% Tốc Độ Thi Triển Pháp Thuật',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 110,
    gridY: -20,
    connections: ['int_1'],
    modifiers: [{ type: 'attack_speed_pct', value: 15 }],
  },
  int_2: {
    id: 'int_2',
    name: 'Hỏa Băng Hủy Diệt',
    description: '+30% Sát Thương Nguyên Tố',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 140,
    gridY: -80,
    connections: ['int_1', 'int_3', 'int_overload'],
    modifiers: [{ type: 'inc_fire_damage', value: 30 }],
  },
  int_overload: {
    id: 'int_overload',
    name: 'Quá Tải Nguyên Tố (Elemental Overload)',
    description: '+8% Tỷ Lệ Chí Mạng, +40 Khiên Năng Lượng',
    nodeType: 'notable',
    branch: 'intelligence',
    gridX: 180,
    gridY: -45,
    connections: ['int_2'],
    modifiers: [
      { type: 'crit_chance', value: 8 },
      { type: 'flat_es', value: 40 },
    ],
  },
  int_3: {
    id: 'int_3',
    name: 'Khai Mở Tiêu Điểm',
    description: '+10% Tỷ Lệ Chí Mạng, +0.3x Sát Thương Chí Mạng',
    nodeType: 'notable',
    branch: 'intelligence',
    gridX: 210,
    gridY: -110,
    connections: ['int_2', 'int_keystone'],
    modifiers: [
      { type: 'crit_chance', value: 10 },
      { type: 'crit_multiplier', value: 0.3 },
    ],
  },
  int_keystone: {
    id: 'int_keystone',
    name: 'Keystone: Archmage',
    description: '+80 Khiên Năng Lượng, +0.5x Sát Thương Chí Mạng',
    nodeType: 'keystone',
    branch: 'intelligence',
    gridX: 280,
    gridY: -140,
    connections: ['int_3'],
    modifiers: [
      { type: 'flat_es', value: 80 },
      { type: 'crit_multiplier', value: 0.5 },
    ],
  },
};
''',

    # 5. Cập nhật LootEngine.ts: Rơi trang bị có Tier (Tier 1 -> Tier 3)
    "src/core/loot/LootEngine.ts": '''import { CurrencyType, EquipmentItem } from '../items/ItemTypes';
import { MonsterRarity } from '../monsters/MonsterTypes';
import { CraftingEngine } from '../crafting/CraftingEngine';

export interface DropResult {
  category: 'currency' | 'equipment' | 'gem';
  currencyType?: CurrencyType;
  equipmentItem?: EquipmentItem;
  gemId?: string;
  name: string;
}

export class LootEngine {
  public static rollMonsterDrops(rarity: MonsterRarity): DropResult[] {
    const drops: DropResult[] = [];
    const roll = Math.random();

    let dropChance = 0.35;
    if (rarity === 'Magic') dropChance = 0.65;
    if (rarity === 'Rare') dropChance = 0.95;
    if (rarity === 'Boss') dropChance = 1.0;

    if (roll > dropChance) return drops;

    const numDrops = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

    for (let i = 0; i < numDrops; i++) {
      const typeRoll = Math.random();

      // 55% rơi Tiền tệ Crafting
      if (typeRoll < 0.55) {
        const cRoll = Math.random() * 100;
        let cur: CurrencyType = 'transmutation';
        let name = 'Orb of Transmutation';

        if (cRoll < 5 && (rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'exalted';
          name = 'Exalted Orb';
        } else if (cRoll < 22 && (rarity === 'Magic' || rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'chaos';
          name = 'Chaos Orb';
        } else if (cRoll < 42) {
          cur = 'regal';
          name = 'Regal Orb';
        } else if (cRoll < 65) {
          cur = 'scouring';
          name = 'Orb of Scouring';
        } else if (cRoll < 85) {
          cur = 'alteration';
          name = 'Orb of Alteration';
        }

        drops.push({ category: 'currency', currencyType: cur, name });
      }
      // 30% rơi Trang bị có Tier
      else if (typeRoll < 0.85) {
        const bases: ('Sword' | 'Bow' | 'Wand' | 'Plate')[] = ['Sword', 'Bow', 'Wand', 'Plate'];
        const base = bases[Math.floor(Math.random() * bases.length)];
        const itemTier = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

        const item: EquipmentItem = {
          id: `eq_${Date.now()}_${Math.random()}`,
          name: `${base}`,
          baseType: base,
          tier: itemTier,
          rarity: 'Normal',
          prefixes: [],
          suffixes: [],
        };

        if (rarity === 'Rare' || rarity === 'Boss') {
          CraftingEngine.applyTransmutation(item);
          CraftingEngine.applyRegal(item);
        } else if (rarity === 'Magic') {
          CraftingEngine.applyTransmutation(item);
        }

        drops.push({
          category: 'equipment',
          equipmentItem: item,
          name: `[T${item.tier} ${item.rarity}] ${item.baseType}`,
        });
      }
      // 15% rơi Ngọc kỹ năng
      else {
        const gemKeys = ['fireball', 'split_arrow', 'ground_slam', 'frostbolt', 'spark', 'blade_vortex', 'arc', 'molten_strike', 'toxic_spore'];
        const gid = gemKeys[Math.floor(Math.random() * gemKeys.length)];
        drops.push({ category: 'gem', gemId: gid, name: `Ngọc ${gid.toUpperCase()}` });
      }
    }

    return drops;
  }
}
''',

    # 6. Cập nhật CraftingUI.ts: Bổ sung tính năng [NÂNG TIER / GHÉP ĐỒ]
    "src/scenes/CraftingUI.ts": '''import Phaser from 'phaser';
import { InventoryData, CurrencyType } from '../core/items/ItemTypes';
import { CraftingEngine } from '../core/crafting/CraftingEngine';
import { Player } from './Player';
import { SoundEffects } from '../core/audio/SoundEffects';

export class CraftingUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isOpen: boolean = false;
  private inventoryData: InventoryData;
  private player: Player;
  private onItemUpdated: () => void;

  private itemTitleText!: Phaser.GameObjects.Text;
  private socketsText!: Phaser.GameObjects.Text;
  private affixesText!: Phaser.GameObjects.Text;
  private tierBonusText!: Phaser.GameObjects.Text;
  private bagElements: Phaser.GameObjects.GameObject[] = [];
  private currencyButtons: Map<CurrencyType, Phaser.GameObjects.Text> = new Map();

  constructor(scene: Phaser.Scene, inv: InventoryData, player: Player, onItemUpdated: () => void) {
    this.scene = scene;
    this.inventoryData = inv;
    this.player = player;
    this.onItemUpdated = onItemUpdated;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(450);
    this.createPanel();
    this.container.setVisible(false);
  }

  public toggle(): void {
    this.isOpen = !this.isOpen;
    this.container.setVisible(this.isOpen);
    if (this.isOpen) {
      this.refresh();
    }
  }

  public getIsOpen(): boolean {
    return this.isOpen;
  }

  private createPanel(): void {
    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    const bg = this.scene.add.rectangle(cx, cy, 780, 530, 0x090d16, 1.0)
      .setStrokeStyle(2, 0x30363d)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 240, 'HÀNH TRANG & RÈN TRANG BỊ (TIER FORGE) [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(header);

    // CỘT TRÁI: ĐANG MẶC
    this.itemTitleText = this.scene.add.text(cx - 200, cy - 200, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.itemTitleText);

    this.tierBonusText = this.scene.add.text(cx - 370, cy - 180, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#fbbf24',
    }).setScrollFactor(0);
    this.container.add(this.tierBonusText);

    this.socketsText = this.scene.add.text(cx - 370, cy - 155, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      lineSpacing: 3,
    }).setScrollFactor(0);
    this.container.add(this.socketsText);

    this.affixesText = this.scene.add.text(cx - 370, cy - 70, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#8888ff',
      lineSpacing: 3,
    });
    this.container.add(this.affixesText);

    // CỘT PHẢI: TÚI ĐỒ & GHÉP ĐỒ
    const bagTitle = this.scene.add.text(cx + 170, cy - 200, '❖ TÚI ĐỒ (BẤM MẶC HOẶC GHÉP TIER):', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(bagTitle);

    // NÚT GHÉP ĐỒ TĂNG TIER
    const forgeBtn = this.scene.add.text(cx + 170, cy - 165, '🔨 HIẾN TẾ 2 MÓN TRONG TÚI ĐỂ NÂNG +1 TIER', {
      fontFamily: 'monospace',
      fontSize: '11px',
      fontStyle: 'bold',
      color: '#000000',
      backgroundColor: '#f59e0b',
      padding: { x: 8, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    forgeBtn.on('pointerdown', () => this.forgeUpgradeTier());
    forgeBtn.on('pointerover', () => forgeBtn.setBackgroundColor('#ffffff'));
    forgeBtn.on('pointerout', () => forgeBtn.setBackgroundColor('#f59e0b'));
    this.container.add(forgeBtn);

    // HÀNG DƯỚI: CRAFTING CURRENCY
    const curList: { type: CurrencyType; name: string }[] = [
      { type: 'transmutation', name: 'Transmute' },
      { type: 'alteration', name: 'Alteration' },
      { type: 'regal', name: 'Regal' },
      { type: 'chaos', name: 'Chaos' },
      { type: 'exalted', name: 'Exalted' },
      { type: 'scouring', name: 'Scouring' },
    ];

    const startY = cy + 135;
    curList.forEach((c, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const bx = cx - 180 + col * 180;
      const by = startY + row * 48;

      const btn = this.scene.add.text(bx, by, '', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#ffffff',
        backgroundColor: '#21262d',
        padding: { x: 10, y: 7 },
        stroke: '#000000',
        strokeThickness: 2,
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

      btn.on('pointerdown', () => this.useCurrency(c.type));
      btn.on('pointerover', () => btn.setBackgroundColor('#388bfd'));
      btn.on('pointerout', () => btn.setBackgroundColor('#21262d'));

      this.currencyButtons.set(c.type, btn);
      this.container.add(btn);
    });

    const closeBtn = this.scene.add.text(cx, cy + 235, '[ĐÓNG GIAO DIỆN (I)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8b949e',
      backgroundColor: '#161b22',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  // TÍNH NĂNG GHÉP ĐỒ HIẾN TẾ NÂNG TIER
  private forgeUpgradeTier(): void {
    if (this.inventoryData.bag.length < 2) {
      alert('Cần ít nhất 2 trang bị trong túi đồ để làm nguyên liệu hiến tế nâng Tier!');
      return;
    }
    if (this.inventoryData.equippedItem.tier >= 5) {
      alert('Trang bị đang mặc đã đạt cấp tối đa (Tier 5)!');
      return;
    }

    // Tiêu thụ 2 món đầu tiên trong túi
    this.inventoryData.bag.splice(0, 2);
    this.inventoryData.equippedItem.tier++;

    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private equipFromBag(index: number): void {
    if (index >= this.inventoryData.bag.length) return;
    const itemToEquip = this.inventoryData.bag[index];
    const oldItem = this.inventoryData.equippedItem;

    this.inventoryData.equippedItem = itemToEquip;
    this.inventoryData.bag[index] = oldItem;

    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private useCurrency(cur: CurrencyType): void {
    const qty = this.inventoryData.currencies[cur] || 0;
    if (qty <= 0) return;

    const success = CraftingEngine.applyCurrency(cur, this.inventoryData.equippedItem);
    if (success) {
      SoundEffects.playHit();
      this.inventoryData.currencies[cur]--;
      this.onItemUpdated();
      this.refresh();
    }
  }

  public refresh(): void {
    const item = this.inventoryData.equippedItem;
    const rarityColor = item.rarity === 'Rare' ? '#ffd700' : item.rarity === 'Magic' ? '#4169e1' : '#ffffff';
    this.itemTitleText.setText(`[TIER ${item.tier} - ${item.rarity.toUpperCase()}] ${item.baseType}`);
    this.itemTitleText.setColor(rarityColor);

    const tierMult = 1 + (item.tier - 1) * 0.4;
    this.tierBonusText.setText(`★ Hiệu Lực Tier ${item.tier}: Gia tăng ${Math.round((tierMult - 1) * 100)}% toàn bộ chỉ số món đồ`);

    let sockStr = '❖ LỖ NGỌC & LIÊN KẾT:\\n';
    this.player.sockets.forEach((s, idx) => {
      const gemName = s.gem ? s.gem.name : '(Trống)';
      sockStr += `  • Ô ${idx + 1} [Nhóm ${s.linkGroup} - ${s.color.toUpperCase()}]: ${gemName}\\n`;
    });
    this.socketsText.setText(sockStr);

    let affStr = '--- PREFIXES ---\\n';
    if (item.prefixes.length === 0) affStr += '(Trống)\\n';
    item.prefixes.forEach((p) => {
      const scaledVal = Math.round(p.value * tierMult);
      affStr += `• ${p.name}: +${scaledVal} (${p.statType})\\n`;
    });

    affStr += '\\n--- SUFFIXES ---\\n';
    if (item.suffixes.length === 0) affStr += '(Trống)\\n';
    item.suffixes.forEach((s) => {
      const scaledVal = Math.round(s.value * tierMult);
      affStr += `• ${s.name}: +${scaledVal} (${s.statType})\\n`;
    });
    this.affixesText.setText(affStr);

    this.bagElements.forEach((el) => el.destroy());
    this.bagElements = [];

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    if (this.inventoryData.bag.length === 0) {
      const emptyText = this.scene.add.text(cx + 40, cy - 125, '(Túi trống - Đánh quái để nhặt trang bị)', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#64748b',
      }).setScrollFactor(0);
      this.bagElements.push(emptyText);
      this.container.add(emptyText);
    } else {
      this.inventoryData.bag.forEach((bagItem, idx) => {
        const itemY = cy - 135 + idx * 44;
        const rColor = bagItem.rarity === 'Rare' ? '#ffd700' : bagItem.rarity === 'Magic' ? '#60a5fa' : '#ffffff';

        const nameTxt = this.scene.add.text(cx + 10, itemY, `[T${bagItem.tier} ${bagItem.rarity}] ${bagItem.baseType}`, {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: rColor,
        }).setScrollFactor(0);

        const equipBtn = this.scene.add.text(cx + 270, itemY, 'MẶC ĐỒ', {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: '#000000',
          backgroundColor: '#38bdf8',
          padding: { x: 8, y: 4 },
        }).setScrollFactor(0).setInteractive({ useHandCursor: true });

        equipBtn.on('pointerdown', () => this.equipFromBag(idx));
        equipBtn.on('pointerover', () => equipBtn.setBackgroundColor('#ffffff'));
        equipBtn.on('pointerout', () => equipBtn.setBackgroundColor('#38bdf8'));

        this.bagElements.push(nameTxt, equipBtn);
        this.container.add([nameTxt, equipBtn]);
      });
    }

    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      btn.setText(`${type.toUpperCase()}\\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
''',

    # 7. Cập nhật Player.ts: Áp dụng Tier Multiplier & Hỗ trợ đa kỹ năng với Gem Level
    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats, getExpNeeded } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill, GroundSlamSkill, ALL_ACTIVE_SKILLS } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquipmentItem } from '../core/items/ItemTypes';
import { PassiveTreeBonus } from '../core/passive/PassiveTreeTypes';
import { Projectile } from './Projectile';

export class Player extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  public characterClass: CharacterClass;
  public sockets: Socket[] = [];
  public compiledSkills: SkillContext[] = [];

  private skillCooldownTimers: Map<string, number> = new Map();
  public skillBonusLevels: Map<string, number> = new Map();

  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private keyW!: Phaser.Input.Keyboard.Key;
  private keyA!: Phaser.Input.Keyboard.Key;
  private keyS!: Phaser.Input.Keyboard.Key;
  private keyD!: Phaser.Input.Keyboard.Key;
  private lastHitTime: number = 0;

  constructor(scene: Phaser.Scene, x: number, y: number, characterClass: CharacterClass) {
    const textureKey = `player_${characterClass.toLowerCase()}`;
    super(scene, x, y, textureKey, 0);

    this.characterClass = characterClass;
    this.stats = { ...CLASS_BASE_STATS[characterClass] };

    scene.add.existing(this);
    scene.physics.add.existing(this);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(18, 22);
      body.setOffset(7, 10);
      body.setCollideWorldBounds(true);
    }

    if (scene.input.keyboard) {
      this.cursors = scene.input.keyboard.createCursorKeys();
      this.keyW = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
      this.keyA = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
      this.keyS = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
      this.keyD = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);
    }

    this.setupClassSkillAndGems();
    this.compileSkills();
  }

  public setClass(newClass: CharacterClass): void {
    this.characterClass = newClass;
    const base = CLASS_BASE_STATS[newClass];
    this.stats = { ...base, level: this.stats.level, currentExp: this.stats.currentExp, maxExp: this.stats.maxExp };
    this.setTexture(`player_${newClass.toLowerCase()}`);
    this.setupClassSkillAndGems();
    this.compileSkills();
  }

  public setupClassSkillAndGems(): void {
    if (this.characterClass === 'Mage') {
      this.sockets = [
        { color: 'blue', linkGroup: 1, gem: FireballSkill },
        { color: 'green', linkGroup: 1, gem: GreaterMultipleProjectiles },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
      this.skillBonusLevels.set('fireball', 1);
    } else if (this.characterClass === 'Archer') {
      this.sockets = [
        { color: 'green', linkGroup: 1, gem: SplitArrowSkill },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
      this.skillBonusLevels.set('split_arrow', 1);
    } else {
      this.sockets = [
        { color: 'red', linkGroup: 1, gem: GroundSlamSkill },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
      ];
      this.skillBonusLevels.set('ground_slam', 1);
    }
  }

  public addOrUpgradeSkill(skillId: string): void {
    const curLvl = this.skillBonusLevels.get(skillId) || 0;
    this.skillBonusLevels.set(skillId, curLvl + 1);

    const existing = this.sockets.find((s) => s.gem && s.gem.id === skillId);
    if (!existing) {
      const newGem = ALL_ACTIVE_SKILLS[skillId];
      if (newGem) {
        this.sockets.push({
          color: newGem.color,
          linkGroup: this.sockets.length + 1,
          gem: newGem,
        });
      }
    }
    this.compileSkills();
  }

  public gainExp(amount: number): boolean {
    this.stats.currentExp += amount;
    if (this.stats.currentExp >= this.stats.maxExp) {
      this.stats.currentExp -= this.stats.maxExp;
      this.stats.level++;
      this.stats.maxExp = getExpNeeded(this.stats.level);
      this.stats.maxLife += 15;
      this.stats.currentLife = this.stats.maxLife;
      if (this.stats.maxEnergyShield > 0) {
        this.stats.maxEnergyShield += 10;
        this.stats.energyShield = this.stats.maxEnergyShield;
      }
      return true;
    }
    return false;
  }

  public recalculateTotalStats(item: EquipmentItem, treeBonus: PassiveTreeBonus): void {
    const base = CLASS_BASE_STATS[this.characterClass];
    const levelBonusLife = (this.stats.level - 1) * 15;
    const levelBonusES = (this.stats.level - 1) * 10;

    // Hệ số khuếch đại theo Tier trang bị: +40% mỗi Tier
    const tierMultiplier = 1 + (item.tier - 1) * 0.4;

    this.stats.maxLife = base.maxLife + levelBonusLife + treeBonus.flatLife;
    this.stats.maxEnergyShield = base.maxEnergyShield + (base.maxEnergyShield > 0 ? levelBonusES : 0) + treeBonus.flatES;
    this.stats.armour = base.armour + treeBonus.flatArmour;
    this.stats.evasion = base.evasion + treeBonus.flatEvasion;
    this.stats.movementSpeed = base.movementSpeed + treeBonus.movementSpeed;

    const allAffixes = [...item.prefixes, ...item.suffixes];
    for (const aff of allAffixes) {
      const scaledVal = Math.round(aff.value * tierMultiplier);
      if (aff.statType === 'flat_life') this.stats.maxLife += scaledVal;
      if (aff.statType === 'flat_es') this.stats.maxEnergyShield += scaledVal;
      if (aff.statType === 'armour') this.stats.armour += scaledVal;
      if (aff.statType === 'movement_speed') this.stats.movementSpeed += scaledVal;
    }

    this.stats.currentLife = Math.min(this.stats.currentLife, this.stats.maxLife);
    this.compileSkills(item, treeBonus);
  }

  public compileSkills(equippedItem?: EquipmentItem, treeBonus?: PassiveTreeBonus): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    let addedDmg = 0;
    let incDmg = 0;
    let atkSpeedPct = 0;
    let critChance = 0;
    let critMultiplier = 0;
    let extraProj = 0;
    let extraPierce = 0;

    const tierMult = equippedItem ? 1 + (equippedItem.tier - 1) * 0.4 : 1;

    if (equippedItem) {
      const allAff = [...equippedItem.prefixes, ...equippedItem.suffixes];
      for (const a of allAff) {
        const val = Math.round(a.value * tierMult);
        if (a.statType === 'added_damage') addedDmg += val;
        if (a.statType === 'inc_damage') incDmg += val;
        if (a.statType === 'attack_speed') atkSpeedPct += val;
        if (a.statType === 'crit_chance') critChance += val;
      }
    }

    if (treeBonus) {
      atkSpeedPct += treeBonus.attackSpeedPct;
      critChance += treeBonus.critChance;
      critMultiplier += treeBonus.critMultiplier;
      extraProj += treeBonus.extraProjectile;
      extraPierce += treeBonus.extraPierce;
    }

    for (const activeSock of activeSockets) {
      const activeGem = activeSock.gem as ActiveGem;
      const sLvl = this.skillBonusLevels.get(activeGem.id) || 1;
      const ctx = activeGem.getInitialContext(sLvl);

      if (ctx.damageType === 'physical' && treeBonus) {
        incDmg += treeBonus.incPhysDamage;
      } else if (ctx.damageType === 'fire' && treeBonus) {
        incDmg += treeBonus.incFireDamage;
      }

      ctx.addedMinDamage += addedDmg;
      ctx.addedMaxDamage += addedDmg;
      ctx.increasedDamagePercent += incDmg;
      ctx.attackSpeedMultiplier *= (1 + atkSpeedPct / 100);
      ctx.critChance += critChance;
      ctx.critMultiplier += critMultiplier;
      ctx.projectileCount += extraProj;
      ctx.pierceCount += extraPierce;

      const linkedSupports = this.sockets.filter(
        (s) => s.linkGroup === activeSock.linkGroup && s.gem && 'apply' in s.gem
      );

      for (const suppSock of linkedSupports) {
        const supportGem = suppSock.gem as SupportGem;
        supportGem.apply(ctx);
      }

      this.compiledSkills.push(ctx);
    }
  }

  public tryCastSkills(
    time: number,
    targetX: number,
    targetY: number,
    projectilePool: Phaser.Physics.Arcade.Group
  ): void {
    if (this.compiledSkills.length === 0) return;

    for (const skill of this.compiledSkills) {
      const lastCast = this.skillCooldownTimers.get(skill.id) || 0;
      const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
      if (time - lastCast < cooldown) continue;

      this.skillCooldownTimers.set(skill.id, time);

      const baseAngle = Phaser.Math.Angle.Between(this.x, this.y, targetX, targetY);
      const count = skill.projectileCount;
      const spreadAngle = 0.16;

      for (let i = 0; i < count; i++) {
        const p = projectilePool.get(this.x, this.y) as Projectile;
        if (!p) continue;

        const offset = (i - (count - 1) / 2) * spreadAngle;
        p.fire(this.x, this.y, baseAngle + offset, skill);
      }
    }
  }

  public getCooldownPercent(skillId: string, time: number): number {
    const skill = this.compiledSkills.find((s) => s.id === skillId);
    if (!skill) return 0;
    const lastCast = this.skillCooldownTimers.get(skillId) || 0;
    const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
    const elapsed = time - lastCast;
    if (elapsed >= cooldown) return 0;
    return 1 - elapsed / cooldown;
  }

  public takePhysicalDamage(rawDamage: number, time: number): boolean {
    if (Math.random() * 100 < this.stats.evasion) {
      return false;
    }

    const dr = this.stats.armour / (this.stats.armour + 5 * rawDamage);
    const damage = Math.max(1, Math.round(rawDamage * (1 - Math.min(dr, 0.9))));

    this.lastHitTime = time;

    let remaining = damage;
    if (this.stats.energyShield > 0) {
      const absorbed = Math.min(this.stats.energyShield, remaining);
      this.stats.energyShield -= absorbed;
      remaining -= absorbed;
    }

    if (remaining > 0) {
      this.stats.currentLife = Math.max(0, this.stats.currentLife - remaining);
    }

    this.setTint(0xff3333);
    this.scene.time.delayedCall(120, () => {
      if (this.active) this.clearTint();
    });

    return true;
  }

  update(time: number, delta: number): void {
    const speed = this.stats.movementSpeed;
    let vx = 0;
    let vy = 0;

    if (this.cursors.left.isDown || this.keyA.isDown) vx -= 1;
    if (this.cursors.right.isDown || this.keyD.isDown) vx += 1;
    if (this.cursors.up.isDown || this.keyW.isDown) vy -= 1;
    if (this.cursors.down.isDown || this.keyS.isDown) vy += 1;

    if (vx !== 0 && vy !== 0) {
      vx *= 0.7071;
      vy *= 0.7071;
    }

    this.setVelocity(vx * speed, vy * speed);

    const prefix = `player_${this.characterClass.toLowerCase()}`;
    if (vx > 0) {
      this.play(`${prefix}_walk_right`, true);
      this.setFlipX(false);
    } else if (vx < 0) {
      this.play(`${prefix}_walk_right`, true);
      this.setFlipX(true);
    } else if (vy > 0) {
      this.play(`${prefix}_walk_down`, true);
      this.setFlipX(false);
    } else if (vy < 0) {
      this.play(`${prefix}_walk_up`, true);
      this.setFlipX(false);
    } else {
      this.anims.stop();
    }

    if (
      this.stats.maxEnergyShield > 0 &&
      this.stats.energyShield < this.stats.maxEnergyShield &&
      time - this.lastHitTime > this.stats.esRechargeDelay * 1000
    ) {
      const rechargeRate = (this.stats.maxEnergyShield * 0.25 * delta) / 1000;
      this.stats.energyShield = Math.min(this.stats.maxEnergyShield, this.stats.energyShield + rechargeRate);
    }
  }
}
''',

    # 8. Cập nhật Projectile.ts: Thêm đồ họa cho Arc, Molten Strike, Toxic Spore
    "src/scenes/Projectile.ts": '''import Phaser from 'phaser';
import { SkillContext } from '../core/gems/GemTypes';

export class Projectile extends Phaser.Physics.Arcade.Sprite {
  public skillCtx!: SkillContext;
  public remainingPierce: number = 0;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'proj_fireball');
  }

  fire(x: number, y: number, angleRad: number, ctx: SkillContext): void {
    this.skillCtx = ctx;
    this.remainingPierce = ctx.pierceCount;

    let texKey = 'proj_fireball';
    if (ctx.id === 'split_arrow') texKey = 'proj_arrow';
    else if (ctx.id === 'ground_slam') texKey = 'proj_slam';
    else if (ctx.id === 'frostbolt') texKey = 'proj_frostbolt';
    else if (ctx.id === 'spark') texKey = 'proj_spark';
    else if (ctx.id === 'blade_vortex') texKey = 'proj_blade';
    else if (ctx.id === 'arc') texKey = 'proj_arc';
    else if (ctx.id === 'molten_strike') texKey = 'proj_molten';
    else if (ctx.id === 'toxic_spore') texKey = 'proj_toxic';

    this.setTexture(texKey);
    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      if (ctx.id === 'ground_slam' || ctx.id === 'molten_strike') {
        body.setSize(24, 24);
      } else if (ctx.id === 'blade_vortex') {
        body.setSize(20, 16);
      } else {
        body.setSize(12, 12);
      }
      this.scene.physics.velocityFromRotation(angleRad, ctx.projectileSpeed, body.velocity);
    }

    const lifeTime = ctx.id === 'ground_slam' ? 500 : ctx.id === 'blade_vortex' ? 1200 : 2500;
    this.scene.time.delayedCall(lifeTime, () => {
      if (this.active) this.kill();
    });
  }

  kill(): void {
    this.disableBody(true, true);
  }
}
''',

    # 9. Cập nhật BattleScene.ts: HUD Kỹ Năng Đang Dùng & Thanh Hồi Chiêu Trực Quan
    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { Monster } from './Monster';
import { LootDrop } from './LootDrop';
import { CraftingUI } from './CraftingUI';
import { PassiveTreeUI } from './PassiveTreeUI';
import { CharacterUI } from './CharacterUI';
import { LevelUpUI, LevelUpChoice } from './LevelUpUI';
import { IntermissionUI } from './IntermissionUI';
import { WaveManager } from '../core/monsters/WaveManager';
import { DamageEngine } from '../core/combat/DamageEngine';
import { LootEngine } from '../core/loot/LootEngine';
import { PassiveTreeManager } from '../core/passive/PassiveTreeManager';
import { InventoryData } from '../core/items/ItemTypes';
import { SoundEffects } from '../core/audio/SoundEffects';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private monsterPool!: Phaser.Physics.Arcade.Group;
  private lootPool!: Phaser.Physics.Arcade.Group;
  private waveManager: WaveManager = new WaveManager();
  private passiveTreeManager: PassiveTreeManager = new PassiveTreeManager();

  private craftingUI!: CraftingUI;
  private passiveTreeUI!: PassiveTreeUI;
  private characterUI!: CharacterUI;
  private levelUpUI!: LevelUpUI;
  private intermissionUI!: IntermissionUI;

  private inventoryData: InventoryData = {
    currencies: {
      transmutation: 4,
      alteration: 8,
      regal: 2,
      chaos: 2,
      exalted: 1,
      scouring: 2,
    },
    equippedItem: {
      id: 'eq_starter',
      name: 'Vũ khí Sắt Rèn',
      baseType: 'Sword',
      tier: 1,
      rarity: 'Normal',
      prefixes: [],
      suffixes: [],
    },
    bag: [],
  };

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
  private bestWaveText!: Phaser.GameObjects.Text;
  private classLevelText!: Phaser.GameObjects.Text;
  private lifeBarGfx!: Phaser.GameObjects.Graphics;
  private esBarGfx!: Phaser.GameObjects.Graphics;
  private expBarGfx!: Phaser.GameObjects.Graphics;

  // HUD THANH KỸ NĂNG CHÍNH (SKILL BAR)
  private skillBarContainer!: Phaser.GameObjects.Container;
  private skillSlotWidgets: { bg: Phaser.GameObjects.Rectangle; icon: Phaser.GameObjects.Text; lvl: Phaser.GameObjects.Text; cdGfx: Phaser.GameObjects.Graphics; id: string }[] = [];

  private isGameOver: boolean = false;
  private bestWave: number = 1;
  private isHoveringInteractiveUI: boolean = false;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2400;
    const mapHeight = 2400;

    this.isGameOver = false;
    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    const savedBest = localStorage.getItem('poe_roguelike_best_wave');
    this.bestWave = savedBest ? parseInt(savedBest, 10) : 1;

    this.createProceduralTextures();

    // Map sàn
    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');
    this.syncPlayerStats();

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    this.projectilePool = this.physics.add.group({
      classType: Projectile,
      maxSize: 150,
      runChildUpdate: false,
    });

    this.monsterPool = this.physics.add.group({
      classType: Monster,
      maxSize: 200,
      runChildUpdate: false,
    });

    this.lootPool = this.physics.add.group({
      classType: LootDrop,
      maxSize: 100,
      runChildUpdate: false,
    });

    // Va chạm: Đạn -> Quái
    this.physics.add.overlap(this.projectilePool, this.monsterPool, (projObj, monObj) => {
      const proj = projObj as Projectile;
      const monster = monObj as Monster;

      if (!proj.active || !monster.active) return;

      const hit = DamageEngine.calculateHit(proj.skillCtx, monster.poeStatsWrapper);
      const isDead = monster.syncLifeAfterHit();

      SoundEffects.playHit();
      CombatUI.showDamageText(this, monster.x, monster.y, hit);

      if (isDead) {
        const leveledUp = this.player.gainExp(monster.monsterStats.expReward);
        if (leveledUp) {
          this.triggerLevelUpChoiceModal();
        }

        this.dropLoot(monster.x, monster.y, monster.monsterStats.rarity);
        monster.kill();
      }

      if (proj.remainingPierce > 0) {
        proj.remainingPierce--;
      } else {
        proj.kill();
      }
    });

    // Va chạm: Nhặt đồ
    this.physics.add.overlap(this.player, this.lootPool, (_playerObj, lootObj) => {
      const loot = lootObj as LootDrop;
      if (!loot.active) return;

      const d = loot.collect();
      if (d.category === 'currency' && d.currencyType) {
        this.inventoryData.currencies[d.currencyType] = (this.inventoryData.currencies[d.currencyType] || 0) + 1;
        this.showPickupNotice(loot.x, loot.y, d.currencyType.toUpperCase());
      } else if (d.category === 'equipment' && d.equipmentItem) {
        if (this.inventoryData.bag.length < 6) {
          this.inventoryData.bag.push(d.equipmentItem);
          this.showPickupNotice(loot.x, loot.y, `TÚI: ${d.name}`);
        } else {
          this.showPickupNotice(loot.x, loot.y, `TÚI ĐÃ ĐẦY!`);
        }
      } else if (d.category === 'gem' && d.gemId) {
        this.player.addOrUpgradeSkill(d.gemId);
        this.syncPlayerStats();
        this.showPickupNotice(loot.x, loot.y, `HỌC NGỌC: ${d.name}`);
      }
    });

    // Va chạm: Quái -> Người chơi
    this.physics.add.overlap(this.player, this.monsterPool, (_playerObj, monObj) => {
      if (this.isGameOver || this.intermissionUI.getIsShowing() || this.levelUpUI.getIsShowing()) return;
      const monster = monObj as Monster;
      if (!monster.active) return;

      const time = this.time.now;
      if (monster.canAttack(time)) {
        const tookDmg = this.player.takePhysicalDamage(monster.monsterStats.damage, time);
        if (tookDmg) {
          CombatUI.showDamageText(this, this.player.x, this.player.y, {
            damage: monster.monsterStats.damage,
            isCrit: false,
            type: 'physical',
            absorbedByES: 0,
            absorbedByLife: monster.monsterStats.damage,
          });
        }

        if (this.player.stats.currentLife <= 0) {
          this.triggerGameOver();
        }
      }
    });

    this.createHUD();
    this.createSkillBarHUD(); // HUD THANH KỸ NĂNG
    this.createTopRightActionMenu();

    this.craftingUI = new CraftingUI(this, this.inventoryData, this.player, () => this.syncPlayerStats());
    this.passiveTreeUI = new PassiveTreeUI(this, this.passiveTreeManager, () => this.syncPlayerStats());
    this.characterUI = new CharacterUI(this, this.player);
    this.levelUpUI = new LevelUpUI(this);

    this.intermissionUI = new IntermissionUI(
      this,
      () => this.startNextWave(),
      () => this.craftingUI.toggle(),
      () => this.passiveTreeUI.toggle()
    );

    this.input.keyboard?.on('keydown-C', () => this.characterUI.toggle());
    this.input.keyboard?.on('keydown-I', () => this.craftingUI.toggle());
    this.input.keyboard?.on('keydown-P', () => this.passiveTreeUI.toggle());
    this.input.keyboard?.on('keydown-SPACE', () => {
      if (this.intermissionUI.getIsShowing()) {
        this.startNextWave();
      }
    });

    this.time.addEvent({
      delay: 1200,
      callback: this.spawnMonsterWave,
      callbackScope: this,
      loop: true,
    });

    this.time.addEvent({
      delay: 1000,
      callback: this.tickWaveTimer,
      callbackScope: this,
      loop: true,
    });
  }

  // TẠO HUD THANH KỸ NĂNG Ở DƯỚI ĐÁY MÀN HÌNH
  private createSkillBarHUD(): void {
    this.skillBarContainer = this.add.container(0, 0).setScrollFactor(0).setDepth(200);
    this.rebuildSkillBarWidgets();
  }

  private rebuildSkillBarWidgets(): void {
    this.skillBarContainer.removeAll(true);
    this.skillSlotWidgets = [];

    const skills = this.player.compiledSkills;
    const startX = this.scale.width / 2 - (skills.length * 60) / 2 + 30;
    const slotY = this.scale.height - 50;

    skills.forEach((skill, idx) => {
      const slotX = startX + idx * 60;

      const bg = this.add.rectangle(slotX, slotY, 50, 50, 0x111827, 0.95)
        .setStrokeStyle(2, 0x38bdf8)
        .setScrollFactor(0);

      const icon = this.add.text(slotX, slotY - 6, skill.name.slice(0, 2).toUpperCase(), {
        fontFamily: 'monospace',
        fontSize: '14px',
        fontStyle: 'bold',
        color: '#ffffff',
      }).setOrigin(0.5).setScrollFactor(0);

      const lvl = this.add.text(slotX, slotY + 14, `Lv.${skill.level}`, {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: '#ffd700',
      }).setOrigin(0.5).setScrollFactor(0);

      const cdGfx = this.add.graphics().setScrollFactor(0);

      this.skillBarContainer.add([bg, icon, lvl, cdGfx]);
      this.skillSlotWidgets.push({ bg, icon, lvl, cdGfx, id: skill.id });
    });
  }

  // BẢNG 3 LỰA CHỌN KHI LÊN CẤP
  private triggerLevelUpChoiceModal(): void {
    SoundEffects.playWaveClear();
    this.passiveTreeManager.unspentPoints++;

    const pool: LevelUpChoice[] = [
      {
        id: 'arc',
        title: 'Arc (Tia Sét Xích)',
        description: 'Tia sét chuỗi giật nhanh, nảy bật qua 2 mục tiêu.',
        type: 'new_skill',
        skillId: 'arc',
        apply: () => {
          this.player.addOrUpgradeSkill('arc');
          this.syncPlayerStats();
        },
      },
      {
        id: 'molten_strike',
        title: 'Molten Strike (Hỏa Nham)',
        description: 'Bắn ra chùm dung nham rực lửa gây sát thương nổ lan.',
        type: 'new_skill',
        skillId: 'molten_strike',
        apply: () => {
          this.player.addOrUpgradeSkill('molten_strike');
          this.syncPlayerStats();
        },
      },
      {
        id: 'toxic_spore',
        title: 'Toxic Spore (Bào Tử Độc)',
        description: 'Bắn các cụm độc tố Chaos nổ tung trên diện rộng.',
        type: 'new_skill',
        skillId: 'toxic_spore',
        apply: () => {
          this.player.addOrUpgradeSkill('toxic_spore');
          this.syncPlayerStats();
        },
      },
      {
        id: 'frostbolt',
        title: 'Frostbolt (Băng Cầu)',
        description: 'Bắn cầu băng xuyên thấu 100% mục tiêu, làm chậm quái.',
        type: 'new_skill',
        skillId: 'frostbolt',
        apply: () => {
          this.player.addOrUpgradeSkill('frostbolt');
          this.syncPlayerStats();
        },
      },
      {
        id: 'spark',
        title: 'Spark (Tia Sét Tán Xạ)',
        description: 'Bắn 4 tia sét giật nhanh tán xạ rộng xung quanh.',
        type: 'new_skill',
        skillId: 'spark',
        apply: () => {
          this.player.addOrUpgradeSkill('spark');
          this.syncPlayerStats();
        },
      },
      {
        id: 'blade_vortex',
        title: 'Blade Vortex (Bão Kiếm)',
        description: 'Tạo các lưỡi kiếm xoay vòng chém liên tục quái áp sát.',
        type: 'new_skill',
        skillId: 'blade_vortex',
        apply: () => {
          this.player.addOrUpgradeSkill('blade_vortex');
          this.syncPlayerStats();
        },
      },
      {
        id: 'upgrade_main',
        title: 'Cường Hóa Kỹ Năng Hiện Có',
        description: '+1 Level cho toàn bộ kỹ năng đang trang bị (+30% Sát thương).',
        type: 'upgrade_skill',
        apply: () => {
          this.player.compiledSkills.forEach((s) => this.player.addOrUpgradeSkill(s.id));
          this.syncPlayerStats();
        },
      },
      {
        id: 'vitality_boost',
        title: 'Thể Lực Bất Hoại',
        description: '+50 Máu Tối Đa và +20 Tốc Độ Di Chuyển.',
        type: 'stat_boost',
        apply: () => {
          this.player.stats.maxLife += 50;
          this.player.stats.currentLife = this.player.stats.maxLife;
          this.player.stats.movementSpeed += 20;
          this.syncPlayerStats();
        },
      },
    ];

    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    const selected3 = shuffled.slice(0, 3);

    this.levelUpUI.show(selected3, () => {
      this.syncPlayerStats();
      this.rebuildSkillBarWidgets();
    });
  }

  private createTopRightActionMenu(): void {
    const rx = this.scale.width - 20;

    const classBtn = this.add.text(rx, 20, '🎭 ĐỔI CLASS', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#a78bfa',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    classBtn.on('pointerdown', () => {
      const classes: ('Mage' | 'Archer' | 'Knight')[] = ['Mage', 'Archer', 'Knight'];
      const nextIdx = (classes.indexOf(this.player.characterClass) + 1) % classes.length;
      this.player.setClass(classes[nextIdx]);
      this.syncPlayerStats();
      this.rebuildSkillBarWidgets();
    });

    const charBtn = this.add.text(rx, 55, '👤 CHỈ SỐ (C)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    charBtn.on('pointerdown', () => this.characterUI.toggle());

    const craftBtn = this.add.text(rx, 90, '⚒️ HÒM & RÈN TIER (I)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#ffd700',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    craftBtn.on('pointerdown', () => this.craftingUI.toggle());

    const treeBtn = this.add.text(rx, 125, '🌲 THIÊN PHÚ (P)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#4ade80',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    treeBtn.on('pointerdown', () => this.passiveTreeUI.toggle());

    [classBtn, charBtn, craftBtn, treeBtn].forEach((btn) => {
      btn.on('pointerover', () => {
        this.isHoveringInteractiveUI = true;
        btn.setBackgroundColor('#30363d');
      });
      btn.on('pointerout', () => {
        this.isHoveringInteractiveUI = false;
        btn.setBackgroundColor('#21262d');
      });
    });
  }

  private syncPlayerStats(): void {
    const bonus = this.passiveTreeManager.calculateTotalBonus();
    this.player.recalculateTotalStats(this.inventoryData.equippedItem, bonus);
  }

  private dropLoot(x: number, y: number, rarity: any): void {
    const drops = LootEngine.rollMonsterDrops(rarity);
    drops.forEach((d) => {
      let loot = this.lootPool.getFirstDead(false) as LootDrop;
      if (!loot) {
        loot = new LootDrop(this, x, y);
        this.lootPool.add(loot);
      }
      loot.spawn(x + (Math.random() * 30 - 15), y + (Math.random() * 30 - 15), d);

      if (d.category === 'currency' && (d.currencyType === 'chaos' || d.currencyType === 'exalted')) {
        SoundEffects.playPoETink();
      }
    });
  }

  private showPickupNotice(x: number, y: number, text: string): void {
    const t = this.add.text(x, y - 20, `+ ${text}`, {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);

    this.tweens.add({
      targets: t,
      y: y - 50,
      alpha: 0,
      duration: 700,
      onComplete: () => t.destroy(),
    });
  }

  private createProceduralTextures(): void {
    if (!this.textures.exists('proj_fireball')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xef4444, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xfde047, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_fireball', 16, 16);
      g.destroy();
    }

    if (!this.textures.exists('proj_arrow')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x22c55e, 1);
      g.fillRect(0, 5, 14, 2);
      g.fillTriangle(16, 6, 11, 2, 11, 10);
      g.generateTexture('proj_arrow', 16, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_slam')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xd97706, 0.9);
      g.fillCircle(12, 12, 12);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(12, 12, 6);
      g.generateTexture('proj_slam', 24, 24);
      g.destroy();
    }

    if (!this.textures.exists('proj_frostbolt')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x06b6d4, 0.9);
      g.fillCircle(9, 9, 9);
      g.fillStyle(0xe0f2fe, 1);
      g.fillCircle(9, 9, 5);
      g.generateTexture('proj_frostbolt', 18, 18);
      g.destroy();
    }

    if (!this.textures.exists('proj_spark')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xfacc15, 1);
      g.fillCircle(6, 6, 5);
      g.fillStyle(0x67e8f9, 1);
      g.fillCircle(6, 6, 3);
      g.generateTexture('proj_spark', 12, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_blade')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x94a3b8, 1);
      g.fillRect(2, 6, 16, 4);
      g.fillStyle(0xffffff, 1);
      g.fillTriangle(20, 8, 16, 4, 16, 12);
      g.generateTexture('proj_blade', 20, 16);
      g.destroy();
    }

    if (!this.textures.exists('proj_arc')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x38bdf8, 1);
      g.fillRect(0, 4, 16, 4);
      g.fillStyle(0xffffff, 1);
      g.fillRect(4, 2, 8, 8);
      g.generateTexture('proj_arc', 16, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_molten')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xf97316, 1);
      g.fillCircle(10, 10, 10);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(10, 10, 5);
      g.generateTexture('proj_molten', 20, 20);
      g.destroy();
    }

    if (!this.textures.exists('proj_toxic')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x10b981, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xd8b4fe, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_toxic', 16, 16);
      g.destroy();
    }

    const list = [
      { key: 'monster_normal', body: 0x991b1b, eye: 0xfef08a, border: 0xef4444 },
      { key: 'monster_magic',  body: 0x1e40af, eye: 0x67e8f9, border: 0x60a5fa },
      { key: 'monster_rare',   body: 0x854d0e, eye: 0xffffff, border: 0xfacc15 },
      { key: 'monster_boss',   body: 0x581c87, eye: 0xff0055, border: 0xd8b4fe },
    ];

    list.forEach((item) => {
      if (!this.textures.exists(item.key)) {
        const g = this.make.graphics({ x: 0, y: 0 });
        g.fillStyle(item.body, 1);
        g.fillCircle(16, 16, 13);
        g.lineStyle(2, item.border, 1);
        g.strokeCircle(16, 16, 13);
        g.fillStyle(item.border, 1);
        g.fillTriangle(7, 8, 12, 13, 5, 14);
        g.fillTriangle(25, 8, 20, 13, 27, 14);
        g.fillStyle(item.eye, 1);
        g.fillCircle(11, 14, 2.5);
        g.fillCircle(21, 14, 2.5);
        g.generateTexture(item.key, 32, 32);
        g.destroy();
      }
    });

    if (!this.textures.exists('loot_dummy_tex')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xffffff, 1);
      g.fillRect(0, 0, 16, 16);
      g.generateTexture('loot_dummy_tex', 16, 16);
      g.destroy();
    }
  }

  private createHUD(): void {
    this.waveText = this.add.text(20, 20, 'ĐỢT: 1', {
      fontFamily: 'monospace',
      fontSize: '20px',
      fontStyle: 'bold',
      color: '#ffffff',
    }).setScrollFactor(0);

    this.timerText = this.add.text(20, 48, 'THỜI GIAN: 45s', {
      fontFamily: 'monospace',
      fontSize: '16px',
      color: '#00ffff',
    }).setScrollFactor(0);

    this.bestWaveText = this.add.text(20, 74, `KỶ LỤC: ĐỢT ${this.bestWave}`, {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setScrollFactor(0);

    this.classLevelText = this.add.text(20, 98, '', {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#a78bfa',
    }).setScrollFactor(0);

    this.lifeBarGfx = this.add.graphics().setScrollFactor(0);
    this.esBarGfx = this.add.graphics().setScrollFactor(0);
    this.expBarGfx = this.add.graphics().setScrollFactor(0);
  }

  private renderHUD(time: number): void {
    this.lifeBarGfx.clear();
    this.esBarGfx.clear();
    this.expBarGfx.clear();

    const barW = 220;
    const barH = 16;
    const x = 20;
    const y = this.scale.height - 45;

    this.classLevelText.setText(`[${this.player.characterClass.toUpperCase()}] CẤP: ${this.player.stats.level} (TIÊN PHONG)`);

    this.lifeBarGfx.fillStyle(0x000000, 0.7);
    this.lifeBarGfx.fillRect(x, y, barW, barH);
    const lifePct = Math.max(0, this.player.stats.currentLife / this.player.stats.maxLife);
    this.lifeBarGfx.fillStyle(0xdc143c, 1);
    this.lifeBarGfx.fillRect(x, y, barW * lifePct, barH);

    if (this.player.stats.maxEnergyShield > 0) {
      const esPct = Math.max(0, this.player.stats.energyShield / this.player.stats.maxEnergyShield);
      this.esBarGfx.fillStyle(0x1e90ff, 0.9);
      this.esBarGfx.fillRect(x, y - 8, barW * esPct, 6);
    }

    const expW = this.scale.width;
    const expPct = Math.max(0, this.player.stats.currentExp / this.player.stats.maxExp);
    this.expBarGfx.fillStyle(0x1e293b, 0.9);
    this.expBarGfx.fillRect(0, this.scale.height - 8, expW, 8);
    this.expBarGfx.fillStyle(0x38bdf8, 1);
    this.expBarGfx.fillRect(0, this.scale.height - 8, expW * expPct, 8);

    // Cập nhật hiệu ứng Hồi Chiêu trên thanh Kỹ Năng
    this.skillSlotWidgets.forEach((w) => {
      w.cdGfx.clear();
      const cdPct = this.player.getCooldownPercent(w.id, time);
      if (cdPct > 0) {
        w.cdGfx.fillStyle(0x000000, 0.65);
        w.cdGfx.fillRect(w.bg.x - 25, w.bg.y - 25 + 50 * (1 - cdPct), 50, 50 * cdPct);
      }
    });
  }

  private spawnMonsterWave(): void {
    if (
      this.isGameOver || 
      !this.waveManager.isWaveActive || 
      this.intermissionUI.getIsShowing() ||
      this.craftingUI.getIsOpen() ||
      this.passiveTreeUI.getIsOpen() ||
      this.characterUI.getIsOpen() ||
      this.levelUpUI.getIsShowing()
    ) {
      return;
    }

    const count = 3 + Math.floor(Math.random() * 3);
    const cam = this.cameras.main;

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const dist = Math.max(cam.width, cam.height) * 0.7;
      const spawnX = this.player.x + Math.cos(angle) * dist;
      const spawnY = this.player.y + Math.sin(angle) * dist;

      let monster = this.monsterPool.getFirstDead(false) as Monster;
      if (!monster) {
        monster = new Monster(this, spawnX, spawnY);
        this.monsterPool.add(monster);
      }

      const stats = this.waveManager.getMonsterStats(this.waveManager.currentWave);
      monster.spawn(spawnX, spawnY, stats);
    }
  }

  private tickWaveTimer(): void {
    if (this.isGameOver || this.intermissionUI.getIsShowing() || this.levelUpUI.getIsShowing()) return;

    this.waveManager.timeRemaining--;
    this.timerText.setText(`THỜI GIAN: ${this.waveManager.timeRemaining}s`);

    if (this.waveManager.timeRemaining <= 0) {
      this.waveManager.isWaveActive = false;

      if (this.waveManager.currentWave > this.bestWave) {
        this.bestWave = this.waveManager.currentWave;
        localStorage.setItem('poe_roguelike_best_wave', this.bestWave.toString());
        this.bestWaveText.setText(`KỶ LỤC: ĐỢT ${this.bestWave}`);
      }

      this.monsterPool.children.each((child) => {
        const mon = child as Monster;
        if (mon.active) mon.kill();
        return true;
      });

      SoundEffects.playWaveClear();

      this.passiveTreeManager.unspentPoints++;
      this.player.stats.currentLife = this.player.stats.maxLife;
      this.player.stats.energyShield = this.player.stats.maxEnergyShield;

      this.intermissionUI.show(this.waveManager.currentWave);
    }
  }

  private startNextWave(): void {
    this.intermissionUI.hide();
    this.waveManager.currentWave++;
    this.waveManager.timeRemaining = this.waveManager.waveDuration;
    this.waveManager.isWaveActive = true;
    this.waveText.setText(`ĐỢT: ${this.waveManager.currentWave}`);
  }

  private triggerGameOver(): void {
    this.isGameOver = true;
    this.player.setTint(0x555555);

    const overText = this.add.text(
      this.scale.width / 2,
      this.scale.height / 2,
      'BẠN ĐÃ TỬ NẠN!\\nNhấn [SPACE] để Hồi Sinh',
      {
        fontFamily: 'monospace',
        fontSize: '32px',
        fontStyle: 'bold',
        color: '#ff0000',
        align: 'center',
        backgroundColor: '#000000ee',
        padding: { x: 20, y: 15 },
      }
    ).setOrigin(0.5).setScrollFactor(0);

    this.input.keyboard?.once('keydown-SPACE', () => {
      overText.destroy();
      this.scene.restart();
    });
  }

  update(time: number, delta: number): void {
    if (this.isGameOver) return;

    const isUIBlocking = 
      this.intermissionUI.getIsShowing() || 
      this.craftingUI.getIsOpen() || 
      this.passiveTreeUI.getIsOpen() ||
      this.characterUI.getIsOpen() ||
      this.levelUpUI.getIsShowing();

    if (isUIBlocking) {
      const body = this.player.body as Phaser.Physics.Arcade.Body;
      if (body) body.setVelocity(0, 0);
      return;
    }

    this.player.update(time, delta);
    this.renderHUD(time);

    this.monsterPool.children.each((child) => {
      const mon = child as Monster;
      if (mon.active) {
        mon.updateAI(this.player.x, this.player.y);
      }
      return true;
    });

    const pointer = this.input.activePointer;
    if (pointer.isDown && !this.isHoveringInteractiveUI) {
      const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
      this.player.tryCastSkills(time, worldPoint.x, worldPoint.y, this.projectilePool);
      SoundEffects.playCast();
    }
  }
}
'''
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Đã cập nhật: {path}")

print("\nHoàn tất tích hợp toàn bộ: HUD Kỹ năng chính, Cấp ngọc, Nâng Tier trang bị & Mở rộng Thiên Phú!")