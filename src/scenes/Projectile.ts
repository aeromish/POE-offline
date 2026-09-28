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

    // Đổi texture theo loại kỹ năng
    const texKey = ctx.id === 'split_arrow' ? 'proj_arrow' : ctx.id === 'ground_slam' ? 'proj_slam' : 'proj_fireball';
    this.setTexture(texKey);

    this.enableBody(true, x, y, true, true);
    this.setRotation(angleRad);

    const body = this.body as Phaser.Physics.Arcade.Body;
    if (body) {
      if (ctx.id === 'ground_slam') {
        body.setSize(24, 24);
      } else {
        body.setSize(12, 12);
      }
      this.scene.physics.velocityFromRotation(angleRad, ctx.projectileSpeed, body.velocity);
    }

    const lifeTime = ctx.id === 'ground_slam' ? 500 : 2500;
    this.scene.time.delayedCall(lifeTime, () => {
      if (this.active) this.kill();
    });
  }

  kill(): void {
    this.disableBody(true, true);
  }
}
