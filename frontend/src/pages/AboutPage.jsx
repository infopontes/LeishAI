// src/pages/AboutPage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import '../styles/About.css';

const REPO_URL = 'https://github.com/infopontes/LeishAI';

function AboutPage() {
  const { t } = useTranslation();

  const sections = [
    {
      title: t('aboutPage.overviewTitle'),
      items: [
        t('aboutPage.overview1'),
        t('aboutPage.overview2'),
      ],
    },
    {
      title: t('aboutPage.frontendTitle'),
      items: [
        t('aboutPage.frontend1'),
        t('aboutPage.frontend2'),
        t('aboutPage.frontend3'),
      ],
    },
    {
      title: t('aboutPage.backendTitle'),
      items: [
        t('aboutPage.backend1'),
        t('aboutPage.backend2'),
        t('aboutPage.backend3'),
        t('aboutPage.backend4'),
      ],
    },
    {
      title: t('aboutPage.mlTitle'),
      items: [
        t('aboutPage.ml1'),
        t('aboutPage.ml2'),
        t('aboutPage.ml3'),
      ],
    },
  ];

  return (
    <div className="about-page">
      <div className="about-hero">
        <div>
          <p className="eyebrow">{t('aboutPage.brand')}</p>
          <h1>{t('aboutPage.title')}</h1>
          <p className="subtitle">{t('aboutPage.subtitle')}</p>
          <a
            className="repo-button"
            href={REPO_URL}
            target="_blank"
            rel="noreferrer"
          >
            {t('aboutPage.repoLink')}
          </a>
        </div>
      </div>

      <div className="about-grid">
        {sections.map((section) => (
          <div className="about-card" key={section.title}>
            <h3>{section.title}</h3>
            <ul>
              {section.items.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AboutPage;
