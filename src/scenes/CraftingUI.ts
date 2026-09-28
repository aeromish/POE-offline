import Phaser from 'phaser';
import { InventoryData, CurrencyType } from '../core/items/ItemTypes';
import { CraftingEngine } from '../core/crafting/CraftingEngine';
import { Player } from './Player';
import { SoundEffects } from '../core/audio/SoundEffects';

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
  private tierBonusText!: Phaser.GameObjects.Text;
  private bagElements: Phaser.GameObjects.GameObject[] = [];
  private currencyButtons: Map<CurrencyType, Phaser.GameObjects.Text> = new Map();

  constructor(scene: Phaser.Scene, inv: InventoryData, player: Player, onItemUpdated: () => void) {
    this.scene = scene;
    this.inventoryData = inv;
    this.player = player;
    this.onItemUpdated = onItemUpdated;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(450);
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

    const bg = this.scene.add.rectangle(cx, cy, 780, 530, 0x090d16, 1.0)
      .setStrokeStyle(2, 0x30363d)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 240, 'HÀNH TRANG & RÈN TRANG BỊ (TIER FORGE) [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(header);

    // CỘT TRÁI: ĐANG MẶC
    this.itemTitleText = this.scene.add.text(cx - 200, cy - 200, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.itemTitleText);

    this.tierBonusText = this.scene.add.text(cx - 370, cy - 180, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#fbbf24',
    }).setScrollFactor(0);
    this.container.add(this.tierBonusText);

    this.socketsText = this.scene.add.text(cx - 370, cy - 155, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      lineSpacing: 3,
    }).setScrollFactor(0);
    this.container.add(this.socketsText);

    this.affixesText = this.scene.add.text(cx - 370, cy - 70, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#8888ff',
      lineSpacing: 3,
    });
    this.container.add(this.affixesText);

    // CỘT PHẢI: TÚI ĐỒ & GHÉP ĐỒ
    const bagTitle = this.scene.add.text(cx + 170, cy - 200, '❖ TÚI ĐỒ (BẤM MẶC HOẶC GHÉP TIER):', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(bagTitle);

    // NÚT GHÉP ĐỒ TĂNG TIER
    const forgeBtn = this.scene.add.text(cx + 170, cy - 165, '🔨 HIẾN TẾ 2 MÓN TRONG TÚI ĐỂ NÂNG +1 TIER', {
      fontFamily: 'monospace',
      fontSize: '11px',
      fontStyle: 'bold',
      color: '#000000',
      backgroundColor: '#f59e0b',
      padding: { x: 8, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    forgeBtn.on('pointerdown', () => this.forgeUpgradeTier());
    forgeBtn.on('pointerover', () => forgeBtn.setBackgroundColor('#ffffff'));
    forgeBtn.on('pointerout', () => forgeBtn.setBackgroundColor('#f59e0b'));
    this.container.add(forgeBtn);

    // HÀNG DƯỚI: CRAFTING CURRENCY
    const curList: { type: CurrencyType; name: string }[] = [
      { type: 'transmutation', name: 'Transmute' },
      { type: 'alteration', name: 'Alteration' },
      { type: 'regal', name: 'Regal' },
      { type: 'chaos', name: 'Chaos' },
      { type: 'exalted', name: 'Exalted' },
      { type: 'scouring', name: 'Scouring' },
    ];

    const startY = cy + 135;
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
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

      btn.on('pointerdown', () => this.useCurrency(c.type));
      btn.on('pointerover', () => btn.setBackgroundColor('#388bfd'));
      btn.on('pointerout', () => btn.setBackgroundColor('#21262d'));

      this.currencyButtons.set(c.type, btn);
      this.container.add(btn);
    });

    const closeBtn = this.scene.add.text(cx, cy + 235, '[ĐÓNG GIAO DIỆN (I)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8b949e',
      backgroundColor: '#161b22',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  // TÍNH NĂNG GHÉP ĐỒ HIẾN TẾ NÂNG TIER
  private forgeUpgradeTier(): void {
    if (this.inventoryData.bag.length < 2) {
      alert('Cần ít nhất 2 trang bị trong túi đồ để làm nguyên liệu hiến tế nâng Tier!');
      return;
    }
    if (this.inventoryData.equippedItem.tier >= 5) {
      alert('Trang bị đang mặc đã đạt cấp tối đa (Tier 5)!');
      return;
    }

    // Tiêu thụ 2 món đầu tiên trong túi
    this.inventoryData.bag.splice(0, 2);
    this.inventoryData.equippedItem.tier++;

    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private equipFromBag(index: number): void {
    if (index >= this.inventoryData.bag.length) return;
    const itemToEquip = this.inventoryData.bag[index];
    const oldItem = this.inventoryData.equippedItem;

    this.inventoryData.equippedItem = itemToEquip;
    this.inventoryData.bag[index] = oldItem;

    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private useCurrency(cur: CurrencyType): void {
    const qty = this.inventoryData.currencies[cur] || 0;
    if (qty <= 0) return;

    const success = CraftingEngine.applyCurrency(cur, this.inventoryData.equippedItem);
    if (success) {
      SoundEffects.playHit();
      this.inventoryData.currencies[cur]--;
      this.onItemUpdated();
      this.refresh();
    }
  }

  public refresh(): void {
    const item = this.inventoryData.equippedItem;
    const rarityColor = item.rarity === 'Rare' ? '#ffd700' : item.rarity === 'Magic' ? '#4169e1' : '#ffffff';
    this.itemTitleText.setText(`[TIER ${item.tier} - ${item.rarity.toUpperCase()}] ${item.baseType}`);
    this.itemTitleText.setColor(rarityColor);

    const tierMult = 1 + (item.tier - 1) * 0.4;
    this.tierBonusText.setText(`★ Hiệu Lực Tier ${item.tier}: Gia tăng ${Math.round((tierMult - 1) * 100)}% toàn bộ chỉ số món đồ`);

    let sockStr = '❖ LỖ NGỌC & LIÊN KẾT:\n';
    this.player.sockets.forEach((s, idx) => {
      const gemName = s.gem ? s.gem.name : '(Trống)';
      sockStr += `  • Ô ${idx + 1} [Nhóm ${s.linkGroup} - ${s.color.toUpperCase()}]: ${gemName}\n`;
    });
    this.socketsText.setText(sockStr);

    let affStr = '--- PREFIXES ---\n';
    if (item.prefixes.length === 0) affStr += '(Trống)\n';
    item.prefixes.forEach((p) => {
      const scaledVal = Math.round(p.value * tierMult);
      affStr += `• ${p.name}: +${scaledVal} (${p.statType})\n`;
    });

    affStr += '\n--- SUFFIXES ---\n';
    if (item.suffixes.length === 0) affStr += '(Trống)\n';
    item.suffixes.forEach((s) => {
      const scaledVal = Math.round(s.value * tierMult);
      affStr += `• ${s.name}: +${scaledVal} (${s.statType})\n`;
    });
    this.affixesText.setText(affStr);

    this.bagElements.forEach((el) => el.destroy());
    this.bagElements = [];

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    if (this.inventoryData.bag.length === 0) {
      const emptyText = this.scene.add.text(cx + 40, cy - 125, '(Túi trống - Đánh quái để nhặt trang bị)', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#64748b',
      }).setScrollFactor(0);
      this.bagElements.push(emptyText);
      this.container.add(emptyText);
    } else {
      this.inventoryData.bag.forEach((bagItem, idx) => {
        const itemY = cy - 135 + idx * 44;
        const rColor = bagItem.rarity === 'Rare' ? '#ffd700' : bagItem.rarity === 'Magic' ? '#60a5fa' : '#ffffff';

        const nameTxt = this.scene.add.text(cx + 10, itemY, `[T${bagItem.tier} ${bagItem.rarity}] ${bagItem.baseType}`, {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: rColor,
        }).setScrollFactor(0);

        const equipBtn = this.scene.add.text(cx + 270, itemY, 'MẶC ĐỒ', {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: '#000000',
          backgroundColor: '#38bdf8',
          padding: { x: 8, y: 4 },
        }).setScrollFactor(0).setInteractive({ useHandCursor: true });

        equipBtn.on('pointerdown', () => this.equipFromBag(idx));
        equipBtn.on('pointerover', () => equipBtn.setBackgroundColor('#ffffff'));
        equipBtn.on('pointerout', () => equipBtn.setBackgroundColor('#38bdf8'));

        this.bagElements.push(nameTxt, equipBtn);
        this.container.add([nameTxt, equipBtn]);
      });
    }

    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      btn.setText(`${type.toUpperCase()}\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
