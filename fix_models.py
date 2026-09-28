import os

files = {
    # 1. Vẽ nhân vật tự động chuẩn 12 frames 32x32
    "src/scenes/BootScene.ts": '''import Phaser from 'phaser';

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
''',

    # 2. Sửa lỗi thân quái vật bị ẩn
    "src/scenes/Monster.ts": '''import Phaser from 'phaser';
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
''',

    # 3. Tạo hình dáng quái vật sắc nét (sừng, mắt quỷ, viền hào quang)
    "src/scenes/BattleScene.ts": None # Sẽ cập nhật phần texture quái trong BattleScene
}

# Cập nhật BootScene & Monster
for path, content in files.items():
    if content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Đã sửa: {path}")

# Cập nhật tạo texture quái sắc nét trong BattleScene
with open("src/scenes/BattleScene.ts", "r", encoding="utf-8") as f:
    bs = f.read()

old_tex_func = """    const list: { key: string; color: number }[] = [
      { key: 'monster_normal', color: 0x8b0000 },
      { key: 'monster_magic', color: 0x4169e1 },
      { key: 'monster_rare', color: 0xffd700 },
      { key: 'monster_boss', color: 0x9400d3 },
    ];

    list.forEach((item) => {
      if (!this.textures.exists(item.key)) {
        const g = this.make.graphics({ x: 0, y: 0 });
        g.fillStyle(item.color, 1);
        g.fillRect(0, 0, 32, 32);
        g.lineStyle(2, 0xffffff, 0.7);
        g.strokeRect(0, 0, 32, 32);
        g.generateTexture(item.key, 32, 32);
        g.destroy();
      }
    });"""

new_tex_func = """    const list = [
      { key: 'monster_normal', body: 0x991b1b, eye: 0xfef08a, border: 0xef4444 },
      { key: 'monster_magic',  body: 0x1e40af, eye: 0x67e8f9, border: 0x60a5fa },
      { key: 'monster_rare',   body: 0x854d0e, eye: 0xffffff, border: 0xfacc15 },
      { key: 'monster_boss',   body: 0x581c87, eye: 0xff0055, border: 0xd8b4fe },
    ];

    list.forEach((item) => {
      if (!this.textures.exists(item.key)) {
        const g = this.make.graphics({ x: 0, y: 0 });
        // Thân quái tròn có viền
        g.fillStyle(item.body, 1);
        g.fillCircle(16, 16, 13);
        g.lineStyle(2, item.border, 1);
        g.strokeCircle(16, 16, 13);
        // Cặp sừng
        g.fillStyle(item.border, 1);
        g.fillTriangle(7, 8, 12, 13, 5, 14);
        g.fillTriangle(25, 8, 20, 13, 27, 14);
        // Cặp mắt phát sáng
        g.fillStyle(item.eye, 1);
        g.fillCircle(11, 14, 2.5);
        g.fillCircle(21, 14, 2.5);
        g.generateTexture(item.key, 32, 32);
        g.destroy();
      }
    });"""

if old_tex_func in bs:
    bs = bs.replace(old_tex_func, new_tex_func)
    with open("src/scenes/BattleScene.ts", "w", encoding="utf-8") as f:
        f.write(bs)
    print("✓ Đã cập nhật texture quái vật có mắt và sừng sắc nét trong BattleScene.ts")

print("\nHoàn tất sửa lỗi Model! Hãy tải lại trang trình duyệt.")