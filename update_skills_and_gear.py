import os

files = {
    # 1. Bổ sung cấu trúc Túi đồ (bag) vào ItemTypes.ts
    "src/core/items/ItemTypes.ts": '''export type ItemRarity = 'Normal' | 'Magic' | 'Rare';

export type CurrencyType = 
  | 'transmutation' 
  | 'alteration' 
  | 'regal' 
  | 'chaos' 
  | 'exalted' 
  | 'scouring';

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
  baseType: 'Sword' | 'Bow' | 'Wand' | 'Plate';
  rarity: ItemRarity;
  prefixes: AffixInstance[];
  suffixes: AffixInstance[];
}

export interface InventoryData {
  currencies: Record<CurrencyType, number>;
  equippedItem: EquipmentItem;
  bag: EquipmentItem[]; // Túi đồ chứa các trang bị nhặt được
}
''',

    # 2. Thêm cấp bậc và các kỹ năng mới vào ActiveGems.ts
    "src/core/gems/ActiveGems.ts": '''import { ActiveGem, SkillContext } from './GemTypes';

export const FireballSkill: ActiveGem = {
  id: 'fireball',
  name: 'Fireball (Hỏa Cầu)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'fireball',
    name: 'Fireball',
    damageType: 'fire',
    baseMinDamage: 28,
    baseMaxDamage: 45,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.0,
    baseCooldown: 700,
    projectileCount: 1,
    projectileSpeed: 380,
    pierceCount: 0,
    aoeRadius: 45,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const SplitArrowSkill: ActiveGem = {
  id: 'split_arrow',
  name: 'Split Arrow (Tên Rẽ)',
  color: 'green',
  getInitialContext: (): SkillContext => ({
    id: 'split_arrow',
    name: 'Split Arrow',
    damageType: 'physical',
    baseMinDamage: 18,
    baseMaxDamage: 32,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.25,
    baseCooldown: 500,
    projectileCount: 3,
    projectileSpeed: 520,
    pierceCount: 0,
    aoeRadius: 0,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const GroundSlamSkill: ActiveGem = {
  id: 'ground_slam',
  name: 'Ground Slam (Địa Chấn)',
  color: 'red',
  getInitialContext: (): SkillContext => ({
    id: 'ground_slam',
    name: 'Ground Slam',
    damageType: 'physical',
    baseMinDamage: 45,
    baseMaxDamage: 80,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.85,
    baseCooldown: 900,
    projectileCount: 1,
    projectileSpeed: 240,
    pierceCount: 99,
    aoeRadius: 75,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 1: BĂNG CẦU XUYÊN THẤU
export const FrostboltSkill: ActiveGem = {
  id: 'frostbolt',
  name: 'Frostbolt (Băng Cầu)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'frostbolt',
    name: 'Frostbolt',
    damageType: 'cold',
    baseMinDamage: 32,
    baseMaxDamage: 52,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.95,
    baseCooldown: 650,
    projectileCount: 1,
    projectileSpeed: 300,
    pierceCount: 99, // Xuyên thấu toàn bộ quái trên đường bay
    aoeRadius: 30,
    critChance: 7,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 2: TIA SÉT TÁN XẠ
export const SparkSkill: ActiveGem = {
  id: 'spark',
  name: 'Spark (Tia Sét)',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'spark',
    name: 'Spark',
    damageType: 'lightning',
    baseMinDamage: 12,
    baseMaxDamage: 48,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.4,
    baseCooldown: 550,
    projectileCount: 4,
    projectileSpeed: 450,
    pierceCount: 1,
    aoeRadius: 0,
    critChance: 8,
    critMultiplier: 1.6,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

// KỸ NĂNG MỚI 3: LƯỠI KIẾM XOAY VÒNG QUANH THÂN
export const BladeVortexSkill: ActiveGem = {
  id: 'blade_vortex',
  name: 'Blade Vortex (Bão Kiếm)',
  color: 'green',
  getInitialContext: (): SkillContext => ({
    id: 'blade_vortex',
    name: 'Blade Vortex',
    damageType: 'physical',
    baseMinDamage: 15,
    baseMaxDamage: 25,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 2.0,
    baseCooldown: 300,
    projectileCount: 3,
    projectileSpeed: 180,
    pierceCount: 99,
    aoeRadius: 40,
    critChance: 6,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};

export const ALL_ACTIVE_SKILLS: Record<string, ActiveGem> = {
  fireball: FireballSkill,
  split_arrow: SplitArrowSkill,
  ground_slam: GroundSlamSkill,
  frostbolt: FrostboltSkill,
  spark: SparkSkill,
  blade_vortex: BladeVortexSkill,
};
''',

    # 3. Tạo Giao Diện Lên Cấp Chọn Thẻ Nâng Cấp Kỹ Năng (LevelUpUI.ts)
    "src/scenes/LevelUpUI.ts": '''import Phaser from 'phaser';

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
''',

    # 4. Cập nhật CraftingUI.ts: Cho phép soi và BẤM [MẶC ĐỒ] từ Túi Đồ
    "src/scenes/CraftingUI.ts": '''import Phaser from 'phaser';
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

    let sockStr = '❖ LỖ NGỌC & LIÊN KẾT:\\n';
    this.player.sockets.forEach((s, idx) => {
      const gemName = s.gem ? s.gem.name : '(Trống)';
      sockStr += `  • Ô ${idx + 1} [Nhóm ${s.linkGroup} - ${s.color.toUpperCase()}]: ${gemName}\\n`;
    });
    this.socketsText.setText(sockStr);

    let affStr = '--- PREFIXES ---\\n';
    if (item.prefixes.length === 0) affStr += '(Trống)\\n';
    item.prefixes.forEach((p) => {
      affStr += `• ${p.name}: +${p.value} (${p.statType})\\n`;
    });

    affStr += '\\n--- SUFFIXES ---\\n';
    if (item.suffixes.length === 0) affStr += '(Trống)\\n';
    item.suffixes.forEach((s) => {
      affStr += `• ${s.name}: +${s.value} (${s.statType})\\n`;
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
      btn.setText(`${type.toUpperCase()}\\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
''',

    # 5. Cập nhật Player.ts: Hỗ trợ thi triển đồng thời nhiều Kỹ Năng & Nâng Cấp Level Kỹ Năng
    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats, getExpNeeded } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill, GroundSlamSkill, ALL_ACTIVE_SKILLS } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquipmentItem } from '../core/items/ItemTypes';
