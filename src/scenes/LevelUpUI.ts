import Phaser from 'phaser';

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
  private cards: Phaser.GameObjects.Container[] = [];

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(500);
    this.container.setVisible(false);
  }

  public show(choices: LevelUpChoice[], onChosen: () => void): void {
    this.isShowing = true;
    this.container.removeAll(true);
    this.cards = [];

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    // Nền mờ toàn màn hình
    const bg = this.scene.add.rectangle(cx, cy, this.scene.scale.width, this.scene.scale.height, 0x030712, 0.85);
    bg.setInteractive();
    this.container.add(bg);

    const banner = this.scene.add.text(cx, cy - 180, '★ LÊN CẤP! CHỌN MỘT NÂNG CẤP KỸ NĂNG ★', {
      fontFamily: 'monospace',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(banner);

    // Vẽ 3 thẻ bài
    choices.forEach((choice, idx) => {
      const cardX = cx - 240 + idx * 240;
      const cardY = cy;

      const cardContainer = this.scene.add.container(cardX, cardY);
      const cardBg = this.scene.add.rectangle(0, 0, 220, 280, 0x111827, 1);
      cardBg.setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b);
      cardBg.setInteractive({ useHandCursor: true });

      const typeLabel = this.scene.add.text(0, -115, choice.type === 'new_skill' ? '[KỸ NĂNG MỚI]' : '[CƯỜNG HÓA]', {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: choice.type === 'new_skill' ? '#38bdf8' : '#f59e0b',
      }).setOrigin(0.5);

      const title = this.scene.add.text(0, -75, choice.title, {
        fontFamily: 'monospace',
        fontSize: '15px',
        fontStyle: 'bold',
        color: '#ffffff',
        align: 'center',
        wordWrap: { width: 190 },
      }).setOrigin(0.5);

      const desc = this.scene.add.text(0, 10, choice.description, {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#94a3b8',
        align: 'center',
        lineSpacing: 4,
        wordWrap: { width: 190 },
      }).setOrigin(0.5);

      const selectBtn = this.scene.add.text(0, 105, 'LỰA CHỌN', {
        fontFamily: 'monospace',
        fontSize: '13px',
        fontStyle: 'bold',
        color: '#000000',
        backgroundColor: '#ffd700',
        padding: { x: 12, y: 6 },
      }).setOrigin(0.5);

      cardBg.on('pointerdown', () => {
        choice.apply();
        this.hide();
        onChosen();
      });

      cardBg.on('pointerover', () => {
        cardBg.setStrokeStyle(3, 0xffffff);
        cardContainer.setScale(1.04);
      });

      cardBg.on('pointerout', () => {
        cardBg.setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b);
        cardContainer.setScale(1.0);
      });

      cardContainer.add([cardBg, typeLabel, title, desc, selectBtn]);
      this.container.add(cardContainer);
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
