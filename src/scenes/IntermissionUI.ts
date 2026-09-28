import Phaser from 'phaser';

export class IntermissionUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isShowing: boolean = false;
  private onStartNextWave: () => void;
  private onOpenCrafting: () => void;
  private onOpenPassives: () => void;

  private waveTitleText!: Phaser.GameObjects.Text;

  constructor(
    scene: Phaser.Scene,
    onStartNextWave: () => void,
    onOpenCrafting: () => void,
    onOpenPassives: () => void
  ) {
    this.scene = scene;
    this.onStartNextWave = onStartNextWave;
    this.onOpenCrafting = onOpenCrafting;
    this.onOpenPassives = onOpenPassives;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(200);
    this.createPanel();
    this.container.setVisible(false);
  }

  public show(clearedWave: number): void {
    this.isShowing = true;
    this.waveTitleText.setText(`ĐÃ VƯỢT QUA ĐỢT ${clearedWave}!\nKHU VỰC AN TOÀN (SAFE ZONE)`);
    this.container.setVisible(true);
  }

  public hide(): void {
    this.isShowing = false;
    this.container.setVisible(false);
  }

  public getIsShowing(): boolean {
    return this.isShowing;
  }

  private createPanel(): void {
    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    const bg = this.scene.add.rectangle(cx, cy, 600, 320, 0x090d16, 0.95);
    bg.setStrokeStyle(2, 0x238636);
    this.container.add(bg);

    this.waveTitleText = this.scene.add.text(cx, cy - 90, '', {
      fontFamily: 'monospace',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffd700',
      align: 'center',
    }).setOrigin(0.5);
    this.container.add(this.waveTitleText);

    const rewardText = this.scene.add.text(cx, cy - 30, '+1 Điểm Kỹ Năng Nội Tại (Passive Skill Point)\nSẵn sàng nâng cấp trang bị và nhánh sức mạnh', {
      fontFamily: 'monospace',
      fontSize: '14px',
      color: '#58a6ff',
      align: 'center',
    }).setOrigin(0.5);
    this.container.add(rewardText);

    // Nút mở Hòm đồ
    const btnCraft = this.scene.add.text(cx - 150, cy + 35, '[I] HÒM ĐỒ & CRAFT', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#ffffff',
      backgroundColor: '#21262d',
      padding: { x: 12, y: 8 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });
    btnCraft.on('pointerdown', () => this.onOpenCrafting());
    this.container.add(btnCraft);

    // Nút mở Cây nội tại
    const btnPassives = this.scene.add.text(cx + 150, cy + 35, '[P] CÂY NỘI TẠI', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#ffffff',
      backgroundColor: '#21262d',
      padding: { x: 12, y: 8 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });
    btnPassives.on('pointerdown', () => this.onOpenPassives());
    this.container.add(btnPassives);

    // Nút bắt đầu đợt kế tiếp
    const btnNext = this.scene.add.text(cx, cy + 105, 'BẮT ĐẦU ĐỢT KẾ TIẾP [SPACE]', {
      fontFamily: 'monospace',
      fontSize: '16px',
      fontStyle: 'bold',
      color: '#ffffff',
      backgroundColor: '#238636',
      padding: { x: 24, y: 12 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    btnNext.on('pointerdown', () => this.onStartNextWave());
    btnNext.on('pointerover', () => btnNext.setBackgroundColor('#2ea043'));
    btnNext.on('pointerout', () => btnNext.setBackgroundColor('#238636'));
    this.container.add(btnNext);
  }
}
