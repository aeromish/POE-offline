import Phaser from 'phaser';
import { InventoryData, CurrencyType, EquipmentItem } from '../core/items/ItemTypes';
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
  private bagContainer!: Phaser.GameObjects.Container;
  private currencyButtons: Map<CurrencyType, Phaser.GameObjects.Text> = new Map();

  constructor(scene: Phaser.Scene, inv: InventoryData, player: Player, onItemUpdated: () => void) {
    this.scene = scene;
    this.inventoryData = inv;
    this.player = player;
    this.onItemUpdated = onItemUpdated;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(300);
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

    const bg = this.scene.add.rectangle(cx, cy, 740, 520, 0x090d16, 1.0);
    bg.setStrokeStyle(2, 0x30363d);
    bg.setInteractive();
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 235, 'HÀNH TRANG & CHẾ TẠO TRANG BỊ [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(header);

    // CỘT TRÁI: TRANG BỊ ĐANG MẶC
    this.itemTitleText = this.scene.add.text(cx - 180, cy - 195, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
    }).setOrigin(0.5);
    this.container.add(this.itemTitleText);

    this.socketsText = this.scene.add.text(cx - 340, cy - 170, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      lineSpacing: 3,
    });
    this.container.add(this.socketsText);

    this.affixesText = this.scene.add.text(cx - 340, cy - 80, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#8888ff',
      lineSpacing: 3,
    });
    this.container.add(this.affixesText);

    // CỘT PHẢI: TÚI ĐỒ (BAG)
    const bagTitle = this.scene.add.text(cx + 170, cy - 195, '❖ TÚI ĐỒ (BẤM ĐỂ MẶC):', {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#38bdf8',
    }).setOrigin(0.5);
    this.container.add(bagTitle);

    this.bagContainer = this.scene.add.container(cx + 40, cy - 165);
    this.container.add(this.bagContainer);

    // HÀNG DƯỚI: NÚT CRAFTING CURRENCY
    const curList: { type: CurrencyType; name: string }[] = [
      { type: 'transmutation', name: 'Transmute' },
      { type: 'alteration', name: 'Alteration' },
      { type: 'regal', name: 'Regal' },
      { type: 'chaos', name: 'Chaos' },
      { type: 'exalted', name: 'Exalted' },
      { type: 'scouring', name: 'Scouring' },
    ];

    const startY = cy + 130;
    curList.forEach((c, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const bx = cx - 180 + col * 180;
      const by = startY + row * 48;

      const btn = this.scene.add.text(bx, by, '', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#ffffff',
        backgroundColor: '#21262d',
        padding: { x: 10, y: 7 },
        stroke: '#000000',
        strokeThickness: 2,
      }).setOrigin(0.5).setInteractive({ useHandCursor: true });

      btn.on('pointerdown', () => this.useCurrency(c.type));
      btn.on('pointerover', () => btn.setBackgroundColor('#388bfd'));
      btn.on('pointerout', () => btn.setBackgroundColor('#21262d'));

      this.currencyButtons.set(c.type, btn);
      this.container.add(btn);
    });

    const closeBtn = this.scene.add.text(cx, cy + 230, '[ĐÓNG GIAO DIỆN (I)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8b949e',
      backgroundColor: '#161b22',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  // MẶC ĐỒ TỪ TÚI
  private equipFromBag(index: number): void {
    if (index >= this.inventoryData.bag.length) return;
    const itemToEquip = this.inventoryData.bag[index];
    const oldItem = this.inventoryData.equippedItem;

    this.inventoryData.equippedItem = itemToEquip;
    this.inventoryData.bag[index] = oldItem; // Tráo món cũ vào lại túi

    this.onItemUpdated();
    this.refresh();
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
    this.itemTitleText.setText(`[ĐANG MẶC: ${item.rarity.toUpperCase()}] ${item.baseType}`);
    this.itemTitleText.setColor(rarityColor);

    let sockStr = '❖ LỖ NGỌC & LIÊN KẾT:\n';
    this.player.sockets.forEach((s, idx) => {
      const gemName = s.gem ? s.gem.name : '(Trống)';
      sockStr += `  • Ô ${idx + 1} [Nhóm ${s.linkGroup} - ${s.color.toUpperCase()}]: ${gemName}\n`;
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
      affStr += `• ${s.name}: +${s.value} (${s.statType})\n`;
    });
    this.affixesText.setText(affStr);

    // VẼ CÁC MÓN TRONG TÚI ĐỒ (BAG)
    this.bagContainer.removeAll(true);
    if (this.inventoryData.bag.length === 0) {
      const emptyText = this.scene.add.text(0, 30, '(Túi trống - Đánh quái để nhặt đồ)', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#64748b',
      });
      this.bagContainer.add(emptyText);
    } else {
      this.inventoryData.bag.forEach((bagItem, idx) => {
        const itemY = idx * 42;
        const rColor = bagItem.rarity === 'Rare' ? '#ffd700' : bagItem.rarity === 'Magic' ? '#60a5fa' : '#ffffff';

        const nameTxt = this.scene.add.text(0, itemY, `[${bagItem.rarity}] ${bagItem.baseType}`, {
          fontFamily: 'monospace',
          fontSize: '12px',
          fontStyle: 'bold',
          color: rColor,
        });

        const equipBtn = this.scene.add.text(180, itemY - 2, 'MẶC ĐỒ', {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: '#000000',
          backgroundColor: '#38bdf8',
          padding: { x: 6, y: 3 },
        }).setInteractive({ useHandCursor: true });

        equipBtn.on('pointerdown', () => this.equipFromBag(idx));

        this.bagContainer.add([nameTxt, equipBtn]);
      });
    }

    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      btn.setText(`${type.toUpperCase()}\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
