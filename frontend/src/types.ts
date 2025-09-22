export interface GroupData {
  [course: string]: {
    [level: string]: string[];
  };
}

export interface InstituteData {
  [institute: string]: GroupData;
}

export interface GroupsData {
  institute: InstituteData;
}

export interface LevelOption {
  value: string;
  label: string;
}

export interface GroupOption {
  value: string;
  label: string;
}

export interface InstituteOption {
  value: string;
  label: string;
}

export interface CourseOption {
  value: string;
  label: string;
}
