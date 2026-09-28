import os

files = {
    # 1. Thống kê nhân vật: Thêm Cấp độ, EXP, Công thức Lên Cấp
    "src/core/stats/CharacterStats.ts": '''export interface PoEStats {
  level: number;
  currentExp: number;
  maxExp: number;
  maxLife: number;
  currentLife: number;
  energyShield: number;
  maxEnergyShield: number;
  armour: number;
  evasion: number;
  movementSpeed: number;
  esRechargeDelay: number;
}

export type CharacterClass = 'Knight' | 'Archer' | 'Mage';

export const CLASS_BASE_STATS: Record<CharacterClass, PoEStats> = {
  Knight: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 160,
    currentLife: 160,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 60,
    evasion: 5,
    movementSpeed: 165,
    esRechargeDelay: 4,
  },
  Archer: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 100,
    currentLife: 100,
    energyShield: 0,
    maxEnergyShield: 0,
    armour: 15,
    evasion: 70,
    movementSpeed: 215,
    esRechargeDelay: 4,
  },
  Mage: {
    level: 1,
    currentExp: 0,
    maxExp: 100,
    maxLife: 80,
    currentLife: 80,
    energyShield: 85,
    maxEnergyShield: 85,
    armour: 0,
    evasion: 10,
    movementSpeed: 180,
    esRechargeDelay: 3,
  },
};

export function getExpNeeded(level: number): number {
  return Math.floor(100 * Math.pow(1.3, level - 1));
}
''',

    # 2. Cây Nội Tại: Tinh chỉnh tọa độ không bị tràn màn hình
    "src/core/passive/PassiveTreeData.ts": '''import { PassiveNode } from './PassiveTreeTypes';

export const PASSIVE_TREE_NODES: Record<string, PassiveNode> = {
  root: {
    id: 'root',
    name: 'Khởi Điểm Lưu Đày',
    description: 'Nguồn cội sức mạnh của kẻ sống sót.',
    nodeType: 'start',
    branch: 'neutral',
    gridX: 0,
    gridY: -10,
    connections: ['str_1', 'dex_1', 'int_1'],
    modifiers: [],
  },

  // === NHÁNH ĐỎ: SỨC MẠNH ===
  str_1: {
    id: 'str_1',
    name: 'Thân Thể Bất Khuất',
    description: '+30 Máu Tối Đa',
    nodeType: 'small',
    branch: 'strength',
    gridX: -70,
    gridY: -60,
    connections: ['root', 'str_2'],
    modifiers: [{ type: 'flat_life', value: 30 }],
  },
  str_2: {
    id: 'str_2',
    name: 'Tôi Luyện Thiết Giáp',
    description: '+40 Giáp Vật Lý',
    nodeType: 'small',
    branch: 'strength',
    gridX: -140,
    gridY: -100,
    connections: ['str_1', 'str_3'],
    modifiers: [{ type: 'flat_armour', value: 40 }],
  },
  str_3: {
    id: 'str_3',
    name: 'Trảm Kích Hùng Lực',
    description: '+25% Sát Thương Vật Lý',
    nodeType: 'notable',
    branch: 'strength',
    gridX: -210,
    gridY: -130,
    connections: ['str_2', 'str_keystone'],
    modifiers: [{ type: 'inc_phys_damage', value: 25 }],
  },
  str_keystone: {
    id: 'str_keystone',
    name: 'Keystone: Juggernaut',
    description: '+70 Máu Tối Đa, +60 Giáp Vật Lý',
    nodeType: 'keystone',
    branch: 'strength',
    gridX: -280,
    gridY: -150,
    connections: ['str_3'],
    modifiers: [
      { type: 'flat_life', value: 70 },
      { type: 'flat_armour', value: 60 },
    ],
  },

  // === NHÁNH XANH LÁ: KHÉO LÉO (Đã thu gọn để không bị chạm đáy) ===
  dex_1: {
    id: 'dex_1',
    name: 'Thần Tốc Hành Quân',
    description: '+20 Tốc Độ Di Chuyển',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 45,
    connections: ['root', 'dex_2'],
    modifiers: [{ type: 'movement_speed', value: 20 }],
  },
  dex_2: {
    id: 'dex_2',
    name: 'Vũ Điệu Cung Vũ',
    description: '+20% Tốc Độ Bắn Kỹ Năng',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 95,
    connections: ['dex_1', 'dex_3'],
    modifiers: [{ type: 'attack_speed_pct', value: 20 }],
  },
  dex_3: {
    id: 'dex_3',
    name: 'Hư Ứng Vô Ảnh',
    description: '+25 Tỷ Lệ Né Đòn (Evasion)',
    nodeType: 'notable',
    branch: 'dexterity',
    gridX: 0,
    gridY: 145,
    connections: ['dex_2', 'dex_keystone'],
    modifiers: [{ type: 'flat_evasion', value: 25 }],
  },
  dex_keystone: {
    id: 'dex_keystone',
    name: 'Keystone: Deadeye',
    description: '+1 Tia Đạn Bổ Sung, +2 Lần Xuyên Thấu',
    nodeType: 'keystone',
    branch: 'dexterity',
    gridX: 0,
    gridY: 195,
    connections: ['dex_3'],
    modifiers: [
      { type: 'extra_projectile', value: 1 },
      { type: 'extra_pierce', value: 2 },
    ],
  },

  // === NHÁNH XANH LAM: TRÍ TUỆ ===
  int_1: {
    id: 'int_1',
    name: 'Màn Chắn Tâm Linh',
    description: '+35 Khiên Năng Lượng (Energy Shield)',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 70,
    gridY: -60,
    connections: ['root', 'int_2'],
    modifiers: [{ type: 'flat_es', value: 35 }],
  },
  int_2: {
    id: 'int_2',
    name: 'Hỏa Cầu Hủy Diệt',
    description: '+25% Sát Thương Lửa',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 140,
    gridY: -100,
    connections: ['int_1', 'int_3'],
    modifiers: [{ type: 'inc_fire_damage', value: 25 }],
  },
  int_3: {
    id: 'int_3',
    name: 'Khai Mở Tiêu Điểm',
    description: '+8% Tỷ Lệ Chí Mạng',
    nodeType: 'notable',
    branch: 'intelligence',
    gridX: 210,
    gridY: -130,
    connections: ['int_2', 'int_keystone'],
    modifiers: [{ type: 'crit_chance', value: 8 }],
  },
  int_keystone: {
    id: 'int_keystone',
    name: 'Keystone: Archmage',
    description: '+60 Khiên Năng Lượng, +30% Sát Thương Chí Mạng',
    nodeType: 'keystone',
    branch: 'intelligence',
    gridX: 280,
    gridY: -150,
    connections: ['int_3'],
    modifiers: [
      { type: 'flat_es', value: 60 },
      { type: 'crit_multiplier', value: 0.3 },
    ],
  },
};
''',

    # 3. Mở rộng Hệ thống Rơi Đồ: Currency + Equipment + Gems
    "src/core/loot/LootEngine.ts": '''import { CurrencyType, EquipmentItem } from '../items/ItemTypes';
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

      // 60% rơi Currency
      if (typeRoll < 0.6) {
        const cRoll = Math.random() * 100;
        let cur: CurrencyType = 'transmutation';
        let name = 'Orb of Transmutation';

        if (cRoll < 4 && (rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'exalted';
          name = 'Exalted Orb';
        } else if (cRoll < 20 && (rarity === 'Magic' || rarity === 'Rare' || rarity === 'Boss')) {
          cur = 'chaos';
          name = 'Chaos Orb';
        } else if (cRoll < 40) {
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
      // 25% rơi Trang Bị (Equipment)
      else if (typeRoll < 0.85) {
        const bases: ('Sword' | 'Bow' | 'Wand' | 'Plate')[] = ['Sword', 'Bow', 'Wand', 'Plate'];
        const base = bases[Math.floor(Math.random() * bases.length)];
        const item: EquipmentItem = {
          id: `eq_${Date.now()}_${Math.random()}`,
          name: `${base}`,
          baseType: base,
          rarity: 'Normal',
          prefixes: [],
          suffixes: [],
        };

        // Quái xịn rơi đồ Magic hoặc Rare luôn
        if (rarity === 'Rare' || rarity === 'Boss') {
          CraftingEngine.applyTransmutation(item);
          CraftingEngine.applyRegal(item);
        } else if (rarity === 'Magic') {
          CraftingEngine.applyTransmutation(item);
        }

        drops.push({
          category: 'equipment',
          equipmentItem: item,
          name: `[${item.rarity}] ${item.baseType}`,
        });
      }
      // 15% rơi Ngọc (Gems)
      else {
        const gems = [
          { id: 'fireball', name: 'Ngọc Hỏa Cầu (Fireball)' },
          { id: 'split_arrow', name: 'Ngọc Tên Rẽ (Split Arrow)' },
          { id: 'gmp', name: 'Ngọc GMP (Tăng Đạn)' },
          { id: 'pierce', name: 'Ngọc Pierce (Xuyên Thấu)' },
          { id: 'added_fire', name: 'Ngọc Added Fire' },
        ];
        const g = gems[Math.floor(Math.random() * gems.length)];
        drops.push({ category: 'gem', gemId: g.id, name: g.name });
      }
    }

    return drops;
  }
}
''',

    # 4. Hiển thị Loot trên sàn (Hỗ trợ nhãn nhiều màu theo chủng loại)
    "src/scenes/LootDrop.ts": '''import Phaser from 'phaser';
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
''',

    # 5. Đồ họa Đạn Bay (Hiệu ứng riêng biệt cho Fireball, Arrow, Slam)
    "src/scenes/Projectile.ts": '''import Phaser from 'phaser';
import { SkillContext } from '../core/gems/GemTypes';

export class Projectile extends Phaser.Physics.Arcade.Sprite {
  public skillCtx!: SkillContext;
  public remainingPierce: number = 0;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'proj_fireball');
  }

  fire(x: number, y: number, angleRad: number, ctx: SkillContext): void {
    this.skillCtx = ctx;
    this.remainingPierce = ctx.pierceCount;

    // Đổi texture theo loại kỹ năng
    const texKey = ctx.id === 'split_arrow' ? 'proj_arrow' : ctx.id === 'ground_slam' ? 'proj_slam' : 'proj_fireball';
    this.setTexture(texKey);

    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      if (ctx.id === 'ground_slam') {
        body.setSize(24, 24);
      } else {
        body.setSize(12, 12);
      }
      this.scene.physics.velocityFromRotation(angleRad, ctx.projectileSpeed, body.velocity);
    }

    const lifeTime = ctx.id === 'ground_slam' ? 500 : 2500;
    this.scene.time.delayedCall(lifeTime, () => {
      if (this.active) this.kill();
    });
  }

  kill(): void {
    this.disableBody(true, true);
  }
}
''',

    # 6. Giao Diện Bảng Chỉ Số Nhân Vật Mới (Character Sheet [Phím C])
    "src/scenes/CharacterUI.ts": '''import Phaser from 'phaser';
import { Player } from './Player';

export class CharacterUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private player: Player;
  private isOpen: boolean = false;
  private infoText!: Phaser.GameObjects.Text;

  constructor(scene: Phaser.Scene, player: Player) {
    this.scene = scene;
    this.player = player;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(350);
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

    const bg = this.scene.add.rectangle(cx, cy, 480, 440, 0x090d16, 1.0);
    bg.setStrokeStyle(2, 0xeab308);
    bg.setInteractive();
    this.container.add(bg);

    const title = this.scene.add.text(cx, cy - 190, 'BẢNG CHỈ SỐ NHÂN VẬT [C]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#eab308',
    }).setOrigin(0.5);
    this.container.add(title);

    this.infoText = this.scene.add.text(cx - 210, cy - 150, '', {
      fontFamily: 'monospace',
      fontSize: '13px',
      lineSpacing: 7,
      color: '#f8fafc',
    });
    this.container.add(this.infoText);

    const closeBtn = this.scene.add.text(cx, cy + 185, '[ĐÓNG (C)]', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#94a3b8',
      backgroundColor: '#1e293b',
      padding: { x: 12, y: 5 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  public refresh(): void {
    const s = this.player.stats;
    const skill = this.player.compiledSkills[0];

    const dpsMin = skill ? Math.round(skill.baseMinDamage + skill.addedMinDamage) : 0;
    const dpsMax = skill ? Math.round(skill.baseMaxDamage + skill.addedMaxDamage) : 0;

    const str = 
      `• Lớp Nhân Vật: ${this.player.characterClass.toUpperCase()}\\n` +
      `• Cấp Độ (Level): ${s.level} (EXP: ${s.currentExp}/${s.maxExp})\\n` +
      `-------------------------------------------\\n` +
      `❤ Máu Tối Đa (Max Life): ${Math.round(s.currentLife)} / ${s.maxLife}\\n` +
      `🛡 Khiên Năng Lượng (ES): ${Math.round(s.energyShield)} / ${s.maxEnergyShield}\\n` +
      `🛡 Giáp Vật Lý (Armour): ${s.armour}\\n` +
      `💨 Tỷ Lệ Né Đòn (Evasion): ${s.evasion}%\\n` +
      `👟 Tốc Độ Di Chuyển: ${s.movementSpeed}\\n` +
      `-------------------------------------------\\n` +
      `⚔ Kỹ Năng Chính: ${skill ? skill.name : 'Chưa gắn'}\\n` +
      `💥 Sát Thương Cơ Bản: ${dpsMin} - ${dpsMax} (${skill ? skill.damageType.toUpperCase() : ''})\\n` +
      `🔥 Tăng Sát Thương (% Inc): +${skill ? skill.increasedDamagePercent : 0}%\\n` +
      `⚡ Tốc Độ Ra Chiêu: ${skill ? skill.attackSpeedMultiplier.toFixed(2) : 1}x\\n` +
      `🎯 Tỷ Lệ Chí Mạng: ${skill ? skill.critChance : 5}% (x${skill ? skill.critMultiplier.toFixed(1) : 1.5})\\n` +
      `🏹 Số Lượng Đạn: ${skill ? skill.projectileCount : 1} | Xuyên: ${skill ? skill.pierceCount : 0}`;

    this.infoText.setText(str);
  }
}
''',

    # 7. Sửa Cây Nội Tại UI: Nền 100% Solid, Không xuyên thấu chữ dưới sàn
    "src/scenes/PassiveTreeUI.ts": '''import Phaser from 'phaser';
import { PassiveTreeManager } from '../core/passive/PassiveTreeManager';
import { PASSIVE_TREE_NODES } from '../core/passive/PassiveTreeData';

export class PassiveTreeUI {
  private scene: Phaser.Scene;
  private treeManager: PassiveTreeManager;
  private container: Phaser.GameObjects.Container;
  private isOpen: boolean = false;
  private onTreeChanged: () => void;

  private pointsText!: Phaser.GameObjects.Text;
  private tooltipText!: Phaser.GameObjects.Text;
  private linesGraphics!: Phaser.GameObjects.Graphics;
  private nodeSprites: Map<string, { circle: Phaser.GameObjects.Arc; text: Phaser.GameObjects.Text }> = new Map();

  constructor(scene: Phaser.Scene, manager: PassiveTreeManager, onTreeChanged: () => void) {
    this.scene = scene;
    this.treeManager = manager;
    this.onTreeChanged = onTreeChanged;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(400); // Lớp trên cùng
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

    // NỀN ĐEN 100% OPAQUE KHÔNG XUYÊN THẤU VẬT PHẨM DƯỚI SÀN
    const bg = this.scene.add.rectangle(cx, cy, 760, 520, 0x070a10, 1.0);
    bg.setStrokeStyle(2, 0x30363d);
    bg.setInteractive();
    this.container.add(bg);

    const title = this.scene.add.text(cx, cy - 230, 'CÂY KỸ NĂNG NỘI TẠI (PASSIVE TREE) [P]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(title);

    this.pointsText = this.scene.add.text(cx, cy - 200, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
      color: '#00ffff',
    }).setOrigin(0.5);
    this.container.add(this.pointsText);

    this.linesGraphics = this.scene.add.graphics();
    this.container.add(this.linesGraphics);

    this.tooltipText = this.scene.add.text(cx, cy + 235, 'Di chuột vào node để xem mô tả. Nhấp chuột để nâng cấp.', {
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#c9d1d9',
      backgroundColor: '#161b22',
      padding: { x: 10, y: 5 },
    }).setOrigin(0.5);
    this.container.add(this.tooltipText);

    for (const [id, node] of Object.entries(PASSIVE_TREE_NODES)) {
      const nx = cx + node.gridX;
      const ny = cy + node.gridY;
      const radius = node.nodeType === 'keystone' ? 17 : node.nodeType === 'notable' ? 13 : 10;

      const circle = this.scene.add.circle(nx, ny, radius, 0x333333).setInteractive({ useHandCursor: true });
      circle.setStrokeStyle(2, 0x666666);

      const label = this.scene.add.text(nx, ny, node.name.slice(0, 1), {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: '#ffffff',
      }).setOrigin(0.5);

      circle.on('pointerdown', () => {
        if (this.treeManager.allocate(id)) {
          this.onTreeChanged();
          this.refresh();
        }
      });

      circle.on('pointerover', () => {
        const status = this.treeManager.allocatedNodeIds.has(id)
          ? '[ĐÃ HỌC]'
          : this.treeManager.canAllocate(id)
          ? '[CÓ THỂ HỌC]'
          : '[CHƯA ĐỦ ĐIỀU KIỆN]';
        this.tooltipText.setText(`${node.name} ${status} - ${node.description}`);
      });

      circle.on('pointerout', () => {
        this.tooltipText.setText('Di chuột vào node để xem mô tả. Nhấp chuột để nâng cấp.');
      });

      this.nodeSprites.set(id, { circle, text: label });
      this.container.add(circle);
      this.container.add(label);
    }
  }

  public refresh(): void {
    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    this.pointsText.setText(`ĐIỂM NỘI TẠI CÒN LẠI: ${this.treeManager.unspentPoints}`);

    this.linesGraphics.clear();
    const drawnEdges = new Set<string>();

    for (const [id, node] of Object.entries(PASSIVE_TREE_NODES)) {
      const x1 = cx + node.gridX;
      const y1 = cy + node.gridY;

      for (const targetId of node.connections) {
        const edgeKey = [id, targetId].sort().join('-');
        if (drawnEdges.has(edgeKey)) continue;
        drawnEdges.add(edgeKey);

        const targetNode = PASSIVE_TREE_NODES[targetId];
        if (!targetNode) continue;

        const x2 = cx + targetNode.gridX;
        const y2 = cy + targetNode.gridY;

        const isConnected = this.treeManager.allocatedNodeIds.has(id) && this.treeManager.allocatedNodeIds.has(targetId);
        this.linesGraphics.lineStyle(isConnected ? 3 : 1, isConnected ? 0xffd700 : 0x22272e, isConnected ? 0.9 : 0.6);
        this.linesGraphics.lineBetween(x1, y1, x2, y2);
      }
    }

    for (const [id, node] of Object.entries(PASSIVE_TREE_NODES)) {
      const sprite = this.nodeSprites.get(id);
      if (!sprite) continue;

      const isAllocated = this.treeManager.allocatedNodeIds.has(id);
      const canAlloc = this.treeManager.canAllocate(id);

      let branchColor = 0x8b949e;
      if (node.branch === 'strength') branchColor = 0xdc143c;
      if (node.branch === 'dexterity') branchColor = 0x2ea043;
      if (node.branch === 'intelligence') branchColor = 0x1f6feb;

      if (isAllocated) {
        sprite.circle.setFillStyle(branchColor, 1);
        sprite.circle.setStrokeStyle(3, 0xffffff);
      } else if (canAlloc) {
        sprite.circle.setFillStyle(0x21262d, 1);
        sprite.circle.setStrokeStyle(2, 0xffd700);
      } else {
        sprite.circle.setFillStyle(0x161b22, 0.9);
        sprite.circle.setStrokeStyle(1, 0x30363d);
      }
    }
  }
}
''',

    # 8. Nhân vật Player: Hỗ trợ nạp EXP, Thăng Cấp (Level Up), Đổi Lớp Nhân Vật
    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats, getExpNeeded } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill, GroundSlamSkill } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquipmentItem } from '../core/items/ItemTypes';
