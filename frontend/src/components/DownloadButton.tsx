import styles from '../App.module.css';

interface DownloadButtonProps {
  selectedGroup: string;
  onDownload: () => void;
}

export default function DownloadButton({
  selectedGroup,
  onDownload
}: DownloadButtonProps) {
  if (!selectedGroup) return null;

  return (
    <div className={styles.formGroup}>
      <button 
        className={styles.downloadBtn}
        onClick={onDownload}
        aria-label={`Скачать расписание для группы ${selectedGroup}`}
      >
        📥 Скачать расписание {selectedGroup}
      </button>
    </div>
  );
}
