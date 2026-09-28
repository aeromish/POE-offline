import Phaser from 'phaser';
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