import { PassiveTreeBonus } from '../core/passive/PassiveTreeTypes';
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

  // Tăng EXP và kiểm tra lên cấp
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
      return true; // Lên cấp thành công
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
    const skill = this.compiledSkills[0];

    const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
    if (time - this.lastCastTime < cooldown) return;

    this.lastCastTime = time;

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

    # 9. BattleScene: Tích hợp đầy đủ Thanh EXP, Chọn Class, Menu Phím [C], [I], [P]
    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { Monster } from './Monster';
import { LootDrop } from './LootDrop';
import { CraftingUI } from './CraftingUI';
import { PassiveTreeUI } from './PassiveTreeUI';
import { CharacterUI } from './CharacterUI';
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
        // Tăng EXP
        const leveledUp = this.player.gainExp(monster.monsterStats.expReward);
        if (leveledUp) {
          this.triggerLevelUpNotice();
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

    // Va chạm: Người chơi -> Nhặt Loot
    this.physics.add.overlap(this.player, this.lootPool, (_playerObj, lootObj) => {
      const loot = lootObj as LootDrop;
      if (!loot.active) return;

      const d = loot.collect();
      if (d.category === 'currency' && d.currencyType) {
        this.inventoryData.currencies[d.currencyType] = (this.inventoryData.currencies[d.currencyType] || 0) + 1;
        this.showPickupNotice(loot.x, loot.y, d.currencyType.toUpperCase());
      } else if (d.category === 'equipment' && d.equipmentItem) {
        // Tự động trang bị nếu đồ mới xịn hơn
        this.inventoryData.equippedItem = d.equipmentItem;
        this.syncPlayerStats();
        this.showPickupNotice(loot.x, loot.y, `ĐỔI: ${d.name}`);
      } else if (d.category === 'gem') {
        this.showPickupNotice(loot.x, loot.y, `NHẶT: ${d.name}`);
      }
    });

    // Va chạm: Quái -> Người chơi
    this.physics.add.overlap(this.player, this.monsterPool, (_playerObj, monObj) => {
      if (this.isGameOver || this.intermissionUI.getIsShowing()) return;
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

    this.intermissionUI = new IntermissionUI(
      this,
      () => this.startNextWave(),
      () => this.craftingUI.toggle(),
      () => this.passiveTreeUI.toggle()
    );

    // Phím tắt bàn phím
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

  private triggerLevelUpNotice(): void {
    this.passiveTreeManager.unspentPoints++;
    SoundEffects.playWaveClear();

    const lvlText = this.add.text(this.player.x, this.player.y - 45, '★ LEVEL UP! (+1 THIÊN PHÚ) ★', {
      fontFamily: 'monospace',
      fontSize: '16px',
      fontStyle: 'bold',
      color: '#ffd700',
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5);

    this.tweens.add({
      targets: lvlText,
      y: this.player.y - 85,
      alpha: 0,
      duration: 1500,
      onComplete: () => lvlText.destroy(),
    });
  }

  private createTopRightActionMenu(): void {
    const rx = this.scale.width - 20;

    // Nút đổi class nhanh
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

    // Nút Bảng Chỉ Số [C]
    const charBtn = this.add.text(rx, 55, '👤 CHỈ SỐ (C)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#38bdf8',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    charBtn.on('pointerdown', () => this.characterUI.toggle());

    // Nút Hòm Đồ [I]
    const craftBtn = this.add.text(rx, 90, '⚒️ HÒM ĐỒ (I)', {
      fontFamily: 'monospace',
      fontSize: '13px',
      fontStyle: 'bold',
      color: '#ffd700',
      backgroundColor: '#21262d',
      padding: { x: 10, y: 6 },
    }).setOrigin(1, 0).setScrollFactor(0).setInteractive({ useHandCursor: true });

    craftBtn.on('pointerdown', () => this.craftingUI.toggle());

    // Nút Cây Thiên Phú [P]
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
    // 1. Cầu lửa (Fireball)
    if (!this.textures.exists('proj_fireball')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xef4444, 1);
      g.fillCircle(8, 8, 8);
      g.fillStyle(0xfde047, 1);
      g.fillCircle(8, 8, 4);
      g.generateTexture('proj_fireball', 16, 16);
      g.destroy();
    }

    // 2. Mũi tên (Split Arrow)
    if (!this.textures.exists('proj_arrow')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x22c55e, 1);
      g.fillRect(0, 5, 14, 2);
      g.fillTriangle(16, 6, 11, 2, 11, 10);
      g.generateTexture('proj_arrow', 16, 12);
      g.destroy();
    }

    // 3. Sóng xung kích (Ground Slam)
    if (!this.textures.exists('proj_slam')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xd97706, 0.9);
      g.fillCircle(12, 12, 12);
      g.fillStyle(0xfef08a, 1);
      g.fillCircle(12, 12, 6);
      g.generateTexture('proj_slam', 24, 24);
      g.destroy();
    }

    // 4. Quái vật sắc nét
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

    // Cập nhật text class và level
    this.classLevelText.setText(`[${this.player.characterClass.toUpperCase()}] CẤP ĐỘ: ${this.player.stats.level}`);

    // Thanh Máu
    this.lifeBarGfx.fillStyle(0x000000, 0.7);
    this.lifeBarGfx.fillRect(x, y, barW, barH);
    const lifePct = Math.max(0, this.player.stats.currentLife / this.player.stats.maxLife);
    this.lifeBarGfx.fillStyle(0xdc143c, 1);
    this.lifeBarGfx.fillRect(x, y, barW * lifePct, barH);

    // Thanh Khiên Năng Lượng (ES)
    if (this.player.stats.maxEnergyShield > 0) {
      const esPct = Math.max(0, this.player.stats.energyShield / this.player.stats.maxEnergyShield);
      this.esBarGfx.fillStyle(0x1e90ff, 0.9);
      this.esBarGfx.fillRect(x, y - 8, barW * esPct, 6);
    }

    // THANH KINH NGHIỆM (EXP) Ở ĐÁY MÀN HÌNH
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
      this.characterUI.getIsOpen()
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
    if (this.isGameOver || this.intermissionUI.getIsShowing()) return;

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
      this.characterUI.getIsOpen();

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

print("\nHoàn tất nâng cấp: EXP & Leveling, Character UI [C], Item/Gem Drops, VFX Skill & Sửa lỗi Cây Nội Tại!")