import Phaser from 'phaser';
import { PoEStats } from '../core/stats/CharacterStats';

export class DummyEnemy extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  private maxLife: number;

  constructor(scene: Phaser.Scene, x: number, y: number, isTanky: boolean = false) {
    super(scene, x, y, 'dummy_texture');

    this.maxLife = isTanky ? 1500 : 300;
    this.stats = {
      maxLife: this.maxLife,
      currentLife: this.maxLife,
      energyShield: isTanky ? 0 : 100,
      maxEnergyShield: isTanky ? 0 : 100,
      armour: isTanky ? 80 : 10,
      evasion: isTanky ? 0 : 15,
      movementSpeed: 0,
      esRechargeDelay: 3,
    };

    scene.add.existing(this);
    scene.physics.add.existing(this, true);
  }

  takeDamage(): void {
    if (this.stats.currentLife <= 0) {
      this.stats.currentLife = this.maxLife;
      this.stats.energyShield = this.stats.maxEnergyShield;
    }
  }
}
