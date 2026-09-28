import { PASSIVE_TREE_NODES } from './PassiveTreeData';
import { PassiveTreeBonus } from './PassiveTreeTypes';

export class PassiveTreeManager {
  public unspentPoints: number = 2;
  public allocatedNodeIds: Set<string> = new Set(['root']);

  public canAllocate(nodeId: string): boolean {
    if (this.unspentPoints <= 0) return false;
    if (this.allocatedNodeIds.has(nodeId)) return false;

    const node = PASSIVE_TREE_NODES[nodeId];
    if (!node) return false;

    return node.connections.some((connectedId) => this.allocatedNodeIds.has(connectedId));
  }

  public allocate(nodeId: string): boolean {
    if (!this.canAllocate(nodeId)) return false;

    this.allocatedNodeIds.add(nodeId);
    this.unspentPoints--;
    return true;
  }

  public calculateTotalBonus(): PassiveTreeBonus {
    const bonus: PassiveTreeBonus = {
      flatLife: 0,
      flatES: 0,
      flatArmour: 0,
      flatEvasion: 0,
      incPhysDamage: 0,
      incFireDamage: 0,
      attackSpeedPct: 0,
      movementSpeed: 0,
      critChance: 0,
      critMultiplier: 0,
      extraProjectile: 0,
      extraPierce: 0,
      pickupRadius: 0,
      expBonusPct: 0,
    };

    for (const id of this.allocatedNodeIds) {
      const node = PASSIVE_TREE_NODES[id];
      if (!node) continue;

      for (const mod of node.modifiers) {
        switch (mod.type) {
          case 'flat_life': bonus.flatLife += mod.value; break;
          case 'flat_es': bonus.flatES += mod.value; break;
          case 'flat_armour': bonus.flatArmour += mod.value; break;
          case 'flat_evasion': bonus.flatEvasion += mod.value; break;
          case 'inc_phys_damage': bonus.incPhysDamage += mod.value; break;
          case 'inc_fire_damage': bonus.incFireDamage += mod.value; break;
          case 'attack_speed_pct': bonus.attackSpeedPct += mod.value; break;
          case 'movement_speed': bonus.movementSpeed += mod.value; break;
          case 'crit_chance': bonus.critChance += mod.value; break;
          case 'crit_multiplier': bonus.critMultiplier += mod.value; break;
          case 'extra_projectile': bonus.extraProjectile += mod.value; break;
          case 'extra_pierce': bonus.extraPierce += mod.value; break;
          case 'pickup_radius': bonus.pickupRadius += mod.value; break;
          case 'exp_bonus_pct': bonus.expBonusPct += mod.value; break;
        }
      }
    }

    return bonus;
  }
}
