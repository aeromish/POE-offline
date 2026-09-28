import { CurrencyType, EquipmentItem } from '../items/ItemTypes';
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
