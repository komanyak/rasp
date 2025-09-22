import type { GroupOption } from '../types';
import styles from '../App.module.css';

interface GroupSelectorProps {
  groups: GroupOption[];
  selectedGroup: string;
  onGroupChange: (group: string) => void;
}

export default function GroupSelector({
  groups,
  selectedGroup,
  onGroupChange
}: GroupSelectorProps) {
  if (groups.length === 0) return null;

  return (
    <div className={styles.formGroup}>
      <label htmlFor="group">Группа:</label>
      <select
        id="group"
        value={selectedGroup}
        onChange={(e) => onGroupChange(e.target.value)}
        aria-label="Выберите группу"
      >
        <option value="">Выберите группу</option>
        {groups.map(group => (
          <option key={group.value} value={group.value}>
            {group.label}
          </option>
        ))}
      </select>
    </div>
  );
}
