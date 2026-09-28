import { MonsterStats, MonsterRarity, MonsterAffix } from './MonsterTypes';
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
