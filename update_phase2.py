import os

files = {
    "src/core/gems/GemTypes.ts": '''export type DamageType = 'physical' | 'fire' | 'cold' | 'lightning';

export interface SkillContext {
  id: string;
  name: string;
  damageType: DamageType;
  baseMinDamage: number;
  baseMaxDamage: number;
  addedMinDamage: number;
  addedMaxDamage: number;
  attackSpeedMultiplier: number;
  baseCooldown: number;
  projectileCount: number;
  projectileSpeed: number;
  pierceCount: number;
  aoeRadius: number;
  critChance: number;
  critMultiplier: number;
  increasedDamagePercent: number;
  moreDamageMultipliers: number[];
}

export type SupportModifier = (ctx: SkillContext) => void;

export interface SupportGem {
  id: string;
  name: string;
  color: 'red' | 'green' | 'blue';
  apply: SupportModifier;
}

export interface ActiveGem {
  id: string;
  name: string;
  color: 'red' | 'green' | 'blue';
  getInitialContext: () => SkillContext;
}

export interface Socket {
  color: 'red' | 'green' | 'blue';
  linkGroup: number;
  gem: ActiveGem | SupportGem | null;
}
''',

    "src/core/gems/SupportGems.ts": '''import { SupportGem } from './GemTypes';

export const GreaterMultipleProjectiles: SupportGem = {
  id: 'gmp',
  name: 'Greater Multiple Projectiles',
  color: 'green',
  apply: (ctx) => {
    ctx.projectileCount += 4;
    ctx.moreDamageMultipliers.push(0.74);
  },
};

export const PierceSupport: SupportGem = {
  id: 'pierce',
  name: 'Pierce Support',
  color: 'green',
  apply: (ctx) => {
    ctx.pierceCount += 2;
    ctx.moreDamageMultipliers.push(1.15);
  },
};

export const AddedFireDamageSupport: SupportGem = {
  id: 'added_fire',
  name: 'Added Fire Damage',
  color: 'red',
  apply: (ctx) => {
    ctx.addedMinDamage += 8;
    ctx.addedMaxDamage += 15;
    ctx.increasedDamagePercent += 20;
  },
};

export const FasterAttacksSupport: SupportGem = {
  id: 'faster_attacks',
  name: 'Faster Attacks Support',
  color: 'green',
  apply: (ctx) => {
    ctx.attackSpeedMultiplier *= 1.35;
  },
};
''',

    "src/core/gems/ActiveGems.ts": '''import { ActiveGem, SkillContext } from './GemTypes';

export const FireballSkill: ActiveGem = {
  id: 'fireball',
  name: 'Fireball',
  color: 'blue',
  getInitialContext: (): SkillContext => ({
    id: 'fireball',
    name: 'Fireball',
    damageType: 'fire',
    baseMinDamage: 25,
    baseMaxDamage: 40,
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
  name: 'Split Arrow',
  color: 'green',
  getInitialContext: (): SkillContext => ({
    id: 'split_arrow',
    name: 'Split Arrow',
    damageType: 'physical',
    baseMinDamage: 18,
    baseMaxDamage: 32,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 1.2,
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
  name: 'Ground Slam',
  color: 'red',
  getInitialContext: (): SkillContext => ({
    id: 'ground_slam',
    name: 'Ground Slam',
    damageType: 'physical',
    baseMinDamage: 40,
    baseMaxDamage: 75,
    addedMinDamage: 0,
    addedMaxDamage: 0,
    attackSpeedMultiplier: 0.85,
    baseCooldown: 900,
    projectileCount: 1,
    projectileSpeed: 220,
    pierceCount: 99,
    aoeRadius: 70,
    critChance: 5,
    critMultiplier: 1.5,
    increasedDamagePercent: 0,
    moreDamageMultipliers: [],
  }),
};
''',

    "src/core/combat/DamageEngine.ts": '''import { SkillContext, DamageType } from '../gems/GemTypes';
import { PoEStats } from '../stats/CharacterStats';

export interface HitResult {
  damage: number;
  isCrit: boolean;
  type: DamageType;
  absorbedByES: number;
  absorbedByLife: number;
}

export class DamageEngine {
  public static calculateHit(skill: SkillContext, targetStats: PoEStats): HitResult {
    const isEvaded = Math.random() * 100 < targetStats.evasion;
    if (isEvaded) {
      return { damage: 0, isCrit: false, type: skill.damageType, absorbedByES: 0, absorbedByLife: 0 };
    }

    const rawMin = skill.baseMinDamage + skill.addedMinDamage;
    const rawMax = skill.baseMaxDamage + skill.addedMaxDamage;
    const rawDamage = rawMin + Math.random() * (rawMax - rawMin);

    const incMultiplier = 1 + skill.increasedDamagePercent / 100;
    const moreMultiplier = skill.moreDamageMultipliers.reduce((acc, cur) => acc * cur, 1.0);

    let damage = rawDamage * incMultiplier * moreMultiplier;

    const isCrit = Math.random() * 100 < skill.critChance;
    if (isCrit) {
      damage *= skill.critMultiplier;
    }

    if (skill.damageType === 'physical') {
      const armourReduction = targetStats.armour / (targetStats.armour + 5 * damage);
      damage *= 1 - Math.min(armourReduction, 0.9);
    }

    const finalDamage = Math.max(1, Math.round(damage));

    let remaining = finalDamage;
    let absorbedES = 0;
    let absorbedLife = 0;

    if (targetStats.energyShield > 0) {
      absorbedES = Math.min(targetStats.energyShield, remaining);
      targetStats.energyShield -= absorbedES;
      remaining -= absorbedES;
    }

    if (remaining > 0) {
      absorbedLife = Math.min(targetStats.currentLife, remaining);
      targetStats.currentLife -= absorbedLife;
    }

    return {
      damage: finalDamage,
      isCrit,
      type: skill.damageType,
      absorbedByES: absorbedES,
      absorbedByLife: absorbedLife,
    };
  }
}
''',

    "src/scenes/Projectile.ts": '''import Phaser from 'phaser';
import { SkillContext } from '../core/gems/GemTypes';

export class Projectile extends Phaser.Physics.Arcade.Sprite {
  public skillCtx!: SkillContext;
  public remainingPierce: number = 0;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'bullet_texture');
  }

  fire(x: number, y: number, angleRad: number, ctx: SkillContext): void {
    this.skillCtx = ctx;
    this.remainingPierce = ctx.pierceCount;

    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      body.setSize(12, 12);
      this.scene.physics.velocityFromRotation(angleRad, ctx.projectileSpeed, body.velocity);
    }

    this.scene.time.delayedCall(2500, () => {
      if (this.active) this.kill();
    });
  }

  kill(): void {
    this.disableBody(true, true);
  }
}
''',

    "src/scenes/DummyEnemy.ts": '''import Phaser from 'phaser';
import { PoEStats } from '../core/stats/CharacterStats';

export class DummyEnemy extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  private maxLife: number;

  constructor(scene: Phaser.Scene, x: number, y: number, isTanky: boolean = false) {
    super(scene, x, y, 'dummy_texture');

    this.maxLife = isTanky ? 1500 : 300;
    this.stats = {
      maxLife: this.maxLife,
      currentLife: this.maxLife,
      energyShield: isTanky ? 0 : 100,
      maxEnergyShield: isTanky ? 0 : 100,
      armour: isTanky ? 80 : 10,
      evasion: isTanky ? 0 : 15,
      movementSpeed: 0,
      esRechargeDelay: 3,
    };

    scene.add.existing(this);
    scene.physics.add.existing(this, true);
  }

  takeDamage(): void {
    if (this.stats.currentLife <= 0) {
      this.stats.currentLife = this.maxLife;
      this.stats.energyShield = this.stats.maxEnergyShield;
    }
  }
}
''',

    "src/scenes/CombatUI.ts": '''import Phaser from 'phaser';
import { HitResult } from '../core/combat/DamageEngine';

export class CombatUI {
  public static showDamageText(scene: Phaser.Scene, x: number, y: number, hit: HitResult): void {
    if (hit.damage === 0) {
      const missText = scene.add.text(x, y - 10, 'EVADED', {
        fontFamily: 'monospace',
        fontSize: '14px',
        color: '#aaaaaa',
      }).setOrigin(0.5);

      scene.tweens.add({
        targets: missText,
        y: y - 35,
        alpha: 0,
        duration: 600,
        onComplete: () => missText.destroy(),
      });
      return;
    }

    const color = hit.isCrit
      ? '#ffdd00'
      : hit.type === 'fire'
      ? '#ff4500'
      : '#ffffff';

    const fontSize = hit.isCrit ? '22px' : '15px';
    const textStr = hit.isCrit ? `${hit.damage}!` : `${hit.damage}`;

    const dmgText = scene.add.text(x + (Math.random() * 20 - 10), y - 15, textStr, {
      fontFamily: 'monospace',
      fontSize,
      fontStyle: hit.isCrit ? 'bold' : 'normal',
      color,
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5);

    scene.tweens.add({
      targets: dmgText,
      y: y - 45,
      alpha: 0,
      duration: 800,
      ease: 'Cubic.easeOut',
      onComplete: () => dmgText.destroy(),
    });
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

  update(): void {
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
  }
}
''',

    "src/scenes/BattleScene.ts": '''import Phaser from 'phaser';
import { Player } from './Player';
import { Projectile } from './Projectile';
import { DummyEnemy } from './DummyEnemy';
import { DamageEngine } from '../core/combat/DamageEngine';
import { CombatUI } from './CombatUI';

export class BattleScene extends Phaser.Scene {
  private player!: Player;
  private projectilePool!: Phaser.Physics.Arcade.Group;
  private dummies!: Phaser.Physics.Arcade.Group;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2000;
    const mapHeight = 2000;

    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    this.createProceduralTextures();

    this.add.grid(mapWidth / 2, mapHeight / 2, mapWidth, mapHeight, 64, 64, 0x161b22, 1, 0x21262d, 1);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Mage');

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.3);

    this.projectilePool = this.physics.add.group({
      classType: Projectile,
      maxSize: 100,
      runChildUpdate: false,
    });

    this.dummies = this.physics.add.group({ runChildUpdate: false });
    this.dummies.add(new DummyEnemy(this, mapWidth / 2 + 150, mapHeight / 2 - 50, false));
    this.dummies.add(new DummyEnemy(this, mapWidth / 2 + 250, mapHeight / 2 + 50, true));

    this.physics.add.overlap(
      this.projectilePool,
      this.dummies,
      (projObj, dummyObj) => {
        const proj = projObj as Projectile;
        const dummy = dummyObj as DummyEnemy;

        if (!proj.active) return;

        const hit = DamageEngine.calculateHit(proj.skillCtx, dummy.stats);
        dummy.takeDamage();

        CombatUI.showDamageText(this, dummy.x, dummy.y, hit);

        if (proj.remainingPierce > 0) {
          proj.remainingPierce--;
        } else {
          proj.kill();
        }
      }
    );

    this.add.text(20, 20, 'Nhấp chuột trái: Bắn kỹ năng\\nWASD / Mũi tên: Di chuyển', {
      fontFamily: 'monospace',
      fontSize: '14px',
      color: '#ffffff',
      backgroundColor: '#00000088',
      padding: { x: 8, y: 6 },
    }).setScrollFactor(0);
  }

  private createProceduralTextures(): void {
    if (!this.textures.exists('bullet_texture')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0xff8c00, 1);
      g.fillCircle(6, 6, 6);
      g.fillStyle(0xffffcc, 1);
      g.fillCircle(6, 6, 3);
      g.generateTexture('bullet_texture', 12, 12);
      g.destroy();
    }

    if (!this.textures.exists('dummy_texture')) {
      const g = this.make.graphics({ x: 0, y: 0 });
      g.fillStyle(0x7c0a02, 1);
      g.fillRect(0, 0, 28, 28);
      g.lineStyle(2, 0xffffff, 0.8);
      g.strokeRect(0, 0, 28, 28);
      g.generateTexture('dummy_texture', 28, 28);
      g.destroy();
    }
  }

  update(time: number): void {
    this.player.update();

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

print("\nĐã đồng bộ toàn bộ Giai đoạn 2!")