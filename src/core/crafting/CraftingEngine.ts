import { EquipmentItem, CurrencyType, AffixInstance, AffixDefinition } from '../items/ItemTypes';
import { PREFIX_POOL, SUFFIX_POOL } from '../items/AffixPool';

export class CraftingEngine {
  private static rollAffix(def: AffixDefinition): AffixInstance {
    const val = Math.floor(def.minValue + Math.random() * (def.maxValue - def.minValue + 1));
    return {
      definitionId: def.id,
      name: def.name,
      type: def.type,
      statType: def.statType,
      value: val,
    };
  }

  private static getRandomAvailable(pool: AffixDefinition[], current: AffixInstance[]): AffixDefinition | null {
    const existingIds = new Set(current.map((a) => a.definitionId));
    const available = pool.filter((p) => !existingIds.has(p.id));
    if (available.length === 0) return null;
    return available[Math.floor(Math.random() * available.length)];
  }

  // Orb of Transmutation: Normal -> Magic (1-2 affixes)
  public static applyTransmutation(item: EquipmentItem): boolean {
    if (item.rarity !== 'Normal') return false;
    item.rarity = 'Magic';
    item.prefixes = [];
    item.suffixes = [];

    const rollP = Math.random() < 0.6;
    const rollS = Math.random() < 0.6 || !rollP;

    if (rollP) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    if (rollS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Orb of Alteration: Reroll Magic item
  public static applyAlteration(item: EquipmentItem): boolean {
    if (item.rarity !== 'Magic') return false;
    item.prefixes = [];
    item.suffixes = [];

    const rollP = Math.random() < 0.6;
    const rollS = Math.random() < 0.6 || !rollP;

    if (rollP) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    if (rollS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Regal Orb: Magic -> Rare (giữ mod cũ, thêm 1 mod mới)
  public static applyRegal(item: EquipmentItem): boolean {
    if (item.rarity !== 'Magic') return false;
    item.rarity = 'Rare';

    const canAddP = item.prefixes.length < 3;
    const canAddS = item.suffixes.length < 3;

    if (canAddP && (Math.random() < 0.5 || !canAddS)) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    } else if (canAddS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Chaos Orb: Reroll Rare item (1-3 Prefixes, 1-3 Suffixes)
  public static applyChaos(item: EquipmentItem): boolean {
    if (item.rarity !== 'Rare') return false;
    item.prefixes = [];
    item.suffixes = [];

    const pCount = 1 + Math.floor(Math.random() * 3);
    const sCount = 1 + Math.floor(Math.random() * 3);

    for (let i = 0; i < pCount; i++) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    for (let i = 0; i < sCount; i++) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Exalted Orb: Thêm 1 affix vào Rare nếu chưa đủ 6
  public static applyExalted(item: EquipmentItem): boolean {
    if (item.rarity !== 'Rare') return false;
    const canAddP = item.prefixes.length < 3;
    const canAddS = item.suffixes.length < 3;
    if (!canAddP && !canAddS) return false;

    if (canAddP && (Math.random() < 0.5 || !canAddS)) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) {
        item.prefixes.push(this.rollAffix(def));
        return true;
      }
    } else if (canAddS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) {
        item.suffixes.push(this.rollAffix(def));
        return true;
      }
    }
    return false;
  }

  // Orb of Scouring: Về Normal, xóa hết Affix
  public static applyScouring(item: EquipmentItem): boolean {
    if (item.rarity === 'Normal') return false;
    item.rarity = 'Normal';
    item.prefixes = [];
    item.suffixes = [];
    return true;
  }

  public static applyCurrency(type: CurrencyType, item: EquipmentItem): boolean {
    switch (type) {
      case 'transmutation': return this.applyTransmutation(item);
      case 'alteration': return this.applyAlteration(item);
      case 'regal': return this.applyRegal(item);
      case 'chaos': return this.applyChaos(item);
      case 'exalted': return this.applyExalted(item);
      case 'scouring': return this.applyScouring(item);
      default: return false;
    }
  }
}
