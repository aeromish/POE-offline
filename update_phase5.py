import os

files = {
    "src/core/passive/PassiveTreeTypes.ts": '''export type PassiveNodeType = 'start' | 'small' | 'notable' | 'keystone';
export type StatModifierType = 
  | 'flat_life'
  | 'flat_es'
  | 'flat_armour'
  | 'flat_evasion'
  | 'inc_phys_damage'
  | 'inc_fire_damage'
  | 'attack_speed_pct'
  | 'movement_speed'
  | 'crit_chance'
  | 'crit_multiplier'
  | 'extra_projectile'
  | 'extra_pierce';

export interface StatModifier {
  type: StatModifierType;
  value: number;
}

export interface PassiveNode {
  id: string;
  name: string;
  description: string;
  nodeType: PassiveNodeType;
  branch: 'strength' | 'dexterity' | 'intelligence' | 'neutral';
  gridX: number; // Tọa độ tương đối trên giao diện
  gridY: number;
  connections: string[]; // Danh sách ID các node liên kết
  modifiers: StatModifier[];
}

export interface PassiveTreeBonus {
  flatLife: number;
  flatES: number;
  flatArmour: number;
  flatEvasion: number;
  incPhysDamage: number;
  incFireDamage: number;
  attackSpeedPct: number;
  movementSpeed: number;
  critChance: number;
  critMultiplier: number;
  extraProjectile: number;
  extraPierce: number;
}
''',

    "src/core/passive/PassiveTreeData.ts": '''import { PassiveNode } from './PassiveTreeTypes';

export const PASSIVE_TREE_NODES: Record<string, PassiveNode> = {
  // Gốc xuất phát
  root: {
    id: 'root',
    name: 'Khởi Điểm Lưu Đày',
    description: 'Nguồn cội sức mạnh của kẻ sống sót.',
    nodeType: 'start',
    branch: 'neutral',
    gridX: 0,
    gridY: 0,
    connections: ['str_1', 'dex_1', 'int_1'],
    modifiers: [],
  },

  // === NHÁNH ĐỎ: CHIẾN BINH / SỨC MẠNH ===
  str_1: {
    id: 'str_1',
    name: 'Thân Thể Bất Khuất',
    description: '+30 Máu Tối Đa',
    nodeType: 'small',
    branch: 'strength',
    gridX: -70,
    gridY: -50,
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
    gridY: -80,
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
    gridY: -110,
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
    gridY: -140,
    connections: ['str_3'],
    modifiers: [
      { type: 'flat_life', value: 70 },
      { type: 'flat_armour', value: 60 },
    ],
  },

  // === NHÁNH XANH LÁ: XẠ THỦ / KHÉO LÉO ===
  dex_1: {
    id: 'dex_1',
    name: 'Thần Tốc Hành Quân',
    description: '+20 Tốc Độ Di Chuyển',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 80,
    connections: ['root', 'dex_2'],
    modifiers: [{ type: 'movement_speed', value: 20 }],
  },
  dex_2: {
    id: 'dex_2',
    name: 'Vũ Điệu Cung Vũ',
    description: '+20% Tốc Độ Bắn/Thi Triển Kỹ Năng',
    nodeType: 'small',
    branch: 'dexterity',
    gridX: 0,
    gridY: 150,
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
    gridY: 220,
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
    gridY: 290,
    connections: ['dex_3'],
    modifiers: [
      { type: 'extra_projectile', value: 1 },
      { type: 'extra_pierce', value: 2 },
    ],
  },

  // === NHÁNH XANH LAM: THUẬT SĨ / TRÍ TUỆ ===
  int_1: {
    id: 'int_1',
    name: 'Màn Chắn Tâm Linh',
    description: '+35 Khiên Năng Lượng (Energy Shield)',
    nodeType: 'small',
    branch: 'intelligence',
    gridX: 70,
    gridY: -50,
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
    gridY: -80,
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
    gridY: -110,
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
    gridY: -140,
    connections: ['int_3'],
    modifiers: [
      { type: 'flat_es', value: 60 },
      { type: 'crit_multiplier', value: 0.3 },
    ],
  },
};
''',

    "src/core/passive/PassiveTreeManager.ts": '''import { PASSIVE_TREE_NODES } from './PassiveTreeData';
import { PassiveTreeBonus } from './PassiveTreeTypes';

export class PassiveTreeManager {
  public unspentPoints: number = 1; // Điểm khởi đầu tặng sẵn
  public allocatedNodeIds: Set<string> = new Set(['root']); // Node gốc đã mở mặc định

  public canAllocate(nodeId: string): boolean {
    if (this.unspentPoints <= 0) return false;
    if (this.allocatedNodeIds.has(nodeId)) return false;

    const node = PASSIVE_TREE_NODES[nodeId];
    if (!node) return false;

    // Kiểm tra có ít nhất 1 node lân cận đã được allocate hay chưa
    return node.connections.some((connectedId) => this.allocatedNodeIds.has(connectedId));
  }

  public allocate(nodeId: string): boolean {
    if (!this.canAllocate(nodeId)) return false;

    this.allocatedNodeIds.add(nodeId);
    this.unspentPoints--;
    return true;
  }

  public calculateTotalBonus(): PassiveTreeBonus {
    const bonus: PassiveTreeBonus = {
      flatLife: 0,
      flatES: 0,
      flatArmour: 0,
      flatEvasion: 0,
      incPhysDamage: 0,
      incFireDamage: 0,
      attackSpeedPct: 0,
      movementSpeed: 0,
      critChance: 0,
      critMultiplier: 0,
      extraProjectile: 0,
      extraPierce: 0,
    };

    for (const id of this.allocatedNodeIds) {
      const node = PASSIVE_TREE_NODES[id];
      if (!node) continue;

      for (const mod of node.modifiers) {
        switch (mod.type) {
          case 'flat_life': bonus.flatLife += mod.value; break;
          case 'flat_es': bonus.flatES += mod.value; break;
          case 'flat_armour': bonus.flatArmour += mod.value; break;
          case 'flat_evasion': bonus.flatEvasion += mod.value; break;
          case 'inc_phys_damage': bonus.incPhysDamage += mod.value; break;
          case 'inc_fire_damage': bonus.incFireDamage += mod.value; break;
          case 'attack_speed_pct': bonus.attackSpeedPct += mod.value; break;
          case 'movement_speed': bonus.movementSpeed += mod.value; break;
          case 'crit_chance': bonus.critChance += mod.value; break;
          case 'crit_multiplier': bonus.critMultiplier += mod.value; break;
          case 'extra_projectile': bonus.extraProjectile += mod.value; break;
          case 'extra_pierce': bonus.extraPierce += mod.value; break;
        }
      }
    }

    return bonus;
  }
}
''',

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
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(150);
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

    // Nền tối mờ che sàn đấu
    const bg = this.scene.add.rectangle(cx, cy, 760, 520, 0x05070a, 0.96);
    bg.setStrokeStyle(2, 0x30363d);
    this.container.add(bg);

    // Tiêu đề
    const title = this.scene.add.text(cx, cy - 230, 'CÂY KỸ NĂNG NỘI TẠI (PASSIVE TREE) [P]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5);
    this.container.add(title);

    // Hiển thị điểm cộng
    this.pointsText = this.scene.add.text(cx, cy - 200, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
      color: '#00ffff',
    }).setOrigin(0.5);
    this.container.add(this.pointsText);

    // Lớp đồ họa vẽ đường dây nối liên kết
    this.linesGraphics = this.scene.add.graphics();
    this.container.add(this.linesGraphics);

    // Tooltip mô tả node
    this.tooltipText = this.scene.add.text(cx, cy + 225, 'Di chuột vào node để xem mô tả. Nhấp chuột để nâng cấp.', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#c9d1d9',
      backgroundColor: '#161b22',
      padding: { x: 10, y: 5 },
    }).setOrigin(0.5);
    this.container.add(this.tooltipText);

    // Tạo các node hình tròn
    for (const [id, node] of Object.entries(PASSIVE_TREE_NODES)) {
      const nx = cx + node.gridX;
      const ny = cy + node.gridY;
      const radius = node.nodeType === 'keystone' ? 18 : node.nodeType === 'notable' ? 14 : 10;

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
          ? '[ĐÃ KÍCH HOẠT]'
          : this.treeManager.canAllocate(id)
          ? '[CÓ THỂ HỌC]'
          : '[CHƯA ĐỦ ĐIỀU KIỆN]';
        this.tooltipText.setText(`${node.name} ${status}\\n${node.description}`);
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

    // Vẽ lại đường nối
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

        // Nếu cả 2 đầu đều đã allocate thì sáng rực, ngược lại xám mờ
        const isConnected = this.treeManager.allocatedNodeIds.has(id) && this.treeManager.allocatedNodeIds.has(targetId);
        this.linesGraphics.lineStyle(isConnected ? 3 : 1, isConnected ? 0xffd700 : 0x22272e, isConnected ? 0.9 : 0.6);
        this.linesGraphics.lineBetween(x1, y1, x2, y2);
      }
    }

    // Cập nhật màu sắc node
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
        sprite.circle.setStrokeStyle(2, 0xffd700); // Viền vàng báo hiệu học được
      } else {
        sprite.circle.setFillStyle(0x161b22, 0.8);
        sprite.circle.setStrokeStyle(1, 0x30363d);
      }
    }
  }
}
''',

    "src/scenes/IntermissionUI.ts": '''import Phaser from 'phaser';

