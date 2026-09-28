import os

files = {
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
}
''',

    "src/core/items/AffixPool.ts": '''import { AffixDefinition } from './ItemTypes';

export const PREFIX_POOL: AffixDefinition[] = [
  {
    id: 'p_flat_dmg',
    name: 'Heavy',
    type: 'prefix',
    statType: 'added_damage',
    minValue: 5,
    maxValue: 18,
  },
  {
    id: 'p_inc_dmg',
    name: 'Flashing',
    type: 'prefix',
    statType: 'inc_damage',
    minValue: 15,
    maxValue: 45,
  },
  {
    id: 'p_flat_life',
    name: 'Robust',
    type: 'prefix',
    statType: 'flat_life',
    minValue: 20,
    maxValue: 60,
  },
  {
    id: 'p_flat_es',
    name: 'Blinking',
    type: 'prefix',
    statType: 'flat_es',
    minValue: 15,
    maxValue: 40,
  },
];

export const SUFFIX_POOL: AffixDefinition[] = [
  {
    id: 's_atk_speed',
    name: 'of Velocity',
    type: 'suffix',
    statType: 'attack_speed',
    minValue: 10,
    maxValue: 25,
  },
  {
    id: 's_move_speed',
    name: 'of the Wind',
    type: 'suffix',
    statType: 'movement_speed',
    minValue: 15,
    maxValue: 35,
  },
  {
    id: 's_armour',
    name: 'of the Iron',
    type: 'suffix',
    statType: 'armour',
    minValue: 25,
    maxValue: 70,
  },
  {
    id: 's_crit',
    name: 'of Piercing',
    type: 'suffix',
    statType: 'crit_chance',
    minValue: 4,
    maxValue: 10,
  },
];
''',

    "src/core/crafting/CraftingEngine.ts": '''import { EquipmentItem, CurrencyType, AffixInstance, AffixDefinition } from '../items/ItemTypes';
import { PREFIX_POOL, SUFFIX_POOL } from '../items/AffixPool';

export class CraftingEngine {
  private static rollAffix(def: AffixDefinition): AffixInstance {
    const val = Math.floor(def.minValue + Math.random() * (def.maxValue - def.minValue + 1));
    return {
      definitionId: def.id,
      name: def.name,
      type: def.type,
      statType: def.statType,
      value: val,
    };
  }

  private static getRandomAvailable(pool: AffixDefinition[], current: AffixInstance[]): AffixDefinition | null {
    const existingIds = new Set(current.map((a) => a.definitionId));
    const available = pool.filter((p) => !existingIds.has(p.id));
    if (available.length === 0) return null;
    return available[Math.floor(Math.random() * available.length)];
  }

