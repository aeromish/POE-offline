import Phaser from 'phaser';
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
    else if (ctx.id === 'arc') texKey = 'proj_arc';
    else if (ctx.id === 'molten_strike') texKey = 'proj_molten';
    else if (ctx.id === 'toxic_spore') texKey = 'proj_toxic';

    this.setTexture(texKey);
    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      if (ctx.id === 'ground_slam' || ctx.id === 'molten_strike') {
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
