export type ItemRarity = 'Normal' | 'Magic' | 'Rare';

export type CurrencyType = 
  | 'transmutation' 
  | 'alteration' 
  | 'regal' 
  | 'chaos' 
  | 'exalted' 
  | 'scouring';

export type EquipmentSlot = 
  | 'weapon' 
  | 'offhand' 
  | 'helmet' 
  | 'bodyArmour' 
  | 'gloves' 
  | 'boots' 
  | 'amulet' 
  | 'ring1' 
  | 'ring2' 
  | 'belt';

export type ItemBaseType = 
  | 'Sword' | 'Bow' | 'Wand'
  | 'Shield' | 'Quiver'
  | 'Helmet' | 'Body Armour' | 'Gloves' | 'Boots'
  | 'Amulet' | 'Ring' | 'Belt';

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
  baseType: ItemBaseType;
  slot: EquipmentSlot;
  tier: number;
  rarity: ItemRarity;
  prefixes: AffixInstance[];
  suffixes: AffixInstance[];
}

export interface EquippedSlots {
  weapon: EquipmentItem | null;
  offhand: EquipmentItem | null;
  helmet: EquipmentItem | null;
  bodyArmour: EquipmentItem | null;
  gloves: EquipmentItem | null;
  boots: EquipmentItem | null;
  amulet: EquipmentItem | null;
  ring1: EquipmentItem | null;
  ring2: EquipmentItem | null;
  belt: EquipmentItem | null;
}

export interface InventoryData {
  currencies: Record<CurrencyType, number>;
  equipped: EquippedSlots;
  bag: EquipmentItem[];
  selectedItemForCraft: EquipmentItem | null;
}
