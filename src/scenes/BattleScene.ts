import Phaser from 'phaser';
import { Player } from './Player';

export class BattleScene extends Phaser.Scene {
  private player!: Player;

  constructor() {
    super('BattleScene');
  }

  create(): void {
    const mapWidth = 2000;
    const mapHeight = 2000;

    this.physics.world.setBounds(0, 0, mapWidth, mapHeight);

    const grid = this.add.grid(
      mapWidth / 2,
      mapHeight / 2,
      mapWidth,
      mapHeight,
      64,
      64,
      0x161b22,
      1,
      0x21262d,
      1
    );
    grid.setOutlineStyle(0x30363d);

    this.player = new Player(this, mapWidth / 2, mapHeight / 2, 'Knight');

    this.cameras.main.setBounds(0, 0, mapWidth, mapHeight);
    this.cameras.main.startFollow(this.player, true, 0.1, 0.1);
    this.cameras.main.setZoom(1.5);
  }

  update(): void {
    this.player.update();
  }
}