import { PassiveTreeBonus } from '../core/passive/PassiveTreeTypes';
import { Projectile } from './Projectile';

export class Player extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  public characterClass: CharacterClass;
  public sockets: Socket[] = [];
  public compiledSkills: SkillContext[] = [];

  // Theo dõi thời gian hồi riêng cho từng kỹ năng (cho phép bắn đa kỹ năng)
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
    } else if (this.characterClass === 'Archer') {
      this.sockets = [
        { color: 'green', linkGroup: 1, gem: SplitArrowSkill },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
    } else {
      this.sockets = [
        { color: 'red', linkGroup: 1, gem: GroundSlamSkill },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
      ];
    }
  }

  // THÊM HOẶC NÂNG CẤP KỸ NĂNG
  public addOrUpgradeSkill(skillId: string): void {
    const existing = this.sockets.find((s) => s.gem && s.gem.id === skillId);
    if (existing) {
      // Đã có -> Tăng level kỹ năng
      const curLvl = this.skillBonusLevels.get(skillId) || 1;
      this.skillBonusLevels.set(skillId, curLvl + 1);
    } else {
      // Chưa có -> Gắn vào một Socket mới
      const newGem = ALL_ACTIVE_SKILLS[skillId];
      if (newGem) {
        this.sockets.push({
          color: newGem.color,
          linkGroup: this.sockets.length + 1,
          gem: newGem,
        });
        this.skillBonusLevels.set(skillId, 1);
      }
    }
    this.compileSkills();
  }

  public gainExp(amount: number): boolean {
    this.stats.currentExp += amount;
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

  public recalculateTotalStats(item: EquipmentItem, treeBonus: PassiveTreeBonus): void {
    const base = CLASS_BASE_STATS[this.characterClass];
    const levelBonusLife = (this.stats.level - 1) * 15;
    const levelBonusES = (this.stats.level - 1) * 10;

    this.stats.maxLife = base.maxLife + levelBonusLife + treeBonus.flatLife;
    this.stats.maxEnergyShield = base.maxEnergyShield + (base.maxEnergyShield > 0 ? levelBonusES : 0) + treeBonus.flatES;
    this.stats.armour = base.armour + treeBonus.flatArmour;
    this.stats.evasion = base.evasion + treeBonus.flatEvasion;
    this.stats.movementSpeed = base.movementSpeed + treeBonus.movementSpeed;

    // Chỉ số từ trang bị mặc trên người
    const allAffixes = [...item.prefixes, ...item.suffixes];
    for (const aff of allAffixes) {
      if (aff.statType === 'flat_life') this.stats.maxLife += aff.value;
      if (aff.statType === 'flat_es') this.stats.maxEnergyShield += aff.value;
      if (aff.statType === 'armour') this.stats.armour += aff.value;
      if (aff.statType === 'movement_speed') this.stats.movementSpeed += aff.value;
    }

    this.stats.currentLife = Math.min(this.stats.currentLife, this.stats.maxLife);
    this.compileSkills(item, treeBonus);
  }

  public compileSkills(equippedItem?: EquipmentItem, treeBonus?: PassiveTreeBonus): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    let addedDmg = 0;
    let incDmg = 0;
    let atkSpeedPct = 0;
    let critChance = 0;
    let critMultiplier = 0;
    let extraProj = 0;
    let extraPierce = 0;

    if (equippedItem) {
      const allAff = [...equippedItem.prefixes, ...equippedItem.suffixes];
      for (const a of allAff) {
        if (a.statType === 'added_damage') addedDmg += a.value;
        if (a.statType === 'inc_damage') incDmg += a.value;
        if (a.statType === 'attack_speed') atkSpeedPct += a.value;
        if (a.statType === 'crit_chance') critChance += a.value;
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
      const ctx = activeGem.getInitialContext();

      // Bonus từ Level kỹ năng: Mỗi cấp tăng 20% sát thương
      const sLvl = this.skillBonusLevels.get(ctx.id) || 1;
      if (sLvl > 1) {
        ctx.increasedDamagePercent += (sLvl - 1) * 20;
      }

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

  // BẮN TOÀN BỘ CÁC KỸ NĂNG ĐƯỢC TRANG BỊ THEO COOLDOWN ĐỘC LẬP
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

    # 6. Cập nhật BattleScene.ts: Kết nối Nhặt Đồ vào Túi & Bật LevelUpUI khi thăng cấp
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
    equippedItem: {
      id: 'eq_starter',
      name: 'Vũ khí Sắt Tập Sự',
      baseType: 'Sword',
      rarity: 'Normal',
      prefixes: [],
      suffixes: [],
    },
    bag: [], // Bắt đầu với túi rỗng
  };

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
  private bestWaveText!: Phaser.GameObjects.Text;
  private classLevelText!: Phaser.GameObjects.Text;
  private lifeBarGfx!: Phaser.GameObjects.Graphics;
  private esBarGfx!: Phaser.GameObjects.Graphics;
  private expBarGfx!: Phaser.GameObjects.Graphics;
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

    // Map sàn
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

      if (isDead) {
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

    // Va chạm: Nhặt đồ (Cho phép nhặt vào Túi đồ Bag)
    this.physics.add.overlap(this.player, this.lootPool, (_playerObj, lootObj) => {
      const loot = lootObj as LootDrop;
      if (!loot.active) return;

      const d = loot.collect();
      if (d.category === 'currency' && d.currencyType) {
        this.inventoryData.currencies[d.currencyType] = (this.inventoryData.currencies[d.currencyType] || 0) + 1;
        this.showPickupNotice(loot.x, loot.y, d.currencyType.toUpperCase());
      } else if (d.category === 'equipment' && d.equipmentItem) {
        if (this.inventoryData.bag.length < 6) {
          this.inventoryData.bag.push(d.equipmentItem);
          this.showPickupNotice(loot.x, loot.y, `TÚI: ${d.name}`);
        } else {
          this.showPickupNotice(loot.x, loot.y, `TÚI ĐỒ ĐÃ ĐẦY!`);
        }
      } else if (d.category === 'gem') {
        this.showPickupNotice(loot.x, loot.y, `NHẶT: ${d.name}`);
      }
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

    // Phím tắt
    this.input.keyboard?.on('keydown-C', () => this.characterUI.toggle());
    this.input.keyboard?.on('keydown-I', () => this.craftingUI.toggle());
    this.input.keyboard?.on('keydown-P', () => this.passiveTreeUI.toggle());
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

  // TẠO 3 LỰA CHỌN KHI LÊN CẤP
  private triggerLevelUpChoiceModal(): void {
    SoundEffects.playWaveClear();
    this.passiveTreeManager.unspentPoints++;

    const pool: LevelUpChoice[] = [
      {
        id: 'frostbolt',
        title: 'Băng Cầu (Frostbolt)',
        description: 'Bắn cầu băng xuyên thấu 100% mục tiêu, gây sát thương Băng cao.',
        type: 'new_skill',
        skillId: 'frostbolt',
        apply: () => {
          this.player.addOrUpgradeSkill('frostbolt');
          this.syncPlayerStats();
        },
      },
      {
        id: 'spark',
        title: 'Tia Sét (Spark)',
        description: 'Bắn 4 tia sét giật nhanh tán xạ rộng ra xung quanh.',
        type: 'new_skill',
        skillId: 'spark',
        apply: () => {
          this.player.addOrUpgradeSkill('spark');
          this.syncPlayerStats();
        },
      },
      {
        id: 'blade_vortex',
        title: 'Bão Kiếm (Blade Vortex)',
        description: 'Tạo các lưỡi kiếm xoay vòng chém liên tục quái vật áp sát.',
        type: 'new_skill',
        skillId: 'blade_vortex',
        apply: () => {
          this.player.addOrUpgradeSkill('blade_vortex');
          this.syncPlayerStats();
        },
      },
      {
        id: 'fireball_up',
        title: 'Cường Hóa Hỏa Cầu',
        description: '+20% Sát thương và tăng tốc độ bay cho Fireball.',
        type: 'upgrade_skill',
        apply: () => {
          this.player.addOrUpgradeSkill('fireball');
          this.syncPlayerStats();
        },
      },
      {
        id: 'vitality_boost',
        title: 'Thể Lực Bất Bại',
        description: '+40 Máu Tối Đa và +15 Tốc Độ Di Chuyển.',
        type: 'stat_boost',
        apply: () => {
          this.player.stats.maxLife += 40;
          this.player.stats.currentLife = this.player.stats.maxLife;
          this.player.stats.movementSpeed += 15;
          this.syncPlayerStats();
        },
      },
    ];

    // Lấy ngẫu nhiên 3 thẻ khác nhau
    const shuffled = [...pool].sort(() => 0.5 - Math.random());
    const selected3 = shuffled.slice(0, 3);

    this.levelUpUI.show(selected3, () => {
      this.syncPlayerStats();
    });
  }

  private createTopRightActionMenu(): void {
    const rx = this.scale.width - 20;

    const classBtn = this.add.text(rx, 20, '🎭 ĐỔI CLASS', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#a78bfa',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    classBtn.on('pointerdown', () => {
      const classes: ('Mage' | 'Archer' | 'Knight')[] = ['Mage', 'Archer', 'Knight'];
      const nextIdx = (classes.indexOf(this.player.characterClass) + 1) % classes.length;
      this.player.setClass(classes[nextIdx]);
      this.syncPlayerStats();
    });

    const charBtn = this.add.text(rx, 55, '👤 CHỈ SỐ (C)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    charBtn.on('pointerdown', () => this.characterUI.toggle());

    const craftBtn = this.add.text(rx, 90, '⚒️ HÒM ĐỒ & TÚI (I)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#ffd700',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    craftBtn.on('pointerdown', () => this.craftingUI.toggle());

    const treeBtn = this.add.text(rx, 125, '🌲 THIÊN PHÚ (P)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#4ade80',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    treeBtn.on('pointerdown', () => this.passiveTreeUI.toggle());

    [classBtn, charBtn, craftBtn, treeBtn].forEach((btn) => {
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
    this.player.recalculateTotalStats(this.inventoryData.equippedItem, bonus);
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
    // 1. Fireball
    if (!this.textures.exists('proj_fireball')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xef4444, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xfde047, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_fireball', 16, 16);
      g.destroy();
    }

    // 2. Split Arrow
    if (!this.textures.exists('proj_arrow')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x22c55e, 1);
      g.fillRect(0, 5, 14, 2);
      g.fillTriangle(16, 6, 11, 2, 11, 10);
      g.generateTexture('proj_arrow', 16, 12);
      g.destroy();
    }

    // 3. Ground Slam
    if (!this.textures.exists('proj_slam')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xd97706, 0.9);
      g.fillCircle(12, 12, 12);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(12, 12, 6);
      g.generateTexture('proj_slam', 24, 24);
      g.destroy();
    }

    // 4. Frostbolt (Xanh băng)
    if (!this.textures.exists('proj_frostbolt')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x06b6d4, 0.9);
      g.fillCircle(9, 9, 9);
      g.fillStyle(0xe0f2fe, 1);
      g.fillCircle(9, 9, 5);
      g.generateTexture('proj_frostbolt', 18, 18);
      g.destroy();
    }

    // 5. Spark (Tia sét vàng xanh)
    if (!this.textures.exists('proj_spark')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xfacc15, 1);
      g.fillCircle(6, 6, 5);
      g.fillStyle(0x67e8f9, 1);
      g.fillCircle(6, 6, 3);
      g.generateTexture('proj_spark', 12, 12);
      g.destroy();
    }

    // 6. Blade Vortex (Lưỡi kiếm xoay)
    if (!this.textures.exists('proj_blade')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x94a3b8, 1);
      g.fillRect(2, 6, 16, 4);
      g.fillStyle(0xffffff, 1);
      g.fillTriangle(20, 8, 16, 4, 16, 12);
      g.generateTexture('proj_blade', 20, 16);
      g.destroy();
    }

    // Quái vật sắc nét
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

    this.lifeBarGfx = this.add.graphics().setScrollFactor(0);
    this.esBarGfx = this.add.graphics().setScrollFactor(0);
    this.expBarGfx = this.add.graphics().setScrollFactor(0);
  }

  private renderHUD(): void {
    this.lifeBarGfx.clear();
    this.esBarGfx.clear();
    this.expBarGfx.clear();

    const barW = 220;
    const barH = 16;
    const x = 20;
    const y = this.scale.height - 45;

    this.classLevelText.setText(`[${this.player.characterClass.toUpperCase()}] CẤP ĐỘ: ${this.player.stats.level}`);

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
    this.renderHUD();

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

for path, content in files.items():
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Đã cập nhật thành công: {path}")

print("\nHoàn tất tích hợp: Mặc đồ từ Túi, Bổ sung Skill mới, Thăng cấp chọn 3 Thẻ!")