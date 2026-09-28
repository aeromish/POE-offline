import Phaser from 'phaser';
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
