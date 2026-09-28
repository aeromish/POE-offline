export type QuestType = 'kill_count' | 'kill_rares' | 'collect_currency' | 'reach_wave';

export interface Quest {
  id: string;
  title: string;
  description: string;
  type: QuestType;
  current: number;
  target: number;
  rewardText: string;
  rewardType: 'exp' | 'skill_point' | 'chaos';
  rewardValue: number;
  isCompleted: boolean;
}
