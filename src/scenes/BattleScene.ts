import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { DummyEnemy } from './DummyEnemy';
import { DamageEngine } from '../core/combat/DamageEngine';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private dummies!: Phaser.Physics.Arcade.Group;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2000;
    const mapHeight = 2000;

    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    this.createProceduralTextures();

    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    this.projectilePool = this.physics.add.group({
      classType: Projectile,
      maxSize: 100,
      runChildUpdate: false,
    });

    this.dummies = this.physics.add.group({ runChildUpdate: false });
    this.dummies.add(new DummyEnemy(this, mapWidth / 2 + 150, mapHeight / 2 - 50, false));
    this.dummies.add(new DummyEnemy(this, mapWidth / 2 + 250, mapHeight / 2 + 50, true));

    this.physics.add.overlap(
      this.projectilePool,
      this.dummies,
      (projObj, dummyObj) => {
        const proj = projObj as Projectile;
        const dummy = dummyObj as DummyEnemy;

        if (!proj.active) return;

        const hit = DamageEngine.calculateHit(proj.skillCtx, dummy.stats);
        dummy.takeDamage();

        CombatUI.showDamageText(this, dummy.x, dummy.y, hit);

        if (proj.remainingPierce > 0) {
          proj.remainingPierce--;
        } else {
          proj.kill();
        }
      }
    );

    this.add.text(20, 20, 'Nhấp chuột trái: Bắn kỹ năng\nWASD / Mũi tên: Di chuyển', {
      fontFamily: 'monospace',
      fontSize: '14px',
      color: '#ffffff',
      backgroundColor: '#00000088',
      padding: { x: 8, y: 6 },
    }).setScrollFactor(0);
  }

  private createProceduralTextures(): void {
    if (!this.textures.exists('bullet_texture')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xff8c00, 1);
      g.fillCircle(6, 6, 6);
      g.fillStyle(0xffffcc, 1);
      g.fillCircle(6, 6, 3);
      g.generateTexture('bullet_texture', 12, 12);
      g.destroy();
    }

    if (!this.textures.exists('dummy_texture')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x7c0a02, 1);
      g.fillRect(0, 0, 28, 28);
      g.lineStyle(2, 0xffffff, 0.8);
      g.strokeRect(0, 0, 28, 28);
      g.generateTexture('dummy_texture', 28, 28);
      g.destroy();
    }
  }

  update(time: number): void {
    this.player.update();

    const pointer = this.input.activePointer;
    if (pointer.isDown) {
      const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
      this.player.tryCastSkills(time, worldPoint.x, worldPoint.y, this.projectilePool);
    }
  }
}
