import React, { useEffect } from "react";
import { Outlet, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import Header from './Header';
import Menu from './Menu';
import LanguageSwitcher from './switchers/LanguageSwitcher';
import { FileProvider } from '../context/FileContext';
import { menuItems } from '../constants/menuItems';
import './styles/Layout.css';

const LayoutContent = () => {
	const { t } = useTranslation();
	const location = useLocation();

	// Reiniciar scroll al cambiar de pantalla
	useEffect(() => {
		window.scrollTo(0, 0);
	}, [location.pathname]);

	const currentItem = menuItems.find((item) => item.path === location.pathname) ?? menuItems[0];

	return (
		<div className="app-shell">
			<aside className="sidebar">
				<div className="sidebar__brand">
					<img src="/LogoSinFondo.png" alt="Auditra Logo" className="sidebar__logo" />
					<p className="sidebar__eyebrow">{t('sidebar.eyebrow')}</p>
				</div>
				<h1 className="sidebar__title">{t('sidebar.title')}</h1>
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

const Layout = () => {
	return (
		<FileProvider>
			<LayoutContent />
		</FileProvider>
	);
};

export default Layout;