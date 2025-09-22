import { useState, useEffect } from 'react';
import styles from '../App.module.css';

interface UpdateInfo {
  lastUpdated: string;
  version: string;
}

export default function LastUpdateInfo() {
  const [updateInfo, setUpdateInfo] = useState<UpdateInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('/update-info.json')
      .then(response => response.json())
      .then(data => {
        setUpdateInfo(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error('Error loading update info:', err);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div className={styles.updateInfo}>
        <span className={styles.updateLabel}>🔄 Загрузка информации об обновлении...</span>
      </div>
    );
  }

  if (!updateInfo) {
    return (
      <div className={styles.updateInfo}>
        <span className={styles.updateLabel}>❓ Информация об обновлении недоступна</span>
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      });
    } catch (error) {
      return 'Неизвестно';
    }
  };

  const getRelativeTime = (dateString: string) => {
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);
      
      if (diffInSeconds < 60) {
        return 'только что';
      } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} мин. назад`;
      } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} ч. назад`;
      } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} дн. назад`;
      }
    } catch (error) {
      return 'неизвестно';
    }
  };

  return (
    <div className={styles.updateInfo}>
      <span className={styles.updateLabel}>📅 Последнее обновление:</span>
      <span className={styles.updateDate} title={formatDate(updateInfo.lastUpdated)}>
        {getRelativeTime(updateInfo.lastUpdated)}
      </span>
      <button 
        className={styles.refreshButton}
        onClick={() => window.location.reload()}
        title="Обновить страницу"
      >
        🔄
      </button>
    </div>
  );
}
