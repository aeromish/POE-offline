import { Quest } from './QuestTypes';

export class QuestManager {
  public activeQuests: Quest[] = [];

  constructor() {
    this.initDefaultQuests();
  }

  public initDefaultQuests(): void {
    this.activeQuests = [
      {
        id: 'q_kill_30',
        title: 'Càn Quét Chiến Trường',
        description: 'Tiêu diệt 30 quái vật bất kỳ',
        type: 'kill_count',
        current: 0,
        target: 30,
        rewardText: '+200 EXP',
        rewardType: 'exp',
        rewardValue: 200,
        isCompleted: false,
      },
      {
        id: 'q_kill_rares',
        title: 'Thợ Săn Tinh Anh',
        description: 'Tiêu diệt 2 quái vật Rare (Vàng)',
        type: 'kill_rares',
        current: 0,
        target: 2,
        rewardText: '+1 Điểm Thiên Phú',
        rewardType: 'skill_point',
        rewardValue: 1,
        isCompleted: false,
      },
      {
        id: 'q_collect_cur',
        title: 'Kẻ Thu Thập Tiền Tệ',
        description: 'Thu thập 5 đồng Tiền Tệ (Currency)',
        type: 'collect_currency',
        current: 0,
        target: 5,
        rewardText: '+2 Chaos Orb',
        rewardType: 'chaos',
        rewardValue: 2,
        isCompleted: false,
      },
    ];
  }

  public onMonsterKilled(isRare: boolean): Quest[] {
    const completedNow: Quest[] = [];
    for (const q of this.activeQuests) {
      if (q.isCompleted) continue;
      if (q.type === 'kill_count') {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      } else if (q.type === 'kill_rares' && isRare) {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      }
    }
    return completedNow;
  }

  public onCurrencyCollected(): Quest[] {
    const completedNow: Quest[] = [];
    for (const q of this.activeQuests) {
      if (q.isCompleted) continue;
      if (q.type === 'collect_currency') {
        q.current++;
        if (q.current >= q.target) {
          q.isCompleted = true;
          completedNow.push(q);
        }
      }
    }
    return completedNow;
  }
}
