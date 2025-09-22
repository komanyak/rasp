import type { InstituteOption } from '../types';
import styles from '../App.module.css';

interface InstituteSelectorProps {
  institutes: InstituteOption[];
  selectedInstitute: string;
  onInstituteChange: (instituteId: string) => void;
}

export default function InstituteSelector({
  institutes,
  selectedInstitute,
  onInstituteChange
}: InstituteSelectorProps) {
  return (
    <div className={styles.formGroup}>
      <label htmlFor="institute">Институт:</label>
      <select
        id="institute"
        value={selectedInstitute}
        onChange={(e) => onInstituteChange(e.target.value)}
        aria-label="Выберите институт"
      >
        <option value="">Выберите институт</option>
        {institutes.map(institute => (
          <option key={institute.value} value={institute.value}>
            {institute.label}
          </option>
        ))}
      </select>
    </div>
  );
}
