import React from 'react';
import { useTranslation } from 'react-i18next';
import { useTheme } from '../../context/ThemeContext';
import '../styles/Switchers.css';

const ThemeSwitcher = () => {
  const { t } = useTranslation();
  const { theme, toggleTheme } = useTheme();
  const nextTheme = theme === 'light' ? 'dark' : 'light';

  return (
    <button
      type="button"
      className="theme-switcher"
      onClick={toggleTheme}
      aria-label={t('theme.toggle', { theme: t(`theme.${nextTheme}`) })}
      title={t('theme.toggle', { theme: t(`theme.${nextTheme}`) })}
    >
      <span className={`theme-switcher__indicator theme-switcher__indicator--${theme}`} aria-hidden="true" />
      <span className="theme-switcher__text">
        <span className="theme-switcher__label">{t('theme.label')}</span>
        <span className="theme-switcher__value">{t(`theme.${theme}`)}</span>
      </span>
    </button>
  );
};

export default ThemeSwitcher;