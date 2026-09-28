import os

# 1. Sửa DummyEnemy.ts (Bổ sung level, currentExp, maxExp)
dummy_path = "src/scenes/DummyEnemy.ts"
if os.path.exists(dummy_path):
    with open(dummy_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_dummy = """    this.stats = {
      maxLife: this.maxLife,"""
    new_dummy = """    this.stats = {
      level: 1,
      currentExp: 0,
      maxExp: 100,
      maxLife: this.maxLife,"""
    
    if old_dummy in content:
        content = content.replace(old_dummy, new_dummy)
        with open(dummy_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✓ Đã sửa src/scenes/DummyEnemy.ts")
    else:
        # Thay thế hoàn chỉnh nếu chuỗi không khớp từng ký tự
        with open(dummy_path, "w", encoding="utf-8") as f:
            f.write('''import Phaser from 'phaser';
import { PoEStats } from '../core/stats/CharacterStats';

export class DummyEnemy extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  private maxLife: number;

  constructor(scene: Phaser.Scene, x: number, y: number, isTanky: boolean = false) {
    super(scene, x, y, 'dummy_texture');

    this.maxLife = isTanky ? 1500 : 300;
    this.stats = {
      level: 1,
      currentExp: 0,
      maxExp: 100,
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
''')
        print("✓ Đã ghi đè sửa src/scenes/DummyEnemy.ts")

# 2. Sửa Monster.ts (Bổ sung level, currentExp, maxExp vào poeStatsWrapper)
monster_path = "src/scenes/Monster.ts"
if os.path.exists(monster_path):
    with open(monster_path, "r", encoding="utf-8") as f:
        m_content = f.read()

    old_mon = """    this.poeStatsWrapper = {
      maxLife: stats.maxLife,"""
    new_mon = """    this.poeStatsWrapper = {
      level: 1,
      currentExp: 0,
      maxExp: 100,
      maxLife: stats.maxLife,"""

    if old_mon in m_content:
        m_content = m_content.replace(old_mon, new_mon)
        with open(monster_path, "w", encoding="utf-8") as f:
            f.write(m_content)
        print("✓ Đã sửa src/scenes/Monster.ts")

# 3. Sửa Player.ts (Thêm dấu ! vào khai báo cursors)
player_path = "src/scenes/Player.ts"
if os.path.exists(player_path):
    with open(player_path, "r", encoding="utf-8") as f:
        p_content = f.read()

    p_content = p_content.replace(
        "private cursors: Phaser.Types.Input.Keyboard.CursorKeys;",
        "private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;"
    )
    with open(player_path, "w", encoding="utf-8") as f:
        f.write(p_content)
    print("✓ Đã sửa src/scenes/Player.ts (thêm cursors!)")

print("\nHoàn tất sửa lỗi biên dịch TypeScript!")