  // Orb of Transmutation: Normal -> Magic (1-2 affixes)
  public static applyTransmutation(item: EquipmentItem): boolean {
    if (item.rarity !== 'Normal') return false;
    item.rarity = 'Magic';
    item.prefixes = [];
    item.suffixes = [];

    const rollP = Math.random() < 0.6;
    const rollS = Math.random() < 0.6 || !rollP;

    if (rollP) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    if (rollS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Orb of Alteration: Reroll Magic item
  public static applyAlteration(item: EquipmentItem): boolean {
    if (item.rarity !== 'Magic') return false;
    item.prefixes = [];
    item.suffixes = [];

    const rollP = Math.random() < 0.6;
    const rollS = Math.random() < 0.6 || !rollP;

    if (rollP) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    if (rollS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Regal Orb: Magic -> Rare (giữ mod cũ, thêm 1 mod mới)
  public static applyRegal(item: EquipmentItem): boolean {
    if (item.rarity !== 'Magic') return false;
    item.rarity = 'Rare';

    const canAddP = item.prefixes.length < 3;
    const canAddS = item.suffixes.length < 3;

    if (canAddP && (Math.random() < 0.5 || !canAddS)) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    } else if (canAddS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Chaos Orb: Reroll Rare item (1-3 Prefixes, 1-3 Suffixes)
  public static applyChaos(item: EquipmentItem): boolean {
    if (item.rarity !== 'Rare') return false;
    item.prefixes = [];
    item.suffixes = [];

    const pCount = 1 + Math.floor(Math.random() * 3);
    const sCount = 1 + Math.floor(Math.random() * 3);

    for (let i = 0; i < pCount; i++) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) item.prefixes.push(this.rollAffix(def));
    }
    for (let i = 0; i < sCount; i++) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) item.suffixes.push(this.rollAffix(def));
    }
    return true;
  }

  // Exalted Orb: Thêm 1 affix vào Rare nếu chưa đủ 6
  public static applyExalted(item: EquipmentItem): boolean {
    if (item.rarity !== 'Rare') return false;
    const canAddP = item.prefixes.length < 3;
    const canAddS = item.suffixes.length < 3;
    if (!canAddP && !canAddS) return false;

    if (canAddP && (Math.random() < 0.5 || !canAddS)) {
      const def = this.getRandomAvailable(PREFIX_POOL, item.prefixes);
      if (def) {
        item.prefixes.push(this.rollAffix(def));
        return true;
      }
    } else if (canAddS) {
      const def = this.getRandomAvailable(SUFFIX_POOL, item.suffixes);
      if (def) {
        item.suffixes.push(this.rollAffix(def));
        return true;
      }
    }
    return false;
  }

  // Orb of Scouring: Về Normal, xóa hết Affix
  public static applyScouring(item: EquipmentItem): boolean {
    if (item.rarity === 'Normal') return false;
    item.rarity = 'Normal';
    item.prefixes = [];
    item.suffixes = [];
    return true;
  }

  public static applyCurrency(type: CurrencyType, item: EquipmentItem): boolean {
    switch (type) {
      case 'transmutation': return this.applyTransmutation(item);
      case 'alteration': return this.applyAlteration(item);
      case 'regal': return this.applyRegal(item);
      case 'chaos': return this.applyChaos(item);
      case 'exalted': return this.applyExalted(item);
      case 'scouring': return this.applyScouring(item);
      default: return false;
    }
  }
}
''',

    "src/core/loot/LootEngine.ts": '''import { CurrencyType } from '../items/ItemTypes';
import { MonsterRarity } from '../monsters/MonsterTypes';

export interface DropResult {
  type: 'currency';
  currencyType: CurrencyType;
  name: string;
}

export class LootEngine {
  public static rollMonsterDrops(rarity: MonsterRarity): DropResult[] {
    const drops: DropResult[] = [];
    const roll = Math.random();

    // Tỉ lệ rơi dựa trên độ hiếm của quái
    let dropChance = 0.25; // Normal: 25% rơi 1 orb
    if (rarity === 'Magic') dropChance = 0.55;
    if (rarity === 'Rare') dropChance = 0.95;
    if (rarity === 'Boss') dropChance = 1.0;

    if (roll > dropChance) return drops;

    const numDrops = rarity === 'Boss' ? 3 : rarity === 'Rare' ? 2 : 1;

    for (let i = 0; i < numDrops; i++) {
      const cRoll = Math.random() * 100;
      let cur: CurrencyType = 'transmutation';
      let name = 'Orb of Transmutation';

      if (cRoll < 3 && (rarity === 'Rare' || rarity === 'Boss')) {
        cur = 'exalted';
        name = 'Exalted Orb';
      } else if (cRoll < 18 && (rarity === 'Magic' || rarity === 'Rare' || rarity === 'Boss')) {
        cur = 'chaos';
        name = 'Chaos Orb';
      } else if (cRoll < 35) {
        cur = 'regal';
        name = 'Regal Orb';
      } else if (cRoll < 60) {
        cur = 'scouring';
        name = 'Orb of Scouring';
      } else if (cRoll < 80) {
        cur = 'alteration';
        name = 'Orb of Alteration';
      }

      drops.push({ type: 'currency', currencyType: cur, name });
    }

    return drops;
  }
}
''',

    "src/scenes/LootDrop.ts": '''import Phaser from 'phaser';
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
''',

    "src/scenes/CraftingUI.ts": '''import Phaser from 'phaser';
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

