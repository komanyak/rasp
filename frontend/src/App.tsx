import type { InstituteOption, CourseOption, LevelOption, GroupOption } from './types';
import styles from './App.module.css';
import InstituteSelector from './components/InstituteSelector';
import CourseSelector from './components/CourseSelector';
import LevelSelector from './components/LevelSelector';
import GroupSelector from './components/GroupSelector';
import DownloadButton from './components/DownloadButton';
import LastUpdateInfo from './components/LastUpdateInfo';
import { useScheduleData } from './hooks/useScheduleData';
import { useFormState } from './hooks/useFormState';

const instituteNames: { [key: string]: string } = {
  '1': 'Институт №1 «Авиационная техника»',
  '2': 'Институт №2 «Двигатели летательных аппаратов»',
  '3': 'Институт №3 «Системы управления, информатика и электроэнергетика»',
  '4': 'Институт №4 «Радиоэлектроника летательных аппаратов»',
  '5': 'Институт №5 «Инженерная экономика и гуманитарные науки»',
  '6': 'Институт №6 «Аэрокосмический»',
  '7': 'Институт №7 «Робототехнические и интеллектуальные системы»',
  '8': 'Институт №8 «Информационные технологии и прикладная математика»',
  '9': 'Институт №9 «Общеинженерной подготовки»',
  '10': 'Институт №10 «Инновационные технологии»',
  '11': 'Институт №11 «Материаловедения и технологий материалов»',
  '12': 'Институт №12 «Аэрокосмические наукоемкие технологии и производства»',
  '14': 'Институт №14 «Специальное машиностроение»'
};

const levelNames: { [key: string]: string } = {
  'bachelor': 'Бакалавриат',
  'magistracy': 'Магистратура',
  'postgraduate': 'Аспирантура',
  'specialty': 'Специалитет',
  'spec_high': 'Специалитет (высшее образование)',
  'basic': 'Базовое образование'
};

function App() {
  const { groupsData, isLoading, error } = useScheduleData();
  const {
    selectedInstitute,
    selectedCourse,
    selectedLevel,
    selectedGroup,
    handleInstituteChange,
    handleCourseChange,
    handleLevelChange,
    setSelectedGroup
  } = useFormState();

  const handleDownload = () => {
    if (!selectedGroup) return;
    
    // Создаем ссылку для скачивания файла
    const link = document.createElement('a');
    link.href = `/rasp/${selectedGroup}.ics`;
    link.download = `${selectedGroup}.ics`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getInstitutes = (): InstituteOption[] => {
    if (!groupsData) return [];
    return Object.keys(groupsData.institute).map(id => ({
      value: id,
      label: instituteNames[id] || `Институт №${id}`
    }));
  };

  const getCourses = (): CourseOption[] => {
    if (!groupsData || !selectedInstitute) return [];
    const institute = groupsData.institute[selectedInstitute];
    return Object.keys(institute).map(course => ({
      value: course,
      label: `${course} курс`
    }));
  };

  const getLevels = (): LevelOption[] => {
    if (!groupsData || !selectedInstitute || !selectedCourse) return [];
    const institute = groupsData.institute[selectedInstitute];
    const course = institute[selectedCourse];
    return Object.keys(course).map(level => ({
      value: level,
      label: levelNames[level] || level
    }));
  };

  const getGroups = (): GroupOption[] => {
    if (!groupsData || !selectedInstitute || !selectedCourse || !selectedLevel) return [];
    const institute = groupsData.institute[selectedInstitute];
    const course = institute[selectedCourse];
    const level = course[selectedLevel];
    return level.map(group => ({
      value: group,
      label: group
    }));
  };

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Загрузка данных...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>📅 Скачивание расписания МАИ</h1>
        <p>Выберите институт и группу для скачивания расписания</p>
        <LastUpdateInfo />
      </header>

      <div className={styles.form}>
        <InstituteSelector
          institutes={getInstitutes()}
          selectedInstitute={selectedInstitute}
          onInstituteChange={handleInstituteChange}
        />

        <CourseSelector
          courses={getCourses()}
          selectedCourse={selectedCourse}
          onCourseChange={handleCourseChange}
        />

        <LevelSelector
          levels={getLevels()}
          selectedLevel={selectedLevel}
          onLevelChange={handleLevelChange}
        />

        <GroupSelector
          groups={getGroups()}
          selectedGroup={selectedGroup}
          onGroupChange={setSelectedGroup}
        />

        <DownloadButton
          selectedGroup={selectedGroup}
          onDownload={handleDownload}
        />
      </div>

      <footer className={styles.footer}>
        <p>Файл будет скачан в формате .ics для импорта в календарь</p>
      </footer>
    </div>
  );
}

export default App;