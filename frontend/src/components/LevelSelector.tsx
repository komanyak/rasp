import type { LevelOption } from '../types';
import styles from '../App.module.css';

interface LevelSelectorProps {
  levels: LevelOption[];
  selectedLevel: string;
  onLevelChange: (level: string) => void;
}

export default function LevelSelector({
  levels,
  selectedLevel,
  onLevelChange
}: LevelSelectorProps) {
  if (levels.length === 0) return null;

  return (
    <div className={styles.formGroup}>
      <label htmlFor="level">Уровень образования:</label>
      <select
        id="level"
        value={selectedLevel}
        onChange={(e) => onLevelChange(e.target.value)}
        aria-label="Выберите уровень образования"
      >
        <option value="">Выберите уровень образования</option>
        {levels.map(level => (
          <option key={level.value} value={level.value}>
            {level.label}
          </option>
        ))}
      </select>
    </div>
  );
}
