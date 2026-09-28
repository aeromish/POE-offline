import Phaser from 'phaser';
import { DropResult } from '../core/loot/LootEngine';

export class LootDrop extends Phaser.Physics.Arcade.Sprite {
  public dropData!: DropResult;
  public labelText!: Phaser.GameObjects.Text;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'loot_dummy_tex');
    this.labelText = scene.add.text(x, y, '', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      stroke: '#000000',
      strokeThickness: 3,
      padding: { x: 6, y: 3 },
    }).setOrigin(0.5);
  }

  public spawn(x: number, y: number, data: DropResult): void {
    this.dropData = data;
    this.enableBody(true, x, y, true, true);
    this.setVisible(false);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(35, 20);
    }

    let color = '#ffffff';
    let bgColor = '#111111ee';

    if (data.category === 'currency') {
      color = data.currencyType === 'chaos' ? '#ffd700' : data.currencyType === 'exalted' ? '#ffffff' : '#aa9e82';
      bgColor = data.currencyType === 'exalted' ? '#78350fee' : '#111827ee';
    } else if (data.category === 'equipment') {
      const r = data.equipmentItem?.rarity;
      color = r === 'Rare' ? '#ffd700' : r === 'Magic' ? '#60a5fa' : '#ffffff';
      bgColor = '#1f2937ee';
    } else if (data.category === 'gem') {
      color = '#2dd4bf'; // Ngọc màu xanh ngọc biển
      bgColor = '#0f766eee';
    }

    this.labelText.setText(data.name);
    this.labelText.setColor(color);
    this.labelText.setBackgroundColor(bgColor);
    this.labelText.setPosition(x, y);
    this.labelText.setVisible(true);

    this.scene.tweens.add({
      targets: [this, this.labelText],
      y: y - 18,
      yoyo: true,
      duration: 180,
      ease: 'Quad.easeOut',
    });
  }

  public collect(): DropResult {
    const d = this.dropData;
    this.labelText.setVisible(false);
    this.disableBody(true, true);
    return d;
  }
}
