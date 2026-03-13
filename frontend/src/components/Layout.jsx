import React from "react";
import { Outlet, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Header from './Header';
import Menu from './Menu';
import LanguageSwitcher from './LanguageSwitcher';
import { menuItems } from '../constants/menuItems';

const Layout = () => {
	const { t } = useTranslation();
	const location = useLocation();
	const currentItem = menuItems.find((item) => item.path === location.pathname) ?? menuItems[0];

	return (
		<div className="app-shell">
			<aside className="sidebar">
				<div className="sidebar__brand">
					<p className="sidebar__eyebrow">{t('sidebar.eyebrow')}</p>
					<h1 className="sidebar__title">{t('sidebar.title')}</h1>
				</div>

				<Menu items={menuItems} />

				<LanguageSwitcher />
			</aside>

			<main className="layout__content">
				<Header
					title={t(`menu.${currentItem.id}.label`)}
					description={t(`menu.${currentItem.id}.description`)}
				/>

				<Outlet />
			</main>
		</div>
	);
};

export default Layout;