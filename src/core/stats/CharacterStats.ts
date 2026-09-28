export interface PoEStats {
  level: number;
  currentExp: number;
  maxExp: number;
  maxLife: number;
  currentLife: number;
  energyShield: number;
  maxEnergyShield: number;
  armour: number;
  evasion: number;
  movementSpeed: number;
  esRechargeDelay: number;
}

export type CharacterClass = 'Knight' | 'Archer' | 'Mage';

export const CLASS_BASE_STATS: Record<CharacterClass, PoEStats> = {
  Knight: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 160,
    currentLife: 160,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 60,
    evasion: 5,
    movementSpeed: 165,
    esRechargeDelay: 4,
  },
  Archer: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 100,
    currentLife: 100,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 15,
    evasion: 70,
    movementSpeed: 215,
    esRechargeDelay: 4,
  },
  Mage: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 80,
    currentLife: 80,
    energyShield: 85,
    maxEnergyShield: 85,
    armour: 0,
    evasion: 10,
    movementSpeed: 180,
    esRechargeDelay: 3,
  },
};

export function getExpNeeded(level: number): number {
  return Math.floor(100 * Math.pow(1.3, level - 1));
}
