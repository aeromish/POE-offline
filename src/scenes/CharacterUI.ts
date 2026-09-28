import Phaser from 'phaser';
import { Player } from './Player';

export class CharacterUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private player: Player;
  private isOpen: boolean = false;
  private infoText!: Phaser.GameObjects.Text;

  constructor(scene: Phaser.Scene, player: Player) {
    this.scene = scene;
    this.player = player;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(350);
    this.createPanel();
    this.container.setVisible(false);
  }

  public toggle(): void {
    this.isOpen = !this.isOpen;
    this.container.setVisible(this.isOpen);
    if (this.isOpen) {
      this.refresh();
    }
  }

  public getIsOpen(): boolean {
    return this.isOpen;
  }

  private createPanel(): void {
    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    const bg = this.scene.add.rectangle(cx, cy, 480, 440, 0x090d16, 1.0);
    bg.setStrokeStyle(2, 0xeab308);
    bg.setInteractive();
    this.container.add(bg);

    const title = this.scene.add.text(cx, cy - 190, 'BẢNG CHỈ SỐ NHÂN VẬT [C]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#eab308',
    }).setOrigin(0.5);
    this.container.add(title);

    this.infoText = this.scene.add.text(cx - 210, cy - 150, '', {
      fontFamily: 'monospace',
      fontSize: '13px',
      lineSpacing: 7,
      color: '#f8fafc',
    });
    this.container.add(this.infoText);

    const closeBtn = this.scene.add.text(cx, cy + 185, '[ĐÓNG (C)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#94a3b8',
      backgroundColor: '#1e293b',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  public refresh(): void {
    const s = this.player.stats;
    const skill = this.player.compiledSkills[0];

    const dpsMin = skill ? Math.round(skill.baseMinDamage + skill.addedMinDamage) : 0;
    const dpsMax = skill ? Math.round(skill.baseMaxDamage + skill.addedMaxDamage) : 0;

    const str = 
      `• Lớp Nhân Vật: ${this.player.characterClass.toUpperCase()}\n` +
      `• Cấp Độ (Level): ${s.level} (EXP: ${s.currentExp}/${s.maxExp})\n` +
      `-------------------------------------------\n` +
      `❤ Máu Tối Đa (Max Life): ${Math.round(s.currentLife)} / ${s.maxLife}\n` +
      `🛡 Khiên Năng Lượng (ES): ${Math.round(s.energyShield)} / ${s.maxEnergyShield}\n` +
      `🛡 Giáp Vật Lý (Armour): ${s.armour}\n` +
      `💨 Tỷ Lệ Né Đòn (Evasion): ${s.evasion}%\n` +
      `👟 Tốc Độ Di Chuyển: ${s.movementSpeed}\n` +
      `-------------------------------------------\n` +
      `⚔ Kỹ Năng Chính: ${skill ? skill.name : 'Chưa gắn'}\n` +
      `💥 Sát Thương Cơ Bản: ${dpsMin} - ${dpsMax} (${skill ? skill.damageType.toUpperCase() : ''})\n` +
      `🔥 Tăng Sát Thương (% Inc): +${skill ? skill.increasedDamagePercent : 0}%\n` +
      `⚡ Tốc Độ Ra Chiêu: ${skill ? skill.attackSpeedMultiplier.toFixed(2) : 1}x\n` +
      `🎯 Tỷ Lệ Chí Mạng: ${skill ? skill.critChance : 5}% (x${skill ? skill.critMultiplier.toFixed(1) : 1.5})\n` +
      `🏹 Số Lượng Đạn: ${skill ? skill.projectileCount : 1} | Xuyên: ${skill ? skill.pierceCount : 0}`;

    this.infoText.setText(str);
  }
}
