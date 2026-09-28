import Phaser from 'phaser';
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
