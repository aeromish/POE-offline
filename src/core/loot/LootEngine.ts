import { CurrencyType, EquipmentItem, ItemBaseType, EquipmentSlot } from '../items/ItemTypes';
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
  private static readonly ITEM_POOLS: { base: ItemBaseType; slot: EquipmentSlot }[] = [
    { base: 'Sword', slot: 'weapon' },
    { base: 'Bow', slot: 'weapon' },
    { base: 'Wand', slot: 'weapon' },
    { base: 'Shield', slot: 'offhand' },
    { base: 'Quiver', slot: 'offhand' },
    { base: 'Helmet', slot: 'helmet' },
    { base: 'Body Armour', slot: 'bodyArmour' },
    { base: 'Gloves', slot: 'gloves' },
    { base: 'Boots', slot: 'boots' },
    { base: 'Amulet', slot: 'amulet' },
    { base: 'Ring', slot: 'ring1' },
    { base: 'Belt', slot: 'belt' },
  ];

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

      // 50% rơi Currency
      if (typeRoll < 0.5) {
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
      // 35% rơi Trang bị thuộc 10 vị trí
      else if (typeRoll < 0.85) {
        const chosen = this.ITEM_POOLS[Math.floor(Math.random() * this.ITEM_POOLS.length)];
        const itemTier = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

        const item: EquipmentItem = {
          id: `eq_${Date.now()}_${Math.random()}`,
          name: chosen.base,
          baseType: chosen.base,
          slot: chosen.slot,
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
