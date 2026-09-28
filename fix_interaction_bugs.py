import os

files = {
    # 1. Sửa LevelUpUI.ts: Làm phẳng cấu trúc, gán setScrollFactor(0), bắt click cả thẻ lẫn nút
    "src/scenes/LevelUpUI.ts": '''import Phaser from 'phaser';
import { SoundEffects } from '../core/audio/SoundEffects';

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

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.container = scene.add.container(0, 0).setScrollFactor(0).setDepth(600);
    this.container.setVisible(false);
  }

  public show(choices: LevelUpChoice[], onChosen: () => void): void {
    this.isShowing = true;
    this.container.removeAll(true);

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    // Nền tối khóa toàn màn hình
    const bg = this.scene.add.rectangle(cx, cy, this.scene.scale.width, this.scene.scale.height, 0x030712, 0.9)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const banner = this.scene.add.text(cx, cy - 180, '★ LÊN CẤP! CHỌN MỘT NÂNG CẤP KỸ NĂNG ★', {
      fontFamily: 'monospace',
      fontSize: '22px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(banner);

    // Vẽ 3 thẻ phẳng trực tiếp vào container chính (Không lồng container phụ)
    choices.forEach((choice, idx) => {
      const cardX = cx - 240 + idx * 240;
      const cardY = cy;

      const cardBg = this.scene.add.rectangle(cardX, cardY, 220, 280, 0x111827, 1)
        .setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b)
        .setScrollFactor(0)
        .setInteractive({ useHandCursor: true });

      const typeLabel = this.scene.add.text(cardX, cardY - 115, choice.type === 'new_skill' ? '[KỸ NĂNG MỚI]' : '[CƯỜNG HÓA]', {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: choice.type === 'new_skill' ? '#38bdf8' : '#f59e0b',
      }).setOrigin(0.5).setScrollFactor(0);

      const title = this.scene.add.text(cardX, cardY - 75, choice.title, {
        fontFamily: 'monospace',
        fontSize: '15px',
        fontStyle: 'bold',
        color: '#ffffff',
        align: 'center',
        wordWrap: { width: 190 },
      }).setOrigin(0.5).setScrollFactor(0);

      const desc = this.scene.add.text(cardX, cardY + 10, choice.description, {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#94a3b8',
        align: 'center',
        lineSpacing: 4,
        wordWrap: { width: 190 },
      }).setOrigin(0.5).setScrollFactor(0);

      const selectBtn = this.scene.add.text(cardX, cardY + 105, 'LỰA CHỌN', {
        fontFamily: 'monospace',
        fontSize: '13px',
        fontStyle: 'bold',
        color: '#000000',
        backgroundColor: '#ffd700',
        padding: { x: 12, y: 6 },
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

      const handleSelect = () => {
        SoundEffects.playPoETink();
        choice.apply();
        this.hide();
        onChosen();
      };

      // Click vào cả thẻ hoặc nút đều nhận lệnh
      cardBg.on('pointerdown', handleSelect);
      selectBtn.on('pointerdown', handleSelect);

      cardBg.on('pointerover', () => {
        cardBg.setStrokeStyle(3, 0xffffff);
        selectBtn.setBackgroundColor('#ffffff');
      });

      cardBg.on('pointerout', () => {
        cardBg.setStrokeStyle(2, choice.type === 'new_skill' ? 0x38bdf8 : 0xf59e0b);
        selectBtn.setBackgroundColor('#ffd700');
      });

      this.container.add([cardBg, typeLabel, title, desc, selectBtn]);
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

    # 2. Sửa CraftingUI.ts: Sửa nút [MẶC ĐỒ], hiển thị chi tiết chỉ số trang bị trong túi
    "src/scenes/CraftingUI.ts": '''import Phaser from 'phaser';
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

    const bg = this.scene.add.rectangle(cx, cy, 760, 520, 0x090d16, 1.0)
      .setStrokeStyle(2, 0x30363d)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const header = this.scene.add.text(cx, cy - 235, 'HÀNH TRANG & CHẾ TẠO TRANG BỊ [I]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(header);

    // CỘT TRÁI: ĐANG MẶC
    this.itemTitleText = this.scene.add.text(cx - 180, cy - 195, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.itemTitleText);

    this.socketsText = this.scene.add.text(cx - 350, cy - 170, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      lineSpacing: 3,
    }).setScrollFactor(0);
    this.container.add(this.socketsText);

    this.affixesText = this.scene.add.text(cx - 350, cy - 80, '', {
      fontFamily: 'monospace',
      fontSize: '11px',
      color: '#8888ff',
      lineSpacing: 3,
    }).setScrollFactor(0);
    this.container.add(this.affixesText);

    // CỘT PHẢI: TÚI ĐỒ
    const bagTitle = this.scene.add.text(cx + 170, cy - 195, '❖ TÚI ĐỒ (BẤM ĐỂ MẶC ĐỒ):', {
      fontFamily: 'monospace',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#38bdf8',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(bagTitle);

    // CÁC NÚT CRAFTING CURRENCY
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
      }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

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
    }).setOrigin(0.5).setScrollFactor(0).setInteractive({ useHandCursor: true });

    closeBtn.on('pointerdown', () => this.toggle());
    this.container.add(closeBtn);
  }

  // TRÁO ĐỒ TỪ TÚI LÊN NGƯỜI
  private equipFromBag(index: number): void {
    if (index >= this.inventoryData.bag.length) return;
    const itemToEquip = this.inventoryData.bag[index];
    const oldItem = this.inventoryData.equippedItem;

    this.inventoryData.equippedItem = itemToEquip;
    this.inventoryData.bag[index] = oldItem;

    SoundEffects.playPoETink();
    this.onItemUpdated(); // Cập nhật lại chỉ số người chơi ngay lập tức
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

    // XÓA PHẦN TỬ CŨ CỦA TÚI ĐỒ VÀ VẼ LẠI
    this.bagElements.forEach((el) => el.destroy());
    this.bagElements = [];

    const cx = this.scene.scale.width / 2;
    const cy = this.scene.scale.height / 2;

    if (this.inventoryData.bag.length === 0) {
      const emptyText = this.scene.add.text(cx + 40, cy - 140, '(Túi trống - Đánh quái để nhặt đồ)', {
        fontFamily: 'monospace',
        fontSize: '12px',
        color: '#64748b',
      }).setScrollFactor(0);
      this.bagElements.push(emptyText);
      this.container.add(emptyText);
    } else {
      this.inventoryData.bag.forEach((bagItem, idx) => {
        const itemY = cy - 150 + idx * 46;
        const rColor = bagItem.rarity === 'Rare' ? '#ffd700' : bagItem.rarity === 'Magic' ? '#60a5fa' : '#ffffff';

        // Tóm tắt chỉ số
        const statsSummary = [...bagItem.prefixes, ...bagItem.suffixes].map((a) => `+${a.value} ${a.statType}`).slice(0, 2).join(', ');

        const nameTxt = this.scene.add.text(cx + 20, itemY, `[${bagItem.rarity}] ${bagItem.baseType}\\n${statsSummary ? '(' + statsSummary + ')' : ''}`, {
          fontFamily: 'monospace',
          fontSize: '11px',
          fontStyle: 'bold',
          color: rColor,
        }).setScrollFactor(0);

        const equipBtn = this.scene.add.text(cx + 260, itemY + 4, 'MẶC ĐỒ', {
          fontFamily: 'monospace',
          fontSize: '12px',
          fontStyle: 'bold',
          color: '#000000',
          backgroundColor: '#38bdf8',
          padding: { x: 8, y: 5 },
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
      btn.setText(`${type.toUpperCase()}\\n(Còn: ${count})`);
      btn.setAlpha(count > 0 ? 1 : 0.4);
    });
  }
}
''',

    # 3. Sửa PassiveTreeUI.ts: Dùng Zone tàng hình bọc quanh mỗi node, bắt click 100% chuẩn xác
    "src/scenes/PassiveTreeUI.ts": '''import Phaser from 'phaser';
import { PassiveTreeManager } from '../core/passive/PassiveTreeManager';
import { PASSIVE_TREE_NODES } from '../core/passive/PassiveTreeData';
import { SoundEffects } from '../core/audio/SoundEffects';

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

    const bg = this.scene.add.rectangle(cx, cy, 760, 520, 0x070a10, 1.0)
      .setStrokeStyle(2, 0x30363d)
      .setScrollFactor(0)
      .setInteractive();
    this.container.add(bg);

    const title = this.scene.add.text(cx, cy - 230, 'CÂY KỸ NĂNG NỘI TẠI (PASSIVE TREE) [P]', {
      fontFamily: 'monospace',
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffd700',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(title);

    this.pointsText = this.scene.add.text(cx, cy - 200, '', {
      fontFamily: 'monospace',
      fontSize: '15px',
      fontStyle: 'bold',
      color: '#00ffff',
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.pointsText);

    this.linesGraphics = this.scene.add.graphics().setScrollFactor(0);
    this.container.add(this.linesGraphics);

    this.tooltipText = this.scene.add.text(cx, cy + 235, 'Di chuột vào node để xem mô tả. Nhấp chuột để nâng cấp.', {
      fontFamily: 'monospace',
      fontSize: '12px',
      color: '#c9d1d9',
      backgroundColor: '#161b22',
      padding: { x: 10, y: 5 },
    }).setOrigin(0.5).setScrollFactor(0);
    this.container.add(this.tooltipText);

    for (const [id, node] of Object.entries(PASSIVE_TREE_NODES)) {
      const nx = cx + node.gridX;
      const ny = cy + node.gridY;
      const radius = node.nodeType === 'keystone' ? 17 : node.nodeType === 'notable' ? 13 : 10;

      const circle = this.scene.add.circle(nx, ny, radius, 0x333333).setScrollFactor(0);
      circle.setStrokeStyle(2, 0x666666);

      const label = this.scene.add.text(nx, ny, node.name.slice(0, 1), {
        fontFamily: 'monospace',
        fontSize: '11px',
        fontStyle: 'bold',
        color: '#ffffff',
      }).setOrigin(0.5).setScrollFactor(0);

      // TẠO ZONE HIT AREA RỘNG 38x38 CÓ SCROLLFACTOR(0) ĐỂ BẮT CLICK TUYỆT ĐỐI CHUẨN XÁC
      const hitZone = this.scene.add.zone(nx, ny, 38, 38)
        .setScrollFactor(0)
        .setInteractive({ useHandCursor: true });

      hitZone.on('pointerdown', () => {
        if (this.treeManager.allocate(id)) {
          SoundEffects.playPoETink();
          this.onTreeChanged();
          this.refresh();
        }
      });

      hitZone.on('pointerover', () => {
        const status = this.treeManager.allocatedNodeIds.has(id)
          ? '[ĐÃ HỌC]'
          : this.treeManager.canAllocate(id)
          ? '[CÓ THỂ HỌC]'
          : '[CHƯA ĐỦ ĐIỀU KIỆN]';
        this.tooltipText.setText(`${node.name} ${status} - ${node.description}`);
      });

      hitZone.on('pointerout', () => {
        this.tooltipText.setText('Di chuột vào node để xem mô tả. Nhấp chuột để nâng cấp.');
      });

      this.nodeSprites.set(id, { circle, text: label });
      this.container.add([circle, label, hitZone]);
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

    # 4. Sửa Projectile.ts: Gán đúng Texture cho tất cả các kỹ năng mới
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

    let texKey = 'proj_fireball';
    if (ctx.id === 'split_arrow') texKey = 'proj_arrow';
    else if (ctx.id === 'ground_slam') texKey = 'proj_slam';
    else if (ctx.id === 'frostbolt') texKey = 'proj_frostbolt';
    else if (ctx.id === 'spark') texKey = 'proj_spark';
    else if (ctx.id === 'blade_vortex') texKey = 'proj_blade';

    this.setTexture(texKey);
    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      if (ctx.id === 'ground_slam') {
        body.setSize(24, 24);
      } else if (ctx.id === 'blade_vortex') {
        body.setSize(20, 16);
      } else {
        body.setSize(12, 12);
      }
      this.scene.physics.velocityFromRotation(angleRad, ctx.projectileSpeed, body.velocity);
    }

    const lifeTime = ctx.id === 'ground_slam' ? 500 : ctx.id === 'blade_vortex' ? 1200 : 2500;
    this.scene.time.delayedCall(lifeTime, () => {
      if (this.active) this.kill();
    });
  }

  kill(): void {
    this.disableBody(true, true);
  }
}
'''
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Đã sửa tương tác: {path}")

print("\nHoàn tất sửa lỗi! Toàn bộ nút chọn kỹ năng, mặc đồ và nâng cấp thiên phú đã sẵn sàng.")