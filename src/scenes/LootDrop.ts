import Phaser from 'phaser';
import { CurrencyType } from '../core/items/ItemTypes';

export class LootDrop extends Phaser.Physics.Arcade.Sprite {
  public currencyType!: CurrencyType;
  public labelText!: Phaser.GameObjects.Text;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'loot_dummy_tex');
    this.labelText = scene.add.text(x, y, '', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 3,
      padding: { x: 5, y: 2 },
    }).setOrigin(0.5);
  }

  public spawn(x: number, y: number, curType: CurrencyType, name: string): void {
    this.currencyType = curType;
    this.enableBody(true, x, y, true, true);
    this.setVisible(false); // Dùng chính labelText làm hình ảnh hiển thị trên sàn

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(30, 20);
    }

    let color = '#aa9e82'; // Transmute / Alteration
    let bgColor = '#111111ee';

    if (curType === 'chaos') {
      color = '#ffd700';
      bgColor = '#332200ee';
    } else if (curType === 'exalted') {
      color = '#ffffff';
      bgColor = '#b8860bee'; // Nền ánh vàng Exalted PoE
    } else if (curType === 'regal') {
      color = '#4169e1';
    } else if (curType === 'scouring') {
      color = '#ffffff';
    }

    this.labelText.setText(name);
    this.labelText.setColor(color);
    this.labelText.setBackgroundColor(bgColor);
    this.labelText.setPosition(x, y);
    this.labelText.setVisible(true);

    // Hiệu ứng nảy nhẹ khi rớt xuống sàn
    this.scene.tweens.add({
      targets: [this, this.labelText],
      y: y - 16,
      yoyo: true,
      duration: 180,
      ease: 'Quad.easeOut',
    });
  }

  public collect(): CurrencyType {
    const c = this.currencyType;
    this.labelText.setVisible(false);
    this.disableBody(true, true);
    return c;
  }
}
