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
      // Nếu không có file ảnh ngoài, tự sinh bộ sprite pixel-art 12 frames hoàn chỉnh
      if (!this.textures.exists(`player_${cls}`)) {
        this.generateProceduralPlayerSpritesheet(cls);
      }

      // Tạo Animations 4 hướng
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

  private generateProceduralPlayerSpritesheet(cls: string): void {
    const g = this.make.graphics({ x: 0, y: 0 });
    const mainColor = cls === 'knight' ? 0x991b1b : cls === 'archer' ? 0x166534 : 0x2563eb;
    const accentColor = cls === 'knight' ? 0xe2e8f0 : cls === 'archer' ? 0x86efac : 0x67e8f9;

    // Vẽ 12 frame, mỗi frame đúng 32x32
    for (let f = 0; f < 12; f++) {
      const offsetX = f * 32;
      const legOffset = (f % 2 === 0) ? 1 : -1;

      // 1. Áo choàng / Thân
      g.fillStyle(mainColor, 1);
      g.fillRect(offsetX + 9, 12, 14, 13);

      // 2. Chân / Bước chạy
      g.fillStyle(0x1e293b, 1);
      g.fillRect(offsetX + 10, 25, 4, 5 + (f % 4 === 1 ? legOffset * 2 : 0));
      g.fillRect(offsetX + 18, 25, 4, 5 + (f % 4 === 3 ? -legOffset * 2 : 0));

      // 3. Đầu / Mũ trùm
      g.fillStyle(0xfde047, 1); // Màu da mặt
      g.fillRect(offsetX + 11, 6, 10, 8);
      g.fillStyle(mainColor, 1); // Mũ
      g.fillRect(offsetX + 9, 3, 14, 5);

      // 4. Mắt phát sáng (nếu quay xuống hoặc ngang)
      if (f < 8) {
        g.fillStyle(0x00ffff, 1);
        g.fillRect(offsetX + 13, 8, 2, 2);
        g.fillRect(offsetX + 17, 8, 2, 2);
      }

      // 5. Vũ khí / Cầu phép trên tay
      g.fillStyle(accentColor, 1);
      g.fillCircle(offsetX + 25, 16 + (f % 2), 4);
      g.fillStyle(0xffffff, 1);
      g.fillCircle(offsetX + 25, 16 + (f % 2), 2);
    }

    g.generateTexture(`player_${cls}`, 384, 32);
    g.destroy();

    // Cắt kết cấu 384x32 thành đúng 12 ô 32x32
    const tex = this.textures.get(`player_${cls}`);
    for (let i = 0; i < 12; i++) {
      tex.add(i, 0, i * 32, 0, 32, 32);
    }
  }
}
