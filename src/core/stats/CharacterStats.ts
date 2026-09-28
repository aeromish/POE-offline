export interface PoEStats {
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
    maxLife: 150,
    currentLife: 150,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 50,
    evasion: 5,
    movementSpeed: 160,
    esRechargeDelay: 4,
  },
  Archer: {
    maxLife: 90,
    currentLife: 90,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 10,
    evasion: 65,
    movementSpeed: 210,
    esRechargeDelay: 4,
  },
  Mage: {
    maxLife: 70,
    currentLife: 70,
    energyShield: 80,
    maxEnergyShield: 80,
    armour: 0,
    evasion: 10,
    movementSpeed: 175,
    esRechargeDelay: 3,
  },
};