import Phaser from 'phaser';
import { SoundEffects } from '../core/audio/SoundEffects';

export interface LevelUpChoice {
  id: string;
  title: string;
  description: string;
  type: 'new_skill' | 'upgrade_skill' | 'stat_boost';
  skillId?: string;
  apply: () => void;
}

export class LevelUpUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isShowing: boolean = false;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(600);
    this.container.setVisible(false);
  }

  public show(choices: LevelUpChoice[], onChosen: () => void): void {
    this.isShowing = true;
    this.container.removeAll(true);

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    // Nền tối khóa toàn màn hình
    const bg = this.scene.add.rectangle(cx, cy, this.scene.scale.width, this.scene.scale.height, 0x030712, 0.9)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const banner = this.scene.add.text(cx, cy - 180, '★ LÊN CẤP! CHỌN MỘT NÂNG CẤP KỸ NĂNG ★', {
      fontFamily: 'monospace',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(banner);

    // Vẽ 3 thẻ phẳng trực tiếp vào container chính (Không lồng container phụ)
    choices.forEach((choice, idx) => {
      const cardX = cx - 240 + idx * 240;
      const cardY = cy;

      const cardBg = this.scene.add.rectangle(cardX, cardY, 220, 280, 0x111827, 1)
        .setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b)
        .setScrollFactor(0)
        .setInteractive({ useHandCursor: true });

      const typeLabel = this.scene.add.text(cardX, cardY - 115, choice.type === 'new_skill' ? '[KỸ NĂNG MỚI]' : '[CƯỜNG HÓA]', {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: choice.type === 'new_skill' ? '#38bdf8' : '#f59e0b',
      }).setOrigin(0.5).setScrollFactor(0);

      const title = this.scene.add.text(cardX, cardY - 75, choice.title, {
        fontFamily: 'monospace',
        fontSize: '15px',
        fontStyle: 'bold',
        color: '#ffffff',
        align: 'center',
        wordWrap: { width: 190 },
      }).setOrigin(0.5).setScrollFactor(0);

      const desc = this.scene.add.text(cardX, cardY + 10, choice.description, {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#94a3b8',
        align: 'center',
        lineSpacing: 4,
        wordWrap: { width: 190 },
      }).setOrigin(0.5).setScrollFactor(0);

      const selectBtn = this.scene.add.text(cardX, cardY + 105, 'LỰA CHỌN', {
        fontFamily: 'monospace',
        fontSize: '13px',
        fontStyle: 'bold',
        color: '#000000',
        backgroundColor: '#ffd700',
        padding: { x: 12, y: 6 },
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

      const handleSelect = () => {
        SoundEffects.playPoETink();
        choice.apply();
        this.hide();
        onChosen();
      };

      // Click vào cả thẻ hoặc nút đều nhận lệnh
      cardBg.on('pointerdown', handleSelect);
      selectBtn.on('pointerdown', handleSelect);

      cardBg.on('pointerover', () => {
        cardBg.setStrokeStyle(3, 0xffffff);
        selectBtn.setBackgroundColor('#ffffff');
      });

      cardBg.on('pointerout', () => {
        cardBg.setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b);
        selectBtn.setBackgroundColor('#ffd700');
      });

      this.container.add([cardBg, typeLabel, title, desc, selectBtn]);
    });

    this.container.setVisible(true);
  }

  public hide(): void {
    this.isShowing = false;
    this.container.setVisible(false);
  }

  public getIsShowing(): boolean {
    return this.isShowing;
  }
}
