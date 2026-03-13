import React from 'react';
import { NavLink } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Menu = ({ items }) => {
	const { t } = useTranslation();

	return (
		<nav className="menu" aria-label={t('menu.aria_label')}>
			{items.map((item) => (
				<NavLink
					key={item.id}
					to={item.path}
					end={item.path === '/'}
					className={({ isActive }) =>
						`menu__item${isActive ? ' menu__item--active' : ''}`
					}
				>
					<span className="menu__label">{t(`menu.${item.id}.label`)}</span>
					<span className="menu__description">{t(`menu.${item.id}.description`)}</span>
				</NavLink>
			))}
		</nav>
	);
};

export default Menu;
