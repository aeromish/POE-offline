import Phaser from 'phaser';
import { CharacterClass, CLASS_BASE_STATS, PoEStats, getExpNeeded } from '../core/stats/CharacterStats';
import { Socket, SkillContext, ActiveGem, SupportGem } from '../core/gems/GemTypes';
import { FireballSkill, SplitArrowSkill, GroundSlamSkill, ALL_ACTIVE_SKILLS } from '../core/gems/ActiveGems';
import { GreaterMultipleProjectiles, AddedFireDamageSupport, PierceSupport } from '../core/gems/SupportGems';
import { EquippedSlots } from '../core/items/ItemTypes';
import { PassiveTreeBonus } from '../core/passive/PassiveTreeTypes';
import { Projectile } from './Projectile';

export class Player extends Phaser.Physics.Arcade.Sprite {
  public stats: PoEStats;
  public characterClass: CharacterClass;
  public sockets: Socket[] = [];
  public compiledSkills: SkillContext[] = [];

  public pickupRadius: number = 160;
  public expBonusPct: number = 0;

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
      this.skillBonusLevels.set('fireball', 1);
    } else if (this.characterClass === 'Archer') {
      this.sockets = [
        { color: 'green', linkGroup: 1, gem: SplitArrowSkill },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
      ];
      this.skillBonusLevels.set('split_arrow', 1);
    } else {
      this.sockets = [
        { color: 'red', linkGroup: 1, gem: GroundSlamSkill },
        { color: 'red', linkGroup: 1, gem: AddedFireDamageSupport },
        { color: 'green', linkGroup: 1, gem: PierceSupport },
      ];
      this.skillBonusLevels.set('ground_slam', 1);
    }
  }

  public addOrUpgradeSkill(skillId: string): void {
    const curLvl = this.skillBonusLevels.get(skillId) || 0;
    this.skillBonusLevels.set(skillId, curLvl + 1);

    const existing = this.sockets.find((s) => s.gem && s.gem.id === skillId);
    if (!existing) {
      const newGem = ALL_ACTIVE_SKILLS[skillId];
      if (newGem) {
        this.sockets.push({
          color: newGem.color,
          linkGroup: this.sockets.length + 1,
          gem: newGem,
        });
      }
    }
    this.compileSkills();
  }

  public gainExp(amount: number): boolean {
    const finalExp = Math.round(amount * (1 + this.expBonusPct / 100));
    this.stats.currentExp += finalExp;
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

  // TÍNH TOÁN CHỈ SỐ TỪ CẢ 10 Ô TRANG BỊ
  public recalculateTotalStats(equipped: EquippedSlots, treeBonus: PassiveTreeBonus): void {
    const base = CLASS_BASE_STATS[this.characterClass];
    const levelBonusLife = (this.stats.level - 1) * 15;
    const levelBonusES = (this.stats.level - 1) * 10;

    this.pickupRadius = 160 + treeBonus.pickupRadius;
    this.expBonusPct = treeBonus.expBonusPct;

    let totalFlatLife = base.maxLife + levelBonusLife + treeBonus.flatLife;
    let totalFlatES = base.maxEnergyShield + (base.maxEnergyShield > 0 ? levelBonusES : 0) + treeBonus.flatES;
    let totalArmour = base.armour + treeBonus.flatArmour;
    let totalEvasion = base.evasion + treeBonus.flatEvasion;
    let totalMoveSpeed = base.movementSpeed + treeBonus.movementSpeed;

    // Duyệt qua toàn bộ 10 ô trang bị đang mặc
    for (const item of Object.values(equipped)) {
      if (!item) continue;
      const tierMult = 1 + (item.tier - 1) * 0.4;
      const allAffixes = [...item.prefixes, ...item.suffixes];

      for (const aff of allAffixes) {
        const scaledVal = Math.round(aff.value * tierMult);
        if (aff.statType === 'flat_life') totalFlatLife += scaledVal;
        if (aff.statType === 'flat_es') totalFlatES += scaledVal;
        if (aff.statType === 'armour') totalArmour += scaledVal;
        if (aff.statType === 'movement_speed') totalMoveSpeed += scaledVal;
      }
    }

    this.stats.maxLife = totalFlatLife;
    this.stats.maxEnergyShield = totalFlatES;
    this.stats.armour = totalArmour;
    this.stats.evasion = totalEvasion;
    this.stats.movementSpeed = totalMoveSpeed;

    this.stats.currentLife = Math.min(this.stats.currentLife, this.stats.maxLife);
    this.compileSkills(equipped, treeBonus);
  }

  public compileSkills(equipped?: EquippedSlots, treeBonus?: PassiveTreeBonus): void {
    this.compiledSkills = [];
    const activeSockets = this.sockets.filter((s) => s.gem && 'getInitialContext' in s.gem);

    let addedDmg = 0;
    let incDmg = 0;
    let atkSpeedPct = 0;
    let critChance = 0;
    let critMultiplier = 0;
    let extraProj = 0;
    let extraPierce = 0;

    // Thu thập chỉ số sát thương từ toàn bộ trang bị
    if (equipped) {
      for (const item of Object.values(equipped)) {
        if (!item) continue;
        const tierMult = 1 + (item.tier - 1) * 0.4;
        const allAff = [...item.prefixes, ...item.suffixes];
        for (const a of allAff) {
          const val = Math.round(a.value * tierMult);
          if (a.statType === 'added_damage') addedDmg += val;
          if (a.statType === 'inc_damage') incDmg += val;
          if (a.statType === 'attack_speed') atkSpeedPct += val;
          if (a.statType === 'crit_chance') critChance += val;
        }
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
      const sLvl = this.skillBonusLevels.get(activeGem.id) || 1;
      const ctx = activeGem.getInitialContext(sLvl);

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

  public getCooldownPercent(skillId: string, time: number): number {
    const skill = this.compiledSkills.find((s) => s.id === skillId);
    if (!skill) return 0;
    const lastCast = this.skillCooldownTimers.get(skillId) || 0;
    const cooldown = skill.baseCooldown / skill.attackSpeedMultiplier;
    const elapsed = time - lastCast;
    if (elapsed >= cooldown) return 0;
    return 1 - elapsed / cooldown;
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
