import os

files = {
    # 1. Hệ thống Quests Core
    "src/core/quests/QuestTypes.ts": '''export type QuestType = 'kill_count' | 'kill_rares' | 'collect_currency' | 'reach_wave';

export interface Quest {
  id: string;
  title: string;
  description: string;
  type: QuestType;
  current: number;
  target: number;
  rewardText: string;
  rewardType: 'exp' | 'skill_point' | 'chaos';
  rewardValue: number;
  isCompleted: boolean;
}
''',

    "src/core/quests/QuestManager.ts": '''import { Quest } from './QuestTypes';

export class QuestManager {
  public activeQuests: Quest[] = [];

  constructor() {
    this.initDefaultQuests();
  }

  public initDefaultQuests(): void {
    this.activeQuests = [
      {
        id: 'q_kill_30',
        title: 'Càn Quét Chiến Trường',
        description: 'Tiêu diệt 30 quái vật bất kỳ',
        type: 'kill_count',
        current: 0,
        target: 30,
        rewardText: '+200 EXP',
        rewardType: 'exp',
        rewardValue: 200,
        isCompleted: false,
      },
      {
        id: 'q_kill_rares',
        title: 'Thợ Săn Tinh Anh',
        description: 'Tiêu diệt 2 quái vật Rare (Vàng)',
        type: 'kill_rares',
        current: 0,
        target: 2,
        rewardText: '+1 Điểm Thiên Phú',
        rewardType: 'skill_point',
        rewardValue: 1,
        isCompleted: false,
      },
      {
        id: 'q_collect_cur',
        title: 'Kẻ Thu Thập Tiền Tệ',
        description: 'Thu thập 5 đồng Tiền Tệ (Currency)',
        type: 'collect_currency',
        current: 0,
        target: 5,
        rewardText: '+2 Chaos Orb',
        rewardType: 'chaos',
        rewardValue: 2,
        isCompleted: false,
      },
    ];
  }

  public onMonsterKilled(isRare: boolean): Quest[] {
    const completedNow: Quest[] = [];
    for (const q of this.activeQuests) {
      if (q.isCompleted) continue;
      if (q.type === 'kill_count') {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      } else if (q.type === 'kill_rares' && isRare) {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      }
    }
    return completedNow;
  }

  public onCurrencyCollected(): Quest[] {
    const completedNow: Quest[] = [];
    for (const q of this.activeQuests) {
      if (q.isCompleted) continue;
      if (q.type === 'collect_currency') {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      }
    }
    return completedNow;
  }
}
''',

    # 2. Cấu trúc 10 Vị Trí Trang Bị Chuẩn ARPG (ItemTypes.ts)
    "src/core/items/ItemTypes.ts": '''export type ItemRarity = 'Normal' | 'Magic' | 'Rare';

export type CurrencyType = 
  | 'transmutation' 
  | 'alteration' 
  | 'regal' 
  | 'chaos' 
  | 'exalted' 
  | 'scouring';

export type EquipmentSlot = 
  | 'weapon' 
  | 'offhand' 
  | 'helmet' 
  | 'bodyArmour' 
  | 'gloves' 
  | 'boots' 
  | 'amulet' 
  | 'ring1' 
  | 'ring2' 
  | 'belt';

export type ItemBaseType = 
  | 'Sword' | 'Bow' | 'Wand'
  | 'Shield' | 'Quiver'
  | 'Helmet' | 'Body Armour' | 'Gloves' | 'Boots'
  | 'Amulet' | 'Ring' | 'Belt';

export interface AffixDefinition {
  id: string;
  name: string;
  type: 'prefix' | 'suffix';
  statType: 
    | 'added_damage' 
    | 'inc_damage' 
    | 'flat_life' 
    | 'flat_es' 
    | 'attack_speed' 
    | 'movement_speed' 
    | 'armour' 
    | 'crit_chance';
  minValue: number;
  maxValue: number;
}

export interface AffixInstance {
  definitionId: string;
  name: string;
  type: 'prefix' | 'suffix';
  statType: string;
  value: number;
}

export interface EquipmentItem {
  id: string;
  name: string;
  baseType: ItemBaseType;
  slot: EquipmentSlot;
  tier: number;
  rarity: ItemRarity;
  prefixes: AffixInstance[];
  suffixes: AffixInstance[];
}

export interface EquippedSlots {
  weapon: EquipmentItem | null;
  offhand: EquipmentItem | null;
  helmet: EquipmentItem | null;
  bodyArmour: EquipmentItem | null;
  gloves: EquipmentItem | null;
  boots: EquipmentItem | null;
  amulet: EquipmentItem | null;
  ring1: EquipmentItem | null;
  ring2: EquipmentItem | null;
  belt: EquipmentItem | null;
}

export interface InventoryData {
  currencies: Record<CurrencyType, number>;
  equipped: EquippedSlots;
  bag: EquipmentItem[];
  selectedItemForCraft: EquipmentItem | null;
}
''',

    # 3. Rơi Trang Bị Đa Dạng Theo Đúng 10 Vị Trí
    "src/core/loot/LootEngine.ts": '''import { CurrencyType, EquipmentItem, ItemBaseType, EquipmentSlot } from '../items/ItemTypes';
import { MonsterRarity } from '../monsters/MonsterTypes';
import { CraftingEngine } from '../crafting/CraftingEngine';

export interface DropResult {
  category: 'currency' | 'equipment' | 'gem';
  currencyType?: CurrencyType;
  equipmentItem?: EquipmentItem;
  gemId?: string;
  name: string;
}

export class LootEngine {
  private static readonly ITEM_POOLS: { base: ItemBaseType; slot: EquipmentSlot }[] = [
    { base: 'Sword', slot: 'weapon' },
    { base: 'Bow', slot: 'weapon' },
    { base: 'Wand', slot: 'weapon' },
    { base: 'Shield', slot: 'offhand' },
    { base: 'Quiver', slot: 'offhand' },
    { base: 'Helmet', slot: 'helmet' },
    { base: 'Body Armour', slot: 'bodyArmour' },
    { base: 'Gloves', slot: 'gloves' },
    { base: 'Boots', slot: 'boots' },
    { base: 'Amulet', slot: 'amulet' },
    { base: 'Ring', slot: 'ring1' },
    { base: 'Belt', slot: 'belt' },
  ];

  public static rollMonsterDrops(rarity: MonsterRarity): DropResult[] {
    const drops: DropResult[] = [];
    const roll = Math.random();

    let dropChance = 0.35;
    if (rarity === 'Magic') dropChance = 0.65;
    if (rarity === 'Rare') dropChance = 0.95;
    if (rarity === 'Boss') dropChance = 1.0;

    if (roll > dropChance) return drops;

    const numDrops = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

    for (let i = 0; i < numDrops; i++) {
      const typeRoll = Math.random();

      // 50% rơi Currency
      if (typeRoll < 0.5) {
        const cRoll = Math.random() * 100;
        let cur: CurrencyType = 'transmutation';
        let name = 'Orb of Transmutation';

        if (cRoll < 5 && (rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'exalted';
          name = 'Exalted Orb';
        } else if (cRoll < 22 && (rarity === 'Magic' || rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'chaos';
          name = 'Chaos Orb';
        } else if (cRoll < 42) {
          cur = 'regal';
          name = 'Regal Orb';
        } else if (cRoll < 65) {
          cur = 'scouring';
          name = 'Orb of Scouring';
        } else if (cRoll < 85) {
          cur = 'alteration';
          name = 'Orb of Alteration';
        }

        drops.push({ category: 'currency', currencyType: cur, name });
      }
      // 35% rơi Trang bị thuộc 10 vị trí
      else if (typeRoll < 0.85) {
        const chosen = this.ITEM_POOLS[Math.floor(Math.random() * this.ITEM_POOLS.length)];
        const itemTier = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

        const item: EquipmentItem = {
          id: `eq_${Date.now()}_${Math.random()}`,
          name: chosen.base,
          baseType: chosen.base,
          slot: chosen.slot,
          tier: itemTier,
          rarity: 'Normal',
          prefixes: [],
          suffixes: [],
        };

        if (rarity === 'Rare' || rarity === 'Boss') {
          CraftingEngine.applyTransmutation(item);
          CraftingEngine.applyRegal(item);
        } else if (rarity === 'Magic') {
          CraftingEngine.applyTransmutation(item);
        }

        drops.push({
          category: 'equipment',
          equipmentItem: item,
          name: `[T${item.tier} ${item.rarity}] ${item.baseType}`,
        });
      }
      // 15% rơi Ngọc kỹ năng
      else {
        const gemKeys = ['fireball', 'split_arrow', 'ground_slam', 'frostbolt', 'spark', 'blade_vortex', 'arc', 'molten_strike', 'toxic_spore'];
        const gid = gemKeys[Math.floor(Math.random() * gemKeys.length)];
        drops.push({ category: 'gem', gemId: gid, name: `Ngọc ${gid.toUpperCase()}` });
      }
    }

    return drops;
  }
}
''',

    # 4. Giao Diện Hòm Đồ Paperdoll 10 Slots Chuẩn ARPG
    "src/scenes/CraftingUI.ts": '''import Phaser from 'phaser';
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

      const label = this.scene.add.text(sc.x, sc.y, `${sc.name}\\n(Trống)`, {
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
        label.setText(`[T${item.tier}]\\n${item.baseType}`);
        label.setColor(colorHex);
      } else {
        label.setText(`${slot.toUpperCase()}\\n(Trống)`);
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
      selected.prefixes.forEach((p) => affStr += `• Prefix: +${p.value} (${p.statType})\\n`);
      selected.suffixes.forEach((s) => affStr += `• Suffix: +${s.value} (${s.statType})\\n`);
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
      btn.setText(`${type.toUpperCase()}\\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
''',

    # 5. Cập nhật Player.ts: Cộng Dồn Chỉ Số từ Cả 10 Ô Trang Bị
    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats, getExpNeeded } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill, GroundSlamSkill, ALL_ACTIVE_SKILLS } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquippedSlots } from '../core/items/ItemTypes';
