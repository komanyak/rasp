import { useState, useEffect } from 'react';
import type { GroupsData } from '../types';

export function useScheduleData() {
  const [groupsData, setGroupsData] = useState<GroupsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/groups.json')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setGroupsData(data);
        setIsLoading(false);
      })
      .catch(err => {
        setError('Ошибка загрузки данных групп');
        setIsLoading(false);
        console.error('Error loading groups data:', err);
      });
  }, []);

  return { groupsData, isLoading, error };
}
