import React from 'react';
import { useTranslation } from 'react-i18next';

const Header = ({ title, description }) => {
  const { t } = useTranslation();

  return (
    <header className="layout__header">
      <div>
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      <span className="layout__badge">{t('header.badge')}</span>
    </header>
  );
};

export default Header;