export class IntermissionUI {
  private scene: Phaser.Scene;
  private container: Phaser.GameObjects.Container;
  private isShowing: boolean = false;
  private onStartNextWave: () => void;
  private onOpenCrafting: () => void;
  private onOpenPassives: () => void;

  private waveTitleText!: Phaser.GameObjects.Text;

  constructor(
    scene: Phaser.Scene,
    onStartNextWave: () => void,
    onOpenCrafting: () => void,
    onOpenPassives: () => void
  ) {
    this.scene = scene;
    this.onStartNextWave = onStartNextWave;
    this.onOpenCrafting = onOpenCrafting;
    this.onOpenPassives = onOpenPassives;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(200);
    this.createPanel();
    this.container.setVisible(false);
  }

  public show(clearedWave: number): void {
    this.isShowing = true;
    this.waveTitleText.setText(`ĐÃ VƯỢT QUA ĐỢT ${clearedWave}!\\nKHU VỰC AN TOÀN (SAFE ZONE)`);
    this.container.setVisible(true);
  }

  public hide(): void {
    this.isShowing = false;
    this.container.setVisible(false);
  }

  public getIsShowing(): boolean {
    return this.isShowing;
  }

  private createPanel(): void {
    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    const bg = this.scene.add.rectangle(cx, cy, 600, 320, 0x090d16, 0.95);
    bg.setStrokeStyle(2, 0x238636);
    this.container.add(bg);

    this.waveTitleText = this.scene.add.text(cx, cy - 90, '', {
      fontFamily: 'monospace',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffd700',
      align: 'center',
    }).setOrigin(0.5);
    this.container.add(this.waveTitleText);

    const rewardText = this.scene.add.text(cx, cy - 30, '+1 Điểm Kỹ Năng Nội Tại (Passive Skill Point)\\nSẵn sàng nâng cấp trang bị và nhánh sức mạnh', {
      fontFamily: 'monospace',
      fontSize: '14px',
      color: '#58a6ff',
      align: 'center',
    }).setOrigin(0.5);
    this.container.add(rewardText);

    // Nút mở Hòm đồ
    const btnCraft = this.scene.add.text(cx - 150, cy + 35, '[I] HÒM ĐỒ & CRAFT', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#ffffff',
      backgroundColor: '#21262d',
      padding: { x: 12, y: 8 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });
    btnCraft.on('pointerdown', () => this.onOpenCrafting());
    this.container.add(btnCraft);

    // Nút mở Cây nội tại
    const btnPassives = this.scene.add.text(cx + 150, cy + 35, '[P] CÂY NỘI TẠI', {
      fontFamily: 'monospace',
      fontSize: '13px',
      color: '#ffffff',
      backgroundColor: '#21262d',
      padding: { x: 12, y: 8 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });
    btnPassives.on('pointerdown', () => this.onOpenPassives());
    this.container.add(btnPassives);

    // Nút bắt đầu đợt kế tiếp
    const btnNext = this.scene.add.text(cx, cy + 105, 'BẮT ĐẦU ĐỢT KẾ TIẾP [SPACE]', {
      fontFamily: 'monospace',
      fontSize: '16px',
      fontStyle: 'bold',
      color: '#ffffff',
      backgroundColor: '#238636',
      padding: { x: 24, y: 12 },
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    btnNext.on('pointerdown', () => this.onStartNextWave());
    btnNext.on('pointerover', () => btnNext.setBackgroundColor('#2ea043'));
    btnNext.on('pointerout', () => btnNext.setBackgroundColor('#238636'));
    this.container.add(btnNext);
  }
}
''',

    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill } from '../core/gems/ActiveGems';
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

  // Tái tính toán toàn bộ chỉ số từ Base + Trang bị + Cây Nội Tại
  public recalculateTotalStats(item: EquipmentItem, treeBonus: PassiveTreeBonus): void {
    const base = CLASS_BASE_STATS[this.characterClass];

    this.stats.maxLife = base.maxLife + treeBonus.flatLife;
    this.stats.maxEnergyShield = base.maxEnergyShield + treeBonus.flatES;
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

      // Cộng thêm bonus từ Tree tùy theo loại sát thương
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
import { PassiveTreeUI } from './PassiveTreeUI';
import { IntermissionUI } from './IntermissionUI';
import { WaveManager } from '../core/monsters/WaveManager';
import { DamageEngine } from '../core/combat/DamageEngine';
import { LootEngine } from '../core/loot/LootEngine';
import { PassiveTreeManager } from '../core/passive/PassiveTreeManager';
import { InventoryData } from '../core/items/ItemTypes';
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
  private hintsText!: Phaser.GameObjects.Text;
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

    // Map sàn
    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');
    this.syncPlayerStats();

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

    // Khởi tạo các Modal UIs
    this.craftingUI = new CraftingUI(this, this.inventoryData, () => this.syncPlayerStats());
    this.passiveTreeUI = new PassiveTreeUI(this, this.passiveTreeManager, () => this.syncPlayerStats());

    this.intermissionUI = new IntermissionUI(
      this,
      () => this.startNextWave(),
      () => this.craftingUI.toggle(),
      () => this.passiveTreeUI.toggle()
    );

    // Phím tắt bàn phím
    this.input.keyboard?.on('keydown-I', () => this.craftingUI.toggle());
    this.input.keyboard?.on('keydown-P', () => this.passiveTreeUI.toggle());
    this.input.keyboard?.on('keydown-SPACE', () => {
      if (this.intermissionUI.getIsShowing()) {
        this.startNextWave();
      }
    });

    // Spawner lặp lại
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

    this.hintsText = this.add.text(20, 76, '[I]: HÒM ĐỒ & CRAFT | [P]: CÂY NỘI TẠI', {
      fontFamily: 'monospace',
      fontSize: '13px',
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
    if (
      this.isGameOver || 
      !this.waveManager.isWaveActive || 
      this.intermissionUI.getIsShowing() ||
      this.craftingUI.getIsOpen() ||
      this.passiveTreeUI.getIsOpen()
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
      // Kết thúc wave hiện tại, bước vào Intermission Safe Phase
      this.waveManager.isWaveActive = false;

      // Xóa sạch quái còn sót
      this.monsterPool.children.each((child) => {
        const mon = child as Monster;
        if (mon.active) mon.kill();
        return true;
      });

      // Tặng 1 Skill Point và hồi đầy Máu/ES
      this.passiveTreeManager.unspentPoints++;
      this.player.stats.currentLife = this.player.stats.maxLife;
      this.player.stats.energyShield = this.player.stats.maxEnergyShield;

      // Hiện bảng Intermission
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

    // Dừng hành động khi mở bất kỳ giao diện modal nào
    const isUIBlocking = 
      this.intermissionUI.getIsShowing() || 
      this.craftingUI.getIsOpen() || 
      this.passiveTreeUI.getIsOpen();

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

print("\nHoàn tất cài đặt Giai đoạn 5: Mini Passive Tree Graph & Intermission Safe Phase!")