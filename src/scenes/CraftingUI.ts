import Phaser from 'phaser';
import { InventoryData, CurrencyType } from '../core/items/ItemTypes';
import { CraftingEngine } from '../core/crafting/CraftingEngine';
import { Player } from './Player';

export class CraftingUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isOpen: boolean = false;
  private inventoryData: InventoryData;
  private player: Player;
  private onItemUpdated: () => void;

  private itemTitleText!: Phaser.GameObjects.Text;
  private socketsText!: Phaser.GameObjects.Text;
  private affixesText!: Phaser.GameObjects.Text;
  private currencyButtons: Map<CurrencyType, Phaser.GameObjects.Text> = new Map();

  constructor(scene: Phaser.Scene, inv: InventoryData, player: Player, onItemUpdated: () => void) {
    this.scene = scene;
    this.inventoryData = inv;
    this.player = player;
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

    const bg = this.scene.add.rectangle(cx, cy, 620, 500, 0x090d16, 0.96);
    bg.setStrokeStyle(2, 0x30363d);
    bg.setInteractive(); // Chặn click xuyên xuống sàn đấu
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 225, 'HÒM ĐỒ & CHẾ TẠO TRANG BỊ [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(header);

    this.itemTitleText = this.scene.add.text(cx, cy - 185, '', {
      fontFamily: 'monospace',
      fontSize: '16px',
      fontStyle: 'bold',
    }).setOrigin(0.5);
    this.container.add(this.itemTitleText);

    // Khu vực hiển thị Sockets & Gems
    this.socketsText = this.scene.add.text(cx - 280, cy - 155, '', {
      fontFamily: 'monospace',
      fontSize: '12px',
      lineSpacing: 4,
    });
    this.container.add(this.socketsText);

    // Khu vực hiển thị Affixes
    this.affixesText = this.scene.add.text(cx - 280, cy - 70, '', {
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#8888ff',
      lineSpacing: 4,
    });
    this.container.add(this.affixesText);

    const curList: { type: CurrencyType; name: string }[] = [
      { type: 'transmutation', name: 'Transmute' },
      { type: 'alteration', name: 'Alteration' },
      { type: 'regal', name: 'Regal' },
      { type: 'chaos', name: 'Chaos' },
      { type: 'exalted', name: 'Exalted' },
      { type: 'scouring', name: 'Scouring' },
    ];

    const startY = cy + 120;
    curList.forEach((c, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const bx = cx - 180 + col * 180;
      const by = startY + row * 52;

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

    const closeBtn = this.scene.add.text(cx, cy + 225, '[ĐÓNG GIAO DIỆN (I)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8b949e',
      backgroundColor: '#161b22',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
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
    const rarityColor = item.rarity === 'Rare' ? '#ffd700' : item.rarity === 'Magic' ? '#4169e1' : '#ffffff';
    this.itemTitleText.setText(`[${item.rarity.toUpperCase()}] ${item.baseType}`);
    this.itemTitleText.setColor(rarityColor);

    // Hiển thị Lỗ Ngọc & Dây nối (Sockets & Links)
    let sockStr = '❖ LỖ NGỌC & LIÊN KẾT (SOCKETS & LINKS):\n';
    this.player.sockets.forEach((s, idx) => {
      const colorHex = s.color === 'red' ? '#ff5555' : s.color === 'green' ? '#55ff55' : '#5599ff';
      const gemName = s.gem ? s.gem.name : '(Trống)';
      sockStr += `  • Socket ${idx + 1} [Nhóm ${s.linkGroup} - ${s.color.toUpperCase()}]: ${gemName}\n`;
    });
    this.socketsText.setText(sockStr);

    let affStr = '--- PREFIXES ---\n';
    if (item.prefixes.length === 0) affStr += '(Trống)\n';
    item.prefixes.forEach((p) => {
      affStr += `• ${p.name}: +${p.value} (${p.statType})\n`;
    });

    affStr += '\n--- SUFFIXES ---\n';
    if (item.suffixes.length === 0) affStr += '(Trống)\n';
    item.suffixes.forEach((s) => {
      affStr += `• ${s.name}: +${p_to_s(s.statType, s.value)})\n`;
    });
    this.affixesText.setText(affStr);

    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      btn.setText(`${type.toUpperCase()}\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}

function p_to_s(stat: string, val: number): string {
  return `${val} ${stat}`;
}
