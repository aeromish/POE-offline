import Phaser from 'phaser';
import { InventoryData, CurrencyType, EquipmentItem, EquipmentSlot } from '../core/items/ItemTypes';
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

  private slotLabels: Map<EquipmentSlot, Phaser.GameObjects.Text> = new Map();
  private selectedItemTitle!: Phaser.GameObjects.Text;
  private selectedItemAffixes!: Phaser.GameObjects.Text;
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

    const bg = this.scene.add.rectangle(cx, cy, 820, 540, 0x090d16, 1.0)
      .setStrokeStyle(2, 0x30363d)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 245, 'HÀNH TRANG & TRANG BỊ NHÂN VẬT (10 SLOTS) [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(header);

    // CỘT TRÁI: 10 Ô TRANG BỊ TRÊN NGƯỜI (PAPERDOLL LAYOUT)
    const slotConfigs: { slot: EquipmentSlot; name: string; x: number; y: number }[] = [
      { slot: 'helmet', name: 'MŨ', x: cx - 290, y: cy - 195 },
      { slot: 'amulet', name: 'DÂY CHUYỀN', x: cx - 290, y: cy - 150 },
      { slot: 'weapon', name: 'VŨ KHÍ', x: cx - 365, y: cy - 105 },
      { slot: 'bodyArmour', name: 'GIÁP NGỰC', x: cx - 290, y: cy - 105 },
      { slot: 'offhand', name: 'TAY PHỤ', x: cx - 215, y: cy - 105 },
      { slot: 'gloves', name: 'GĂNG TAY', x: cx - 365, y: cy - 60 },
      { slot: 'belt', name: 'THẮT LƯNG', x: cx - 290, y: cy - 60 },
      { slot: 'boots', name: 'GIÀY', x: cx - 215, y: cy - 60 },
      { slot: 'ring1', name: 'NHẪN 1', x: cx - 340, y: cy - 15 },
      { slot: 'ring2', name: 'NHẪN 2', x: cx - 240, y: cy - 15 },
    ];

    slotConfigs.forEach((sc) => {
      const slotBg = this.scene.add.rectangle(sc.x, sc.y, 70, 36, 0x1e293b, 1)
        .setStrokeStyle(1, 0x475569)
        .setScrollFactor(0)
        .setInteractive({ useHandCursor: true });

      const label = this.scene.add.text(sc.x, sc.y, `${sc.name}\n(Trống)`, {
        fontFamily: 'monospace',
        fontSize: '10px',
        align: 'center',
        color: '#94a3b8',
      }).setOrigin(0.5).setScrollFactor(0);

      slotBg.on('pointerdown', () => this.handleSlotClick(sc.slot));
      slotBg.on('pointerover', () => slotBg.setStrokeStyle(2, 0xffd700));
      slotBg.on('pointerout', () => slotBg.setStrokeStyle(1, 0x475569));

      this.slotLabels.set(sc.slot, label);
      this.container.add([slotBg, label]);
    });

    // KHU VỰC THÔNG TIN MÓN ĐỒ ĐANG CHỌN ĐỂ CHẾ TẠO / RÈN
    this.selectedItemTitle = this.scene.add.text(cx - 290, cy + 30, '', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.selectedItemTitle);

    this.selectedItemAffixes = this.scene.add.text(cx - 390, cy + 45, '', {
      fontFamily: 'monospace',
      fontSize: '10px',
      color: '#8888ff',
      lineSpacing: 2,
    }).setScrollFactor(0);
    this.container.add(this.selectedItemAffixes);

    // CỘT PHẢI: TÚI ĐỒ (BAG)
    const bagTitle = this.scene.add.text(cx + 175, cy - 200, '❖ TÚI HÀNH TRANG (BẤM MẶC ĐỒ):', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(bagTitle);

    // NÚT GHÉP ĐỒ TĂNG TIER
    const forgeBtn = this.scene.add.text(cx + 175, cy - 170, '🔨 HIẾN TẾ 2 MÓN TRONG TÚI ĐỂ +1 TIER MÓN ĐANG CHỌN', {
      fontFamily: 'monospace',
      fontSize: '10px',
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

    const startY = cy + 160;
    curList.forEach((c, idx) => {
      const col = idx % 3;
      const row = Math.floor(idx / 3);
      const bx = cx - 180 + col * 180;
      const by = startY + row * 44;

      const btn = this.scene.add.text(bx, by, '', {
        fontFamily: 'monospace',
        fontSize: '11px',
        color: '#ffffff',
        backgroundColor: '#21262d',
        padding: { x: 8, y: 6 },
        stroke: '#000000',
        strokeThickness: 2,
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

      btn.on('pointerdown', () => this.useCurrency(c.type));
      btn.on('pointerover', () => btn.setBackgroundColor('#388bfd'));
      btn.on('pointerout', () => btn.setBackgroundColor('#21262d'));

      this.currencyButtons.set(c.type, btn);
      this.container.add(btn);
    });

    const closeBtn = this.scene.add.text(cx, cy + 245, '[ĐÓNG GIAO DIỆN (I)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#8b949e',
      backgroundColor: '#161b22',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  // Click vào ô đồ đang mặc: Tháo ra túi hoặc chọn làm mục tiêu chế đồ
  private handleSlotClick(slot: EquipmentSlot): void {
    const item = this.inventoryData.equipped[slot];
    if (!item) return;

    this.inventoryData.selectedItemForCraft = item;
    SoundEffects.playPoETink();
    this.refresh();
  }

  // Mặc đồ từ túi vào đúng ô tương ứng
  private equipFromBag(index: number): void {
    if (index >= this.inventoryData.bag.length) return;
    const item = this.inventoryData.bag[index];
    let targetSlot = item.slot;

    // Riêng nhẫn: Ưu tiên gắn vào ô trống
    if (item.baseType === 'Ring') {
      if (!this.inventoryData.equipped.ring1) targetSlot = 'ring1';
      else if (!this.inventoryData.equipped.ring2) targetSlot = 'ring2';
      else targetSlot = 'ring1';
    }

    const currentEquipped = this.inventoryData.equipped[targetSlot];

    // Tráo đồ
    this.inventoryData.equipped[targetSlot] = item;
    if (currentEquipped) {
      this.inventoryData.bag[index] = currentEquipped;
    } else {
      this.inventoryData.bag.splice(index, 1);
    }

    this.inventoryData.selectedItemForCraft = item;
    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private forgeUpgradeTier(): void {
    if (!this.inventoryData.selectedItemForCraft) {
      alert('Hãy bấm chọn một món đồ để nâng Tier!');
      return;
    }
    if (this.inventoryData.bag.length < 2) {
      alert('Cần ít nhất 2 trang bị trong túi để hiến tế nâng Tier!');
      return;
    }
    if (this.inventoryData.selectedItemForCraft.tier >= 5) {
      alert('Trang bị đã đạt cấp tối đa (Tier 5)!');
      return;
    }

    this.inventoryData.bag.splice(0, 2);
    this.inventoryData.selectedItemForCraft.tier++;

    SoundEffects.playPoETink();
    this.onItemUpdated();
    this.refresh();
  }

  private useCurrency(cur: CurrencyType): void {
    if (!this.inventoryData.selectedItemForCraft) {
      alert('Hãy chọn một món đồ để dùng Currency chế tác!');
      return;
    }
    const qty = this.inventoryData.currencies[cur] || 0;
    if (qty <= 0) return;

    const success = CraftingEngine.applyCurrency(cur, this.inventoryData.selectedItemForCraft);
    if (success) {
      SoundEffects.playHit();
      this.inventoryData.currencies[cur]--;
      this.onItemUpdated();
      this.refresh();
    }
  }

  public refresh(): void {
    // 1. Cập nhật 10 ô Paperdoll
    this.slotLabels.forEach((label, slot) => {
      const item = this.inventoryData.equipped[slot];
      if (item) {
        const colorHex = item.rarity === 'Rare' ? '#ffd700' : item.rarity === 'Magic' ? '#60a5fa' : '#ffffff';
        label.setText(`[T${item.tier}]\n${item.baseType}`);
        label.setColor(colorHex);
      } else {
        label.setText(`${slot.toUpperCase()}\n(Trống)`);
        label.setColor('#64748b');
      }
    });

    // 2. Cập nhật thông tin món đang chọn để Craft
    const selected = this.inventoryData.selectedItemForCraft || this.inventoryData.equipped.weapon;
    if (selected) {
      const rColor = selected.rarity === 'Rare' ? '#ffd700' : selected.rarity === 'Magic' ? '#4169e1' : '#ffffff';
      this.selectedItemTitle.setText(`[ĐANG CHỌN: T${selected.tier} ${selected.rarity.toUpperCase()}] ${selected.baseType}`);
      this.selectedItemTitle.setColor(rColor);

      let affStr = '';
      selected.prefixes.forEach((p) => affStr += `• Prefix: +${p.value} (${p.statType})\n`);
      selected.suffixes.forEach((s) => affStr += `• Suffix: +${s.value} (${s.statType})\n`);
      this.selectedItemAffixes.setText(affStr || '(Chưa có Affix nào)');
    } else {
      this.selectedItemTitle.setText('CHƯA CHỌN MÓN ĐỒ NÀO ĐỂ RÈN');
      this.selectedItemTitle.setColor('#94a3b8');
      this.selectedItemAffixes.setText('');
    }

    // 3. Vẽ các món trong túi (Tối đa 12 món)
    this.bagElements.forEach((el) => el.destroy());
    this.bagElements = [];

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    if (this.inventoryData.bag.length === 0) {
      const emptyTxt = this.scene.add.text(cx + 60, cy - 130, '(Túi trống - Đánh quái để nhặt trang bị)', {
        fontFamily: 'monospace',
        fontSize: '11px',
        color: '#64748b',
      }).setScrollFactor(0);
      this.bagElements.push(emptyTxt);
      this.container.add(emptyTxt);
    } else {
      this.inventoryData.bag.slice(0, 6).forEach((bItem, idx) => {
        const itemY = cy - 140 + idx * 42;
        const color = bItem.rarity === 'Rare' ? '#ffd700' : bItem.rarity === 'Magic' ? '#60a5fa' : '#ffffff';

        const nameTxt = this.scene.add.text(cx + 30, itemY, `[T${bItem.tier} ${bItem.rarity}] ${bItem.baseType}`, {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color,
        }).setScrollFactor(0);

        const equipBtn = this.scene.add.text(cx + 280, itemY, 'MẶC ĐỒ', {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: '#000000',
          backgroundColor: '#38bdf8',
          padding: { x: 8, y: 3 },
        }).setScrollFactor(0).setInteractive({ useHandCursor: true });

        equipBtn.on('pointerdown', () => this.equipFromBag(idx));

        this.bagElements.push(nameTxt, equipBtn);
        this.container.add([nameTxt, equipBtn]);
      });
    }

    // 4. Cập nhật số lượng Currency
    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      btn.setText(`${type.toUpperCase()}\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
