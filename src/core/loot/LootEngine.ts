import { CurrencyType } from '../items/ItemTypes';
import { MonsterRarity } from '../monsters/MonsterTypes';

export interface DropResult {
  type: 'currency';
  currencyType: CurrencyType;
  name: string;
}

export class LootEngine {
  public static rollMonsterDrops(rarity: MonsterRarity): DropResult[] {
    const drops: DropResult[] = [];
    const roll = Math.random();

    // Tỉ lệ rơi dựa trên độ hiếm của quái
    let dropChance = 0.25; // Normal: 25% rơi 1 orb
    if (rarity === 'Magic') dropChance = 0.55;
    if (rarity === 'Rare') dropChance = 0.95;
    if (rarity === 'Boss') dropChance = 1.0;

    if (roll > dropChance) return drops;

    const numDrops = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

    for (let i = 0; i < numDrops; i++) {
      const cRoll = Math.random() * 100;
      let cur: CurrencyType = 'transmutation';
      let name = 'Orb of Transmutation';

      if (cRoll < 3 && (rarity === 'Rare' || rarity === 'Boss')) {
        cur = 'exalted';
        name = 'Exalted Orb';
      } else if (cRoll < 18 && (rarity === 'Magic' || rarity === 'Rare' || rarity === 'Boss')) {
        cur = 'chaos';
        name = 'Chaos Orb';
      } else if (cRoll < 35) {
        cur = 'regal';
        name = 'Regal Orb';
      } else if (cRoll < 60) {
        cur = 'scouring';
        name = 'Orb of Scouring';
      } else if (cRoll < 80) {
        cur = 'alteration';
        name = 'Orb of Alteration';
      }

      drops.push({ type: 'currency', currencyType: cur, name });
    }

    return drops;
  }
}
