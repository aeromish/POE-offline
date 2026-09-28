import Phaser from 'phaser';
import { MonsterStats } from '../core/monsters/MonsterTypes';
import { PoEStats } from '../core/stats/CharacterStats';

export class Monster extends Phaser.Physics.Arcade.Sprite {
  public monsterStats!: MonsterStats;
  public poeStatsWrapper!: PoEStats;
  private hpBar!: Phaser.GameObjects.Graphics;
  private lastAttackTime: number = 0;
  private attackCooldown: number = 700;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'monster_normal');
    scene.add.existing(this); // ĐƯA VÀO DANH SÁCH HIỂN THỊ
    scene.physics.add.existing(this);
    this.hpBar = scene.add.graphics();
  }

  public spawn(x: number, y: number, stats: MonsterStats): void {
    this.monsterStats = stats;
    this.poeStatsWrapper = {
      level: 1,
      currentExp: 0,
      maxExp: 100,
      maxLife: stats.maxLife,
      currentLife: stats.currentLife,
      energyShield: 0,
      maxEnergyShield: 0,
      armour: stats.armour,
      evasion: stats.evasion,
      movementSpeed: stats.movementSpeed,
      esRechargeDelay: 0,
    };

    this.enableBody(true, x, y, true, true);
    this.setVisible(true);
    this.setTexture(`monster_${stats.rarity.toLowerCase()}`);

    const size = stats.rarity === 'Boss' ? 44 : stats.rarity === 'Rare' ? 32 : 24;
    this.setDisplaySize(size, size);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(size, size);
    }

    this.hpBar.setVisible(true);
    this.updateHpBar();
  }

  public updateAI(targetX: number, targetY: number): void {
    if (!this.active) return;

    const angle = Phaser.Math.Angle.Between(this.x, this.y, targetX, targetY);
    const speed = this.monsterStats.movementSpeed;
    const body = this.body as Phaser.Physics.Arcade.Body;

    if (body) {
      this.scene.physics.velocityFromRotation(angle, speed, body.velocity);
    }

    this.updateHpBar();
  }

  public canAttack(time: number): boolean {
    if (time - this.lastAttackTime > this.attackCooldown) {
      this.lastAttackTime = time;
      return true;
    }
    return false;
  }

  public syncLifeAfterHit(): boolean {
    this.monsterStats.currentLife = this.poeStatsWrapper.currentLife;
    this.updateHpBar();
    return this.monsterStats.currentLife <= 0;
  }

  private updateHpBar(): void {
    this.hpBar.clear();
    if (!this.active) return;

    const width = this.monsterStats.rarity === 'Boss' ? 48 : 26;
    const height = 4;
    const x = this.x - width / 2;
    const y = this.y - (this.displayHeight / 2 + 8);

    this.hpBar.fillStyle(0x000000, 0.7);
    this.hpBar.fillRect(x, y, width, height);

    const pct = Math.max(0, this.monsterStats.currentLife / this.monsterStats.maxLife);
    const color = this.monsterStats.rarity === 'Boss' ? 0xff0055 : 0x00ff66;
    this.hpBar.fillStyle(color, 1);
    this.hpBar.fillRect(x, y, width * pct, height);
  }

  public kill(): void {
    this.hpBar.clear();
    this.hpBar.setVisible(false);
    this.disableBody(true, true);
    this.setVisible(false);
  }
}
