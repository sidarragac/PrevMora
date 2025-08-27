import { useState } from 'react';

import { localStorageProps } from '@/types/local-storage';

export const useLocalStorage = ({ key, value }: localStorageProps) => {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      if (typeof window !== 'undefined') {
        const item = window.localStorage.getItem(key);
        return item ? JSON.parse(item) : value;
      }
    } catch (error) {
      console.log(error);
      return value;
    }
  });

  const setValue = ({ value }: localStorageProps) => {
    try {
      setStoredValue(value);
      if (typeof window !== 'undefined')
        window.localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.log(error);
    }
  };
  return [storedValue, setValue];
};
