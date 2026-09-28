import Phaser from 'phaser';

export class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  preload(): void {
    const classes = ['knight', 'archer', 'mage'];
    classes.forEach((cls) => {
      this.load.spritesheet(`player_${cls}`, `assets/characters/${cls}.png`, {
        frameWidth: 32,
        frameHeight: 32,
      });
    });
  }

  create(): void {
    const classes = ['knight', 'archer', 'mage'];

    classes.forEach((cls) => {
      // Fallback: nếu chưa tải ảnh về, tự vẽ ô màu để test
      if (!this.textures.exists(`player_${cls}`)) {
        const graphics = this.make.graphics({ x: 0, y: 0 });
        const color = cls === 'knight' ? 0xb22222 : cls === 'archer' ? 0x228b22 : 0x1e90ff;
        graphics.fillStyle(color, 1);
        graphics.fillRect(0, 0, 32 * 12, 32);
        graphics.generateTexture(`player_${cls}`, 32 * 12, 32);
        graphics.destroy();
      }

      this.anims.create({
        key: `player_${cls}_walk_down`,
        frames: this.anims.generateFrameNumbers(`player_${cls}`, { start: 0, end: 3 }),
        frameRate: 8,
        repeat: -1,
      });

      this.anims.create({
        key: `player_${cls}_walk_right`,
        frames: this.anims.generateFrameNumbers(`player_${cls}`, { start: 4, end: 7 }),
        frameRate: 8,
        repeat: -1,
      });

      this.anims.create({
        key: `player_${cls}_walk_up`,
        frames: this.anims.generateFrameNumbers(`player_${cls}`, { start: 8, end: 11 }),
        frameRate: 8,
        repeat: -1,
      });
    });

    this.scene.start('BattleScene');
  }
}