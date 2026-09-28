export type ItemRarity = 'Normal' | 'Magic' | 'Rare';

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
