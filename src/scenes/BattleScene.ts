import Phaser from 'phaser';
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
      name: 'Vũ khí Sắt Rèn',
      baseType: 'Sword',
      tier: 1,
      rarity: 'Normal',
      prefixes: [],
      suffixes: [],
    },
    bag: [],
  };

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
  private bestWaveText!: Phaser.GameObjects.Text;
  private classLevelText!: Phaser.GameObjects.Text;
  private lifeBarGfx!: Phaser.GameObjects.Graphics;
  private esBarGfx!: Phaser.GameObjects.Graphics;
  private expBarGfx!: Phaser.GameObjects.Graphics;

  // HUD THANH KỸ NĂNG CHÍNH (SKILL BAR)
  private skillBarContainer!: Phaser.GameObjects.Container;
  private skillSlotWidgets: { bg: Phaser.GameObjects.Rectangle; icon: Phaser.GameObjects.Text; lvl: Phaser.GameObjects.Text; cdGfx: Phaser.GameObjects.Graphics; id: string }[] = [];

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

    // Va chạm: Nhặt đồ
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
          this.showPickupNotice(loot.x, loot.y, `TÚI ĐÃ ĐẦY!`);
        }
      } else if (d.category === 'gem' && d.gemId) {
        this.player.addOrUpgradeSkill(d.gemId);
        this.syncPlayerStats();
        this.showPickupNotice(loot.x, loot.y, `HỌC NGỌC: ${d.name}`);
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
    this.createSkillBarHUD(); // HUD THANH KỸ NĂNG
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

  // TẠO HUD THANH KỸ NĂNG Ở DƯỚI ĐÁY MÀN HÌNH
  private createSkillBarHUD(): void {
    this.skillBarContainer = this.add.container(0, 0).setScrollFactor(0).setDepth(200);
    this.rebuildSkillBarWidgets();
  }

  private rebuildSkillBarWidgets(): void {
    this.skillBarContainer.removeAll(true);
    this.skillSlotWidgets = [];

    const skills = this.player.compiledSkills;
    const startX = this.scale.width / 2 - (skills.length * 60) / 2 + 30;
    const slotY = this.scale.height - 50;

    skills.forEach((skill, idx) => {
      const slotX = startX + idx * 60;

      const bg = this.add.rectangle(slotX, slotY, 50, 50, 0x111827, 0.95)
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

  // BẢNG 3 LỰA CHỌN KHI LÊN CẤP
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
        id: 'blade_vortex',
        title: 'Blade Vortex (Bão Kiếm)',
        description: 'Tạo các lưỡi kiếm xoay vòng chém liên tục quái áp sát.',
        type: 'new_skill',
        skillId: 'blade_vortex',
        apply: () => {
          this.player.addOrUpgradeSkill('blade_vortex');
          this.syncPlayerStats();
        },
      },
      {
        id: 'upgrade_main',
        title: 'Cường Hóa Kỹ Năng Hiện Có',
        description: '+1 Level cho toàn bộ kỹ năng đang trang bị (+30% Sát thương).',
        type: 'upgrade_skill',
        apply: () => {
          this.player.compiledSkills.forEach((s) => this.player.addOrUpgradeSkill(s.id));
          this.syncPlayerStats();
        },
      },
      {
        id: 'vitality_boost',
        title: 'Thể Lực Bất Hoại',
        description: '+50 Máu Tối Đa và +20 Tốc Độ Di Chuyển.',
        type: 'stat_boost',
        apply: () => {
          this.player.stats.maxLife += 50;
          this.player.stats.currentLife = this.player.stats.maxLife;
          this.player.stats.movementSpeed += 20;
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
      this.rebuildSkillBarWidgets();
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

    const craftBtn = this.add.text(rx, 90, '⚒️ HÒM & RÈN TIER (I)', {
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

    // Cập nhật hiệu ứng Hồi Chiêu trên thanh Kỹ Năng
    this.skillSlotWidgets.forEach((w) => {
      w.cdGfx.clear();
      const cdPct = this.player.getCooldownPercent(w.id, time);
      if (cdPct > 0) {
        w.cdGfx.fillStyle(0x000000, 0.65);
        w.cdGfx.fillRect(w.bg.x - 25, w.bg.y - 25 + 50 * (1 - cdPct), 50, 50 * cdPct);
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
      this.characterUI.getIsOpen() ||
      this.levelUpUI.getIsShowing();

    if (isUIBlocking) {
      const body = this.player.body as Phaser.Physics.Arcade.Body;
      if (body) body.setVelocity(0, 0);
      return;
    }

    this.player.update(time, delta);
    this.renderHUD(time);

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
