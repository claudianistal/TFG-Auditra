import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './HomePage.css';

const HomePage = () => {
  const { t } = useTranslation();

  return (
    <section className="home-guide" aria-label={t('pages.home.title')}>
      <div className="home-guide__hero">
        <p className="home-guide__eyebrow">{t('pages.home.eyebrow')}</p>
        <h3>{t('pages.home.title')}</h3>
        <p className="home-guide__intro">{t('pages.home.intro')}</p>
      </div>

      <div className="home-guide__steps">
        <article className="home-guide__step">
          <p className="home-guide__step-number">01</p>
          <h4>{t('pages.home.steps.upload.title')}</h4>
          <p>{t('pages.home.steps.upload.description')}</p>
          <Link to="/upload" className="home-guide__step-link">
            {t('pages.home.steps.upload.link')}
          </Link>
        </article>

        <article className="home-guide__step">
          <p className="home-guide__step-number">02</p>
          <h4>{t('pages.home.steps.metadata.title')}</h4>
          <p>{t('pages.home.steps.metadata.description')}</p>
          <Link to="/metadata" className="home-guide__step-link">
            {t('pages.home.steps.metadata.link')}
          </Link>
        </article>

        <article className="home-guide__step">
          <p className="home-guide__step-number">03</p>
          <h4>{t('pages.home.steps.patterns.title')}</h4>
          <p>{t('pages.home.steps.patterns.description')}</p>
          <Link to="/patterns" className="home-guide__step-link">
            {t('pages.home.steps.patterns.link')}
          </Link>
        </article>

        <article className="home-guide__step">
          <p className="home-guide__step-number">04</p>
          <h4>{t('pages.home.steps.analysis.title')}</h4>
          <p>{t('pages.home.steps.analysis.description')}</p>
          <Link to="/analysis" className="home-guide__step-link">
            {t('pages.home.steps.analysis.link')}
          </Link>
        </article>
      </div>

      <div className="home-guide__notice" role="note">
        <strong>{t('pages.home.noticeTitle')}</strong>
        <p>{t('pages.home.noticeText')}</p>
      </div>
    </section>
  );
};

export default HomePage;
