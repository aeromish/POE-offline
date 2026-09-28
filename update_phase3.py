import os

files = {
    "src/core/monsters/MonsterTypes.ts": '''export type MonsterRarity = 'Normal' | 'Magic' | 'Rare' | 'Boss';

export interface MonsterAffix {
  id: string;
  name: string;
  color: string;
  apply: (stats: MonsterStats) => void;
}

export interface MonsterStats {
  maxLife: number;
  currentLife: number;
  damage: number;
  movementSpeed: number;
  armour: number;
  evasion: number;
  rarity: MonsterRarity;
  affixes: MonsterAffix[];
  expReward: number;
}
''',

    "src/core/monsters/MonsterAffixes.ts": '''import { MonsterAffix } from './MonsterTypes';

export const MONSTER_AFFIXES: MonsterAffix[] = [
  {
    id: 'haste',
    name: 'Haste Aura',
    color: '#00ffff',
    apply: (stats) => {
      stats.movementSpeed *= 1.35;
    },
  },
  {
    id: 'extra_fire',
    name: 'Extra Fire Damage',
    color: '#ff4400',
    apply: (stats) => {
      stats.damage *= 1.4;
    },
  },
  {
    id: 'armoured',
    name: 'Armoured',
    color: '#ffd700',
    apply: (stats) => {
      stats.armour += 60;
      stats.maxLife = Math.round(stats.maxLife * 1.3);
      stats.currentLife = stats.maxLife;
    },
  },
];
''',

    "src/core/monsters/WaveManager.ts": '''import { MonsterStats, MonsterRarity, MonsterAffix } from './MonsterTypes';
import { MONSTER_AFFIXES } from './MonsterAffixes';

export class WaveManager {
  public currentWave: number = 1;
  public waveDuration: number = 45; // 45 giây mỗi wave
  public timeRemaining: number = 45;
  public isWaveActive: boolean = true;

  public getMonsterStats(wave: number): MonsterStats {
    // Công thức Endless Scaling PoE: +15% HP và +8% Damage mỗi đợt
    const hpScale = Math.pow(1.15, wave - 1);
    const dmgScale = Math.pow(1.08, wave - 1);

    const roll = Math.random();
    let rarity: MonsterRarity = 'Normal';

    if (wave % 5 === 0 && roll < 0.25) {
      rarity = 'Boss';
    } else if (wave >= 3 && roll < 0.15) {
      rarity = 'Rare';
    } else if (roll < 0.4) {
      rarity = 'Magic';
    }

    let baseHp = 35 * hpScale;
    let baseDmg = 7 * dmgScale;
    let speed = 80 + Math.min(50, wave * 2);
    let armour = wave * 4;
    let exp = 10 * wave;
    const affixes: MonsterAffix[] = [];

    if (rarity === 'Magic') {
      baseHp *= 1.8;
      baseDmg *= 1.25;
      exp *= 2.5;
      const aff = MONSTER_AFFIXES[Math.floor(Math.random() * MONSTER_AFFIXES.length)];
      affixes.push(aff);
    } else if (rarity === 'Rare') {
      baseHp *= 4.5;
      baseDmg *= 1.6;
      exp *= 6;
      const shuffled = [...MONSTER_AFFIXES].sort(() => 0.5 - Math.random());
      affixes.push(shuffled[0], shuffled[1]);
    } else if (rarity === 'Boss') {
      baseHp *= 15;
      baseDmg *= 2.2;
      speed *= 0.85;
      exp *= 20;
      affixes.push(...MONSTER_AFFIXES);
    }

    const stats: MonsterStats = {
      maxLife: Math.max(1, Math.round(baseHp)),
      currentLife: Math.max(1, Math.round(baseHp)),
      damage: Math.max(1, Math.round(baseDmg)),
      movementSpeed: Math.round(speed),
      armour: Math.round(armour),
      evasion: Math.min(30, 5 + wave),
      rarity,
      affixes: [],
      expReward: Math.round(exp),
    };

    for (const aff of affixes) {
      aff.apply(stats);
      stats.affixes.push(aff);
    }

    return stats;
  }
}
''',

    "src/scenes/Monster.ts": '''import Phaser from 'phaser';
import { MonsterStats } from '../core/monsters/MonsterTypes';
import { PoEStats } from '../core/stats/CharacterStats';

export class Monster extends Phaser.Physics.Arcade.Sprite {
  public monsterStats!: MonsterStats;
  public poeStatsWrapper!: PoEStats;
  private hpBar!: Phaser.GameObjects.Graphics;
  private lastAttackTime: number = 0;
  private attackCooldown: number = 700; // 700ms cắn 1 lần

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'monster_normal');
    this.hpBar = scene.add.graphics();
  }

  public spawn(x: number, y: number, stats: MonsterStats): void {
    this.monsterStats = stats;
    this.poeStatsWrapper = {
      maxLife: stats.maxLife,
      currentLife: stats.currentLife,
      energyShield: 0,
      maxEnergyShield: 0,
      armour: stats.armour,
      evasion: stats.evasion,
      movementSpeed: stats.movementSpeed,
      esRechargeDelay: 0,
    };

    this.enableBody(true, x, y, true, true);
    this.setTexture(`monster_${stats.rarity.toLowerCase()}`);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      const size = stats.rarity === 'Boss' ? 44 : stats.rarity === 'Rare' ? 32 : 22;
      body.setSize(size, size);
      this.setDisplaySize(size, size);
    }

    this.hpBar.setVisible(true);
    this.updateHpBar();
  }

  public updateAI(targetX: number, targetY: number): void {
    if (!this.active) return;

    const angle = Phaser.Math.Angle.Between(this.x, this.y, targetX, targetY);
    const speed = this.monsterStats.movementSpeed;
    const body = this.body as Phaser.Physics.Arcade.Body;

    if (body) {
      this.scene.physics.velocityFromRotation(angle, speed, body.velocity);
    }

    this.updateHpBar();
  }

  public canAttack(time: number): boolean {
    if (time - this.lastAttackTime > this.attackCooldown) {
      this.lastAttackTime = time;
      return true;
    }
    return false;
  }

  public syncLifeAfterHit(): boolean {
    this.monsterStats.currentLife = this.poeStatsWrapper.currentLife;
    this.updateHpBar();
    return this.monsterStats.currentLife <= 0;
  }

  private updateHpBar(): void {
    this.hpBar.clear();
    if (!this.active) return;

    const width = this.monsterStats.rarity === 'Boss' ? 48 : 26;
    const height = 4;
    const x = this.x - width / 2;
    const y = this.y - (this.displayHeight / 2 + 8);

    // Nền xám
    this.hpBar.fillStyle(0x000000, 0.7);
    this.hpBar.fillRect(x, y, width, height);

    // Máu đỏ / vàng
    const pct = Math.max(0, this.monsterStats.currentLife / this.monsterStats.maxLife);
    const color = this.monsterStats.rarity === 'Boss' ? 0xff0044 : 0x00ff66;
    this.hpBar.fillStyle(color, 1);
    this.hpBar.fillRect(x, y, width * pct, height);
  }

  public kill(): void {
    this.hpBar.clear();
    this.hpBar.setVisible(false);
    this.disableBody(true, true);
  }
}
''',

    "src/scenes/Player.ts": '''import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
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

  public compileSkills(): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    for (const activeSock of activeSockets) {
      const activeGem = activeSock.gem as ActiveGem;
      const ctx = activeGem.getInitialContext();

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
    // 1. Evasion Entropy
    if (Math.random() * 100 < this.stats.evasion) {
      return false; // Né thành công
    }

    // 2. Armour Mitigation
    const dr = this.stats.armour / (this.stats.armour + 5 * rawDamage);
    const damage = Math.max(1, Math.round(rawDamage * (1 - Math.min(dr, 0.9))));

    this.lastHitTime = time;

    // 3. Trừ Khiên Năng Lượng trước, Máu sau
    let remaining = damage;
    if (this.stats.energyShield > 0) {
      const absorbed = Math.min(this.stats.energyShield, remaining);
      this.stats.energyShield -= absorbed;
      remaining -= absorbed;
    }

    if (remaining > 0) {
      this.stats.currentLife = Math.max(0, this.stats.currentLife - remaining);
    }

    // Nhấp nháy đỏ báo hiệu nhận đòn
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

    // PoE Mechanics: Hồi phục Energy Shield sau X giây không dính đòn
    if (
      this.stats.maxEnergyShield > 0 &&
      this.stats.energyShield < this.stats.maxEnergyShield &&
      time - this.lastHitTime > this.stats.esRechargeDelay * 1000
    ) {
      const rechargeRate = (this.stats.maxEnergyShield * 0.25 * delta) / 1000; // Hồi 25% ES mỗi giây
      this.stats.energyShield = Math.min(this.stats.maxEnergyShield, this.stats.energyShield + rechargeRate);
    }
  }
}
''',

    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { Monster } from './Monster';
import { WaveManager } from '../core/monsters/WaveManager';
import { DamageEngine } from '../core/combat/DamageEngine';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private monsterPool!: Phaser.Physics.Arcade.Group;
  private waveManager: WaveManager = new WaveManager();

  private waveText!: Phaser.GameObjects.Text;
  private timerText!: Phaser.GameObjects.Text;
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

    this.createMonsterTextures();

    // Map sàn
    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    // Object Pooling
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

    // Va chạm: Đạn -> Quái
    this.physics.add.overlap(this.projectilePool, this.monsterPool, (projObj, monObj) => {
      const proj = projObj as Projectile;
      const monster = monObj as Monster;

      if (!proj.active || !monster.active) return;

      const hit = DamageEngine.calculateHit(proj.skillCtx, monster.poeStatsWrapper);
      const isDead = monster.syncLifeAfterHit();

      CombatUI.showDamageText(this, monster.x, monster.y, hit);

      if (isDead) {
        monster.kill();
      }

      if (proj.remainingPierce > 0) {
        proj.remainingPierce--;
      } else {
        proj.kill();
      }
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

    // Spawner lặp lại mỗi 1.2s
    this.time.addEvent({
      delay: 1200,
      callback: this.spawnMonsterWave,
      callbackScope: this,
      loop: true,
    });

    // Bộ đếm lùi Wave (mỗi giây)
    this.time.addEvent({
      delay: 1000,
      callback: this.tickWaveTimer,
      callbackScope: this,
      loop: true,
    });
  }

  private createMonsterTextures(): void {
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

    // Nền thanh máu
    this.lifeBarGfx.fillStyle(0x000000, 0.7);
    this.lifeBarGfx.fillRect(x, y, barW, barH);

    // Máu đỏ
    const lifePct = Math.max(0, this.player.stats.currentLife / this.player.stats.maxLife);
    this.lifeBarGfx.fillStyle(0xdc143c, 1);
    this.lifeBarGfx.fillRect(x, y, barW * lifePct, barH);

    // Khiên Energy Shield xanh dương xếp đè phía trên
    if (this.player.stats.maxEnergyShield > 0) {
      const esPct = Math.max(0, this.player.stats.energyShield / this.player.stats.maxEnergyShield);
      this.esBarGfx.fillStyle(0x1e90ff, 0.85);
      this.esBarGfx.fillRect(x, y - 8, barW * esPct, 6);
    }
  }

  private spawnMonsterWave(): void {
    if (this.isGameOver || !this.waveManager.isWaveActive) return;

    // Sinh 3 - 6 quái vật ở viền ngoài camera
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
    if (this.isGameOver) return;

    this.waveManager.timeRemaining--;
    this.timerText.setText(`THỜI GIAN: ${this.waveManager.timeRemaining}s`);

    if (this.waveManager.timeRemaining <= 0) {
      // Chuyển đợt mới
      this.waveManager.currentWave++;
      this.waveManager.timeRemaining = this.waveManager.waveDuration;
      this.waveText.setText(`ĐỢT: ${this.waveManager.currentWave}`);

      // Xóa quái cũ để bắt đầu đợt mới dồn dập hơn
      this.monsterPool.children.each((child) => {
        const mon = child as Monster;
        if (mon.active) mon.kill();
        return true;
      });

      const clearBanner = this.add.text(
        this.scale.width / 2,
        this.scale.height / 3,
        `VƯỢT QUA ĐỢT ${this.waveManager.currentWave - 1}!\\nĐỘ KHÓ TĂNG LÊN!`,
        {
          fontFamily: 'monospace',
          fontSize: '28px',
          fontStyle: 'bold',
          color: '#ffd700',
          align: 'center',
          backgroundColor: '#000000cc',
          padding: { x: 16, y: 10 },
        }
      ).setOrigin(0.5).setScrollFactor(0);

      this.tweens.add({
        targets: clearBanner,
        alpha: 0,
        duration: 2500,
        onComplete: () => clearBanner.destroy(),
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

    this.player.update(time, delta);
    this.renderHUD();

    // Điều khiển AI toàn bộ quái vật hướng về người chơi
    this.monsterPool.children.each((child) => {
      const mon = child as Monster;
      if (mon.active) {
        mon.updateAI(this.player.x, this.player.y);
      }
      return true;
    });

    // Nhấp chuột trái để bắn kỹ năng
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

print("\nHoàn tất cài đặt Giai đoạn 3: Monster AI, Wave Scaling & Survival Combat!")