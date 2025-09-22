import { useState } from 'react';

export function useFormState() {
  const [selectedInstitute, setSelectedInstitute] = useState<string>('');
  const [selectedCourse, setSelectedCourse] = useState<string>('');
  const [selectedLevel, setSelectedLevel] = useState<string>('');
  const [selectedGroup, setSelectedGroup] = useState<string>('');

  const handleInstituteChange = (instituteId: string) => {
    setSelectedInstitute(instituteId);
    setSelectedCourse('');
    setSelectedLevel('');
    setSelectedGroup('');
  };

  const handleCourseChange = (course: string) => {
    setSelectedCourse(course);
    setSelectedLevel('');
    setSelectedGroup('');
  };

  const handleLevelChange = (level: string) => {
    setSelectedLevel(level);
    setSelectedGroup('');
  };

  const resetForm = () => {
    setSelectedInstitute('');
    setSelectedCourse('');
    setSelectedLevel('');
    setSelectedGroup('');
  };

  return {
    selectedInstitute,
    selectedCourse,
    selectedLevel,
    selectedGroup,
    handleInstituteChange,
    handleCourseChange,
    handleLevelChange,
    setSelectedGroup,
    resetForm
  };
}