    // Cập nhật số lượng trên các nút bấm
    this.currencyButtons.forEach((btn, type) => {
      const count = this.inventoryData.currencies[type] || 0;
      const label = `${type.toUpperCase()}\\n(Còn: ${count})`;
      btn.setText(label);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
''',

    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquipmentItem } from '../core/items/ItemTypes';
import { Projectile } from './Projectile';

export class Player extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  public characterClass: CharacterClass;
  public sockets: Socket[] = [];
  public compiledSkills: SkillContext[] = [];

  private cursors: Phaser.Types.Input.Keyboard.CursorKeys;
  private keyW!: Phaser.Input.Keyboard.Key;
  private keyA!: Phaser.Input.Keyboard.Key;
  private keyS!: Phaser.Input.Keyboard.Key;
  private keyD!: Phaser.Input.Keyboard.Key;
  private lastCastTime: number = 0;
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
    } else {
      throw new Error('Keyboard plugin không khả dụng.');
    }

    this.setupDefaultGems();
    this.compileSkills();
  }

  private setupDefaultGems(): void {
    if (this.characterClass === 'Mage') {
      this.sockets = [
        { color: 'blue', linkGroup: 1, gem: FireballSkill },
        { color: 'green', linkGroup: 1, gem: GreaterMultipleProjectiles },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
    } else {
      this.sockets = [
        { color: 'green', linkGroup: 1, gem: SplitArrowSkill },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
    }
  }

  public applyEquippedItemStats(item: EquipmentItem): void {
    const base = CLASS_BASE_STATS[this.characterClass];
    this.stats.armour = base.armour;
    this.stats.movementSpeed = base.movementSpeed;
    this.stats.maxLife = base.maxLife;
    this.stats.maxEnergyShield = base.maxEnergyShield;

    const allAffixes = [...item.prefixes, ...item.suffixes];
    for (const aff of allAffixes) {
      if (aff.statType === 'flat_life') this.stats.maxLife += aff.value;
      if (aff.statType === 'flat_es') this.stats.maxEnergyShield += aff.value;
      if (aff.statType === 'armour') this.stats.armour += aff.value;
      if (aff.statType === 'movement_speed') this.stats.movementSpeed += aff.value;
    }

    this.stats.currentLife = Math.min(this.stats.currentLife, this.stats.maxLife);
    this.compileSkills(item);
  }

  public compileSkills(equippedItem?: EquipmentItem): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    let addedDmg = 0;
    let incDmg = 0;
    let atkSpeedPct = 0;
    let critChance = 0;

    if (equippedItem) {
      const allAff = [...equippedItem.prefixes, ...equippedItem.suffixes];
      for (const a of allAff) {
        if (a.statType === 'added_damage') addedDmg += a.value;
        if (a.statType === 'inc_damage') incDmg += a.value;
        if (a.statType === 'attack_speed') atkSpeedPct += a.value;
        if (a.statType === 'crit_chance') critChance += a.value;
      }
    }

    for (const activeSock of activeSockets) {
      const activeGem = activeSock.gem as ActiveGem;
      const ctx = activeGem.getInitialContext();

      ctx.addedMinDamage += addedDmg;
      ctx.addedMaxDamage += addedDmg;
      ctx.increasedDamagePercent += incDmg;
      ctx.attackSpeedMultiplier *= (1 + atkSpeedPct / 100);
      ctx.critChance += critChance;

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
    const skill = this.compiledSkills[0];

    const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
    if (time - this.lastCastTime < cooldown) return;

    this.lastCastTime = time;

    const baseAngle = Phaser.Math.Angle.Between(this.x, this.y, targetX, targetY);
    const count = skill.projectileCount;
    const spreadAngle = 0.15;

    for (let i = 0; i < count; i++) {
      const p = projectilePool.get(this.x, this.y) as Projectile;
      if (!p) continue;

      const offset = (i - (count - 1) / 2) * spreadAngle;
      p.fire(this.x, this.y, baseAngle + offset, skill);
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

    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { Monster } from './Monster';
import { LootDrop } from './LootDrop';
import { CraftingUI } from './CraftingUI';
import { WaveManager } from '../core/monsters/WaveManager';
import { DamageEngine } from '../core/combat/DamageEngine';
import { LootEngine } from '../core/loot/LootEngine';
import { InventoryData } from '../core/items/ItemTypes';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private monsterPool!: Phaser.Physics.Arcade.Group;
  private lootPool!: Phaser.Physics.Arcade.Group;
  private waveManager: WaveManager = new WaveManager();

  private craftingUI!: CraftingUI;
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
      id: 'eq_1',
      name: 'Vũ khí Sắt',
      baseType: 'Sword',
      rarity: 'Normal',
      prefixes: [],
      suffixes: [],
    },
  };

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
  private invHintText!: Phaser.GameObjects.Text;
  private lifeBarGfx!: Phaser.GameObjects.Graphics;
  private esBarGfx!: Phaser.GameObjects.Graphics;
  private isGameOver: boolean = false;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2400;
    const mapHeight = 2400;

    this.isGameOver = false;
    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    this.createProceduralTextures();

    // Map nền
    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');
    this.player.applyEquippedItemStats(this.inventoryData.equippedItem);

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    // Object Pools
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

      CombatUI.showDamageText(this, monster.x, monster.y, hit);

      if (isDead) {
        this.dropLoot(monster.x, monster.y, monster.monsterStats.rarity);
        monster.kill();
      }

      if (proj.remainingPierce > 0) {
        proj.remainingPierce--;
      } else {
        proj.kill();
      }
    });

    // Va chạm: Người chơi -> Nhặt Loot
    this.physics.add.overlap(this.player, this.lootPool, (_playerObj, lootObj) => {
      const loot = lootObj as LootDrop;
      if (!loot.active) return;

      const curType = loot.collect();
      this.inventoryData.currencies[curType] = (this.inventoryData.currencies[curType] || 0) + 1;
      this.showPickupNotice(loot.x, loot.y, curType);
    });

    // Va chạm: Quái -> Người chơi
    this.physics.add.overlap(this.player, this.monsterPool, (_playerObj, monObj) => {
      if (this.isGameOver) return;
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

    // Khởi tạo Crafting UI
    this.craftingUI = new CraftingUI(this, this.inventoryData, () => {
      this.player.applyEquippedItemStats(this.inventoryData.equippedItem);
    });

    // Phím [I] mở Hòm đồ / Crafting
    this.input.keyboard?.on('keydown-I', () => {
      this.craftingUI.toggle();
    });

    // Spawner
    this.time.addEvent({
      delay: 1200,
      callback: this.spawnMonsterWave,
      callbackScope: this,
      loop: true,
    });

    // Timer Wave
    this.time.addEvent({
      delay: 1000,
      callback: this.tickWaveTimer,
      callbackScope: this,
      loop: true,
    });
  }

  private dropLoot(x: number, y: number, rarity: any): void {
    const drops = LootEngine.rollMonsterDrops(rarity);
    drops.forEach((d) => {
      let loot = this.lootPool.getFirstDead(false) as LootDrop;
      if (!loot) {
        loot = new LootDrop(this, x, y);
        this.lootPool.add(loot);
      }
      loot.spawn(x + (Math.random() * 30 - 15), y + (Math.random() * 30 - 15), d.currencyType, d.name);
    });
  }

  private showPickupNotice(x: number, y: number, cur: string): void {
    const t = this.add.text(x, y - 20, `+1 ${cur.toUpperCase()}`, {
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
    const list: { key: string; color: number }[] = [
      { key: 'monster_normal', color: 0x8b0000 },
      { key: 'monster_magic', color: 0x4169e1 },
      { key: 'monster_rare', color: 0xffd700 },
      { key: 'monster_boss', color: 0x9400d3 },
    ];

    list.forEach((item) => {
      if (!this.textures.exists(item.key)) {
        const g = this.make.graphics({ x: 0, y: 0 });
        g.fillStyle(item.color, 1);
        g.fillRect(0, 0, 32, 32);
        g.lineStyle(2, 0xffffff, 0.7);
        g.strokeRect(0, 0, 32, 32);
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

    this.invHintText = this.add.text(20, 76, '[I]: HÒM ĐỒ & CHẾ ĐỒ (CRAFT)', {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#ffd700',
      backgroundColor: '#000000aa',
      padding: { x: 6, y: 4 },
    }).setScrollFactor(0);

    this.lifeBarGfx = this.add.graphics().setScrollFactor(0);
    this.esBarGfx = this.add.graphics().setScrollFactor(0);
  }

  private renderHUD(): void {
    this.lifeBarGfx.clear();
    this.esBarGfx.clear();

    const barW = 200;
    const barH = 16;
    const x = 20;
    const y = this.scale.height - 40;

    this.lifeBarGfx.fillStyle(0x000000, 0.7);
    this.lifeBarGfx.fillRect(x, y, barW, barH);

    const lifePct = Math.max(0, this.player.stats.currentLife / this.player.stats.maxLife);
    this.lifeBarGfx.fillStyle(0xdc143c, 1);
    this.lifeBarGfx.fillRect(x, y, barW * lifePct, barH);

    if (this.player.stats.maxEnergyShield > 0) {
      const esPct = Math.max(0, this.player.stats.energyShield / this.player.stats.maxEnergyShield);
      this.esBarGfx.fillStyle(0x1e90ff, 0.85);
      this.esBarGfx.fillRect(x, y - 8, barW * esPct, 6);
    }
  }

  private spawnMonsterWave(): void {
    if (this.isGameOver || !this.waveManager.isWaveActive || this.craftingUI.getIsOpen()) return;

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
    if (this.isGameOver || this.craftingUI.getIsOpen()) return;

    this.waveManager.timeRemaining--;
    this.timerText.setText(`THỜI GIAN: ${this.waveManager.timeRemaining}s`);

    if (this.waveManager.timeRemaining <= 0) {
      this.waveManager.currentWave++;
      this.waveManager.timeRemaining = this.waveManager.waveDuration;
      this.waveText.setText(`ĐỢT: ${this.waveManager.currentWave}`);

      this.monsterPool.children.each((child) => {
        const mon = child as Monster;
        if (mon.active) mon.kill();
        return true;
      });
    }
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

    // Khi đang mở bảng Crafting thì tạm dừng di chuyển và tấn công
    if (this.craftingUI.getIsOpen()) {
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
    if (pointer.isDown) {
      const worldPoint = this.cameras.main.getWorldPoint(pointer.x, pointer.y);
      this.player.tryCastSkills(time, worldPoint.x, worldPoint.y, this.projectilePool);
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
    print(f"Cập nhật thành công: {path}")

print("\nHoàn tất cài đặt Giai đoạn 4: Itemization, Drop Tables & Currency Crafting!")