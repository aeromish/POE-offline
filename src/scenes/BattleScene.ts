import Phaser from 'phaser';
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
      'BẠN ĐÃ TỬ NẠN!\nNhấn [SPACE] để Hồi Sinh',
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
