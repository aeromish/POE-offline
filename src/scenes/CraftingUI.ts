import Phaser from 'phaser';
import { InventoryData, CurrencyType } from '../core/items/ItemTypes';
import { CraftingEngine } from '../core/crafting/CraftingEngine';

export class CraftingUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isOpen: boolean = false;
  private inventoryData: InventoryData;
  private onItemUpdated: () => void;

  private itemTitleText!: Phaser.GameObjects.Text;
  private affixesText!: Phaser.GameObjects.Text;
  private currencyButtons: Map<CurrencyType, Phaser.GameObjects.Text> = new Map();

  constructor(scene: Phaser.Scene, inv: InventoryData, onItemUpdated: () => void) {
    this.scene = scene;
    this.inventoryData = inv;
    this.onItemUpdated = onItemUpdated;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(100);
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

    // Nền modal
    const bg = this.scene.add.rectangle(cx, cy, 540, 420, 0x0d1117, 0.95);
    bg.setStrokeStyle(2, 0x30363d);
    this.container.add(bg);

    // Tiêu đề modal
    const header = this.scene.add.text(cx, cy - 180, 'HÒM ĐỒ & CHẾ TẠO TRANG BỊ [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(header);

    // Thông tin Item
    this.itemTitleText = this.scene.add.text(cx, cy - 135, '', {
      fontFamily: 'monospace',
      fontSize: '16px',
      fontStyle: 'bold',
    }).setOrigin(0.5);
    this.container.add(this.itemTitleText);

    this.affixesText = this.scene.add.text(cx - 240, cy - 105, '', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8888ff',
      lineSpacing: 5,
    });
    this.container.add(this.affixesText);

    // Nút Crafting Currency
    const curList: { type: CurrencyType; name: string }[] = [
      { type: 'transmutation', name: 'Transmute' },
      { type: 'alteration', name: 'Alteration' },
      { type: 'regal', name: 'Regal' },
      { type: 'chaos', name: 'Chaos' },
      { type: 'exalted', name: 'Exalted' },
      { type: 'scouring', name: 'Scouring' },
    ];

    const startY = cy + 50;
    curList.forEach((c, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const bx = cx - 170 + col * 170;
      const by = startY + row * 55;

      const btn = this.scene.add.text(bx, by, '', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#ffffff',
        backgroundColor: '#21262d',
        padding: { x: 10, y: 8 },
        stroke: '#000000',
        strokeThickness: 2,
      }).setOrigin(0.5).setInteractive({ useHandCursor: true });

      btn.on('pointerdown', () => this.useCurrency(c.type));
      btn.on('pointerover', () => btn.setBackgroundColor('#388bfd'));
      btn.on('pointerout', () => btn.setBackgroundColor('#21262d'));

      this.currencyButtons.set(c.type, btn);
      this.container.add(btn);
    });

    const closeTip = this.scene.add.text(cx, cy + 185, 'Nhấn [I] để đóng bảng & tiếp tục chiến đấu', {
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#8b949e',
    }).setOrigin(0.5);
    this.container.add(closeTip);
  }

  private useCurrency(cur: CurrencyType): void {
    const qty = this.inventoryData.currencies[cur] || 0;
    if (qty <= 0) return;

    const success = CraftingEngine.applyCurrency(cur, this.inventoryData.equippedItem);
    if (success) {
      this.inventoryData.currencies[cur]--;
      this.onItemUpdated();
      this.refresh();
    }
  }

  public refresh(): void {
    const item = this.inventoryData.equippedItem;

    // Màu sắc độ hiếm
    const rarityColor = item.rarity === 'Rare' ? '#ffd700' : item.rarity === 'Magic' ? '#4169e1' : '#ffffff';
    this.itemTitleText.setText(`[${item.rarity.toUpperCase()}] ${item.baseType}`);
    this.itemTitleText.setColor(rarityColor);

    // Liệt kê Affixes
    let affStr = '--- PREFIXES ---\n';
    if (item.prefixes.length === 0) affStr += '(Trống)\n';
    item.prefixes.forEach((p) => {
      affStr += `• ${p.name}: +${p.value} (${p.statType})\n`;
    });

    affStr += '\n--- SUFFIXES ---\n';
    if (item.suffixes.length === 0) affStr += '(Trống)\n';
    item.suffixes.forEach((s) => {
      affStr += `• ${s.name}: +${s.value} (${s.statType})\n`;
    });

    this.affixesText.setText(affStr);

    // Cập nhật số lượng trên các nút bấm
    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      const label = `${type.toUpperCase()}\n(Còn: ${count})`;
      btn.setText(label);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