import { PassiveTreeBonus } from '../core/passive/PassiveTreeTypes';
import { Projectile } from './Projectile';

export class Player extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  public characterClass: CharacterClass;
  public sockets: Socket[] = [];
  public compiledSkills: SkillContext[] = [];

  public pickupRadius: number = 160;
  public expBonusPct: number = 0;

  private skillCooldownTimers: Map<string, number> = new Map();
  public skillBonusLevels: Map<string, number> = new Map();

  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private keyW!: Phaser.Input.Keyboard.Key;
  private keyA!: Phaser.Input.Keyboard.Key;
  private keyS!: Phaser.Input.Keyboard.Key;
  private keyD!: Phaser.Input.Keyboard.Key;
  private lastHitTime: number = 0;

  constructor(scene: Phaser.Scene, x: number, y: number, characterClass: CharacterClass) {
    const textureKey = `player_${characterClass.toLowerCase()}`;
    super(scene, x, y, textureKey, 0);

    this.characterClass = characterClass;
    this.stats = { ...CLASS_BASE_STATS[characterClass] };

    scene.add.existing(this);
    scene.physics.add.existing(this);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(18, 22);
      body.setOffset(7, 10);
      body.setCollideWorldBounds(true);
    }

    if (scene.input.keyboard) {
      this.cursors = scene.input.keyboard.createCursorKeys();
      this.keyW = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
      this.keyA = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
      this.keyS = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
      this.keyD = scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);
    }

    this.setupClassSkillAndGems();
    this.compileSkills();
  }

  public setClass(newClass: CharacterClass): void {
    this.characterClass = newClass;
    const base = CLASS_BASE_STATS[newClass];
    this.stats = { ...base, level: this.stats.level, currentExp: this.stats.currentExp, maxExp: this.stats.maxExp };
    this.setTexture(`player_${newClass.toLowerCase()}`);
    this.setupClassSkillAndGems();
    this.compileSkills();
  }

  public setupClassSkillAndGems(): void {
    if (this.characterClass === 'Mage') {
      this.sockets = [
        { color: 'blue', linkGroup: 1, gem: FireballSkill },
        { color: 'green', linkGroup: 1, gem: GreaterMultipleProjectiles },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
      this.skillBonusLevels.set('fireball', 1);
    } else if (this.characterClass === 'Archer') {
      this.sockets = [
        { color: 'green', linkGroup: 1, gem: SplitArrowSkill },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
      this.skillBonusLevels.set('split_arrow', 1);
    } else {
      this.sockets = [
        { color: 'red', linkGroup: 1, gem: GroundSlamSkill },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
      ];
      this.skillBonusLevels.set('ground_slam', 1);
    }
  }

  public addOrUpgradeSkill(skillId: string): void {
    const curLvl = this.skillBonusLevels.get(skillId) || 0;
    this.skillBonusLevels.set(skillId, curLvl + 1);

    const existing = this.sockets.find((s) => s.gem && s.gem.id === skillId);
    if (!existing) {
      const newGem = ALL_ACTIVE_SKILLS[skillId];
      if (newGem) {
        this.sockets.push({
          color: newGem.color,
          linkGroup: this.sockets.length + 1,
          gem: newGem,
        });
      }
    }
    this.compileSkills();
  }

  public gainExp(amount: number): boolean {
    const finalExp = Math.round(amount * (1 + this.expBonusPct / 100));
    this.stats.currentExp += finalExp;
    if (this.stats.currentExp >= this.stats.maxExp) {
      this.stats.currentExp -= this.stats.maxExp;
      this.stats.level++;
      this.stats.maxExp = getExpNeeded(this.stats.level);
      this.stats.maxLife += 15;
      this.stats.currentLife = this.stats.maxLife;
      if (this.stats.maxEnergyShield > 0) {
        this.stats.maxEnergyShield += 10;
        this.stats.energyShield = this.stats.maxEnergyShield;
      }
      return true;
    }
    return false;
  }

  // TÍNH TOÁN CHỈ SỐ TỪ CẢ 10 Ô TRANG BỊ
  public recalculateTotalStats(equipped: EquippedSlots, treeBonus: PassiveTreeBonus): void {
    const base = CLASS_BASE_STATS[this.characterClass];
    const levelBonusLife = (this.stats.level - 1) * 15;
    const levelBonusES = (this.stats.level - 1) * 10;

    this.pickupRadius = 160 + treeBonus.pickupRadius;
    this.expBonusPct = treeBonus.expBonusPct;

    let totalFlatLife = base.maxLife + levelBonusLife + treeBonus.flatLife;
    let totalFlatES = base.maxEnergyShield + (base.maxEnergyShield > 0 ? levelBonusES : 0) + treeBonus.flatES;
    let totalArmour = base.armour + treeBonus.flatArmour;
    let totalEvasion = base.evasion + treeBonus.flatEvasion;
    let totalMoveSpeed = base.movementSpeed + treeBonus.movementSpeed;

    // Duyệt qua toàn bộ 10 ô trang bị đang mặc
    for (const item of Object.values(equipped)) {
      if (!item) continue;
      const tierMult = 1 + (item.tier - 1) * 0.4;
      const allAffixes = [...item.prefixes, ...item.suffixes];

      for (const aff of allAffixes) {
        const scaledVal = Math.round(aff.value * tierMult);
        if (aff.statType === 'flat_life') totalFlatLife += scaledVal;
        if (aff.statType === 'flat_es') totalFlatES += scaledVal;
        if (aff.statType === 'armour') totalArmour += scaledVal;
        if (aff.statType === 'movement_speed') totalMoveSpeed += scaledVal;
      }
    }

    this.stats.maxLife = totalFlatLife;
    this.stats.maxEnergyShield = totalFlatES;
    this.stats.armour = totalArmour;
    this.stats.evasion = totalEvasion;
    this.stats.movementSpeed = totalMoveSpeed;

    this.stats.currentLife = Math.min(this.stats.currentLife, this.stats.maxLife);
    this.compileSkills(equipped, treeBonus);
  }

  public compileSkills(equipped?: EquippedSlots, treeBonus?: PassiveTreeBonus): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    let addedDmg = 0;
    let incDmg = 0;
    let atkSpeedPct = 0;
    let critChance = 0;
    let critMultiplier = 0;
    let extraProj = 0;
    let extraPierce = 0;

    // Thu thập chỉ số sát thương từ toàn bộ trang bị
    if (equipped) {
      for (const item of Object.values(equipped)) {
        if (!item) continue;
        const tierMult = 1 + (item.tier - 1) * 0.4;
        const allAff = [...item.prefixes, ...item.suffixes];
        for (const a of allAff) {
          const val = Math.round(a.value * tierMult);
          if (a.statType === 'added_damage') addedDmg += val;
          if (a.statType === 'inc_damage') incDmg += val;
          if (a.statType === 'attack_speed') atkSpeedPct += val;
          if (a.statType === 'crit_chance') critChance += val;
        }
      }
    }

    if (treeBonus) {
      atkSpeedPct += treeBonus.attackSpeedPct;
      critChance += treeBonus.critChance;
      critMultiplier += treeBonus.critMultiplier;
      extraProj += treeBonus.extraProjectile;
      extraPierce += treeBonus.extraPierce;
    }

    for (const activeSock of activeSockets) {
      const activeGem = activeSock.gem as ActiveGem;
      const sLvl = this.skillBonusLevels.get(activeGem.id) || 1;
      const ctx = activeGem.getInitialContext(sLvl);

      if (ctx.damageType === 'physical' && treeBonus) {
        incDmg += treeBonus.incPhysDamage;
      } else if (ctx.damageType === 'fire' && treeBonus) {
        incDmg += treeBonus.incFireDamage;
      }

      ctx.addedMinDamage += addedDmg;
      ctx.addedMaxDamage += addedDmg;
      ctx.increasedDamagePercent += incDmg;
      ctx.attackSpeedMultiplier *= (1 + atkSpeedPct / 100);
      ctx.critChance += critChance;
      ctx.critMultiplier += critMultiplier;
      ctx.projectileCount += extraProj;
      ctx.pierceCount += extraPierce;

      const linkedSupports = this.sockets.filter(
        (s) => s.linkGroup === activeSock.linkGroup && s.gem && 'apply' in s.gem
      );

      for (const suppSock of linkedSupports) {
        const supportGem = suppSock.gem as SupportGem;
        supportGem.apply(ctx);
      }

      this.compiledSkills.push(ctx);
    }
  }

  public tryCastSkills(
    time: number,
    targetX: number,
    targetY: number,
    projectilePool: Phaser.Physics.Arcade.Group
  ): void {
    if (this.compiledSkills.length === 0) return;

    for (const skill of this.compiledSkills) {
      const lastCast = this.skillCooldownTimers.get(skill.id) || 0;
      const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
      if (time - lastCast < cooldown) continue;

      this.skillCooldownTimers.set(skill.id, time);

      const baseAngle = Phaser.Math.Angle.Between(this.x, this.y, targetX, targetY);
      const count = skill.projectileCount;
      const spreadAngle = 0.16;

      for (let i = 0; i < count; i++) {
        const p = projectilePool.get(this.x, this.y) as Projectile;
        if (!p) continue;

        const offset = (i - (count - 1) / 2) * spreadAngle;
        p.fire(this.x, this.y, baseAngle + offset, skill);
      }
    }
  }

  public getCooldownPercent(skillId: string, time: number): number {
    const skill = this.compiledSkills.find((s) => s.id === skillId);
    if (!skill) return 0;
    const lastCast = this.skillCooldownTimers.get(skillId) || 0;
    const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
    const elapsed = time - lastCast;
    if (elapsed >= cooldown) return 0;
    return 1 - elapsed / cooldown;
  }

  public takePhysicalDamage(rawDamage: number, time: number): boolean {
    if (Math.random() * 100 < this.stats.evasion) {
      return false;
    }

    const dr = this.stats.armour / (this.stats.armour + 5 * rawDamage);
    const damage = Math.max(1, Math.round(rawDamage * (1 - Math.min(dr, 0.9))));

    this.lastHitTime = time;

    let remaining = damage;
    if (this.stats.energyShield > 0) {
      const absorbed = Math.min(this.stats.energyShield, remaining);
      this.stats.energyShield -= absorbed;
      remaining -= absorbed;
    }

    if (remaining > 0) {
      this.stats.currentLife = Math.max(0, this.stats.currentLife - remaining);
    }

    this.setTint(0xff3333);
    this.scene.time.delayedCall(120, () => {
      if (this.active) this.clearTint();
    });

    return true;
  }

  update(time: number, delta: number): void {
    const speed = this.stats.movementSpeed;
    let vx = 0;
    let vy = 0;

    if (this.cursors.left.isDown || this.keyA.isDown) vx -= 1;
    if (this.cursors.right.isDown || this.keyD.isDown) vx += 1;
    if (this.cursors.up.isDown || this.keyW.isDown) vy -= 1;
    if (this.cursors.down.isDown || this.keyS.isDown) vy += 1;

    if (vx !== 0 && vy !== 0) {
      vx *= 0.7071;
      vy *= 0.7071;
    }

    this.setVelocity(vx * speed, vy * speed);

    const prefix = `player_${this.characterClass.toLowerCase()}`;
    if (vx > 0) {
      this.play(`${prefix}_walk_right`, true);
      this.setFlipX(false);
    } else if (vx < 0) {
      this.play(`${prefix}_walk_right`, true);
      this.setFlipX(true);
    } else if (vy > 0) {
      this.play(`${prefix}_walk_down`, true);
      this.setFlipX(false);
    } else if (vy < 0) {
      this.play(`${prefix}_walk_up`, true);
      this.setFlipX(false);
    } else {
      this.anims.stop();
    }

    if (
      this.stats.maxEnergyShield > 0 &&
      this.stats.energyShield < this.stats.maxEnergyShield &&
      time - this.lastHitTime > this.stats.esRechargeDelay * 1000
    ) {
      const rechargeRate = (this.stats.maxEnergyShield * 0.25 * delta) / 1000;
      this.stats.energyShield = Math.min(this.stats.maxEnergyShield, this.stats.energyShield + rechargeRate);
    }
  }
}
''',

    # 6. Cập nhật BattleScene.ts: Khởi tạo đầy đủ 10 ô trang bị & Auto Loot/Attack
    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { Monster } from './Monster';
import { LootDrop } from './LootDrop';
import { CraftingUI } from './CraftingUI';
import { PassiveTreeUI } from './PassiveTreeUI';
import { CharacterUI } from './CharacterUI';
import { LevelUpUI, LevelUpChoice } from './LevelUpUI';
import { IntermissionUI } from './IntermissionUI';
import { WaveManager } from '../core/monsters/WaveManager';
import { DamageEngine } from '../core/combat/DamageEngine';
import { LootEngine } from '../core/loot/LootEngine';
import { PassiveTreeManager } from '../core/passive/PassiveTreeManager';
import { QuestManager } from '../core/quests/QuestManager';
import { InventoryData } from '../core/items/ItemTypes';
import { SoundEffects } from '../core/audio/SoundEffects';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private monsterPool!: Phaser.Physics.Arcade.Group;
  private lootPool!: Phaser.Physics.Arcade.Group;
  private waveManager: WaveManager = new WaveManager();
  private passiveTreeManager: PassiveTreeManager = new PassiveTreeManager();
  private questManager: QuestManager = new QuestManager();

  private craftingUI!: CraftingUI;
  private passiveTreeUI!: PassiveTreeUI;
  private characterUI!: CharacterUI;
  private levelUpUI!: LevelUpUI;
  private intermissionUI!: IntermissionUI;

  private inventoryData: InventoryData = {
    currencies: {
      transmutation: 4,
      alteration: 8,
      regal: 2,
      chaos: 2,
      exalted: 1,
      scouring: 2,
    },
    equipped: {
      weapon: {
        id: 'eq_starter_wep',
        name: 'Kiếm Sắt Rèn',
        baseType: 'Sword',
        slot: 'weapon',
        tier: 1,
        rarity: 'Normal',
        prefixes: [],
        suffixes: [],
      },
      offhand: null,
      helmet: null,
      bodyArmour: null,
      gloves: null,
      boots: null,
      amulet: null,
      ring1: null,
      ring2: null,
      belt: null,
    },
    bag: [],
    selectedItemForCraft: null,
  };

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
  private bestWaveText!: Phaser.GameObjects.Text;
  private classLevelText!: Phaser.GameObjects.Text;
  private lifeBarGfx!: Phaser.GameObjects.Graphics;
  private esBarGfx!: Phaser.GameObjects.Graphics;
  private expBarGfx!: Phaser.GameObjects.Graphics;

  private skillBarContainer!: Phaser.GameObjects.Container;
  private skillSlotWidgets: { bg: Phaser.GameObjects.Rectangle; icon: Phaser.GameObjects.Text; lvl: Phaser.GameObjects.Text; cdGfx: Phaser.GameObjects.Graphics; id: string }[] = [];
  private questTrackerText!: Phaser.GameObjects.Text;

  public autoAttackEnabled: boolean = true;
  public autoLootEnabled: boolean = true;
  private autoAtkBtn!: Phaser.GameObjects.Text;
  private autoLootBtn!: Phaser.GameObjects.Text;

  private isGameOver: boolean = false;
  private bestWave: number = 1;
  private isHoveringInteractiveUI: boolean = false;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2400;
    const mapHeight = 2400;

    this.isGameOver = false;
    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    const savedBest = localStorage.getItem('poe_roguelike_best_wave');
    this.bestWave = savedBest ? parseInt(savedBest, 10) : 1;

    this.createProceduralTextures();

    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');
    this.syncPlayerStats();

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    this.projectilePool = this.physics.add.group({
      classType: Projectile,
      maxSize: 150,
      runChildUpdate: false,
    });

    this.monsterPool = this.physics.add.group({
      classType: Monster,
      maxSize: 200,
      runChildUpdate: false,
    });

    this.lootPool = this.physics.add.group({
      classType: LootDrop,
      maxSize: 100,
      runChildUpdate: false,
    });

    // Va chạm: Đạn -> Quái
    this.physics.add.overlap(this.projectilePool, this.monsterPool, (projObj, monObj) => {
      const proj = projObj as Projectile;
      const monster = monObj as Monster;

      if (!proj.active || !monster.active) return;

      const hit = DamageEngine.calculateHit(proj.skillCtx, monster.poeStatsWrapper);
      const isDead = monster.syncLifeAfterHit();

      SoundEffects.playHit();
      CombatUI.showDamageText(this, monster.x, monster.y, hit);
      this.spawnSkillImpactBurst(monster.x, monster.y, proj.skillCtx.damageType);

      if (isDead) {
        const isRare = monster.monsterStats.rarity === 'Rare' || monster.monsterStats.rarity === 'Boss';
        const completed = this.questManager.onMonsterKilled(isRare);
        this.processCompletedQuests(completed);

        const leveledUp = this.player.gainExp(monster.monsterStats.expReward);
        if (leveledUp) {
          this.triggerLevelUpChoiceModal();
        }

        this.dropLoot(monster.x, monster.y, monster.monsterStats.rarity);
        monster.kill();
      }

      if (proj.remainingPierce > 0) {
        proj.remainingPierce--;
      } else {
        proj.kill();
      }
    });

    // Va chạm: Nhặt đồ
    this.physics.add.overlap(this.player, this.lootPool, (_playerObj, lootObj) => {
      const loot = lootObj as LootDrop;
      if (!loot.active) return;
      this.collectLootItem(loot);
    });

    // Va chạm: Quái -> Người chơi
    this.physics.add.overlap(this.player, this.monsterPool, (_playerObj, monObj) => {
      if (this.isGameOver || this.intermissionUI.getIsShowing() || this.levelUpUI.getIsShowing()) return;
      const monster = monObj as Monster;
      if (!monster.active) return;

      const time = this.time.now;
      if (monster.canAttack(time)) {
        const tookDmg = this.player.takePhysicalDamage(monster.monsterStats.damage, time);
        if (tookDmg) {
          CombatUI.showDamageText(this, this.player.x, this.player.y, {
            damage: monster.monsterStats.damage,
            isCrit: false,
            type: 'physical',
            absorbedByES: 0,
            absorbedByLife: monster.monsterStats.damage,
          });
        }

        if (this.player.stats.currentLife <= 0) {
          this.triggerGameOver();
        }
      }
    });

    this.createHUD();
    this.createSkillBarHUD();
    this.createTopRightActionMenu();

    this.craftingUI = new CraftingUI(this, this.inventoryData, this.player, () => this.syncPlayerStats());
    this.passiveTreeUI = new PassiveTreeUI(this, this.passiveTreeManager, () => this.syncPlayerStats());
    this.characterUI = new CharacterUI(this, this.player);
    this.levelUpUI = new LevelUpUI(this);

    this.intermissionUI = new IntermissionUI(
      this,
      () => this.startNextWave(),
      () => this.craftingUI.toggle(),
      () => this.passiveTreeUI.toggle()
    );

    this.input.keyboard?.on('keydown-C', () => this.characterUI.toggle());
    this.input.keyboard?.on('keydown-I', () => this.craftingUI.toggle());
    this.input.keyboard?.on('keydown-P', () => this.passiveTreeUI.toggle());
    this.input.keyboard?.on('keydown-T', () => this.toggleAutoAttack());
    this.input.keyboard?.on('keydown-F', () => this.toggleAutoLoot());
    this.input.keyboard?.on('keydown-SPACE', () => {
      if (this.intermissionUI.getIsShowing()) {
        this.startNextWave();
      }
    });

    this.time.addEvent({
      delay: 1200,
      callback: this.spawnMonsterWave,
      callbackScope: this,
      loop: true,
    });

    this.time.addEvent({
      delay: 1000,
      callback: this.tickWaveTimer,
      callbackScope: this,
      loop: true,
    });
  }

  private performAutoAttack(time: number): void {
    if (!this.autoAttackEnabled || this.player.compiledSkills.length === 0) return;

    let nearestMonster: Monster | null = null;
    let minDistance = 750;

    this.monsterPool.children.each((child) => {
      const mon = child as Monster;
      if (mon.active) {
        const dist = Phaser.Math.Distance.Between(this.player.x, this.player.y, mon.x, mon.y);
        if (dist < minDistance) {
          minDistance = dist;
          nearestMonster = mon;
        }
      }
      return true;
    });

    if (nearestMonster) {
      this.player.tryCastSkills(time, (nearestMonster as Monster).x, (nearestMonster as Monster).y, this.projectilePool);
    }
  }

  private performAutoLoot(): void {
    if (!this.autoLootEnabled) return;

    const magnetRadius = this.player.pickupRadius;
    this.lootPool.children.each((child) => {
      const loot = child as LootDrop;
      if (loot.active) {
        const dist = Phaser.Math.Distance.Between(this.player.x, this.player.y, loot.x, loot.y);
        if (dist <= magnetRadius) {
          this.physics.moveToObject(loot, this.player, 550);
          if (dist < 25) {
            this.collectLootItem(loot);
          }
        }
      }
      return true;
    });
  }

  private collectLootItem(loot: LootDrop): void {
    const d = loot.collect();
    if (d.category === 'currency' && d.currencyType) {
      this.inventoryData.currencies[d.currencyType] = (this.inventoryData.currencies[d.currencyType] || 0) + 1;
      this.showPickupNotice(loot.x, loot.y, d.currencyType.toUpperCase());

      const completed = this.questManager.onCurrencyCollected();
      this.processCompletedQuests(completed);
    } else if (d.category === 'equipment' && d.equipmentItem) {
      if (this.inventoryData.bag.length < 12) {
        this.inventoryData.bag.push(d.equipmentItem);
        this.showPickupNotice(loot.x, loot.y, `TÚI: ${d.name}`);
      } else {
        this.showPickupNotice(loot.x, loot.y, `TÚI ĐÃ ĐẦY!`);
      }
    } else if (d.category === 'gem' && d.gemId) {
      this.player.addOrUpgradeSkill(d.gemId);
      this.syncPlayerStats();
      this.rebuildSkillBarWidgets();
      this.showPickupNotice(loot.x, loot.y, `HỌC NGỌC: ${d.name}`);
    }
  }

  private spawnSkillImpactBurst(x: number, y: number, damageType: string): void {
    let color = 0xef4444;
    if (damageType === 'cold') color = 0x06b6d4;
    else if (damageType === 'lightning') color = 0xfacc15;
    else if (damageType === 'chaos') color = 0xa855f7;

    for (let i = 0; i < 6; i++) {
      const spark = this.add.circle(x, y, 3, color);
      const angle = Math.random() * Math.PI * 2;
      const speed = 40 + Math.random() * 60;
      this.tweens.add({
        targets: spark,
        x: x + Math.cos(angle) * speed,
        y: y + Math.sin(angle) * speed,
        alpha: 0,
        scale: 0.2,
        duration: 250,
        onComplete: () => spark.destroy(),
      });
    }
  }

  private processCompletedQuests(quests: any[]): void {
    for (const q of quests) {
      SoundEffects.playPoETink();
      if (q.rewardType === 'exp') {
        const leveled = this.player.gainExp(q.rewardValue);
        if (leveled) this.triggerLevelUpChoiceModal();
      } else if (q.rewardType === 'skill_point') {
        this.passiveTreeManager.unspentPoints += q.rewardValue;
      } else if (q.rewardType === 'chaos') {
        this.inventoryData.currencies['chaos'] += q.rewardValue;
      }

      const qNotice = this.add.text(this.scale.width / 2, 140, `🏆 HOÀN THÀNH: ${q.title}\\nNHẬN: ${q.rewardText}`, {
        fontFamily: 'monospace',
        fontSize: '15px',
        fontStyle: 'bold',
        color: '#ffd700',
        align: 'center',
        backgroundColor: '#111827ee',
        padding: { x: 12, y: 8 },
      }).setOrigin(0.5).setScrollFactor(0);

      this.tweens.add({
        targets: qNotice,
        y: 100,
        alpha: 0,
        duration: 2200,
        onComplete: () => qNotice.destroy(),
      });
    }
  }

  private toggleAutoAttack(): void {
    this.autoAttackEnabled = !this.autoAttackEnabled;
    this.autoAtkBtn.setText(this.autoAttackEnabled ? '🎯 TỰ ĐÁNH: BẬT [T]' : '🎯 TỰ ĐÁNH: TẮT [T]');
    this.autoAtkBtn.setColor(this.autoAttackEnabled ? '#4ade80' : '#94a3b8');
  }

  private toggleAutoLoot(): void {
    this.autoLootEnabled = !this.autoLootEnabled;
    this.autoLootBtn.setText(this.autoLootEnabled ? '🧲 HÚT ĐỒ: BẬT [F]' : '🧲 HÚT ĐỒ: TẮT [F]');
    this.autoLootBtn.setColor(this.autoLootEnabled ? '#38bdf8' : '#94a3b8');
  }

  private createSkillBarHUD(): void {
    this.skillBarContainer = this.add.container(0, 0).setScrollFactor(0).setDepth(200);
    this.rebuildSkillBarWidgets();
  }

  private rebuildSkillBarWidgets(): void {
    this.skillBarContainer.removeAll(true);
    this.skillSlotWidgets = [];

    const skills = this.player.compiledSkills;
    const startX = this.scale.width / 2 - (skills.length * 62) / 2 + 31;
    const slotY = this.scale.height - 50;

    skills.forEach((skill, idx) => {
      const slotX = startX + idx * 62;

      const bg = this.add.rectangle(slotX, slotY, 52, 52, 0x111827, 0.95)
        .setStrokeStyle(2, 0x38bdf8)
        .setScrollFactor(0);

      const icon = this.add.text(slotX, slotY - 6, skill.name.slice(0, 2).toUpperCase(), {
        fontFamily: 'monospace',
        fontSize: '14px',
        fontStyle: 'bold',
        color: '#ffffff',
      }).setOrigin(0.5).setScrollFactor(0);

      const lvl = this.add.text(slotX, slotY + 14, `Lv.${skill.level}`, {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: '#ffd700',
      }).setOrigin(0.5).setScrollFactor(0);

      const cdGfx = this.add.graphics().setScrollFactor(0);

      this.skillBarContainer.add([bg, icon, lvl, cdGfx]);
      this.skillSlotWidgets.push({ bg, icon, lvl, cdGfx, id: skill.id });
    });
  }

  private triggerLevelUpChoiceModal(): void {
    SoundEffects.playWaveClear();
    this.passiveTreeManager.unspentPoints++;

    const pool: LevelUpChoice[] = [
      {
        id: 'arc',
        title: 'Arc (Tia Sét Xích)',
        description: 'Tia sét chuỗi giật nhanh, nảy bật qua 2 mục tiêu.',
        type: 'new_skill',
        skillId: 'arc',
        apply: () => {
          this.player.addOrUpgradeSkill('arc');
          this.syncPlayerStats();
        },
      },
      {
        id: 'molten_strike',
        title: 'Molten Strike (Hỏa Nham)',
        description: 'Bắn ra chùm dung nham rực lửa gây sát thương nổ lan.',
        type: 'new_skill',
        skillId: 'molten_strike',
        apply: () => {
          this.player.addOrUpgradeSkill('molten_strike');
          this.syncPlayerStats();
        },
      },
      {
        id: 'toxic_spore',
        title: 'Toxic Spore (Bào Tử Độc)',
        description: 'Bắn các cụm độc tố Chaos nổ tung trên diện rộng.',
        type: 'new_skill',
        skillId: 'toxic_spore',
        apply: () => {
          this.player.addOrUpgradeSkill('toxic_spore');
          this.syncPlayerStats();
        },
      },
      {
        id: 'frostbolt',
        title: 'Frostbolt (Băng Cầu)',
        description: 'Bắn cầu băng xuyên thấu 100% mục tiêu, làm chậm quái.',
        type: 'new_skill',
        skillId: 'frostbolt',
        apply: () => {
          this.player.addOrUpgradeSkill('frostbolt');
          this.syncPlayerStats();
        },
      },
      {
        id: 'spark',
        title: 'Spark (Tia Sét Tán Xạ)',
        description: 'Bắn 4 tia sét giật nhanh tán xạ rộng xung quanh.',
        type: 'new_skill',
        skillId: 'spark',
        apply: () => {
          this.player.addOrUpgradeSkill('spark');
          this.syncPlayerStats();
        },
      },
      {
        id: 'upgrade_main',
        title: 'Cường Hóa Kỹ Năng Đang Có',
        description: '+1 Level cho toàn bộ kỹ năng (+30% Sát thương).',
        type: 'upgrade_skill',
        apply: () => {
          this.player.compiledSkills.forEach((s) => this.player.addOrUpgradeSkill(s.id));
          this.syncPlayerStats();
        },
      },
      {
        id: 'magnet_boost',
        title: 'Từ Tính Siêu Phàm',
        description: '+100 Phạm Vi Hút Đồ và +15% Tốc Độ Di Chuyển.',
        type: 'stat_boost',
        apply: () => {
          this.player.pickupRadius += 100;
          this.player.stats.movementSpeed += 15;
          this.syncPlayerStats();
        },
      },
    ];

    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    const selected3 = shuffled.slice(0, 3);

    this.levelUpUI.show(selected3, () => {
      this.syncPlayerStats();
      this.rebuildSkillBarWidgets();
    });
  }

  private createTopRightActionMenu(): void {
    const rx = this.scale.width - 20;

    this.autoAtkBtn = this.add.text(rx, 20, '🎯 TỰ ĐÁNH: BẬT [T]', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#4ade80',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });
    this.autoAtkBtn.on('pointerdown', () => this.toggleAutoAttack());

    this.autoLootBtn = this.add.text(rx, 50, '🧲 HÚT ĐỒ: BẬT [F]', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#38bdf8',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });
    this.autoLootBtn.on('pointerdown', () => this.toggleAutoLoot());

    const classBtn = this.add.text(rx, 80, '🎭 ĐỔI CLASS', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#a78bfa',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    classBtn.on('pointerdown', () => {
      const classes: ('Mage' | 'Archer' | 'Knight')[] = ['Mage', 'Archer', 'Knight'];
      const nextIdx = (classes.indexOf(this.player.characterClass) + 1) % classes.length;
      this.player.setClass(classes[nextIdx]);
      this.syncPlayerStats();
      this.rebuildSkillBarWidgets();
    });

    const charBtn = this.add.text(rx, 110, '👤 CHỈ SỐ (C)', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#38bdf8',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });
    charBtn.on('pointerdown', () => this.characterUI.toggle());

    const craftBtn = this.add.text(rx, 140, '⚒️ 10 Ô ĐỒ & TÚI (I)', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#ffd700',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });
    craftBtn.on('pointerdown', () => this.craftingUI.toggle());

    const treeBtn = this.add.text(rx, 170, '🌲 THIÊN PHÚ (P)', {
      fontFamily: 'monospace',
      fontSize: '12px',
      fontStyle: 'bold',
      color: '#4ade80',
      backgroundColor: '#21262d',
      padding: { x: 8, y: 5 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });
    treeBtn.on('pointerdown', () => this.passiveTreeUI.toggle());

    [this.autoAtkBtn, this.autoLootBtn, classBtn, charBtn, craftBtn, treeBtn].forEach((btn) => {
      btn.on('pointerover', () => {
        this.isHoveringInteractiveUI = true;
        btn.setBackgroundColor('#30363d');
      });
      btn.on('pointerout', () => {
        this.isHoveringInteractiveUI = false;
        btn.setBackgroundColor('#21262d');
      });
    });
  }

  private syncPlayerStats(): void {
    const bonus = this.passiveTreeManager.calculateTotalBonus();
    this.player.recalculateTotalStats(this.inventoryData.equipped, bonus);
  }

  private dropLoot(x: number, y: number, rarity: any): void {
    const drops = LootEngine.rollMonsterDrops(rarity);
    drops.forEach((d) => {
      let loot = this.lootPool.getFirstDead(false) as LootDrop;
      if (!loot) {
        loot = new LootDrop(this, x, y);
        this.lootPool.add(loot);
      }
      loot.spawn(x + (Math.random() * 30 - 15), y + (Math.random() * 30 - 15), d);

      if (d.category === 'currency' && (d.currencyType === 'chaos' || d.currencyType === 'exalted')) {
        SoundEffects.playPoETink();
      }
    });
  }

  private showPickupNotice(x: number, y: number, text: string): void {
    const t = this.add.text(x, y - 20, `+ ${text}`, {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);

    this.tweens.add({
      targets: t,
      y: y - 50,
      alpha: 0,
      duration: 700,
      onComplete: () => t.destroy(),
    });
  }

  private createProceduralTextures(): void {
    if (!this.textures.exists('proj_fireball')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xef4444, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xfde047, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_fireball', 16, 16);
      g.destroy();
    }

    if (!this.textures.exists('proj_arrow')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x22c55e, 1);
      g.fillRect(0, 5, 14, 2);
      g.fillTriangle(16, 6, 11, 2, 11, 10);
      g.generateTexture('proj_arrow', 16, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_slam')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xd97706, 0.9);
      g.fillCircle(12, 12, 12);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(12, 12, 6);
      g.generateTexture('proj_slam', 24, 24);
      g.destroy();
    }

    if (!this.textures.exists('proj_frostbolt')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x06b6d4, 0.9);
      g.fillCircle(9, 9, 9);
      g.fillStyle(0xe0f2fe, 1);
      g.fillCircle(9, 9, 5);
      g.generateTexture('proj_frostbolt', 18, 18);
      g.destroy();
    }

    if (!this.textures.exists('proj_spark')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xfacc15, 1);
      g.fillCircle(6, 6, 5);
      g.fillStyle(0x67e8f9, 1);
      g.fillCircle(6, 6, 3);
      g.generateTexture('proj_spark', 12, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_blade')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x94a3b8, 1);
      g.fillRect(2, 6, 16, 4);
      g.fillStyle(0xffffff, 1);
      g.fillTriangle(20, 8, 16, 4, 16, 12);
      g.generateTexture('proj_blade', 20, 16);
      g.destroy();
    }

    if (!this.textures.exists('proj_arc')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x38bdf8, 1);
      g.fillRect(0, 4, 16, 4);
      g.fillStyle(0xffffff, 1);
      g.fillRect(4, 2, 8, 8);
      g.generateTexture('proj_arc', 16, 12);
      g.destroy();
    }

    if (!this.textures.exists('proj_molten')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xf97316, 1);
      g.fillCircle(10, 10, 10);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(10, 10, 5);
      g.generateTexture('proj_molten', 20, 20);
      g.destroy();
    }

    if (!this.textures.exists('proj_toxic')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x10b981, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xd8b4fe, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_toxic', 16, 16);
      g.destroy();
    }

    const list = [
      { key: 'monster_normal', body: 0x991b1b, eye: 0xfef08a, border: 0xef4444 },
      { key: 'monster_magic',  body: 0x1e40af, eye: 0x67e8f9, border: 0x60a5fa },
      { key: 'monster_rare',   body: 0x854d0e, eye: 0xffffff, border: 0xfacc15 },
      { key: 'monster_boss',   body: 0x581c87, eye: 0xff0055, border: 0xd8b4fe },
    ];

    list.forEach((item) => {
      if (!this.textures.exists(item.key)) {
        const g = this.make.graphics({ x: 0, y: 0 });
        g.fillStyle(item.body, 1);
        g.fillCircle(16, 16, 13);
        g.lineStyle(2, item.border, 1);
        g.strokeCircle(16, 16, 13);
        g.fillStyle(item.border, 1);
        g.fillTriangle(7, 8, 12, 13, 5, 14);
        g.fillTriangle(25, 8, 20, 13, 27, 14);
        g.fillStyle(item.eye, 1);
        g.fillCircle(11, 14, 2.5);
        g.fillCircle(21, 14, 2.5);
        g.generateTexture(item.key, 32, 32);
        g.destroy();
      }
    });

    if (!this.textures.exists('loot_dummy_tex')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xffffff, 1);
      g.fillRect(0, 0, 16, 16);
      g.generateTexture('loot_dummy_tex', 16, 16);
      g.destroy();
    }
  }

  private createHUD(): void {
    this.waveText = this.add.text(20, 20, 'ĐỢT: 1', {
      fontFamily: 'monospace',
      fontSize: '20px',
      fontStyle: 'bold',
      color: '#ffffff',
    }).setScrollFactor(0);

    this.timerText = this.add.text(20, 48, 'THỜI GIAN: 45s', {
      fontFamily: 'monospace',
      fontSize: '16px',
      color: '#00ffff',
    }).setScrollFactor(0);

    this.bestWaveText = this.add.text(20, 74, `KỶ LỤC: ĐỢT ${this.bestWave}`, {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setScrollFactor(0);

    this.classLevelText = this.add.text(20, 98, '', {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#a78bfa',
    }).setScrollFactor(0);

    this.questTrackerText = this.add.text(this.scale.width - 20, 210, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#cbd5e1',
      align: 'right',
      backgroundColor: '#090d16cc',
      padding: { x: 8, y: 6 },
      lineSpacing: 4,
    }).setOrigin(1, 0).setScrollFactor(0);

    this.lifeBarGfx = this.add.graphics().setScrollFactor(0);
    this.esBarGfx = this.add.graphics().setScrollFactor(0);
    this.expBarGfx = this.add.graphics().setScrollFactor(0);
  }

  private renderHUD(time: number): void {
    this.lifeBarGfx.clear();
    this.esBarGfx.clear();
    this.expBarGfx.clear();

    const barW = 220;
    const barH = 16;
    const x = 20;
    const y = this.scale.height - 45;

    this.classLevelText.setText(`[${this.player.characterClass.toUpperCase()}] CẤP: ${this.player.stats.level} (TIÊN PHONG)`);

    this.lifeBarGfx.fillStyle(0x000000, 0.7);
    this.lifeBarGfx.fillRect(x, y, barW, barH);
    const lifePct = Math.max(0, this.player.stats.currentLife / this.player.stats.maxLife);
    this.lifeBarGfx.fillStyle(0xdc143c, 1);
    this.lifeBarGfx.fillRect(x, y, barW * lifePct, barH);

    if (this.player.stats.maxEnergyShield > 0) {
      const esPct = Math.max(0, this.player.stats.energyShield / this.player.stats.maxEnergyShield);
      this.esBarGfx.fillStyle(0x1e90ff, 0.9);
      this.esBarGfx.fillRect(x, y - 8, barW * esPct, 6);
    }

    const expW = this.scale.width;
    const expPct = Math.max(0, this.player.stats.currentExp / this.player.stats.maxExp);
    this.expBarGfx.fillStyle(0x1e293b, 0.9);
    this.expBarGfx.fillRect(0, this.scale.height - 8, expW, 8);
    this.expBarGfx.fillStyle(0x38bdf8, 1);
    this.expBarGfx.fillRect(0, this.scale.height - 8, expW * expPct, 8);

    let qStr = '❖ NHIỆM VỤ ĐANG LÀM:\\n';
    this.questManager.activeQuests.forEach((q) => {
      const status = q.isCompleted ? '✓ XONG' : `${q.current}/${q.target}`;
      qStr += `• ${q.title}: ${status}\\n`;
    });
    this.questTrackerText.setText(qStr);

    this.skillSlotWidgets.forEach((w) => {
      w.cdGfx.clear();
      const cdPct = this.player.getCooldownPercent(w.id, time);
      if (cdPct > 0) {
        w.cdGfx.fillStyle(0x000000, 0.65);
        w.cdGfx.fillRect(w.bg.x - 26, w.bg.y - 26 + 52 * (1 - cdPct), 52, 52 * cdPct);
      }
    });
  }

  private spawnMonsterWave(): void {
    if (
      this.isGameOver || 
      !this.waveManager.isWaveActive || 
      this.intermissionUI.getIsShowing() ||
      this.craftingUI.getIsOpen() ||
      this.passiveTreeUI.getIsOpen() ||
      this.characterUI.getIsOpen() ||
      this.levelUpUI.getIsShowing()
    ) {
      return;
    }

    const count = 3 + Math.floor(Math.random() * 3);
    const cam = this.cameras.main;

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const dist = Math.max(cam.width, cam.height) * 0.7;
      const spawnX = this.player.x + Math.cos(angle) * dist;
      const spawnY = this.player.y + Math.sin(angle) * dist;

      let monster = this.monsterPool.getFirstDead(false) as Monster;
      if (!monster) {
        monster = new Monster(this, spawnX, spawnY);
        this.monsterPool.add(monster);
      }

      const stats = this.waveManager.getMonsterStats(this.waveManager.currentWave);
      monster.spawn(spawnX, spawnY, stats);
    }
  }

  private tickWaveTimer(): void {
    if (this.isGameOver || this.intermissionUI.getIsShowing() || this.levelUpUI.getIsShowing()) return;

    this.waveManager.timeRemaining--;
    this.timerText.setText(`THỜI GIAN: ${this.waveManager.timeRemaining}s`);

    if (this.waveManager.timeRemaining <= 0) {
      this.waveManager.isWaveActive = false;

      if (this.waveManager.currentWave > this.bestWave) {
        this.bestWave = this.waveManager.currentWave;
        localStorage.setItem('poe_roguelike_best_wave', this.bestWave.toString());
        this.bestWaveText.setText(`KỶ LỤC: ĐỢT ${this.bestWave}`);
      }

      this.monsterPool.children.each((child) => {
        const mon = child as Monster;
        if (mon.active) mon.kill();
        return true;
      });

      SoundEffects.playWaveClear();

      this.passiveTreeManager.unspentPoints++;
      this.player.stats.currentLife = this.player.stats.maxLife;
      this.player.stats.energyShield = this.player.stats.maxEnergyShield;

      this.intermissionUI.show(this.waveManager.currentWave);
    }
  }

  private startNextWave(): void {
    this.intermissionUI.hide();
    this.waveManager.currentWave++;
    this.waveManager.timeRemaining = this.waveManager.waveDuration;
    this.waveManager.isWaveActive = true;
    this.waveText.setText(`ĐỢT: ${this.waveManager.currentWave}`);
  }

  private triggerGameOver(): void {
    this.isGameOver = true;
    this.player.setTint(0x555555);

    const overText = this.add.text(
      this.scale.width / 2,
      this.scale.height / 2,
      'BẠN ĐÃ TỬ NẠN!\\nNhấn [SPACE] để Hồi Sinh',
      {
        fontFamily: 'monospace',
        fontSize: '32px',
        fontStyle: 'bold',
        color: '#ff0000',
        align: 'center',
        backgroundColor: '#000000ee',
        padding: { x: 20, y: 15 },
      }
    ).setOrigin(0.5).setScrollFactor(0);

    this.input.keyboard?.once('keydown-SPACE', () => {
      overText.destroy();
      this.scene.restart();
    });
  }

  update(time: number, delta: number): void {
    if (this.isGameOver) return;

    const isUIBlocking = 
      this.intermissionUI.getIsShowing() || 
      this.craftingUI.getIsOpen() || 
      this.passiveTreeUI.getIsOpen() ||
      this.characterUI.getIsOpen() ||
      this.levelUpUI.getIsShowing();

    if (isUIBlocking) {
      const body = this.player.body as Phaser.Physics.Arcade.Body;
      if (body) body.setVelocity(0, 0);
      return;
    }

    this.player.update(time, delta);
    this.renderHUD(time);

    this.performAutoAttack(time);
    this.performAutoLoot();

    this.monsterPool.children.each((child) => {
      const mon = child as Monster;
      if (mon.active) {
        mon.updateAI(this.player.x, this.player.y);
      }
      return true;
    });

    const pointer = this.input.activePointer;
    if (pointer.isDown && !this.isHoveringInteractiveUI) {
      const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
      this.player.tryCastSkills(time, worldPoint.x, worldPoint.y, this.projectilePool);
      SoundEffects.playCast();
    }
  }
}
'''
}

# ĐẢM BẢO TẠO THƯ MỤC CHA TRƯỚC KHI GHI FILE ĐỂ KHÔNG BAO GIỜ BỊ LỖI FILENOTFOUNDERROR
for path, content in files.items():
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Đã cập nhật thành công: {path}")

print("\nHoàn tất nâng cấp: Sửa lỗi thư mục, Hệ thống 10 Ô Trang Bị Chuẩn ARPG, Auto Attack/Loot & Quests!")