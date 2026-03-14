import React from 'react';
import { useTranslation } from 'react-i18next';
import ThemeSwitcher from './switchers/ThemeSwitcher';

const Header = ({ title, description }) => {
  const { t } = useTranslation();

  return (
    <header className="layout__header">
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <div className="layout__header-actions">
        <ThemeSwitcher />
      </div>
    </header>
  );
};

export default Header;