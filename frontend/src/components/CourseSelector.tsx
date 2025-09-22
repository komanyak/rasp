import type { CourseOption } from '../types';
import styles from '../App.module.css';

interface CourseSelectorProps {
  courses: CourseOption[];
  selectedCourse: string;
  onCourseChange: (course: string) => void;
}

export default function CourseSelector({
  courses,
  selectedCourse,
  onCourseChange
}: CourseSelectorProps) {
  if (courses.length === 0) return null;

  return (
    <div className={styles.formGroup}>
      <label htmlFor="course">Курс:</label>
      <select
        id="course"
        value={selectedCourse}
        onChange={(e) => onCourseChange(e.target.value)}
        aria-label="Выберите курс"
      >
        <option value="">Выберите курс</option>
        {courses.map(course => (
          <option key={course.value} value={course.value}>
            {course.label}
          </option>
        ))}
      </select>
    </div>
  );
}
